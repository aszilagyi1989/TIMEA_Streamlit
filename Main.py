import geopandas as gpd
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_folium import st_folium
import folium
import plotly.express as px

#st.cache_resource
def initialize_counties():
  Attributes = pd.read_csv("https://github.com/aszilagyi1989/Shiny_CSV/raw/refs/heads/main/TIMEA_Mutatok_2024.csv", sep = ";")

  Counties = gpd.read_file('https://github.com/aszilagyi1989/Shiny_CSV/raw/refs/heads/main/JSon/megye_pbi.shp')
  Counties = Counties[['Megyenév', 'geometry', 'Shape_Leng', 'Shape_Area']]
  Counties['Megyenév'] = Counties['Megyenév'].replace(['Csongrád'], 'Csongrád-Csanád')
  
  ValuesCounties = pd.read_csv("https://github.com/aszilagyi1989/Shiny_CSV/raw/refs/heads/main/TIMEA_Megyek_2024.csv", sep = ";")
  ValuesCounties['NEV'] = ValuesCounties['NEV'].str.replace(r' vármegye', '', regex = True)
  
  Counties = pd.merge(Counties, ValuesCounties, how = 'left', left_on = 'Megyenév', right_on = 'NEV')
  Counties = pd.merge(Counties, Attributes, how = 'left', left_on = 'M_KOD', right_on = 'MUTATO_KOD')
  Counties = Counties[['Megyenév', 'VALUE', 'geometry', 'M_KOD', 'MUTATO_FOCSOP_MEGNEV', 'MUTATO_MEGNEV', 'VON_IDO', 'Shape_Leng', 'Shape_Area']]
  Counties['VALUE'] = Counties['VALUE'].str.replace(',', '.')
  Counties['VALUE'] = Counties.VALUE.astype(float)
  
  return Counties

@st.cache_resource
def initialize_cities():
  Attributes = pd.read_csv("https://github.com/aszilagyi1989/Shiny_CSV/raw/refs/heads/main/TIMEA_Mutatok_2024.csv", sep = ";")

  Cities = gpd.read_file('https://github.com/aszilagyi1989/Shiny_CSV/raw/refs/heads/main/JSon/telepules_BP_egesz.shp')
  Cities = Cities[['NAME', 'geometry']]
  
  ValuesCities = pd.read_csv("https://github.com/aszilagyi1989/Shiny_CSV/raw/refs/heads/main/TIMEA_Varosok_2024.csv", sep = ";")
  
  Cities = pd.merge(Cities, ValuesCities, how = 'left', left_on = 'NAME', right_on = 'NEV')
  Cities = pd.merge(Cities, Attributes, how = 'left', left_on = 'M_KOD', right_on = 'MUTATO_KOD')
  Cities = Cities[['NAME', 'VALUE', 'geometry', 'M_KOD', 'MUTATO_FOCSOP_MEGNEV', 'MUTATO_MEGNEV', 'VON_IDO']]
  Cities['VALUE'] = Cities['VALUE'].str.replace(',', '.')
  Cities['VALUE'] = Cities.VALUE.astype(float)
  
  return Cities

