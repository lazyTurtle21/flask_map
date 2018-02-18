import folium
import re
import random
import os
from geopy import ArcGIS


def input_data(data_type, condition="a", message=""):
    """
    (type, str, str) -> (object)
    Returns the valid for data_type and condition
    input with message for user
    """
    while True:
        try:
            a = data_type(input(message))
            if not eval(condition):
                raise ValueError
            return a
        except ValueError:
            print("Invalid input. Try again.")


def read_file(path):
    """
    (str) -> (list)
    Returns list of film lines from file.
    """
    lst = []
    with open(path, 'r', encoding='utf-8', errors='ignore') as file:
        line = file.readline()
        while not line.startswith('"'):
            line = file.readline()
        for x in file:
            lst.append(x.strip())
    return lst


def country_dict(lines_list, year):
    """
    (list) -> (list)
    Returns list of tuples made of list of lines with
    name of movie as the first element in a tuple and
    place where it was filmed as the second element.
    """
    lst = []
    for line in lines_list:
        if ('(' + str(year)) in line:
            line = re.sub(r'\([^()]*\)', '', line)
            line = re.sub(r'{[^()]*}', '', line)
            lines = re.split(r'\s\t+', line.strip())
            lst.append((lines[0], lines[1]))
    return lst


def country_lst(lines_list, year):
    """
    (list) -> (list)
    Returns list of tuples made of list of lines with
    name of movie as the first element in a tuple and
    place where it was filmed as the second element.
    """
    lst = []
    for line in lines_list:
        if ('(' + str(year) + ')') in line:
            indx = line.find('('+str(year))
            lines = line.split('\t')
            lst.append((line[0:indx-1], lines[-1] if lines[-1][0] != '('
                        else lines[-2]))
    return lst


def get_locations(lst, max_locat=50):
    """
    (list, int) -> (list)
    :param lst: list of locations and films
    :param max_locat: a max number of locations function finds
    :return: list of tuples = [(film_name,(location.latitude,
                                           location.longitude)]
    """
    locations = []
    geolocator = ArcGIS(timeout=10)
    for element in lst:
        try:
            location = geolocator.geocode(element[1])
            locations.append((element[0], (location.latitude,
                                           location.longitude)))
            if len(locations) == max_locat:
                break
        except:
            continue
    return locations


def icon_layer(locations):
    """
    (list of tuples) -> (layer of map)
    Creates and return markers as layer of the map
    with name of film as popup and locations where it was filmed.
    :param locations: list with name of films and locations
    :return: films layer of map
    """
    films = folium.FeatureGroup(name="films")
    for el in locations:
        popup = folium.Popup(el[0], parse_html=True)
        films.add_child(folium.Marker(location=[el[1][0], el[1][1]],
                                      popup=popup, icon=folium.Icon(color='darkred',
                                                                    icon='info-circle',
                                                                    prefix='fa')))
    return films


def pop_layer(filename="world.json", name="population", encoding="utf-8-sig"):
    """
    Returns population layer of the map
    :param filename: name of file with info about countries
    :param name: name of layer
    :param encoding: encoding of the file
    :return: layer of the map
    """
    layer = folium.FeatureGroup(name=name)
    layer.add_child(folium.GeoJson(data=open(filename, 'r',
                                             encoding=encoding).read(),
                                   style_function=lambda x: {'fillColor': 'red'
                                   if x['properties']['POP2005'] < 10000000
                                   else 'orange' if 10000000 <=
                                   x['properties']['POP2005'] < 20000000
                                   else 'green'}))
    return layer


def area_layer(filename="world.json", name="area", encoding="utf-8-sig"):
    """
    Returns the area layer of map
    :param filename: name of file with info about countries
    :param name: name of layer
    :param encoding: encoding of the file
    :return: layer of the map
    """
    def fill_color(number):
        """Returns color depending on the number"""
        if number < 20000:
            return '#FF0000'
        elif 20000 <= number < 60000:
            return '#FF8800'
        elif 60000 <= number < 100000:
            return '#F2FF00'
        elif 100000 <= number < 140000:
            return '#66FF00'
        elif 140000 <= number < 180000:
            return '#00FFFB'
        elif 180000 <= number < 220000:
            return '#CC00FF'
        elif 220000 <= number < 260000:
            return '#FF00C3'
        else:
            return '#007D45'
    layer = folium.FeatureGroup(name=name)
    layer.add_child(folium.GeoJson(data=open(filename, 'r',
                                             encoding=encoding).read(),
                                   style_function=lambda x:
                                       {'fillColor':
                                           fill_color(x['properties']['AREA'])
                                        }))
    return layer


def map_creator(*layers):
    """
    Creates and saves in html file map with layers.
    Also adds additional layers for map.
    :param layers: layer for the map(area layer, film layer...)
    :return: None
    """
    map_f = folium.Map()
    for layer in layers:
        map_f.add_child(layer)
    folium.TileLayer('cartodbdark_matter').add_to(map_f)
    folium.TileLayer('stamentoner').add_to(map_f)
    folium.TileLayer('Mapbox Control Room').add_to(map_f)
    map_f.add_child(folium.LayerControl())

    dir_path = os.path.dirname(os.path.realpath(__file__))
    map_f.save(dir_path + r'\templates\\map.html')


def main():
    """Main function which calls all other functions"""
    year = input_data(int, "1887 < a < 2027", "Input year: ")
    max_mark = input_data(int, "0 < a < 101",
                          "Input max number of markers(up to 100): ")
    lines = read_file('locations.list')
    random.shuffle(lines)
    countries = country_lst(lines, year)
    random.shuffle(countries)
    locations = get_locations(countries, max_mark)
    map_creator(icon_layer(locations))


if __name__ == '__main__':
    main()
