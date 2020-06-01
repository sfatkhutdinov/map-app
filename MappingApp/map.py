import folium
import pandas as pd 

data = pd.read_csv('volcanoes.txt')
latitude = list(data['LAT'])
longitude = list(data['LON'])
volcanoe_name = list(data['NAME'])
volcoane_elevation = list(data['ELEV'])

def color_picker(elevation):
    if elevation < 1000:
        return 'green'
    elif elevation <= 1000 or elevation < 3000:
        return 'orange'
    else:
        return 'red'

map = folium.Map(location=[38.58, -99.09], zoom_start=6, tiles='OpenStreetMap')

feature_group_volcanoes = folium.FeatureGroup(name='Volcanoes')

for lat, lon, name, elevation in zip(latitude, longitude, volcanoe_name, volcoane_elevation):
    popup_string = name + ' ' + str(elevation) + ' m'
    feature_group_volcanoes.add_child(folium.CircleMarker(location=[lat, lon], 
                                        popup=popup_string, 
                                        radius=6,
                                        fill_opacity=0.7,
                                        fill=True,
                                        fill_color=color_picker(elevation),
                                        color='grey'))

feature_group_population = folium.FeatureGroup(name='Population')

feature_group_population.add_child(folium.GeoJson(data=open('world.json', 'r', 
                                        encoding='utf-8-sig').read(), 
                                        style_function=lambda style: 
                                        {'fillColor':'green' if style['properties']['POP2005'] < 10000000 
                                                                                        else 'orange' if 10000000 <= style['properties']['POP2005'] < 20000000
                                                                                        else 'red'}))


map.add_child(feature_group_volcanoes)
map.add_child(feature_group_population)
map.add_child(folium.LayerControl())

map.save('map.html')