@st.cache_resource
def initialize_regions():
  Attributes = pd.read_csv("https://github.com/aszilagyi1989/Shiny_CSV/raw/refs/heads/main/TIMEA_Mutatok_2024.csv", sep = ";")

  Regions = gpd.read_file('https://github.com/aszilagyi1989/Shiny_CSV/raw/refs/heads/main/JSon/regio.shp')
  Regions = Regions[['Régió_ne', 'geometry', 'Shape_Leng', 'Shape_Area']]
  
  ValuesRegions = pd.read_csv("https://github.com/aszilagyi1989/Shiny_CSV/raw/refs/heads/main/TIMEA_Regiok.csv", sep = ";")
  ValuesRegions['NEV'] = ValuesRegions['NEV'].str.replace(' (Budapest)', '')
  ValuesRegions['NEV'] = ValuesRegions['NEV'].str.replace(' (Bács-Kiskun, Békés, Csongrád)', '')
  ValuesRegions['NEV'] = ValuesRegions['NEV'].str.replace(' (Bács-Kiskun, Békés, Csongrád-Csanád)', '')
  ValuesRegions['NEV'] = ValuesRegions['NEV'].str.replace(' (Baranya, Somogy, Tolna)', '')
  ValuesRegions['NEV'] = ValuesRegions['NEV'].str.replace(' (Hajdú-Bihar, Jász-Nagykun-Szolnok, Szabolcs-Szatmár-Bereg)', '')
  ValuesRegions['NEV'] = ValuesRegions['NEV'].str.replace(' (Borsod-Abaúj-Zemplén, Heves, Nógrád)', '')
  ValuesRegions['NEV'] = ValuesRegions['NEV'].str.replace(' (Fejér, Komárom-Esztergom, Veszprém)', '')
  ValuesRegions['NEV'] = ValuesRegions['NEV'].str.replace(' (Győr-Moson-Sopron, Vas, Zala)', '')
  ValuesRegions['NEV'] = ValuesRegions['NEV'].str.replace(' (Pest)', '')
  
  Regions = pd.merge(Regions, ValuesRegions, how = 'left', left_on = 'Régió_ne', right_on = 'NEV')
  Regions = pd.merge(Regions, Attributes, how = 'left', left_on = 'M_KOD', right_on = 'MUTATO_KOD')
  Regions = Regions[['Régió_ne', 'VALUE', 'geometry', 'M_KOD', 'MUTATO_FOCSOP_MEGNEV', 'MUTATO_MEGNEV', 'VON_IDO', 'Shape_Leng', 'Shape_Area']]
  
  return Regions

@st.cache_resource
def initialize_jaras():
  Attributes = pd.read_csv("https://github.com/aszilagyi1989/Shiny_CSV/raw/refs/heads/main/TIMEA_Mutatok_2024.csv", sep = ";")

  Jaras = gpd.read_file('https://github.com/aszilagyi1989/Shiny_CSV/raw/refs/heads/main/JSon/jaras_pbi_BP_egesz.shp')
  Jaras = Jaras[['jaras', 'geometry', 'Shape_Leng', 'Shape_Area']]
  
  ValuesJaras = pd.read_csv("https://github.com/aszilagyi1989/Shiny_CSV/raw/refs/heads/main/TIMEA_Jarasok.csv", sep = ";")
  ValuesJaras['NEV'] = ValuesJaras['NEV'].str.replace(' járás', '')
  ValuesJaras['NEV'] = ValuesJaras['NEV'].str.replace('Nyíregyházai', 'Nyíregyházi')
  ValuesJaras['NEV'] = ValuesJaras['NEV'].str.replace('Budapest, illetve fiktív területi egység', 'Budapesti')
  
  Jaras = pd.merge(Jaras, ValuesJaras, how = 'left', left_on = 'jaras', right_on = 'NEV')
  Jaras = pd.merge(Jaras, Attributes, how = 'left', left_on = 'M_KOD', right_on = 'MUTATO_KOD')
  Jaras = Jaras[['jaras', 'VALUE', 'geometry', 'M_KOD', 'MUTATO_FOCSOP_MEGNEV', 'MUTATO_MEGNEV', 'VON_IDO', 'Shape_Leng', 'Shape_Area']]
  
  return Jaras


st.set_page_config(
  layout = 'wide',
  page_title = 'TIMEA',
  page_icon = 'https://map.ksh.hu/timea/images/shortcut.ico',
  menu_items = {'Get help': 'mailto:adam.szilagyi@ksh.hu',
                'Report a bug': 'mailto:adam.szilagyi@ksh.hu',
                'About': 'Térképes interaktív megjelenítő alkalmazás.'}
  )
  
st.title('Térképes Interaktív Megjelenítő Alkalmazás')

selected = option_menu(None, ['Megye', 'Település', 'Járás', 'Régió'], menu_icon = 'cast', default_index = 0, orientation = 'horizontal')

