import requests
import serpapi
from serpapi import GoogleSearch
from bs4 import BeautifulSoup
import requests, lxml, os, json

import openpyxl
import pybliometrics
import pyarrow.parquet as pq
import pandas as pd
from pybliometrics.scopus import ScopusSearch
import os

import pybliometrics
pybliometrics.init()


insttoken: "c9013ed7d28a25c1215094538c3d9288"

api_key ="95a28278698ec66120c62d27ac19edd7"

# there is a max number of 8 boolean connectors in science direct. lets use the same in scopus and scidir

# Replace 'YOUR_API_KEY' with your actual API key
#api_key = 'A'
search_params = {
    'date': '1950-2026',  # Adjust the date range as needed
}

# Create a ScopusSearch instance with the query and search parameters

beg = ['TITLE-ABS-KEY(("ecosystem services") AND ("Ebro"))']

#mid=[
#') AND (conservation OR restoration)',
#') AND (job OR labor)',
#') AND (poverty OR livelihood)',
#') AND (wage OR income)',
#') AND ("environment* quality" OR pollut* OR contamina*)',
#') AND (bird OR wildlife)'
#]

#las=[
#')AND (regression OR quant* OR estimat* OR statistic*)'
#]

Qs = beg
#Qs = []

for element_B in mid:
    combined_element = f'{beg[0]} {element_B} {las[0]}'  # Combine elements from A, B, and C
    Qs.append(combined_element)



#last=[
#'AND (regression OR quantitative OR estimat* OR statistic*))',
#'AND (econometric OR experiment OR quasi*experiment'
#]

for i, query in enumerate(Qs):
    scopus_search = ScopusSearch(query, verbose=True, refresh=True) #date='1980-1999'
    df = pd.DataFrame(scopus_search.results)

    # Check if the DataFrame is not empty
    if not df.empty:
        df_subset = df.loc[:, ['eid', 'doi', 'title', 'subtype', 'creator', 'affiliation_country', 'author_count', 'author_names', 'author_ids', 'publicationName', 'volume', 'pageRange', 'coverDate', 'description', 'authkeywords', 'citedby_count']]
        parquet_file_path = f'ScopusSearches/search_test_{i}.parquet'
        df_subset.to_parquet(parquet_file_path)
    else:
        print(f"No results for query {query}")

dfs = []
for i in range(6):
    file_path = f'ScopusSearches/search_test_{i}.parquet'
    table = pq.read_table(file_path)
    df = table.to_pandas()
    df['wave'] = i
    dfs.append(df)

scopus_all = pd.concat(dfs, ignore_index=True)

scopus_all = scopus_all.dropna(subset=['title', 'author_names', 'doi', 'coverDate'])
scopus_all = scopus_all[(scopus_all['subtype'] == 'ar') | (scopus_all['subtype'] == 're')]

scopus_all['year'] = scopus_all['coverDate'].astype(str).str[:4]
scopus_all = scopus_all[['title', 'description', 'doi', 'year', 'authkeywords', 'author_names','publicationName']]

scopus_all.loc[:, 'doi'] = scopus_all['doi'].str.replace('https://doi.org/', '')

scopus_all['doi_duplicated'] = scopus_all.duplicated(subset=['doi']).astype(int)
scopus_all['doi_duplicated'] = scopus_all.groupby('doi')['doi_duplicated'].transform('max')
scopus_all['no_abstract'] = scopus_all['description'].isna().astype(int)
scopus_all['no_ab_dup'] = scopus_all['no_abstract']*scopus_all['doi_duplicated']
scopus_all['no_ab_dup_all'] = scopus_all.groupby('doi')['no_ab_dup'].transform('min')
scopus_all = scopus_all[(scopus_all['no_abstract'] == 1) | (scopus_all['no_ab_dup_all'] == 0)]
scopus_all = scopus_all.drop_duplicates(subset=['doi'], keep='first')

# now I want to merge with all search and get only the ones that did not come in that search.
scopus_all.rename(columns={'doi': 'DOI'}, inplace=True)

all_search = pd.read_excel('clean_search/all_clean_search.xlsx')

# Perform an anti-join to keep only elements of park search that had not been found before.
parksnew = scopus_all[~scopus_all['DOI'].isin(all_search['DOI'])]
parksnew = parksnew.sort_values(by="DOI", ascending=False)
parksnew.to_excel("ScopusSearches/parks_new_cleaned.xlsx", index=False, engine='openpyxl')
# and from these I will follow the protocol again....with this I convert to RIS and take it from there...








