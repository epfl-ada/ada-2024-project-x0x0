import pandas as pd
import geopandas as gpd
import plotly.express as px



def draw_map(state_groups):
    #us_map_path = '../../USData/map/us_states_modified.shp'
    #us_states_map = gpd.read_file(us_map_path)
    
    grouped_states_df = to_group_number(state_groups)
    print(grouped_states_df.head(2))
    
    num_groups = len(grouped_states_df['group'].unique())
    colors = px.colors.qualitative.Pastel
    color_map = {f'Group {idx + 1}': colors[idx % len(colors)] for idx in range(num_groups)}
    color_map['No Group'] = 'grey'

    fig = px.choropleth(
        grouped_states_df, 
        locations='state_abbreviation', 
        color='group', 
        color_discrete_map=color_map,
        title="USA State Groups",
        locationmode="USA-states"
    )

    fig.update_traces(hovertemplate='%{customdata[0]}<br><br>%{customdata[3]}')

    fig.update_layout(
        title_text = 'State clustered by beer style parameters',
        geo_scope='usa',
        width=900,  # Adjust width
        height=600,  # Adjust height
        title_font=dict(size=20),  # Optional: Increase title font size
        geo=dict(
            projection_type="albers usa"  # Optional: Adjust projection style if necessary
        )
    )

    fig.show()
    
    return


def to_group_number(clustered_states):
    
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
    
    #map each state to a group number
    state_to_group = {}
    for cluster_num, states in clustered_states.items():
        for state in states:
            state_to_group[state] = f'Group {cluster_num}'

    all_states = set(state_to_abbr.keys())  # Get all states
    grouped_states = [{'state_name': state, 'group': state_to_group.get(state, 'No Group')} for state in all_states]

    grouped_states_df = pd.DataFrame(grouped_states)
    
    grouped_states_df['state_abbreviation'] = grouped_states_df['state_name'].map(state_to_abbr)
    
    return grouped_states_df