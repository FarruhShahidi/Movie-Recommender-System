import numpy as np
import pandas as pd
from  tmdb_api import get_genre

import requests
import bs4 as bs
import urllib.request


def get_person(lis, who):
    """


    :param lis: list of strings
    :param who: actor_1_name, actor_2_name, actor_3_name
    :return: name depending on who
    """
    people = []
    for item in lis:
        people.append(item.get('name'))
    print(people)
    if who == 'actor_1_name' and len(people) > 0:
        return (people[0])
    elif who == 'actor_2_name':
        if len(people) > 1:
            return (people[0])
        else:
            return np.NaN
    elif who == 'actor_3_name' and len(people) > 2:
        return (people[2])
    else:
        return np.NaN
def extract_from_wiki(link):
    source = urllib.request.urlopen(link).read()
    soup = bs.BeautifulSoup(source, 'lxml')
    tables = soup.find_all('table', class_='wikitable sortable')

    # get dataframe for each tables
    df1 = pd.read_html(str(tables[0]))[0]
    df2 = pd.read_html(str(tables[1]))[0]
    df3 = pd.read_html(str(tables[2]))[0]
    df4 = pd.read_html(str(tables[3]).replace("'1\"\'", '"1"'))[0]

    df = df1.append(df2.append(df3.append(df4, ignore_index=True),
                                               ignore_index=True),
                                               ignore_index=True)
    df = df[['Title', 'Cast and crew']]

    return df

def convert_genre(genres):
    """

    :param words: a list of genres
    :return: string of genres separated by a whitespace
    """
    converted = ""
    if not genres or type(genres) == float: return np.NaN
    return genres.replace(',', '').replace('[','').replace(']','').replace("'",'')



def add_genres(df, column='Title'):
    """

    :param df: pandas dataframe
    :param column: just a 'Title' column
    :return: None, just adds two columns
    """
    df['Genre'] = df[column].map(lambda movie: get_genre(str(movie)))
    df['genres'] = df['Genre'].map(lambda g: convert_genre(g))



def get_director(col):
    if " (director)" in col:
        return col.split(" (director)")[0]
    else:
        return col.split(" (director/screenplay)")[0]
def add_director(df):
    df['director_name'] = df['Cast and crew'].map(lambda cc: get_director(str(cc)))

def get_actors(cc):
    actors = cc.split("screenplay); ")[-1].split(", ")
    actor1 = actors[0]
    actor2 = actors[1] if len(actors) > 1 else np.NaN
    actor3 = actors[2] if len(actors) > 2 else np.NaN
    return (actor1, actor2, actor3)
def add_actors(df, cc='Cast and crew'):
    df['actor_1_name'] = df[cc].map(lambda cc: get_actors(str(cc))[0])
    df['actor_2_name'] = df[cc].map(lambda cc: get_actors(str(cc))[1])
    df['actor_3_name'] = df[cc].map(lambda cc: get_actors(str(cc))[2])
def drop_Genres_and_rename_Title(df):
    df = df.rename(columns={'Title': 'movie_title'})
    df['movie_title'] = df['movie_title'].str.lower()
    df.drop(columns=['Genre'], axis=1, inplace=True)
    return df
def combine_cols(df):
    df['all_cast'] = df['actor_1_name'] + ' ' + df['actor_2_name'] + ' ' + df[
        'actor_3_name'] + ' ' + df['director_name'] + ' ' + df['genres']
def replace_nans(df):
    for col in df:
        df[col] = df[col].replace(np.nan, 'unknown')

def process_all(link):
    df = extract_from_wiki(link)
    add_genres(df)
    add_director(df)
    add_actors(df)
    # return type is different
    df = drop_Genres_and_rename_Title(df)
    combine_cols(df)
    replace_nans(df)
    return df