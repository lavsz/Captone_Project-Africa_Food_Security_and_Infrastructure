import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import folium
import streamlit as st
from streamlit_folium import folium_static 
import time


#df = pd.read_csv('Social_conflict.csv')
#df_2019 = df[df.year == 2019]
#gdf_2019 = gpd.GeoDataFrame(df_2019, 
 #               geometry=gpd.points_from_xy(df_2019.longitude, df_2019.latitude))

## Source files 
Health_acc = gpd.read_file('health.geojson')
Speed = gpd.read_file('speed.geojson')
Solar_raw = gpd.read_file('solar.geojson')
Wind = gpd.read_file('wind.geojson')
Light = gpd.read_file('nl.geojson')
Solar_need_raw = gpd.read_file('solar_need.geojson')

Solar = Solar_raw[~(Solar_raw['mean'] == 'No info')]
Solar_need = Solar_need_raw[~(Solar_need_raw['region_MW'] == 'No info')]

## Source field formatting
Solar['mean_2'] = Solar['mean'].astype(float).round(2)
Solar_need['region_MW'] = Solar_need['region_MW'].astype(float).round(2)
Wind['mean_wind_2'] = Wind['mean_wind'].astype(float).round(2)
Light['mean'] = Light['mean_nl'].astype(float).round(2)
Health_acc['health_access_mean_hr'] = (Health_acc['health_access_mean']/60).astype(float).round(2)
Speed['travelspeed_access_mean_km'] = (Speed['travelspeed_access_mean'] * 1000).astype(float).round(2)



## Streamlit Board structure
# Main Display
st.title('Africa Development & Potentials Map')
st.write("This project derived the most recent data from: \n  - Google Earth Engine \n - the World Bank") 
st.write ("Data are used to evaluate the currently development stage and future potentials in infrastructure investment. \n Click on the map to find the value.")

# Sidebar and options
add_select = st.sidebar.selectbox("Which basemap do you want?",("OpenStreetMap", "Stamen Terrain", "Stamen Toner"))

select_region = st.sidebar.radio("Pick an Area:",
("North Africa", "East Africa", "Southern Africa", "Western Africa", "Central Africa"))

NA = ['Algeria', 'Egypt', 'Libya', 'Morocco', 'Tunisia', 'Ceuta', 'Melilla', 'Western Sahara'] 
EA = ['Tanzania', 'Kenya', 'Uganda', 'Rwanda', 'Burundi', 'South Sudan', 'Djibouti', 'Eritrea', 'Ethiopia', 'Somalia', 'Somaliland', 'Comoros', 'Mauritius', 'Seychelles', 'Sudan']
SA = ['Angola', 'Botswana', 'Swaziland', 'Lesotho', 'Malawi', 'Mozambique', 'Namibia', 'South Africa', 'Zambia', 'Zimbabwe', 'Tanzania', 'Madagascar']
WA = ['Benin', 'Burkina Faso', 'Cape Verde', 'Gambia', 'Ghana', 'Guinea', 'Guinea-Bissau', "Cï¿½te d'Ivoire", 'Liberia', 'Mali', 'Mauritania', 'Niger', 'Nigeria', 
      'Senegal', 'Sierra Leone', 'Togo', 'Western Sahara', 'Cameroon']
CA = ['Congo', 'Democratic Republic of the Congo', 'Central African Republic', 'Gabon', 'Chad', 
     'Sao Tome and Principe']

region_list = [NA, EA, SA, WA, CA]
regions_list = ["North Africa", "East Africa", "Southern Africa", "Western Africa", "Central Africa"]

select_data = st.sidebar.radio("Pick an indicator:",
("Health Facility Accessibiltiy", "Ground Travel Speed", "Solar Potential", "Wind Potential", "Night Light"))

select_prediction = st.sidebar.radio("Pick a Prediction:",
("Solar Development Need", "Wind Development Need"))
pred_list = ["Solar Development Need", "Wind Development Need"]

## Visualization map function

