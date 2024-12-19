import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.colors import Normalize, LinearSegmentedColormap
from matplotlib.cm import ScalarMappable

from src.questions.question3.utils.cohenD import cohen_d


def state_cohen_D(df_US_ratings: pd.DataFrame):
    
    US_ratings = df_US_ratings
    
    US_ratings['state_IN_VS_OUT'] = np.where(
        US_ratings['user_state'] == US_ratings['beer_state'], 'In-State', 'Out-of-State'
    )

    unique_states = US_ratings['beer_state'].unique()
    unique_states.sort()

    cohen_results = {}

    for state in unique_states:
        subset = US_ratings[US_ratings['beer_state'] == state]
        in_state_ratings = subset[subset['state_IN_VS_OUT'] == 'In-State']['rating']
        out_of_state_ratings = subset[subset['state_IN_VS_OUT'] == 'Out-of-State']['rating']
        
        if len(in_state_ratings) == 0 or len(out_of_state_ratings) == 0:
            print("Warning nan")
            cohen_results[state] = np.nan
            continue
        
        d_value = cohen_d(in_state_ratings, out_of_state_ratings)
        cohen_results[state] = d_value

    cohen_df = pd.DataFrame.from_dict(cohen_results, orient='index', columns=['Cohen_d'])
    cohen_df = cohen_df.sort_values(by='Cohen_d') 

    cohen_df = cohen_df.dropna()

    custom_colors = ['#1e0f0d', '#6e4b3c', '#f2a900', '#f8d53f']
    custom_cmap = LinearSegmentedColormap.from_list("custom_cmap", custom_colors)

    values = cohen_df['Cohen_d']
    norm = Normalize(vmin=min(values), vmax=max(values))
    sm = ScalarMappable(norm=norm, cmap=custom_cmap)
    colors = [sm.to_rgba(v) for v in values]

    plt.figure(figsize=(12, 8))

    sns.barplot(
        x=cohen_df.index, 
        y='Cohen_d', 
        data=cohen_df, 
        palette= colors

    )
    

    plt.axhline(y=0, color='black', linewidth=1)

    plt.axhline(y=0.2, color='#FFA07A', linestyle=':', linewidth=2, label='Small effect (d=0.2)')
    plt.axhline(y=-0.2, color='#FFA07A', linestyle=':', linewidth=2)
    plt.axhline(y=0.5, color='#FF8C00', linestyle=':', linewidth=2, label='Medium effect (d=0.5)')
    plt.axhline(y=-0.5, color='#FF8C00', linestyle=':', linewidth=2)
    plt.axhline(y=0.8, color='#CD3700', linestyle=':', linewidth=2, label='Large effect (d=0.8)')
    plt.axhline(y=-0.8, color='#CD3700', linestyle=':', linewidth=2)

    plt.xlabel('State')
    plt.ylabel('Cohen’s D')
    plt.title('Cohen’s D for In-State vs Out-of-State Ratings by State')

    plt.xticks(rotation=90)

    plt.legend(title='Effect Size Thresholds', loc='upper right')

    plt.tight_layout()
    plt.show()
    
    return cohen_df


def state_distribution(cohen_df, US_ratings):
    
    significant_states = cohen_df[
        (cohen_df['Cohen_d'] > 0.2) | (cohen_df['Cohen_d'] < -0.2)
    ].index
    significant_states = sorted(significant_states)

    filtered_ratings = US_ratings[US_ratings['beer_state'].isin(significant_states)]
    average_ratings = filtered_ratings.groupby(['beer_state', 'state_IN_VS_OUT'])['rating'].mean().reset_index()
    
    plt.figure(figsize=(12, 8))

    # Plot violin plot
    ax = sns.violinplot(
        x='beer_state', 
        y='rating', 
        hue='state_IN_VS_OUT', 
        data=filtered_ratings, 
        split=True, 
        inner=None, 
        palette='Set2',
        cut=0
    )

    # Add scatter points for averages
    colors = {'In-State': '#5b8a72', 'Out-of-State': 'orange'}
    labels_added = set()  

    for i, state in enumerate(significant_states):
        state_avg_ratings = average_ratings[average_ratings['beer_state'] == state]
        for relation, color in colors.items():
            avg_value = state_avg_ratings[state_avg_ratings['state_IN_VS_OUT'] == relation]['rating']
            if not avg_value.empty:
                offset = -0.2 if relation == 'In-State' else 0.2
                label = f'{relation} Average' if f'{relation} Average' not in labels_added else None
                plt.scatter(
                    x=i + offset, 
                    y=avg_value, 
                    color=color, 
                    edgecolor='black', 
                    s=100, 
                    zorder=3, 
                    label=label
                )
                if label is not None:
                    labels_added.add(label)

    # Set axis limits and labels
    ax.set_xlabel('State')
    ax.set_ylabel('Rating')
    ax.set_ylim(0, 5)  # Set y-axis limits
    ax.set_title('Ratings Distribution and Average Ratings for States with |Cohen’s D| > 0.2')

    # Customize x-axis
    ax.set_xticks(range(len(significant_states)))
    ax.set_xticklabels(significant_states, rotation=90)

    # Merge and deduplicate legends
    lines, labels = ax.get_legend_handles_labels()
    unique_labels = dict(zip(labels, lines))  # Remove duplicate labels
    ax.legend(unique_labels.values(), unique_labels.keys(), title='Reviewer Type & Averages', loc='lower right')

    plt.tight_layout()
    plt.show()
    
    return