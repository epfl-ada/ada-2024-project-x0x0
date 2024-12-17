import pandas as pd
import geopandas as gpd
import plotly.express as px



def draw_map(state_groups, final_cohen_df):
    #us_map_path = '../../USData/map/us_states_modified.shp'
    #us_states_map = gpd.read_file(us_map_path)
    
    grouped_states_df = to_group_number(state_groups)
    
    # Filter Cohen's d data based on region and state
    filtered_cohen_df = final_cohen_df[
        (final_cohen_df['Region'] == final_cohen_df['State1']) | (final_cohen_df['Region'] == final_cohen_df['State2'])
    ]

    adjusted_df = adjust_cohen_d(filtered_cohen_df)

    region_dict = create_region_dict(adjusted_df)
    
    hover_df = hover_text(region_dict)
    
    grouped_states_df = grouped_states_df.merge(hover_df[['state_abbreviation', 'hover_text']], on='state_abbreviation', how='left')
    
    # Step 10: Plot choropleth map
    num_groups = len(grouped_states_df['group'].unique())
    colors = px.colors.qualitative.Set2
    color_map = {f'Group {idx + 1}': colors[idx % len(colors)] for idx in range(num_groups)}
    color_map['No Group'] = 'grey'

    fig = px.choropleth(
        grouped_states_df, 
        locations='state_abbreviation', 
        color='group', 
        color_discrete_map=color_map,
        title="USA State Groups",
        locationmode="USA-states",
        hover_name='state_name',
        hover_data={'state_name': False, 'group': False, 'state_abbreviation': False, 'hover_text': True}  # Disable state abbreviation and hover text
    )

    fig.update_traces(hovertemplate='%{customdata[0]}<br><br>%{customdata[3]}')

    fig.update_layout(
        title_text = 'State Groups by Cohen\'s d',
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
    
    
def to_group_number(state_groups):
    
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
    for idx, group in enumerate(state_groups):
        for state in group['States']:
            state_to_group[state] = f'Group {idx + 1}'

    all_states = set(state_to_abbr.keys())  # Get all states
    grouped_states = [{'state_name': state, 'group': state_to_group.get(state, 'No Group')} for state in all_states]

    grouped_states_df = pd.DataFrame(grouped_states)
    
    grouped_states_df['state_abbreviation'] = grouped_states_df['state_name'].map(state_to_abbr)
    
    return grouped_states_df
    
    
def adjust_cohen_d(filtered_cohen_df):
    
    mask = filtered_cohen_df['State2'] == filtered_cohen_df['Region']
    
    # Switch State1 and State2, and invert Cohen_d
    filtered_cohen_df.loc[mask, ['State1', 'State2']] = filtered_cohen_df.loc[mask, ['State2', 'State1']].values
    filtered_cohen_df.loc[mask, 'Cohen_d'] = -filtered_cohen_df.loc[mask, 'Cohen_d']
    
    return filtered_cohen_df


def create_region_dict(adjusted_df):
    
    region_dict = {}
    for region, group in adjusted_df.groupby('Region'):
        region_dict[region] = group[['State2', 'Cohen_d']].to_dict(orient='records')
    return region_dict


def hover_text(region_dict):
    
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
    
    #create hover text and state abbreviation mapping for visualization
    hover_data = []
    for region, cohen_d_values in region_dict.items():
        for entry in cohen_d_values:
            hover_data.append({
                'state_name': region,
                'State2': entry['State2'],
                'Cohen_d': entry['Cohen_d'],
                'Region': region
            })
    
    hover_df = pd.DataFrame(hover_data)
    
    hover_df['hover_text'] = hover_df.apply(
    lambda row: "Cohen's d values:<br>" + 
                '<br>'.join([f"{state}: {cohen_d:.4f}" for state, cohen_d in zip(hover_df[hover_df['Region'] == row['Region']]['State2'], 
                                                                            hover_df[hover_df['Region'] == row['Region']]['Cohen_d']) ]),
                                                                            axis=1
                                                                            )
    
    hover_df = hover_df.drop(columns=['state_name','State2', 'Cohen_d'])

    #drop duplicates, keeping only one row per region
    hover_df = hover_df.drop_duplicates(subset='Region').reset_index(drop=True)
    
    hover_df['state_abbreviation'] = hover_df['Region'].map(state_to_abbr)
    
    return hover_df