def show_maps(select_data):
    
    m = folium.Map(tiles=add_select, location=[4, 22], zoom_scale = 5)
    
    for i in range(0, 5):
    
        if select_region == regions_list[i]:
        
        
            if select_data == 'Health Facility Accessibiltiy':
            
                NAs = Health_acc[Health_acc.ADM0_NAME.isin(region_list[i])].reset_index(drop=True)
          
        
                map1 = folium.Choropleth(
                    geo_data = NAs, 
                    data = NAs,
            
                    columns=['ADM1_NAME','health_access_mean_hr'], 
                    key_on='feature.properties.ADM1_NAME',
                  fill_color='BuPu', fill_opacity=0.6, line_opacity=1,line_color='white',                            legend_name='Average Travel Time (hr) to the Closest Health Facility',
                highlight=True).add_to(m)
            
                map1.geojson.add_child(
                folium.features.GeoJsonTooltip(
                                     fields=['ADM1_NAME', 'ADM0_NAME', 'health_access_mean_hr'],
                                    aliases=['Region Name:', 'Country:', 'Average Travel Time (hr):'],
                          label='{}:{}'.format(NAs['ADM1_NAME'],
                                  NAs['ADM0_NAME'], NAs['health_access_mean_hr'])))
                #folium.LayerControl().add_to(m)
           
            if select_data == "Ground Travel Speed":
        
                NAs = Speed[Speed.ADM0_NAME.isin(region_list[i])].reset_index(drop=True)
        
                myscale = (NAs['travelspeed_access_mean_km'].quantile((0,0.1,0.75,0.9,0.98,1))).tolist()
        
                map1 = folium.Choropleth(
                    geo_data = NAs, 
                    data = NAs,
            
                    columns=['ADM1_NAME','travelspeed_access_mean_km'], 
                    key_on='feature.properties.ADM1_NAME',
                  fill_color='PuRd',
                  fill_opacity=0.6, line_opacity=1,line_color='white', threshold_scale=myscale, legend_name='Average Ground Travel Speed',
                highlight=True).add_to(m)
            
                map1.geojson.add_child(
                folium.features.GeoJsonTooltip(
                                    fields=['ADM1_NAME', 'ADM0_NAME', 'travelspeed_access_mean_km'],
                                    aliases=['Region Name:', 'Country:',
                                             'Average Travel Time (min/km):'],
                    label='{}:{}'.format(NAs['ADM1_NAME'],
                                         NAs['ADM0_NAME'], NAs['travelspeed_access_mean_km'])))
                
            if select_data == "Solar Potential":
        
                NAs = Solar[Solar.ADM0_NAME.isin(region_list[i])].reset_index(drop=True)
        
                myscale = (NAs['mean_2'].quantile((0,0.1,0.75,0.9,0.98,1))).tolist()
        
                map1 = folium.Choropleth(
                   geo_data = NAs, 
                    data = NAs,
           
                    columns=['ADM1_NAME','mean_2'], 
                    key_on='feature.properties.ADM1_NAME',
                  fill_color='YlOrRd', fill_opacity=0.6, line_opacity=1,line_color='white',                                 threshold_scale=myscale, 
                    legend_name='Average Annual Solar Potential Sum (kWh/kWp)', 
                highlight=True).add_to(m)
            
                map1.geojson.add_child(
                folium.features.GeoJsonTooltip(
                                    fields=['ADM1_NAME', 'ADM0_NAME', 'mean_2'],
                                    aliases=['Region Name:', 'Country:', 
                                           'Solar Potential (kWh/kWp):'],
                    label='{}:{}'.format(NAs['ADM1_NAME'],
                                         NAs['ADM0_NAME'], NAs['mean_2'])))
                
                 
            if select_data == "Wind Potential":
        
                NAs = Wind[Wind.ADM0_NAME.isin(region_list[i])].reset_index(drop=True)
        
                myscale = (NAs['mean_wind_2'].quantile((0,0.1,0.75,0.9,0.98,1))).tolist()
        
                map1 = folium.Choropleth(
                   geo_data = NAs, 
                    data = NAs,
           
                    columns=['ADM1_NAME','mean_wind_2'], 
                    key_on='feature.properties.ADM1_NAME',
                  fill_color='YlOrBr', fill_opacity=0.6, line_opacity=1,line_color='white',                                 threshold_scale=myscale, 
                    legend_name='Average Annual Wind Power Density (W/sq-meter)', 
                highlight=True).add_to(m)
            
                map1.geojson.add_child(
                folium.features.GeoJsonTooltip(
                                    fields=['ADM1_NAME', 'ADM0_NAME', 'mean_wind_2'],
                                    aliases=['Region Name:', 'Country:', 
                                           'Wind Power Density (W/sq-meter):'],
                    label='{}:{}'.format(NAs['ADM1_NAME'],
                                         NAs['ADM0_NAME'], NAs['mean_wind_2'])))
            if select_data == "Night Light":
        
                NAs = Light[Light.ADM0_NAME.isin(region_list[i])].reset_index(drop=True)
        
                myscale = (NAs['mean'].quantile((0,0.1,0.75,0.9,0.98,1))).tolist()
        
                map1 = folium.Choropleth(
                   geo_data = NAs, 
                    data = NAs,
           
                    columns=['ADM1_NAME','mean'], 
                    key_on='feature.properties.ADM1_NAME',
                  fill_color='GnBu', fill_opacity=0.6, line_opacity=1,line_color='white',                                 threshold_scale=myscale, 
                    legend_name='Average Annual Nighttime Light Radiance (nanoWatts/cm2/sr)', 
                highlight=True).add_to(m)
            
                map1.geojson.add_child(
                folium.features.GeoJsonTooltip(
                                    fields=['ADM1_NAME', 'ADM0_NAME', 'mean'],
                                    aliases=['Region Name:', 'Country:', 
                                           'Nighttime Light Radiance (nanoWatts/cm2/sr):'],
                    label='{}:{}'.format(NAs['ADM1_NAME'],
                                         NAs['ADM0_NAME'], NAs['mean'])))
            
    return(folium_static(m))
