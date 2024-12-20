import pandas as pd
from src.questions.question2.utils.cohenD import cohen_d
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px



def regions_cohenD(neighbours_df, US_ratings, plot=True):
    
    df_neighbours = neighbours_df
    #df_neighbours["neighbours"] = df_neighbours["neighbours"].fillna("").str.split(";")
    df_neighbours["neighbours"] = df_neighbours["neighbours"].fillna("").apply(lambda x: x.split(";") if isinstance(x, str) and x else [])

    cohen_results_by_region = {}
    
    for index, row in df_neighbours.iterrows():
        state = row['state']
        neighbours = row['neighbours']

        if neighbours:
            region_states = [state] + neighbours
        else:
            region_states = [state] #if a state doesn't have neighbours we consider it as a region (like Alaska and Hawaii)

        in_region_ratings = US_ratings[US_ratings['user_state'].isin(region_states)]['rating']
        out_of_region_ratings = US_ratings[~US_ratings['user_state'].isin(region_states)]['rating']

        if len(in_region_ratings) < 2 or len(out_of_region_ratings) < 2: #in order to do correctly the cohen test
            print("Warning nan")
            cohen_results_by_region[state] = np.nan
            continue

        d_value = cohen_d(in_region_ratings, out_of_region_ratings)
        cohen_results_by_region[state] = d_value

    #table to see the Cohen factor for each region
    cohen_by_region_df = pd.DataFrame.from_dict(cohen_results_by_region, orient='index', columns=['Cohen_d'])
    cohen_by_region_df.index.name = 'Center State of each Region'
    cohen_by_region_df = cohen_by_region_df.reset_index()
    cohen_by_region_df = cohen_by_region_df.sort_values(by='Cohen_d', ascending=False)

    if plot:
        plt.figure(figsize=(14, 8))
        sns.barplot(data=cohen_by_region_df, x='Center State of each Region', y='Cohen_d', palette='viridis')
        plt.title("Cohen's D for in-region ratings compared to out-of-region ratings for the region's users")
        plt.xlabel("Center State of each Region")
        plt.ylabel("Cohen's D value")
        plt.xticks(rotation=90)
        
        plt.axhline(y=0, color='black', linewidth=1)

        plt.axhline(y=0.2, color='#FFA07A', linestyle=':', linewidth=2, label='Small effect (d=0.2)')
        plt.axhline(y=-0.2, color='#FFA07A', linestyle=':', linewidth=2)
        plt.axhline(y=0.5, color='#FF8C00', linestyle=':', linewidth=2, label='Medium effect (d=0.5)')
        plt.axhline(y=-0.5, color='#FF8C00', linestyle=':', linewidth=2)

        plt.tight_layout()
        plt.show()
        
    return cohen_by_region_df

def regions_cohenD_Q1_plotly(US_ratings, state_groups_df, plot=True):
    cohen_results_by_region = {}
    group_states = {}

    for index, row in state_groups_df.iterrows():
        group = row['States']
        
        # Store states in the group for hover info
        group_states[index] = ", ".join(group)

        # Get in-region and out-of-region ratings
        in_region_ratings = US_ratings[US_ratings['user_state'].isin(group)]['rating']
        out_of_region_ratings = US_ratings[~US_ratings['user_state'].isin(group)]['rating']

        if len(in_region_ratings) < 2 or len(out_of_region_ratings) < 2:
            print("Warning: Insufficient data, setting Cohen's d to NaN for group", index)
            cohen_results_by_region[index] = np.nan
            continue

        d_value = cohen_d(in_region_ratings, out_of_region_ratings)
        cohen_results_by_region[index] = d_value

    cohen_by_region_df = pd.DataFrame.from_dict(cohen_results_by_region, orient='index', columns=['Cohen_d'])
    cohen_by_region_df.index.name = 'Group name'
    cohen_by_region_df = cohen_by_region_df.reset_index()

    # Add hover text with states in each group
    cohen_by_region_df['Group States'] = cohen_by_region_df['Group name'].map(group_states)
    
    cohen_by_region_df_sorted = cohen_by_region_df.sort_values(by='Cohen_d', ascending=True).reset_index(drop=True)
    print(cohen_by_region_df_sorted.head())
    
    if plot:
        colour_scale = ['#1e0f0d', '#6e4b3c', '#f2a900', '#f8d53f']

        # Plot the bar chart with Plotly
        fig = px.bar(
            cohen_by_region_df_sorted,
            x=cohen_by_region_df_sorted.index,
            y="Cohen_d",
            custom_data=["Group States"],
            title="Cohen's D for in-region ratings compared to out-of-region ratings",
        )
        
        # Add reference lines for small and medium effects
        fig.add_hline(y=0, line_dash="solid", line_color="black")
        fig.add_hline(y=0.2, line_dash="dot", line_color="#FFA07A", annotation_text="Small effect (d=0.2)", annotation_position="top left")
        fig.add_hline(y=-0.2, line_dash="dot", line_color="#FFA07A")
        fig.add_hline(y=0.5, line_dash="dot", line_color="#FF8C00", annotation_text="Medium effect (d=0.5)", annotation_position="top left")
        fig.add_hline(y=-0.5, line_dash="dot", line_color="#FF8C00")
        
        
        fig.update_traces(
            hovertemplate="<b>States:</b> %{customdata[0]}<extra></extra>"
        )
        
        fig.update_traces(
            marker=dict(
                color=cohen_by_region_df_sorted['Cohen_d'],
                colorscale=colour_scale,
                cmin=-0.2,
                cmax=0.2,
                colorbar=dict(
                    title="Cohen's D",
                    tickvals=[-0.2, 0, 0.2],
                    ticktext=["-0.2", "0", "0.2"]
                )  
            )
        )

        fig.update_layout(
            xaxis_title="Region Group",
            yaxis_title="Cohen's D Value",
            title_font=dict(size=20),
            width=700,
            height=450,
            xaxis=dict(showticklabels=False),
            yaxis=dict(range=[-0.6, 0.6])
        )

        fig.show()

    return cohen_by_region_df