from utils.prepNLP import prepare_state_data, create_nlp_doc

import pandas as pd
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import numpy as np
import gzip
import pickle
import os

def sentiment_analysis(docs, state, plots = False):
   analyzer = SentimentIntensityAnalyzer()

   positive_sent = []
   #iterate through the sentences, get polarity scores, choose a value
   [positive_sent.append(analyzer.polarity_scores(sent.text)['pos']) for doc in docs for sent in doc.sents]

   negative_sent = []
   [negative_sent.append(analyzer.polarity_scores(sent.text)['neg']) for doc in docs for sent in doc.sents]

   compound_sent = []
   [compound_sent.append(analyzer.polarity_scores(sent.text)['compound']) for doc in docs for sent in doc.sents]
   
   positive_hist_y, positive_hist_x, _ = plt.hist(positive_sent, bins=15)
   negative_hist_y, negative_hist_x, _ = plt.hist(negative_sent, bins=15)
   total_hist_y, total_hist_x, _ = plt.hist(compound_sent, bins=15)
   
   plt.clf() #otherwise our graphs superpose
   #plt.cla()
   
   if plots: 
      #so we can dynamically set y max
      max_y = max(max(positive_hist_y), max(negative_hist_y), max(total_hist_y))
      max_y = max_y*1.1 #makes the graphs better
      print('Max y: ',max_y)
      if max_y > 1000: #always the case I think
         max_y = round(max_y, -3) #rounds to the thousand    
      print('Max y: ',max_y)
      
      plt.hist(positive_sent,bins=15)
      plt.xlim([0,1])
      plt.ylim([0,max_y])
      plt.xlabel('Positive sentiment')
      plt.ylabel('Number of sentences')
      plt.tight_layout()
      plt.show()
      
      
      plt.hist(negative_sent,bins=15)
      plt.xlim([0,1])
      plt.ylim([0,max_y])
      plt.xlabel('Negative sentiment')
      plt.ylabel('Number of sentences')
      plt.tight_layout()
      plt.show()
      
      
      plt.hist(compound_sent,bins = 15)
      plt.xlim([-1,1])
      plt.ylim([0,max_y])
      plt.xlabel('Compound sentiment')
      plt.ylabel('Number of sentences')
      plt.tight_layout()
      plt.show()
    
   print('Number of positive sentences:',sum(np.array(compound_sent)>=0.05))
   print('Number of negative sentences:',sum(np.array(compound_sent)<=-0.05))
   print('Number of neutral sentences:',sum(np.abs(np.array(compound_sent))<0.05))
    
   return positive_sent, negative_sent, compound_sent



def sentiment_analysis_stats(sentences):
   sentences = np.array(sentences)
   total = len(sentences)
   positive = sum(sentences >= 0.05)
   negative = sum(sentences <= -0.05)
   neutral = sum(np.abs(sentences) < 0.05)
   
   percent_positive = positive/total*100
   percent_negative = negative/total*100
   percent_neutral = neutral/total*100

   data = {
      "sentences": ["total","positive","negative","neutral"],
      "count": [total, positive, negative, neutral],
      "percentage": ['N/A', percent_positive, percent_negative, percent_neutral],
   }

   df = pd.DataFrame(data)
   print(df.head(4))
   
   return df


def sentiment_analysis_results(state = str, baseData  = pd.DataFrame, save_dfs = True, plots = False):
    print("Running...")
    #formatting our df based on input state
    df_local, df_nonlocal = prepare_state_data(state, baseData)
    
    #turning text into spacy objects, this can take a while...
    docs_local = create_nlp_doc(df_local)
    docs_nonlocal = create_nlp_doc(df_nonlocal)
    
    #turning into sentences and analysing postive/negative sentiment
    #use plots = True if you want to see some plots
    local_positive_sent, local_negative_sent, local_compound_sent = sentiment_analysis(docs_local, state)
    nonlocal_positive_sent, nonlocal_negative_sent, nonlocal_compound_sent = sentiment_analysis(docs_nonlocal, state)
    
    path = 'NLP_results/'
    os.makedirs(os.path.dirname(path), exist_ok=True)
    path = path+state+'_local_sent'
    #these take a while to compute, lets save them!
    with gzip.open(path+"_positive.pkl.gz", "wb") as f:
        pickle.dump(local_positive_sent, f)    
    with gzip.open(path+"_negative.pkl.gz", "wb") as f:
        pickle.dump(local_negative_sent, f)   
    with gzip.open(path+"_compound.pkl.gz", "wb") as f:
        pickle.dump(local_compound_sent, f)

    path = 'NLP_results/'+state+'_nonlocal_sent'
    #these take a while to compute, lets save them!
    with gzip.open(path+"_positive.pkl.gz", "wb") as f:
        pickle.dump(nonlocal_positive_sent, f)    
    with gzip.open(path+"_negative.pkl.gz", "wb") as f:
        pickle.dump(nonlocal_negative_sent, f)   
    with gzip.open(path+"_compound.pkl.gz", "wb") as f:
        pickle.dump(nonlocal_compound_sent, f)
        
        
    #basic stats based on the analysis
    df_stats_local = sentiment_analysis_stats(local_compound_sent)
    df_stats_nonlocal = sentiment_analysis_stats(nonlocal_compound_sent)
    
    if save_dfs:  #these dfs took a lot of computation to get! Lets save them!
        df_save_local = df_stats_local
        df_save_local['Local/Nonlocal'] = 'Local'
        df_save_local['user_state_NLP'] = state
        
        df_save_nonlocal = df_stats_nonlocal
        df_save_nonlocal['Local/Nonlocal'] = 'Nonlocal'
        df_save_nonlocal['user_state_NLP'] = state
        
        df_combined = pd.concat([df_save_local, df_save_nonlocal], ignore_index=True)
        #'src/questions/sentimentAnalysis/NLP_results/' if running the py file directly
        path = 'NLP_results/'
        os.makedirs(os.path.dirname(path), exist_ok=True)
        path = path + state + '_sentimentAnalysis.csv'
        df_combined.to_csv(path, index=False)
        print("Saved!")
    
    return df_stats_local, df_stats_nonlocal