if selected == 'Megye': 
  
  Counties = initialize_counties()
  
  with st.sidebar:
    st.sidebar.title('Adatlekérdező')
    year = st.selectbox('Év', Counties['VON_IDO'].unique())
    
    selection = Counties[(Counties['VON_IDO'] == year)]
    selection = selection['MUTATO_FOCSOP_MEGNEV'].unique()
    group = st.selectbox('Főcsoport', selection)
    
    selection = Counties[(Counties['MUTATO_FOCSOP_MEGNEV'] == group) & (Counties['VON_IDO'] == year)] #& (Attributes['MUTATO_KOD'].isin(ValuesCounties['M_KOD']))]
    selection = selection['MUTATO_MEGNEV'].unique()
    item = st.selectbox('Mutató', selection)
    
    filter = st.multiselect(label = 'Keresés', options = Counties['Megyenév'].unique(), default = Counties['Megyenév'].unique())
    
    Counties = Counties[(Counties['MUTATO_MEGNEV'] == item) & (Counties['VON_IDO'] == year) & (Counties['Megyenév'].isin(filter))]

  try: 
    with st.spinner('A térkép megjelenítése folyamatban...'):
      Counties.crs = 'EPSG:23700'
      # Counties['centroid'] = Counties.centroid.to_crs('EPSG:4326') # folium-hoz kell
      # 
      # Counties['lat'] = Counties['centroid'].y
      # Counties['lon'] = Counties['centroid'].x
      
      # fig = px.scatter_map(Counties,
      #                   lat = "lat",
      #                   lon = "lon",
      #                   size = 'size', # size = 'VALUE', # Adjust for larger circles if desired
      #                   color = "VALUE",
      #                   hover_name = "Megyenév",
      #                   zoom = 6,
      #                   )
      # 
      # fig.update_layout(height = 600) # , sizemin = 10
      # st.plotly_chart(fig, height = 600)
    
      # map = folium.Map(location = [47.162494, 19.503304], zoom_start = 7, tiles = "cartodb voyager") # positron darkmatter voyager
      # 
      # for _, r in Counties.iterrows():
      #   # print(f"{r['lat']}, {r['lon']} és {r['centroid']}")
      #   folium.Marker(location = [r['lat'], r['lon']], popup = 'Megye: {} <br> Érték: {}'.format(r['Megyenév'], r['VALUE'])).add_to(map)
      # 
      # popup = folium.GeoJsonPopup(
      #          fields = ['Megyenév', 'VALUE'],
      #          aliases = ['Megye:', 'Érték:'],
      #          )
      # 
      # folium.GeoJson(data = Counties[['geometry', 'Megyenév', 'VALUE']],
      #                popup = popup
      #                ).add_to(map)
      # 
      # st.components.v1.html(folium.Figure().add_child(map).render(), height = 500) # , width = 1000, scrolling = False
      
      m = Counties.explore(
        column = "VALUE", # Oszlop a színezéshez
        cmap = "viridis",   # Színskála # "viridis", "inferno", "Set2"
        tooltip = ["Megyenév", "VALUE"], 
        tooltip_kwds = {
          "aliases": ["Megye:", "Érték"],
          "labels": True
        },
        legend = True       # Jelmagyarázat
      )
      st_folium(m, width = 1400, height = 500, returned_objects = [])
      
  except Exception as e:
    st.error(f"Kérlek, válassz ki legalább egy megyét! Hibaüzenet: {e}")

