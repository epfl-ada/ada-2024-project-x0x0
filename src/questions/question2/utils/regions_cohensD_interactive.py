import pandas as pd
from src.questions.question2.utils.cohenD import cohen_d
import numpy as np
import plotly.express as px
import os

def regions_cohenD_interactive(df_neighbours, US_ratings, plot=True):
    cohen_results_by_region = {}
    
    for index, row in df_neighbours.iterrows():
        state = row['state']
        neighbours = row['neighbours']

        if neighbours:
            region_states = [state] + neighbours
        else:
            region_states = [state]  

        in_region_ratings = US_ratings[US_ratings['user_state'].isin(region_states)]['rating']
        out_of_region_ratings = US_ratings[~US_ratings['user_state'].isin(region_states)]['rating'] 

        if len(in_region_ratings) < 2 or len(out_of_region_ratings) < 2:  
            print(f"Warning: Insufficient data for Cohen's d test for region: {state}")
            cohen_results_by_region[state] = np.nan
            continue

        d_value = cohen_d(in_region_ratings, out_of_region_ratings)
        cohen_results_by_region[state] = d_value

    cohen_by_region_df = pd.DataFrame.from_dict(cohen_results_by_region, orient='index', columns=['Cohen_d'])
    cohen_by_region_df.index.name = 'Center State of each Region'
    cohen_by_region_df = cohen_by_region_df.reset_index()
    cohen_by_region_df = cohen_by_region_df.sort_values(by='Cohen_d', ascending=False)

    if plot:
        colour_scale = ['#1e0f0d', '#6e4b3c', '#f2a900', '#f8d53f']

        fig = px.bar(cohen_by_region_df,
                     x='Center State of each Region',
                     y='Cohen_d',
                     color='Cohen_d',
                     color_continuous_scale=colour_scale,
                     title="Cohen's D for In-Region Ratings Compared to Out-of-Region Ratings",
                     labels={'Cohen_d': "Cohen's D Value", 'Center State of each Region': 'Region Group'})

        fig.add_hline(y=0.2, line_dash="dot", line_color="orange", annotation_text="Small effect (d=0.2)", annotation_position="top right")
        fig.add_hline(y=-0.2, line_dash="dot", line_color="orange")
        fig.add_hline(y=0.5, line_dash="dot", line_color="red", annotation_text="Medium effect (d=0.5)", annotation_position="top right")
        fig.add_hline(y=-0.5, line_dash="dot", line_color="red")

        fig.update_traces(
            marker_line_color='black',
            marker_line_width=1,
            text=None
        )

        fig.update_layout(
            plot_bgcolor='white', 
            paper_bgcolor='white',
            xaxis=dict(
                title='Region Group',
                showline=True,
                linecolor='black',
                tickangle=-45,
                mirror=True
            ),
            yaxis=dict(
                title="Cohen's D Value",
                showgrid=True,
                gridcolor='lightgray',
                zeroline=True,
                zerolinecolor='black'
            ),
            font=dict(
                family="Arial",
                size=12,
                color="black"
            ),
            title=dict(
                font=dict(size=16),
                x=0.5
            ),
            coloraxis_colorbar=dict(
                title="Cohen's D"
            )
        )

        fig.show()
        directory = "img/question2/"
        fig.write_html(os.path.join(directory, "neighbours_regions_cohend.html"))

    return cohen_by_region_df
