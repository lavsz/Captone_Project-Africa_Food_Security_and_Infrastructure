import ee
import pandas as pd

def ee_data(subnational): 
            
'''subnational is a geojson that contains the area polygon. 
'''

    mean_ = []
    std_ = []
    subnational['mean_nl'] = 1.000
    subnational['std_nl'] = 1.000

    for i in range(len(subnational)):
        points = ee.ImageCollection('NOAA/VIIRS/DNB/MONTHLY_V1/VCMCFG').filter(ee.Filter.date('2019-12-01' ,
                                  '2020-12-01'))
        image = points.select('avg_rad').first()
    
        mean_.append(image.reduceRegion(**{
    'reducer': ee.Reducer.mean(),
    'geometry': subnational.geom_ee[i],
    'scale': 50,
    'maxPixels': 3e9}))

        std_.append(image.reduceRegion(**{
    'reducer': ee.Reducer.stdDev(),
    'geometry': subnational.geom_ee[i],
    'scale': 50,
    'maxPixels': 3e9}))
    
    
        subnational['mean_nl'][i] = mean_[i].getInfo()['avg_rad']
        subnational['std_nl'][i] = std_[i].getInfo()['avg_rad']