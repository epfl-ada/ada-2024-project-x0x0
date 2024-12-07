import numpy as np
from scipy.stats import chi2_contingency
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


#seperating this function so i can run it just based off of saved csv data
def NLP_chi_test(df_stats_local, df_stats_nonlocal, state, print = False):
    
    #should i just make it output np arrays in the first place...?
    local_counts = df_stats_local[df_stats_local['sentences'] != 'total']['count'].values
    nonlocal_counts = df_stats_nonlocal[df_stats_nonlocal['sentences'] != 'total']['count'].values
    contingency_table = np.array([local_counts, nonlocal_counts])
    
    #chi-square test
    chi2, p, dof, expected = chi2_contingency(contingency_table)

    #cramer's V
    n = contingency_table.sum()  #tot
    min_dim = min(contingency_table.shape) - 1  #degrees freedom
    cramers_v = np.sqrt(chi2 / (n * min_dim))
    
    if print:
        print('\n'+state)
        print(f"Chi-Square Statistic: {chi2}")
        print(f"P-value: {p}")
        if p < 0.05:
            print("The populations are significantly different.")
        else:
            print("No significant difference between the populations.")
            
        print(f"Cramer's V: {cramers_v}")
        if cramers_v < 0.1:
            print("Effect size: Small")
        elif cramers_v < 0.3:
            print("Effect size: Medium")
        else:
            print("Effect size: Large")
        
    return chi2, p , cramers_v


def plot_stacked_sentiments(df_local, df_nonlocal):

    combined_df = pd.concat([df_local, df_nonlocal], ignore_index=True)

    #pivot  for plotting
    
    plot_data = combined_df.pivot_table(
        index=['state', 'Local/Nonlocal'],  #group by state and type
        columns='sentences',     
        values='percentage'
    )
    #turn (state, local) into state (local)
    plot_data.index = plot_data.index.map(lambda x: f"{x[0]} ({x[1]})")
    
    plot_data.plot(
        kind='bar', stacked=True, figsize=(16, 8),
        color=['#1f77b4', '#ff7f0e', '#2ca02c'], edgecolor='black'
    )

    plt.title('Stacked Sentiment Analysis for Local and Nonlocal Reviews')
    plt.xlabel('State and Local/Nonlocal')
    plt.ylabel('Percent')
    plt.ylim(0, 100)
    plt.xticks(rotation=90)
    plt.legend(title='Sentiment', loc='upper right')
    plt.tight_layout()
    plt.show()
    
    
def plot_chi_results(df_results):

    plt.figure(figsize=(16, 12))
        
    sns.barplot(
        x='state', y='cramers_v', data=df_results, 
        palette='viridis'
    )
    
    # Add p-value as text annotation
    for idx, row in df_results.iterrows():
        plt.text(
            idx,  
            row['cramers_v'] + 0.005,  #just above the bar
            f"p={row['p_value']:.3f}", 
            color='black',
            fontsize=10,
            ha='center',
            rotation=90 
        )
    
    #significance thresholds
    plt.axhline(0.1, color='orange', linestyle='--', linewidth=1, label='Small effect threshold (0.1)')

    plt.title('Cramers V Results with p-values by State')
    plt.xlabel('State')
    plt.ylabel("Cramers V")
    plt.xticks(rotation=90)
    plt.legend(title="Effect Size Thresholds", loc='upper right')
    
    plt.tight_layout()
    plt.show()
    