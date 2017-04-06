import folium
coordX = 51.89855
coordY = 4.418458

map_osm = folium.Map(location=[coordX, coordY], zoom_start=15)
first = True
with open('coords.txt') as f:
    for line in f:
        x, y = line.split(',')
        if first:
            folium.Marker([x, y]).add_to(map_osm)
            first = False
        else:
            folium.CircleMarker(location=[x, y], radius=2, fill_color='#3186cc').add_to(map_osm)
map_osm.save('osm.html')
