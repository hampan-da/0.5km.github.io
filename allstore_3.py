# Spatial Distribution of Supermarkets within the United Kingdom
# Using the attribute and spatial data of each Supermarket
import folium
import os
import pandas as pd
from folium import plugins

# Creating Feature Grouping for each Feature Layer
fg1 = folium.FeatureGroup(name='0.5km Radius')
fg2 = folium.FeatureGroup(name='Nodes')
fg3 = folium.FeatureGroup(name='Customer Access Point')
fg4 = folium.FeatureGroup(name='Customer Entrance')

# Creating the Map Location and Zoom Level
m = folium.Map(location=[55.171, -2.82], zoom_start=8, control_scale=True)

# Connecting the File Directory and Assigning them to their Variables
store = os.path.join('data', 'supermarket.csv')
node = os.path.join('data', 'new_new_node2.csv')
Customer_Entrance = os.path.join('data', 'customer_entrance.csv')
Customer_Access_Point = os.path.join('data', 'customer_access_point.csv')

# Reading through the CSV file for each Feature Layer
df_st = pd.read_csv(store, usecols=['LONG', 'LAT'])

df_no = pd.read_csv(node, usecols=['id', 'LONG', 'LAT'], dtype={'id':'int32', 'LONG':'float16', 'LAT':'float16'})

df_cap = pd.read_csv(Customer_Access_Point, usecols=['Store_ID', 'JS_Name', 'Latitude', 'Longtiude'],
                     dtype={'Store_ID':'int32', 'Longtiude':'float16', 'Latitude':'float16'})

df_ce = pd.read_csv(Customer_Entrance, usecols=['Store_ID', 'JS_Name', 'Latitude', 'Longtiude'],
                    dtype={'Store_ID':'int32', 'Longtiude':'float16', 'Latitude':'float16'})

# Iterating through the supermarket location file and creating a 500 meters radius.
df_st.apply(lambda row: folium.Circle(radius=500, location=(row['LAT'], row['LONG']), color='brown').add_to(fg1),
            axis=1)

# Iterating through the supermarket location file and creating a 500 meters radius.
df_no.apply(lambda row: folium.Circle(radius=1, location=(row['LAT'], row['LONG']), color='black', tooltip=row['id'],
                                      popup=row['id']).add_to(fg2), axis=1)

# Adding Markers for the supermarket (Customer Access Point)
for index, row in df_cap.iterrows():
    folium.RegularPolygonMarker([row['Latitude'], row['Longtiude']],
                  number_of_sides=3,
                  radius=3,
                  color='red',
                  fill_color='red',
                  popup=(row['JS_Name'], row['Store_ID']),
                  tooltip=row['Store_ID'],
                  ).add_to(fg3)

# Adding Markers for the supermarket (Customer Entrance)
for index, row in df_ce.iterrows():
    folium.RegularPolygonMarker([row['Latitude'], row['Longtiude']],
                  number_of_sides=4,
                  radius=3,
                  color='green',
                  fill_color='green',
                  popup=(row['JS_Name'], row['Store_ID']),
                  tooltip=row['Store_ID'],
                  ).add_to(fg4)

# Adding The Feature Groups to the Map
m.add_child(fg1)
m.add_child(fg2)
m.add_child(fg3)
m.add_child(fg4)

# create Mini Map
Minimap = plugins.MiniMap(toggle_display=True)

# add mini map to the Map (m)
m.add_child(Minimap)

# Add full Screen
plugins.Fullscreen(position='topright').add_to(m)

# Adding Draw Tools to the Map (m)
draw = plugins.Draw(export=True,)
m.add_child(draw)

# Add Measure Control tools to the Map (m)
measure = plugins.MeasureControl(position='topleft',
                                 active_color='yellow',
                                 completed_color='red',
                                 primary_length_unit='meters')
m.add_child(measure)

# Adding Longitude and latitude tool to the map (m)
m.add_child(folium.LatLngPopup())

# Creating Layer control to the map (m)
m.add_child(folium.LayerControl(
    collapsed=True,
    position='topleft'))

m.save('allstore_3.html')
