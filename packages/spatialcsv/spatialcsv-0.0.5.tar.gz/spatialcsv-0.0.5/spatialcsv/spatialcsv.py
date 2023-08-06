"""Main module."""
import pandas as pd
import csv
import ipyleaflet
import xyzservices.providers as xyz

#def import_csv(filepath, skip=none, delimiters=','):
 #   pass



class Locations:
    """Inputs a csv with locational data and outputs the proper format to import into a webmap"""

    def __init__(self, csv, lat=None, long=None, **kwargs):
        """
        Keyword arguments:
        csv -- the filepath to the csv file. It is assumed that the delimiter is ','
        lat -- the column header name of the latitude values
        long -- the column header name of the longitude values
        """
        self.csv = csv
        self.lat = lat
        self.long = long


    def checks(self):
        """
        Checks to make sure file exists, has a header, 
        the lat and long variables exist in the header
        """
        with open(self.csv, 'r') as csvfile:
            head = csv.Sniffer().has_header(csvfile.read(1024))
                
            if head:
                pass
            else:
                print("This csv file does not seem to have a header. Please add column names in the top line of the csv.")
        
        # add exception  FileNotFoundError:
        
        if self.lat in self.header():
            pass
        else:
            print(f"The value '{self.lat}' is not in the header.")
        if self.long in self.header():
            pass
        else:
            print(f"The value '{self.long}' is not in the header.")
        print("done")


    def header(self):
        """Returns header row"""
        with open(self.csv) as csvfile:
            reader = csv.DictReader(csvfile)
            header = reader.fieldnames
            print(list(header))
            return header


class Map(ipyleaflet.Map):
    
    def __init__(self, **kwargs):
        #self.bbox = bbox
        #self.csv = csv


        def fit_bounds():
            """Zooms map to the bounds of the csv"""
            bbox = [[],[]] #south, west, north, east
            self.fit_bounds(bbox)
        #get extreme lat and long from the csv, import into bbox so the map is centered at the right spot
        #alternatively center the map around the center lat/long?

    def add_tile_layer(self, url, name, attribution="", **kwargs):
        """Adds a tile layer to the map.
        Args:
            url (str): The URL of the tile layer.
            name (str): The name of the tile layer.
            attribution (str, optional): The attribution of the tile layer. Defaults to "".
        """
        tile_layer = ipyleaflet.TileLayer(
            url=url,
            name=name,
            attribution=attribution,
            **kwargs
        )
        self.add_layer(tile_layer)


    def add_basemap(self, basemap):
        """Change the default basemap"""
        basemap = eval(f"xyz.{basemap}")
        url = basemap.build_url()
        attribution = basemap.attribution
        self.add_tile_layer(url, name=basemap.name, attribution=attribution)
                


    def add_geojson(self, data, name='GeoJSON', **kwargs):
        """Adds a GeoJSON layer to the map.
        Args:
            data (dict): The GeoJSON data.
        """

        if isinstance(data, str):
            import json
            with open(data, "r") as f:
                data = json.load(f)

        geojson = ipyleaflet.GeoJSON(data=data,name=name, **kwargs)
        self.add_layer(geojson)

    def add_shp(self, data, name='Shapefile', **kwargs):
        """Adds a Shapefile layer to the map.
        Args:
            data (str): The path to the Shapefile.
        """
        import geopandas as gpd
        gdf = gpd.read_file(data)
        geojson = gdf.__geo_interface__
        self.add_geojson(geojson, name=name, **kwargs)


    def add_geojson(self, data, **kwargs):
        """Adds a GeoJSON layer to the map.
        Args:
            data (dict): The GeoJSON data.
            kwargs: Keyword arguments to pass to the GeoJSON layer.
        """
        import json

        if isinstance(data, str):
            with open(data, "r") as f:
                data = json.load(f)

        geojson = ipyleaflet.GeoJSON(data=data, **kwargs)
        self.add_layer(geojson)



m = Map()
m.add_basemap('CartoDB.Positron')