elif selected == 'Település':
  
  Cities = initialize_cities()
  
  with st.sidebar:
    st.sidebar.title('Adatlekérdező')
    year = st.selectbox('Év', Cities['VON_IDO'].unique())
    
    selection = Cities[(Cities['VON_IDO'] == year)]
    selection = selection['MUTATO_FOCSOP_MEGNEV'].unique()
    group = st.selectbox('Főcsoport', selection)
    
    selection = Cities[(Cities['MUTATO_FOCSOP_MEGNEV'] == group) & (Cities['VON_IDO'] == year)] #& (Attributes['MUTATO_KOD'].isin(ValuesCounties['M_KOD']))]
    selection = selection['MUTATO_MEGNEV'].unique()
    item = st.selectbox('Mutató', selection)
    
    filter_option = Cities[(Cities['MUTATO_MEGNEV'] == item) & (Cities['VON_IDO'] == year)]
    filter_number = st.slider('Érték tartománya', filter_option['VALUE'].min(), filter_option['VALUE'].max(), (filter_option['VALUE'].min(), filter_option['VALUE'].max()))
    
    selection = Cities[(Cities['MUTATO_MEGNEV'] == item) & (Cities['VON_IDO'] == year)]
    selection = selection['NAME'].unique()
    
    selection2 = Cities[(Cities['MUTATO_MEGNEV'] == item) & (Cities['VON_IDO'] == year) & (Cities['VALUE'] >= filter_number[0]) & (Cities['VALUE'] <= filter_number[1])]
    selection2 = selection2['NAME'].unique()
    # selection = selection.sort_index(axis = 1) # by = '0'
    
    filter = st.multiselect(label = 'Keresés', options = selection, default = selection2)
    
    Cities = Cities[(Cities['MUTATO_MEGNEV'] == item) & (Cities['VON_IDO'] == year) & (Cities['NAME'].isin(filter))]
  
  try:
    with st.spinner('A térkép megjelenítése folyamatban...'):
      # Cities.crs = 'EPSG:23700' # folium-hoz kell
      Cities.crs = 'EPSG:4326' # geopandas-hoz kell
      
      # Cities['centroid'] = Cities.centroid
      # 
      # Cities['lat'] = Cities['centroid'].y
      # Cities['lon'] = Cities['centroid'].x
      
      # fig = px.scatter_map(Cities,
      #                   lat = "lat",
      #                   lon = "lon",
      #                   size = "VALUE", # Adjust for larger circles if desired
      #                   color = "VALUE",
      #                   hover_name = "NAME",
      #                   zoom = 6,
      #                   )
      # 
      # fig.update_layout(height = 600)
      # st.plotly_chart(fig, height = 600)
      
      # map = folium.Map(location = [47.162494, 19.503304], zoom_start = 7, tiles = "cartodb voyager") # positron darkmatter voyager
      # 
      # for _, r in Cities.iterrows():
      #   # print(f"{r['lat']}, {r['lon']} és {r['centroid']}")
      #   folium.Marker(location = [r['lat'], r['lon']], popup = 'Település: {} <br> Érték: {}'.format(r['NAME'], r['VALUE'])).add_to(map)
      # 
      # folium.GeoJson(data = Cities[['geometry', 'NAME', 'VALUE']],
      #                 ).add_to(map)
      # 
      # st.components.v1.html(folium.Figure().add_child(map).render(), height = 500) # , width = 1000, scrolling = False
      
      m = Cities.explore(
        column = "VALUE", # Oszlop a színezéshez
        # cmap = "viridis",   # Színskála # "viridis", "inferno", "Set2"
        tooltip = ["NAME", "VALUE"], 
        tooltip_kwds = {
          "aliases": ["Település:", "Érték"],
          "labels": True
        },
        legend = True       # Jelmagyarázat
      )
      st_folium(m, width = 1400, height = 500, returned_objects = [])
      
  except Exception as e:
    st.error('Kérlek, válassz ki legalább egy települést!')

elif selected == 'Járás':
  
  Jaras = initialize_jaras()
  
  with st.sidebar:
    st.sidebar.title('Adatlekérdező')
    year = st.selectbox('Év', Jaras['VON_IDO'].unique())
    
    selection = Jaras[(Jaras['VON_IDO'] == year)]
    selection = selection['MUTATO_FOCSOP_MEGNEV'].unique()
    group = st.selectbox('Főcsoport', selection)
    
    selection = Jaras[(Jaras['MUTATO_FOCSOP_MEGNEV'] == group) & (Jaras['VON_IDO'] == year)]
    selection = selection['MUTATO_MEGNEV'].unique()
    item = st.selectbox('Mutató', selection)
    
    filter = st.multiselect(label = 'Keresés', options = Jaras['jaras'].unique(), default = Jaras['jaras'].unique())
    
    Jaras = Jaras[(Jaras['MUTATO_MEGNEV'] == item) & (Jaras['VON_IDO'] == year) & (Jaras['jaras'].isin(filter))]
  
  try:
    with st.spinner('A térkép megjelenítése folyamatban...'):
      # Jaras.crs = 'EPSG:23700' # folium-hoz kell
      Jaras.crs = 'EPSG:4326' # geopandas-hoz kell
      
      # Jaras['centroid'] = Jaras.centroid# .to_crs('EPSG:4326')
      # 
      # Jaras['lat'] = Jaras['centroid'].y
      # Jaras['lon'] = Jaras['centroid'].x
    
      # map = folium.Map(location = [47.162494, 19.503304], zoom_start = 7, tiles = "cartodb voyager") # positron darkmatter voyager
      # 
      # for _, r in Jaras.iterrows():
      #   # print(f"{r['lat']}, {r['lon']} és {r['centroid']}")
      #   folium.Marker(location = [r['lat'], r['lon']], popup = 'Járás: {} <br> Érték: {}'.format(r['jaras'], r['VALUE'])).add_to(map)
      # 
      # popup = folium.GeoJsonPopup(
      #          fields = ['jaras', 'VALUE'],
      #          aliases = ['Járás:', 'Érték:'],
      #          )
      #            
      # folium.GeoJson(data = Jaras[['geometry', 'jaras', 'VALUE']],
      #                popup = popup
      #                ).add_to(map)
      # 
      # st.components.v1.html(folium.Figure().add_child(map).render(), height = 500) # , width = 1000, scrolling = False
      
      m = Jaras.explore(
        column = "VALUE", # Oszlop a színezéshez
        # cmap = "viridis",   # Színskála # "viridis", "inferno", "Set2"
        tooltip = ["jaras", "VALUE"], 
        tooltip_kwds = {
          "aliases": ["Járás:", "Érték"],
          "labels": True
        },
        legend = True       # Jelmagyarázat
      )
      st_folium(m, width = 1400, height = 500, returned_objects = [])
      
  except Exception as e:
    st.error('Kérlek, válassz ki legalább egy járást!')
  
