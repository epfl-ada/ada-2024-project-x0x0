import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd
import matplotlib.patches as mpatches


def draw_map(top_style_per_state):

    top_style_per_state.rename(columns={'style': 'preferred_style_beer'}, inplace=True)
    
    # Load US States shapefile (GeoJSON)
    us_states = gpd.read_file("https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json")

    all_states = us_states['name'].unique()
    matched_states = top_style_per_state['user_state'].unique()
    missing_states = set(all_states) - set(matched_states)
    print("Missing states:", missing_states)

    for state in missing_states:
        top_style_per_state = pd.concat([
            top_style_per_state, 
            pd.DataFrame({'user_state': [state], 'preferred_style_beer': ['No Data']})
        ])

    us_states = us_states.merge(
        top_style_per_state, 
        left_on="name", 
        right_on="user_state", 
        how="left"
    )

    us_states['preferred_style_beer'].fillna("No Data", inplace=True)

    print(us_states.columns)
    print(top_style_per_state.columns)

    unique_styles = us_states['preferred_style_beer'].unique()
    style_colors = {
        style: plt.cm.tab20(i / len(unique_styles)) if style != "No Data" else "red"
        for i, style in enumerate(unique_styles)
    }

    us_states['color'] = us_states['preferred_style_beer'].map(style_colors)

    fig, ax = plt.subplots(1, 1, figsize=(15, 10))
    us_states.plot(
        ax=ax,
        color=us_states['color'],
        edgecolor='black'
    )

    legend_patches = [mpatches.Patch(color=color, label=style) for style, color in style_colors.items()]
    ax.legend(handles=legend_patches, title="Preferred Beer Style", loc="lower left", fontsize=10)
    ax.set_title("Top Beer Style Preference by State", fontsize=16)
    ax.axis("off")
    plt.tight_layout()
    plt.show()
    
    return