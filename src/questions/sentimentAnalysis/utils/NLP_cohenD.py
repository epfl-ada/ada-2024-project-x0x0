import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from utils.cohenD import cohen_d
import gzip
import pickle


def NLP_cohen_D(state, plot = True):
    
    localpathp = 'NLP_results/'+state+'_local_sent_positive.pkl.gz'
    localpathn = 'NLP_results/'+state+'_local_sent_negative.pkl.gz'
    localpathc = 'NLP_results/'+state+'_local_sent_compound.pkl.gz'

    with gzip.open(localpathp, 'rb') as f:
        local_positive_sent = pickle.load(f)
    with gzip.open(localpathn, 'rb') as f:
        local_negative_sent = pickle.load(f)
    with gzip.open(localpathc, 'rb') as f:
        local_compound_sent = pickle.load(f)
        
    nonlocalpathp = 'NLP_results/'+state+'_nonlocal_sent_positive.pkl.gz'
    nonlocalpathn = 'NLP_results/'+state+'_nonlocal_sent_negative.pkl.gz'
    nonlocalpathc = 'NLP_results/'+state+'_nonlocal_sent_compound.pkl.gz'

    with gzip.open(nonlocalpathp, 'rb') as f:
        nonlocal_positive_sent = pickle.load(f)
    with gzip.open(nonlocalpathn, 'rb') as f:
        nonlocal_negative_sent = pickle.load(f)
    with gzip.open(nonlocalpathc, 'rb') as f:
        nonlocal_compound_sent = pickle.load(f)

    
    cohen_d_positive = cohen_d(local_positive_sent, nonlocal_positive_sent)
    cohen_d_negative = cohen_d(local_negative_sent, nonlocal_negative_sent)
    cohen_d_compound = cohen_d(local_compound_sent, nonlocal_compound_sent)

    cohen_df = pd.DataFrame(columns=['state','positive','negative','compound'])
    #iloc cant make it bigger but loc can, kind of a hacky way to make our df but whatever
    cohen_df.loc[0] = [state,cohen_d_positive,cohen_d_negative,cohen_d_compound]

    if plot:
        plt.figure(figsize=(12, 8))

        sns.barplot(
            x=cohen_df.columns, 
            y=cohen_df.iloc[0], 
            palette='viridis'
        )

        plt.axhline(y=0, color='black', linewidth=1)

        plt.axhline(y=0.2, color='#FFA07A', linestyle=':', linewidth=2, label='Small effect (d=0.2)')
        plt.axhline(y=-0.2, color='#FFA07A', linestyle=':', linewidth=2)
        plt.axhline(y=0.5, color='#FF8C00', linestyle=':', linewidth=2, label='Medium effect (d=0.5)')
        plt.axhline(y=-0.5, color='#FF8C00', linestyle=':', linewidth=2)
        plt.axhline(y=0.8, color='#CD3700', linestyle=':', linewidth=2, label='Large effect (d=0.8)')
        plt.axhline(y=-0.8, color='#CD3700', linestyle=':', linewidth=2)

        plt.xlabel('sentence analysis type')
        plt.ylabel('Cohen’s D')
        plt.title(state+' : cohen’s D for local vs non local sentence sentiment analysis')

        plt.legend(title='Effect Size Thresholds', loc='upper right')

        plt.tight_layout()
        plt.show()
        
    return cohen_df


def NLP_cohen_D_all_states(states):
    
    df_cohen_all_states = pd.DataFrame(columns=['state', 'positive', 'negative', 'compound'])
    
    for state in states:
        df_cohen = NLP_cohen_D(state, plot=False)
        
        df_cohen_all_states = pd.concat([df_cohen_all_states, df_cohen], ignore_index=True)

    # Now, plot the results for all states
    plt.figure(figsize=(16, 12))
    
    # Use seaborn's barplot with 'state' on the x-axis and the Cohen's D values on the y-axis
    sns.barplot(
        data=df_cohen_all_states.melt(id_vars='state', value_vars=['positive', 'negative', 'compound']),
        x='state', 
        y='value', 
        hue='variable', 
        palette='viridis',
        dodge=True  
    )

    plt.axhline(y=0, color='black', linewidth=1)
    plt.axhline(y=0.2, color='#FFA07A', linestyle=':', linewidth=2, label='Small effect (d=0.2)')
    plt.axhline(y=-0.2, color='#FFA07A', linestyle=':', linewidth=2)
    plt.axhline(y=0.5, color='#FF8C00', linestyle=':', linewidth=2, label='Medium effect (d=0.5)')
    plt.axhline(y=-0.5, color='#FF8C00', linestyle=':', linewidth=2)
    plt.axhline(y=0.8, color='#CD3700', linestyle=':', linewidth=2, label='Large effect (d=0.8)')
    plt.axhline(y=-0.8, color='#CD3700', linestyle=':', linewidth=2)

    plt.xlabel('State')
    plt.ylabel('Cohens D')
    plt.title('Cohens D for Local vs Non-Local Sentiment Analysis Across States')

    plt.legend(title='Effect Size Thresholds', loc='upper right')
    
    # Rotate the state names for better readability
    plt.xticks(rotation=90)

    x_ticks = plt.gca().get_xticks()

    # Loop through x-ticks and add vertical lines
    for tick in x_ticks:
        plt.axvline(x=tick, color='gray', linestyle='--', linewidth=1, alpha=0.2)
    
    plt.tight_layout()
    plt.show()