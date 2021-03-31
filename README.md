# Project: Africa Development Potentials and Food Security
by Shenghao (Lavender) Zhang

The year of Covid-19 strengthens more about Sustainability Development worldwide and disease spreading prevention made people start to think more about food security. 

## Overview
This project cooks a two-course meal:

1. Studying geophysical and social factors that contributes to Food Security concerns in selected region
2. Looking at infrastructure development potential


**The first course**: aims to built a classification model that can identifies areas with higher food security concerns. 

**The second course**: aims to look at different geophysical, accessibility, facilities, and social factors to propose a new evaluation method for development potentials in the infrastructure sector. 

## First Course: Food Security Machine Learning Model

**How's the distribution of different food security class?**

<img src = 'https://github.com/lavsz/Captone_Project-Africa_Sustainability_and_Food_Security/blob/main/Images/Screen%20Shot%202021-03-29%20at%2010.39.44%20PM.png' width="350" height="210">

**On Average, how are different countries throughout the year looks like?**

<img src = 'https://github.com/lavsz/Captone_Project-Africa_Sustainability_and_Food_Security/blob/main/Images/Screen%20Shot%202021-03-30%20at%2012.56.17%20AM.png' width="450" height="250">

Note: Madagascar was note evaluated for 2010 to 2015. 

**Are there many social conflict events happening?**

<img src = 'https://github.com/lavsz/Captone_Project-Africa_Sustainability_and_Food_Security/blob/main/Images/Screen%20Shot%202021-03-29%20at%2011.40.39%20PM.png' width="520" height="250"> 

Protests went by a lot in 2020. 

**Machine Learning Models**

To classify the severity level of food security in Africa, time-specific geophysical data, nighttime light, and social conflict records were added to the model. After the first evaluation, it was noticed that imbalanced classes are really affecting the modeling results. The goal is the model is to be able to alert regions that would have high possibility in severe food crisis.  

To better separate very severe vs less severe conditions, Class 1 (minimal) and Class 2 (stressed) are being grouped into Class 2 (less severe); Class 3 (crisis), Class 4 (emergency), and Class 5 (famine) are group into Class 3 (very severe). 

Two winning model algorithms are:

XGBoost - 81.04% 
Random Forest Classifier = 80.8%

XGBoost is slightly stronger with also less discrepancies between training and testing sets. 


**What are the top contributors?**

<img src = 'https://github.com/lavsz/Captone_Project-Africa_Sustainability_and_Food_Security/blob/main/Images/Screen%20Shot%202021-03-30%20at%201.01.18%20AM.png' width="520" height="250">

Top 5: Number of battles, Net Primary Productivity, Net Sensible heat net flux, Soil Moisture Level, and Nighttime Light Radiance

## Second Course: Development Potentials Evaluation
After realizing the importance of social and infrastructure in food security, a simple dashboard has been built to demonstrate the current situation of infrastructures & potentials as well as predicting development needs in Africa. 

**Selected infrastructures & status are:**
1. Accessibility to Health Facilities (2019 Annual Average)
2. Ground Travel Speed (reflection for transportation quality) (2019 Annual Average)
3. Nighttime Light (2020 Annual Average)
4. Solar Potentials (most recent available from Global Solar Atlas)
5. Wind Potentials (most recent available from Global Wind Atlas)

**Development needs are predicted:**
1. Regional Development needs of Solar
2. Regional Development needs of Wind

The predictions are based on current production of electricity, population percentage with electricity access, and regional potentials. 

Here's a look of the dashboard:

<img src = 'https://github.com/lavsz/Captone_Project-Africa_Sustainability_and_Food_Security/blob/main/Images/Screen%20Shot%202021-03-30%20at%201.13.40%20AM.png' width="520" height="250">

## Data Source:
1. Famine Early Warning Network: website access [here](https://fews.net)
2. Famine Early Warning Systems Network (FEWS NET) Land Data Assimilation System: documentation [here](https://developers.google.com/earth-engine/datasets/catalog/NASA_FLDAS_NOAH01_C_GL_M_V001)
3. VIIRS Nighttime Day/Night Band Composites: documentation [here](https://developers.google.com/earth-engine/datasets/catalog/NOAA_VIIRS_DNB_MONTHLY_V1_VCMCFG)
4. DMSP OLS: Nighttime Lights Time Series Version 4, Defense Meteorological Program Operational Linescan System: documentation [here](https://developers.google.com/earth-engine/datasets/catalog/NOAA_DMSP-OLS_NIGHTTIME_LIGHTS?hl=en)
5. POR Dekadal Net Primary Production: documentation [here](https://developers.google.com/earth-engine/datasets/catalog/FAO_WAPOR_2_L1_NPP_D?hl=en)
6. The Armed Conflict Location & Event Data Project: documentation [here](https://acleddata.com/#/dashboard)


