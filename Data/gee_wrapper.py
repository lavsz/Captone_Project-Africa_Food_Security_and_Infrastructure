from shapely.geometry import Point, LineString, Polygon
import geopandas

class geometry_object:

    def __init__(self, geo_object):
    '''
    geo_object: a geometry object that is in the format of: Polygon or MultiPolygon 
    '''
        self.geo_object = geo_object
    # obtain geometry type
        self.object_type = geo_object.geom_type
    # obtain object centroid
        self.centre = geo_object.centroid.wkt
    # obtain a list of coordinates for conversion
        self.coord_list = list(mapping(geo_object)['coordinates'])

    def real_distance (lat1, lat2, lon1, lon2):
        R_earth = 6360.57
        dlon = math.radians(lon2 - lon1)
        dlat = math.radians(lat2 - lat1)
        a = float((sin(dlat/2))**2 + cos(lat1) * cos(lat2) * (sin(dlon/2))**2)
        c = float(2 * atan2(sqrt(a), sqrt(1-a)))
        distance = float(R_earth * c)
        return distance
    
    def geo_distance(self, other):
        
    '''
    calculating distance between two geometry objects
    two points - real distance between two points
    one point vs one polygon - real distance between the point and polygon centroid
    two polygons - real distance between the two centroids
    two polylines - minimum real distance between the two lines
    '''    
    
        if self.object_type == 'Point' and other.geom_type == 'Point':
            lat1 = self.coords[0][1]
            lat2 = self.coords[0][1]
            lon1 = other.coords[0][0]
            lon2 = other.coords[0][0]
            return real_distance(lat1, lat2, lon1, lon2)
        
        elif self.object_type == 'Point' and other.geom_type == 'Polygon':
            lat1 = self.centre.coords[0][1]
            lat2 = self.centre.coords[0][1]
            lon1 = other.centroid.coords[0][0]
            lon2 = other.centroid.coords[0][0]
            return real_distance(lat1, lat2, lon1, lon2)

        elif self.object_type == 'Polygon' and other.geom_type == 'Polygon':
            lat1 = self.centroid.coords[0][0]
            lat2 = self.centroid.coords[0][1]
            lon1 = other.centroid.coords[0][0]
            lon2 = other.centroid.coords[0][0]
            return real_distance(lat1, lat2, lon1, lon2)

        elif self.object_type == 'Polyline' and other.geom_type == 'Polyline':   
            l1 = LineString(self.coord_list)
            l2 = LineString(other.coordinates) 
            return l1.distance(l2)
    
    def gee_object(self):
    '''
    converting the geometry object to a GEE engine readable object
    '''
        if self.object_type == 'Polygon':
            return ee.Geometry.Polygon(self.coord_list)

        elif self.object_type == 'MultiPolygon':
            return ee.Geometry.MultiPolygon(self.coord_list)
        
        elif self.object_type == 'Point':
            return ee.Geometry.Point(self.coord_list)
            
        elif self.object_type == 'Polyline':
            return ee.Geometry.LineString(self.coord_list)

    def stats_reducer(self, map_name, layer_name, start_date, end_date, target_stats = None, scale = None, max_pixel = None):
    '''
    caculate statistics for specified region and date ranges
    map_name, layer_name: accessible from GEE catelog
   
    '''
    # Stats options
        reducer_options = {'mean': ee.Reducer.mean(), 
                  'median': ee.Reducer.median(), 
                  'min': ee.Reducer.min(),
                  'max': ee.Reducer.max(),
                  'stdev': ee.Reducer.stdDev(),
                  'skewness': ee.Reducer.kurtosis()}
    # Collect images from the map
        layers = ee.ImageCollection("{}".format(map_name)).filter(ee.Filter.date('{}'.format(start_date) ,
                                  '{}'.format(end_date)))
        image = layers.select('{}'.format(layer_name)).first()
    
    # Create reducer dictionary for calculation
        reducer_dict = {}
        reducer_dict['geometry'] = self.gee_object()

        if target_stats:
            reducer_dict['reducer'] = reducer_options[target_stats]
        else:
            reducer_dict['reducer'] = ee.Reducer.mean()

        if scale:
            reducer_dict['scale'] = scale
        else:
            reducer_dict['scale'] = 50

        if max_pixel:
            reducer_dict['maxPixels'] = max_pixel
        else:
            reducer_dict['maxPixels'] = 3e9

        return '{}'.format(target_stats), image.reduceRegion(**reducer_dict).getInfo()

    def __repr__(self):
        return "geometry_object(item:'{}', type:'{}')".format(self.centre, self.object_type)

  