import pandas as pd
import plotly.express as px
import os



def draw_umap_map(df_cleaned):

    state_to_abbr = {
        'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
        'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA',
        'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA',
        'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
        'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS', 'Missouri': 'MO',
        'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ',
        'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH',
        'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
        'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT',
        'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'
    }

    df_cleaned['state_abbreviation'] = df_cleaned['user_state'].map(state_to_abbr)

    df_cleaned['Cluster'] = df_cleaned['Cluster'].astype(str) #should be already done but just in case
    
    cluster_color_map = {
        '0': '#5b8a72',  
        '1': '#4f0205',  
        '2': '#a46e51', 
        '3': '#6e6456', 
        '4': '#dd660d', 
        '5': '#3d5d44' 
    }

    fig = px.choropleth(
        df_cleaned, 
        locations='state_abbreviation', 
        color='Cluster', 
        color_discrete_map=cluster_color_map,  
        title="USA State Clusters Based on DBSCAN",
        locationmode="USA-states",
        hover_name='user_state',  
        hover_data={'user_state': False, 'Cluster': False, 'state_abbreviation': False}
    )

    fig.update_layout(
        geo_scope='usa',
        width=700,
        height=500,  
        title_font=dict(size=20),
        geo=dict(projection_type="albers usa")
    )

    fig.show()
    directory = 'img/question4/'
    fig.write_html(os.path.join(directory, "usa_state_cluster_based_on_dbscan.html"))
    
    return