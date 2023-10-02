# Load data from newscatcher
#%%
import json
import pandas as pd
import sqlite3
import news_api as api
search_terms = ["United Nations", "United Nations universal periodic review", "united nations committee against torture", "refugees", "migrants"]
filenames = []
from_date="2023/08/15"
page_size=20
safe_from_date = from_date.replace('/', '_')

for term in search_terms:
    filenames.append(f"{q}_{safe_from_date}_page_size_{page_size}.json")
    api.fetch_and_save_to_excel(q=term, from_date="2023/08/15", page_size=20)


# Deserialize and dump
#%% 
def add_unique_id(df):
    """
    Add a unique ID column to the DataFrame.
    """
    df['unique_id'] = range(1, len(df) + 1)
    return df

def load_data(filename,db_name,table_name):
    with open(filename, 'r') as f:
        json_data = json.load(f)
    df = pd.DataFrame(json_data['articles'])
    
    # Step 2: Add Unique ID
    df = add_unique_id(df)
    
    # Step 3: Create SQLite DB
    conn = sqlite3.connect(db_name)
    
    # Step 4: Create Table and Insert Data
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    print(f"Successfully loaded data into {db_name}, table name: {table_name}")
    conn.close()
    return 

def mass_load(filenames,db_name,table_name):
    for name in filenames:
        load_data(name,db_name,table_name)
        
    return
 
# Testing 
#%% 
filename = 'migrants_2023_08_15_page_size_20.json'
db_name = 'articles.sqlite'
table_name = 'articles_table'
load_data(filename,db_name,table_name)

