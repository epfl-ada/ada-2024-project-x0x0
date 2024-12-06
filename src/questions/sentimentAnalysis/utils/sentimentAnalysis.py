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

   total_sent = []
   [total_sent.append(analyzer.polarity_scores(sent.text)['compound']) for doc in docs for sent in doc.sents]

   path = 'NLP_results/'
   os.makedirs(os.path.dirname(path), exist_ok=True)
   path = path + state
   #these take a while to compute, lets save them!
   with gzip.open(path+"_positive_sent.pkl.gz", "wb") as f:
      pickle.dump(positive_sent, f)
      
   with gzip.open(path+"_negative_sent.pkl.gz", "wb") as f:
      pickle.dump(negative_sent, f)
      
   with gzip.open(path+"_compound_sent.pkl.gz", "wb") as f:
      pickle.dump(total_sent, f)
   
   positive_hist_y, positive_hist_x, _ = plt.hist(positive_sent, bins=15)
   negative_hist_y, negative_hist_x, _ = plt.hist(negative_sent, bins=15)
   total_hist_y, total_hist_x, _ = plt.hist(total_sent, bins=15)
   
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
      
      
      plt.hist(total_sent,bins = 15)
      plt.xlim([-1,1])
      plt.ylim([0,max_y])
      plt.xlabel('Compound sentiment')
      plt.ylabel('Number of sentences')
      plt.tight_layout()
      plt.show()
    
   sents = [analyzer.polarity_scores(sent.text)['compound'] for doc in docs for sent in doc.sents]
   print('Number of positive sentences:',sum(np.array(sents)>=0.05))
   print('Number of negative sentences:',sum(np.array(sents)<=-0.05))
   print('Number of neutral sentences:',sum(np.abs(np.array(sents))<0.05))
    
   return sents



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