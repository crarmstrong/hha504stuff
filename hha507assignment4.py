#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 14:48:54 2020

@author: hantswilliams

TO RUN: 
    streamlit run week13_streamlit.py

"""
#Imports
import streamlit as st

import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import time


#Loading Data
@st.cache
def load_hospitals():
    df_hospital_2 = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_hospital_2.csv')
    return df_hospital_2

@st.cache
def load_inatpatient():
    df_inpatient_2 = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_inpatient_2.csv')
    return df_inpatient_2

@st.cache
def load_outpatient():
    df_outpatient_2 = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_outpatient_2.csv')
    return df_outpatient_2

#Overview and Intro
st.title('NY Hospital Medicare Purchasing Summary with Comparison of Two NY Geographically Different Areas and their Hospitals')

st.write('Summary of Medicare Purchasing Data along with visualizations of differences between Stony Brook Hospital and New York City Hospitals as a collective.') 
  
# Loading Data   
df_hospital_2 = load_hospitals()
df_inpatient_2 = load_inatpatient()
df_outpatient_2 = load_outpatient()

hospitals_ny = df_hospital_2[df_hospital_2['state'] == 'NY']

#Overview of NY
st.title('Quick Overview of Hospitals in New York')

st.subheader('Hospital Type - NY')
bar1 = hospitals_ny['hospital_type'].value_counts().reset_index()
st.dataframe(bar1)

st.markdown('Number of Hospitals in NY along with type. Acute Care hospitals are most frequent.')

st.markdown('There are a total of 191 hospitals in NY.')
#Average Costs of NY Hospitals Setup
inpatient_ny = df_inpatient_2[df_inpatient_2['provider_state'] == 'NY']
costs = inpatient_ny.groupby('provider_name')['average_total_payments'].sum().reset_index()
costs['average_total_payments'] = costs['average_total_payments'].astype('int64')


costs_medicare = inpatient_ny.groupby('provider_name')['average_medicare_payments'].sum().reset_index()
costs_medicare['average_medicare_payments'] = costs_medicare['average_medicare_payments'].astype('int64')


costs_sum = costs.merge(costs_medicare, how='left', left_on='provider_name', right_on='provider_name')
costs_sum['delta'] = costs_sum['average_total_payments'] - costs_sum['average_medicare_payments']

#Bargraph of Provider Costs
st.title('Costs Between Providers')

bar3 = px.bar(costs_sum, x='provider_name', y='average_total_payments')
st.plotly_chart(bar3)
st.header("Providers along with their average costs")
st.dataframe(costs_sum)


#Costs by Condition and Hospital / Average Total Payments
costs_condition_hospital = inpatient_ny.groupby(['provider_name', 'drg_definition'])['average_total_payments'].sum().reset_index()
st.header("Costs by Condition and Hospital - Average Total Payments")
st.dataframe(costs_condition_hospital)

#Average Inpatient Medicare Payments in SB Hospital vs NYC Hospitals

inpatient_sbu = df_inpatient_2[df_inpatient_2['provider_city'] == 'STONY BROOK']

inpatient_newyork = df_inpatient_2[df_inpatient_2['provider_city'] == 'NEW YORK']

bar4 = inpatient_sbu['average_medicare_payments'].value_counts().reset_index()

bar5 = inpatient_newyork['average_medicare_payments'].value_counts().reset_index()

st.markdown('Before we get into the Cost Comparison, I will list out all NYC hospitals being compared. This list does not include ones that do not provide information such as entries with N/A in them.')

st.markdown('Harlem Hospital Center, Bellevue Hospital Center, Metropolitan Hospital Center, Mount Sinai Beth Israel, Lenox Hill Hospital, New York Presbyterian Hospital, Mount Sinai St. Lukes Roosevelt Hospital, Mount Sinai Hospital, NYU Langone Medical Center, Hospital For Special Surgery.')

st.title('Comparison between Costs of Stony Brook and New York City')

totalvsmedicare1 = inpatient_sbu.groupby('average_total_payments')['average_medicare_payments'].sum().reset_index()

st.dataframe(totalvsmedicare1)

st.markdown('Average Total Payments vs Average Medicare Payments in Stony Brook.')

totalvsmedicare2 = inpatient_newyork.groupby('average_total_payments')['average_medicare_payments'].sum().reset_index()

st.dataframe(totalvsmedicare2)

st.markdown('Average Total Payments vs Average Medicare Payments in New York')

st.markdown('Comparison in average payments between Stony Brook and New York City.')

st.markdown('The average medicare payments in Stony Brook is $19,174.52. The average total payments in Stony Brook is $24,249.19. As a comparison, New York City has an average medicare payment of $19295.26. The average total payments in New York City is $22740.38. New York City has a higher average medicare payment while Stony Brook has a higher total payment.')

st.markdown('Does Stony Brook and New York City compare differently in standards of care?')

st.title('Comparison of Standards of Care between Stony Brook and New York City')

hospital_sbu = df_hospital_2[df_hospital_2['city'] == 'STONY BROOK']

hospital_newyork = df_hospital_2[df_hospital_2['city'] == 'NEW YORK']
#Timelieness Comparison
st.markdown('First, we will look at Timelieness of Care.')


#Timeliness of Care
st.subheader('SBU Hospital - Timelieness of Care')
bar3 = hospital_sbu['timeliness_of_care_national_comparison'].value_counts().reset_index()
fig1 = px.bar(bar3, x='index', y='timeliness_of_care_national_comparison')
st.plotly_chart(fig1)

st.subheader('NYC Hospitals - Timelieness of Care')
bar4 = hospital_newyork['timeliness_of_care_national_comparison'].value_counts().reset_index()
fig2 = px.bar(bar4, x='index', y='timeliness_of_care_national_comparison')
st.plotly_chart(fig2)

st.markdown('It seems like that Stony Brook Hospital has a very similar score of Timeliness of care compared to the Hospitals in NYC. Now, let us look at effectiveness of care.')
#Effectiveness Comparison
st.subheader('SBU Hospital - Effectiveness of Care')
bar3 = hospital_sbu['effectiveness_of_care_national_comparison'].value_counts().reset_index()
fig1 = px.bar(bar3, x='index', y='effectiveness_of_care_national_comparison')
st.plotly_chart(fig1)

st.subheader('NYC Hospitals - Effectiveness of Care')
bar4 = hospital_newyork['effectiveness_of_care_national_comparison'].value_counts().reset_index()
fig2 = px.bar(bar4, x='index', y='effectiveness_of_care_national_comparison')
st.plotly_chart(fig2)
#Same numbers = Same performance???
st.markdown('We can see a very similar story for effectiveness of care when comparing the results to timeliness of care.')
#ending
st.markdown('Despite different geographical locations, both Stony Brook Hospital and the average between all NYC hospitals have almost exact numbers when it comes to both medicare and total payments. There are also very similar results when looking at scoring of care as well. Although we cannot directly show a correlation between both geographical areas and their performance to cost ratios, we can see that there are similarities. With further research into NYC hospitals with data that is not available and more descritive statistics on the scoring process, we can come up with a more accurate response on the relationship between costs of care versus the performances of each hospital in their respective geographical location.')
