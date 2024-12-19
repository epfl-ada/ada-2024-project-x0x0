import pandas as pd
import matplotlib.pyplot as plt


def stacked_styles(US_ratings):
    
    top_5_styles = US_ratings['style'].value_counts().head(20).index

    US_ratings['style_category'] = US_ratings['style'].apply(
        lambda x: x if x in top_5_styles else 'Other'
    )

    style_counts = US_ratings.groupby(['user_state', 'style_category']).size().unstack(fill_value=0)

    style_percentages = style_counts.div(style_counts.sum(axis=1), axis=0) * 100

    global_order = (
        style_counts.sum(axis=0)
        .sort_values(ascending=False)
        .index.tolist()
    )

    #put other at the end
    if "Other" in global_order:
        global_order.remove("Other")
        global_order.append("Other")

    style_percentages = style_percentages[global_order]

    if 'American IPA' in style_percentages.columns:
        style_percentages = style_percentages.sort_values(by='American IPA', ascending=False)

    style_percentages.plot(kind='bar', stacked=True, figsize=(15, 7), cmap='tab20')

    plt.title('Percentage Share of Beer Styles by User State (Ordered by American IPA)', fontsize=16)
    plt.xlabel('User State', fontsize=12)
    plt.ylabel('Percentage (%)', fontsize=12)
    plt.legend(title='Beer Style', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()

    plt.show()
    
    return