show_maps(select_data)    

st.write("Are you interested in the development potential?")

## Visualization pred results

def show_ind(select_prediction):
    
    m = folium.Map(tiles=add_select, location=[4, 22], zoom_scale = 5)
    
    for i in range(0, 5):
    
        if select_region == regions_list[i]:
        
        
            if select_prediction == 'Solar Development Need':
            
                NAs = Solar_need[Solar_need.ADM0_NAME.isin(region_list[i])].reset_index(drop=True)
          
        
                map1 = folium.Choropleth(
                    geo_data = NAs, 
                    data = NAs,
            
                    columns=['ADM1_NAME','region_MW'], 
                    key_on='feature.properties.ADM1_NAME',
                  fill_color='BuPu', fill_opacity=0.6, line_opacity=1,line_color='white',                            legend_name='Estimated Regional Solar Development Need (MW)',
                highlight=True).add_to(m)
            
                map1.geojson.add_child(
                folium.features.GeoJsonTooltip(
                                     fields=['ADM1_NAME', 'ADM0_NAME', 'pop_percent_with_elec', 'region_MW'],
                                    aliases=['Region Name:', 'Country:', 'Existing Electricity Access (%)', 'Estimated Regional Solar Development Need (MW)'],
                          label='{}:{}'.format(NAs['ADM1_NAME'],NAs['ADM0_NAME'],
                                   NAs['pop_percent_with_elec'], NAs['region_MW'])))
                
            if select_prediction == 'Wind Development Need':
            
                NAs = Solar_need[Solar_need.ADM0_NAME.isin(region_list[i])].reset_index(drop=True)
          
        
                map1 = folium.Choropleth(
                    geo_data = NAs, 
                    data = NAs,
            
                    columns=['ADM1_NAME','region_MW'], 
                    key_on='feature.properties.ADM1_NAME',
                  fill_color='BuPu', fill_opacity=0.6, line_opacity=1,line_color='white',                            legend_name='Estimated Regional Solar Development Need (MW)',
                highlight=True).add_to(m)
            
                map1.geojson.add_child(
                folium.features.GeoJsonTooltip(
                                     fields=['ADM1_NAME', 'ADM0_NAME', 'pop_percent_with_elec', 'region_MW'],
                                    aliases=['Region Name:', 'Country:', 'Existing Electricity Access (%)', 'Estimated Regional Solar Development Need (MW)'],                     
                                             label='{}:{}'.format(NAs['ADM1_NAME'],NAs['ADM0_NAME'],
                                   NAs['pop_percent_with_elec'], NAs['region_MW'])))
         
         
    return(folium_static(m))
    

with st.spinner('Wait for it...'):
    time.sleep(5)
st.success('Done!')   


show_ind(select_prediction)
