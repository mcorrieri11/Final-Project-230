"""
Class: CS230--Section 004
Name: Matt Corrieri
Description: (Exercise Name)
I pledge that I have completed the programming assignment independently. 
I have not copied the code from a student or any source.
I have not given my code to any student. 
"""
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import pydeck as pdk
from PIL import Image

st.set_page_config(layout="wide")
st.title("California Fire Incidents",)
st.header("Analyzing Data of California Wildfires")

df = pd.read_csv('California_Fire_Incidents (1).csv',
                 header=0,
                 names=['AcresBurned', 'Active', 'AdminUnit', 'AirTankers', 'ArchiveYear', 'CalFireIncident',
                        'CanonicalUrl', 'ConditionStatement', 'ControlStatement', 'Counties', 'CountyIds',
                        'CrewsInvolved', 'Dozers', 'Engines', 'Extinguished', 'Fatalities', 'Featured', 'Final',
                        'FuelType', 'Helicopters', 'Injuries', 'Latitude', 'Location', 'Longitude', 'MajorIncident',
                        'Name', 'PercentContained', 'PersonnelInvolved', 'Public', 'SearchDescription',
                        'SearchKeywords', 'Started', 'Status', 'StructuresDamaged', 'StructuresDestroyed',
                        'StructuresEvacuated', 'StructuresThreatened', 'UniqueId', 'Updated', 'WaterTenders'])


def sidebar():
    with st.sidebar:
        favorite = st.sidebar.radio("What made you visit the site?",
                                    ('Python Class', 'Forest Fire Interest', 'Research Report'))
        if favorite == 'Python Class':
            st.sidebar.write("CS 230 is a great class!")
        elif favorite == 'Forest Fire Interest':
            st.sidebar.write("California is notorious for its rampant forest fires.")
        elif favorite == 'Research Report':
            st.sidebar.write("Lots of great data on this page!")
def city(input):
    st.write(f'{input} is a great city!')
    return input


option = st.sidebar.selectbox("Click which page you would like to visit",
                              ('Home Page', 'Graph #1: Acres Burned by County', 'Graph #2: Wildfires by Year',
                               'Graph #3: Total Amount of Dozers and Helicopters Used', 'Map of Wildfires'))

if option == 'Home Page':
    st.subheader('Welcome to the Home Page!')
    img = Image.open('wildfire.jfif')
    width, height = img.size
    resized_img = img.resize((width * 3, height * 2))
    st.image(resized_img)

    if st.checkbox("Click to display of the heroic Admin Units of CA!"):
        st.image("paradiseCali.jfif", use_column_width=True)
        st.image('firemen.jfif', use_column_width=True)
        st.subheader("These men risk their lives everyday to save the state of CA from ablaze.")

if option == 'Graph #1: Acres Burned by County':
    st.subheader('Graph #1: Acres Burned by County')
    counties = df['Counties'].unique()
    counties = counties.tolist()
    list_of_counties = df['Counties'].tolist()
    input = city(st.text_input("What is your favorite city in California?"))

    fires = []
    for i in counties:
        amount_of_fires = 0
        for j in list_of_counties:
            if j == i:
                amount_of_fires += 1
        fires.append(amount_of_fires)
        fires.sort()

    first_graph = plt.figure()
    plt.bar(counties, fires, color='maroon', width=.75)
    plt.ylabel('Total Forest Fires', font='Times New Roman', fontsize='medium')
    plt.xlabel('Counties', font='Times New Roman', fontsize='medium')
    plt.yticks(font='Times New Roman', fontsize='small')
    plt.xticks(font='Times New Roman', fontsize='xx-small', rotation=90)
    plt.title("Total Amount of Fires per County", font='Times New Roman', fontsize='large', fontweight='bold')
    st.pyplot(first_graph)
    st.markdown("<hr>", unsafe_allow_html=True)



if option == 'Graph #2: Wildfires by Year':
    st.subheader('Graph #2: Wildfires by Year')

    year = df['ArchiveYear'].unique().tolist()
    list_of_years = df['ArchiveYear'].tolist()

    fires = [list_of_years.count(i) for i in year]
    colors = ['red', 'blue', 'yellow', 'green', 'purple', 'pink', 'orange']
    years_of_data = ['2013', '2014', '2015', '2016', '2017', '2018', '2019']

    fig, ax = plt.subplots()
    plt.xlabel('This pie chart examines the proportion of fires from 2013 - 2019.', fontfamily='Serif',
               fontsize='small')
    plt.title("% of Wildfires by Year", fontfamily='Serif', fontweight='bold')
    plt.pie(fires, colors=colors, autopct='%.2f%%', )
    plt.legend(labels=years_of_data, loc='upper left', fontsize='x-small')
    st.pyplot(fig, ax)
    st.markdown("<hr>", unsafe_allow_html=True)

    wildfires = st.number_input("How many wildfires do you think started in CA in 2021? ")
    if wildfires > 7396:
        st.write(f'{wildfires} is way too many! Hopefully this never happens.')
    elif wildfires < 7396:
        st.write(f'No, there were more than {wildfires} wildfires. Shocking!')
    else:
        st.write(f"That's correct! There were {wildfires} in CA last year.")

if option == 'Graph #3: Total Amount of Dozers and Helicopters Used':
    st.subheader('Graph #3: Total Amount of Dozers and Helicopters Used')
    df4 = pd.DataFrame(df, columns=['ArchiveYear', 'Dozers', 'Helicopters'])
    df4 = df4.dropna()
    df4 = df4.groupby('ArchiveYear')['Dozers', 'Helicopters'].sum()
    st.write(df4)

    third_graph = plt.figure(figsize=(8, 6))
    plt.bar(df4.index, df4['Dozers'], color='blue', width=.2, label='Dozers')
    plt.bar(df4.index, df4['Helicopters'], color='red', width=.2, label='Helicopters')
    plt.ylabel('Total Amount of Dozers and Helicopters', font='Times New Roman', fontsize='x-large')
    plt.xlabel('Year', font='Times New Roman', fontsize='x-large')
    plt.yticks(font='Times New Roman', fontsize='small')
    plt.xticks(font='Times New Roman', fontsize='small', rotation=90)
    plt.title("Total Amount of Dozers and Helicopters used per Year", font='Times New Roman', fontsize='xx-large',
              fontweight='bold')
    plt.legend(labels=['Dozers', 'Helicopters'], loc='upper right', fontsize='small')
    st.pyplot(third_graph)

    st.markdown("<hr>", unsafe_allow_html=True)

if option == 'Map of Wildfires':
    st.subheader('Map of Wildfires')
    new_df = df[['Latitude', 'Longitude']]
    new_df['lat'] = df['Latitude']
    new_df['lon'] = df['Longitude']

    view_state = pdk.ViewState(
        latitude=new_df['lat'].mean(),
        longitude=new_df['lon'].mean(),
        zoom=5,
        pitch=0)

    layers = pdk.Layer('ScatterplotLayer',
                       data=new_df,
                       get_position=['lon', 'lat'],
                       get_radius=1000,
                       get_color='blue',
                       pickable=True)
    new_map = pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=view_state,
        layers=layers)

    st.write("Here is a map of CA Wildfires. Interact to learn more!")
    st.pydeck_chart(new_map)
    st.markdown("<hr>", unsafe_allow_html=True)

sidebar()