elif selected == 'Régió':
  
  Regions = initialize_regions()
  
  with st.sidebar:
    st.sidebar.title('Adatlekérdező')
    year = st.selectbox('Év', Regions['VON_IDO'].unique())
    
    selection = Regions[(Regions['VON_IDO'] == year)]
    selection = selection['MUTATO_FOCSOP_MEGNEV'].unique()
    group = st.selectbox('Főcsoport', selection)
    
    selection = Regions[(Regions['MUTATO_FOCSOP_MEGNEV'] == group) & (Regions['VON_IDO'] == year)]
    selection = selection['MUTATO_MEGNEV'].unique()
    item = st.selectbox('Mutató', selection)
    
    filter = st.multiselect(label = 'Keresés', options = Regions['Régió_ne'].unique(), default = Regions['Régió_ne'].unique())
    
    Regions = Regions[(Regions['MUTATO_MEGNEV'] == item) & (Regions['VON_IDO'] == year) & (Regions['Régió_ne'].isin(filter))]
  
  try:
    with st.spinner('A térkép megjelenítése folyamatban...'):
      # Regions.crs = 'EPSG:23700' # folium-hoz kell
      Regions.crs = 'EPSG:4326' # geopandas-hoz kell
      
      # Regions['centroid'] = Regions.centroid# .to_crs('EPSG:4326') # folium-hoz kell
      # 
      # Regions['lat'] = Regions['centroid'].y
      # Regions['lon'] = Regions['centroid'].x
    
      # map = folium.Map(location = [47.162494, 19.503304], zoom_start = 7, tiles = "cartodb voyager") # positron darkmatter voyager
      # 
      # for _, r in Regions.iterrows():
      #   # print(f"{r['lat']}, {r['lon']} és {r['centroid']}")
      #   folium.Marker(location = [r['lat'], r['lon']], popup = 'Régió: {} <br> Érték: {}'.format(r['Régió_ne'], r['VALUE'])).add_to(map)
      # 
      # popup = folium.GeoJsonPopup(
      #          fields = ['Régió_ne', 'VALUE'],
      #          aliases = ['Régió:', 'Érték:'],
      #          )
      #            
      # folium.GeoJson(data = Regions[['geometry', 'Régió_ne', 'VALUE']],
      #                popup = popup
      #                ).add_to(map)
      # 
      # st.components.v1.html(folium.Figure().add_child(map).render(), height = 500) # , width = 1000, scrolling = False
      
      m = Regions.explore(
        column = "VALUE", # Oszlop a színezéshez
        # cmap = "viridis",   # Színskála # "viridis", "inferno", "Set2"
        tooltip = ["Régió_ne", "VALUE"], 
        tooltip_kwds = {
          "aliases": ["Régió:", "Érték"],
          "labels": True
        },
        legend = True       # Jelmagyarázat
      )
      st_folium(m, width = 1400, height = 500, returned_objects = [])
      
  except Exception as e:
    st.error('Kérlek, válassz ki legalább egy régiót!')
