import folium
import pandas as pd
import time
coordX = 51.8980995
coordY = 4.4171458


def RefreshMap():
    map_osm = None
    first = True
    with open('coords.txt') as f:
        for line in f:
            coords = line.split(',')
            if(len(coords) < 2): 
                break
            x = coords[0]
            y = coords[1]
            if first:
                map_osm = folium.Map(location=[x, y], zoom_start=18)
                folium.Marker([x, y]).add_to(map_osm)
                first = False
            else:
                folium.CircleMarker(location=[x, y], radius=2, fill_color='#3186cc').add_to(map_osm)
    if map_osm is not None:
        #map_osm.save('osm.html')
        display(map_osm)

RefreshMap()
#while True:
#    RefreshMap()
#    time.sleep(2)
#    print('Refreshed map')