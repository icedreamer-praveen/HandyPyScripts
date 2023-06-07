import geocoder

address = "Kathmandu"
coordinates = geocoder.arcgis(address)
geo = geocoder.arcgis(address)
print(geo.latlng)

location = geocoder.arcgis([27.693290000000047, 85.32227000000006], method='reverse')
print(location)