class gee_wrapper:

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

    def gee_object(self):
    '''
    converting the geometry object to a GEE engine readable object
    '''
    if self.object_type == 'Polygon':
        return ee.Geometry.Polygon(self.coord_list)

    else:
        return ee.Geometry.MultiPolygon(self.coord_list)

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
        return "gee_wrapper_object(item:'{}', type:'{}')".format(self.centre, self.object_type)

  