from fmo.lease import Lease
import folium
import webbrowser
import tempfile
import os


def preview_geojson(file, location=None, zoom=None):
    if location is None:
        location = (0,0)
        if zoom is None:
            zoom = 4 # zoom far out if we dont have a location

    lat, lng = location

    if zoom is None:
        zoom = 14

    map = folium.Map(location=(lat, lng), zoom_start=zoom, max_zoom=20)

    # Create a GeoJSON object to represent the path
    folium.GeoJson(file, name="geojson").add_to(map)

    # Save the map as an HTML file
    temp_file = tempfile.NamedTemporaryFile(suffix=".html", delete=False)
    temp_file.close()
    map.save(temp_file.name)

    # Open the HTML file in the default web browser
    webbrowser.open_new_tab("file://" + os.path.realpath(temp_file.name))


def preview_lease(lease: Lease):
    map = folium.Map(location=lease.center(), zoom_start=15)

    # Create a GeoJSON object to represent the path
    folium.GeoJson(data=lease.geojson_data()["geometry"], name="geojson").add_to(map)
    #folium.GeoJson(geojson_data).add_to(map)

    # Save the map as an HTML file
    temp_file = tempfile.NamedTemporaryFile(suffix=".html", delete=False)
    temp_file.close()
    map.save(temp_file.name)

    # Open the HTML file in the default web browser
    webbrowser.open_new_tab("file://" + os.path.realpath(temp_file.name))
