import pandas as pd
import spacy
import gc



def prepare_state_data(state_name: str, df: pd.DataFrame):
    
    df_state_name = df[df['user_state'] == state_name].reset_index(drop=True)
    print(df_state_name.shape)
    
    df_state_name = df_state_name.dropna(subset='text')
    print("Drop NA: ",df_state_name.shape)
    
    df_local = df_state_name[df_state_name['beer_state'] == state_name]
    print("Locals: ",df_local.shape)
    
    df_nonlocal = df_state_name[df_state_name['beer_state'] != state_name]
    print("Non locals: ",df_nonlocal.shape)
    
    return df_local, df_nonlocal


def split_text_into_chunks(large_text, nlp, chunk_size=100_000):
    #nlp = spacy.load("en_core_web_sm")
    print("Need around "+ str(round(len(large_text)/chunk_size))+" chunks")
    
    chunk_number = 0
    for i in range(0, len(large_text), chunk_size):
        if chunk_number%10 == 0: 
            gc.collect() #for memory
            print('Tasty garbage!')
            
        chunk = large_text[i:i + chunk_size]
        doc = nlp(chunk)
        print("Chunk: ",i//chunk_size)
        chunk_number += 1
        #yield so we process bt by bit
        yield doc
        
        
def create_nlp_doc(df):
    #the bare bare minimum for speed, we have a lot of text to process...
    nlp = spacy.load("en_core_web_sm")
    nlp.remove_pipe('parser')
    nlp.remove_pipe('tagger')
    nlp.remove_pipe('ner')
    nlp.remove_pipe('lemmatizer')
    nlp.remove_pipe('tok2vec')
    nlp.remove_pipe('attribute_ruler')
    nlp.add_pipe('sentencizer')
    
    #remove new lines #unnecessary but just in case
    df['text'] = df['text'].apply(lambda l: " ".join(l.split()))
    df_text = " ".join(df["text"]) #concat all rows
    print("Length of text: ",len(df_text))
    print(df_text[0:100])
    
    docs = []
    for doc in split_text_into_chunks(df_text, nlp, chunk_size=100_000):
        docs.append(doc)
    
    print("Done")  
    
    return docs