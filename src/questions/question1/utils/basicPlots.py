import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from src.questions.question1.utils.cohenD import cohen_d


def region_avg_scatter(ratings_df):
    
    for region in ratings_df['region'].unique():
        
        subset = ratings_df[ratings_df['region'] == region]
    
        avg_ratings = subset.groupby('user_state')['rating'].mean().reset_index()
        
        plt.figure(figsize=(14, 6))
        
        sns.scatterplot(data=avg_ratings, x='user_state', y='rating', color='blue', s=100, marker='o', label='Average Rating')

        plt.title(f'Average Rating by User State for Region: {region}')
        plt.xlabel('User State')
        plt.ylabel('Average Rating')
        plt.xticks(rotation=90)
        plt.ylim(0,5)
        plt.legend(title='Rating Type')
        plt.tight_layout()
        plt.show()
        
    return
    
    
def region_avg_violin(ratings_df):
    #violin plot for each region displaying rating distributions for each user state in the region
    unique_regions = ratings_df['region'].unique()

    for region in unique_regions:
        subset_data = ratings_df[ratings_df['region'] == region]
        
        plt.figure(figsize=(12, 8))
        sns.violinplot(
            x='user_state',
            y='rating',
            data=subset_data,
            inner='quartile',
            palette='Set2',
            hue='user_state'
        )
        
        plt.title(f"Violin Plot of Ratings by User State Within Region: {region}")
        plt.xlabel("User State")
        plt.ylabel("Rating")
        plt.xticks(rotation=90)
        plt.ylim(0,5)
        plt.tight_layout()
        plt.show()
        
    return


def plot_cohenD(ratings_df, plot = False):
    #plot of the Cohen's D values between every user_state of a region without calculating it twice.
    all_cohen_results = []

    for region in ratings_df['region'].unique():
        subset = ratings_df[ratings_df['region'] == region]
        cohen_results = []
        processed_pairs = set()
        
        for state1 in subset['user_state'].unique():
            for state2 in subset['user_state'].unique():
                if state1 != state2:
                    state_pair = tuple(sorted([state1, state2]))
                    
                    if state_pair in processed_pairs:
                        continue
                    
                    ratings_state1 = subset[subset['user_state'] == state1]['rating']
                    ratings_state2 = subset[subset['user_state'] == state2]['rating']
                    
                    if len(ratings_state1) == 0 or len(ratings_state2) == 0:
                        continue
                    
                    d_value = cohen_d(ratings_state1, ratings_state2)
                    cohen_results.append((state1, state2, d_value, region))
                    processed_pairs.add(state_pair)    
        
        cohen_df_region = pd.DataFrame(cohen_results, columns=['State1', 'State2', 'Cohen_d', 'Region'])
        
        cohen_df_region = cohen_df_region.sort_values(by='Cohen_d')
        
        all_cohen_results.append(cohen_df_region)

        if plot:
            plt.figure(figsize=(12, 8))
            sns.barplot(
                x='State1', 
                y='Cohen_d', 
                data=cohen_df_region, 
                palette='viridis', 
                hue='State2'
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
            plt.title(f'Cohen’s D for State pair Ratings by Region: Center state {region}')
            plt.xticks(rotation=0)
            plt.legend(title='State Pairs', loc='upper right')
            plt.tight_layout()
            
            plt.show()

    final_cohen_df = pd.concat(all_cohen_results, ignore_index=True)
    
    return final_cohen_df


def plot_cohenD_some_states(ratings_df, plot = False):
    #plot of the Cohen's D values between every user_state of a region without calculating it twice.
    all_cohen_results = []

    for region in ratings_df['region'].unique():
        if region != 'Illinois' and region != 'Nevada': continue
        
        subset = ratings_df[ratings_df['region'] == region]
        cohen_results = []
        processed_pairs = set()
        
        for state1 in subset['user_state'].unique():
            
            for state2 in subset['user_state'].unique():
                if state1 != state2:
                    state_pair = tuple(sorted([state1, state2]))
                    
                    if state_pair in processed_pairs:
                        continue
                    
                    ratings_state1 = subset[subset['user_state'] == state1]['rating']
                    ratings_state2 = subset[subset['user_state'] == state2]['rating']
                    
                    if len(ratings_state1) == 0 or len(ratings_state2) == 0:
                        continue
                    
                    
                    d_value = cohen_d(ratings_state1, ratings_state2)
                    cohen_results.append((state1, state2, d_value, region))
                    processed_pairs.add(state_pair)    
        
        cohen_df_region = pd.DataFrame(cohen_results, columns=['State1', 'State2', 'Cohen_d', 'Region'])
        
        cohen_df_region = cohen_df_region.sort_values(by='Cohen_d')
        
        all_cohen_results.append(cohen_df_region)

        if plot:
            plt.figure(figsize=(12, 8))
            sns.barplot(
                x='State1', 
                y='Cohen_d', 
                data=cohen_df_region, 
                palette='viridis', 
                hue='State2'
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
            plt.title(f'Cohen’s D for State pair Ratings by Region: Center state {region}')
            plt.xticks(rotation=0)
            plt.legend(title='State Pairs', loc='upper right')
            plt.tight_layout()
            
            plt.show()

    final_cohen_df = pd.concat(all_cohen_results, ignore_index=True)
    
    return final_cohen_df