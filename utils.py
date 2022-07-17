from this import d
import numpy as np
import pandas as pd
import zipfile
import urllib.request
from url_utils import *
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from sklearn.model_selection import train_test_split

def get_raw_data_100k(url="http://files.grouplens.org/datasets/movielens/ml-100k.zip"):
    ## Get data from url and extract
    print("Data Downloading")

    urllib.request.urlretrieve(url, "movielens.zip")
    zip_ref = zipfile.ZipFile('movielens.zip', "r")
    zip_ref.extractall()

    print("Done")

def get_users(url='ml-100k/u.user'):
    users_cols = ['user_id', 'age', 'sex', 'occupation', 'zip_code']
    users = pd.read_csv(
        url, sep='|', names=users_cols, encoding='latin-1')
    return users

def get_ratings(url='ml-100k/u.data'):
    ratings_cols = ['user_id', 'movie_id', 'rating', 'unix_timestamp']
    ratings = pd.read_csv(
        url, sep='\t', names=ratings_cols, encoding='latin-1')
    return ratings

def get_movies(url="ml-100k/u.item"):
    # The movies file contains a binary feature for each genre.
    genre_cols = [
        "genre_unknown", "Action", "Adventure", "Animation", "Children", "Comedy",
        "Crime", "Documentary", "Drama", "Fantasy", "Film-Noir", "Horror",
        "Musical", "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western"
    ]
    movies_cols = [
        'movie_id', 'title', 'release_date', "video_release_date", "imdb_url"] + genre_cols

    movies = pd.read_csv(
        url, sep='|', names=movies_cols, encoding='latin-1')
    
    return movies

def get_dataframe_from_csv(url, sep, cols):
    return pd.read_csv(url, sep=sep, names=cols, encoding='latin-1')

def get_full_details(url="full_details.csv", sep=","):
    full_details = pd.read_csv(url, sep=sep)
    full_details["writers"] = full_details["writers"].apply(lambda x: x.split("|")) 
    full_details["casts"] = full_details["casts"].apply(lambda x: x.split("|"))
    return full_details

def title_to_query(title):
    query_dict = dict({
        "?" : "%3F",
        "!" : "%21",
        "(" : "%28",
        ")" : "%29",
        "," : "%2C",
        "/" : "%2F",
        "'" : "%27",
        "&" : "%26",
        ":" : "%3A"
    })
    tokens = title.strip().split(" ")
    queries= []
    for token in tokens:
        query = ""
        for char in token:
            if char in query_dict:
                query += query_dict[char]
            else:
                query += char
        queries.append(query)
    return "https://www.imdb.com/find?q=" + "+".join(queries) + "&ref_=nv_sr_sm"

def get_link_from_title(title):
    query = title_to_query(title)
    link = get_link_from_webpage(query)
    return link

def get_link_all():
    print("Processing")
    movies = get_movies()
    data = dict({"movieID": [], "movie_url" : []})
    try:
        for i in range(len(movies)):
            link = get_link_from_title(movies.loc[i, 'title'])
            data["movieID"].append(i)
            data["movie_url"].append(link)
    except Exception:
        pass
    df = pd.DataFrame(data)
    df.to_csv("links.csv")
    print("Done")
def mark_genres(movies):
    genres = [
        "genre_unknown", "Action", "Adventure", "Animation", "Children", "Comedy",
        "Crime", "Documentary", "Drama", "Fantasy", "Film-Noir", "Horror",
        "Musical", "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western"
    ]
    def get_all_genres(gs):
      active = [genre for genre, g in zip(genres, gs) if g==1]
      if len(active) == 0:
        return 'Unknown'
      return active
    movies['genres'] = [
        get_all_genres(gs) for gs in zip(*[movies[genre] for genre in genres])]

## clean_data not brief
def clean_data(x):
    if isinstance(x, list):
        return [str.lower(i.replace(" ", "")) for i in x]
    else:
        if isinstance(x, str):
            return str.lower(x.replace(" ", ""))
        else:
            return ""

def clean_brief(brief):
    stop_words = set(stopwords.words("english"))
    stop_words.update((",", ".", '"',"!", "?"))
    brief = brief.lower()
    ps = PorterStemmer()
    work_tokens = word_tokenize(brief)
    filtered_sentence = []

    for w in work_tokens:
        if w not in stop_words:
            filtered_sentence.append(ps.stem(w))
    return filtered_sentence

def clean(movies_details):
    features = ["genres", "director", "writers", "casts"]

    for feature in features:
        movies_details[feature] = movies_details[feature].apply(clean_data)
    
    movies_details["movie_brief"] = movies_details["movie_brief"].apply(clean_brief)

    return movies_details

def split_dataset(valid_size=0.2, test_size=0.2):
    ratings = get_ratings()
    ratings = ratings.values
    n_users = int(np.max(ratings[:, 0]))
    n_items = int(np.max(ratings[:, 1]))

    def get_ratings_by_user(n, ratings):
        return ratings[ratings[:, 0] == n]
    
    def train_valid_test(ratings, valid_size=valid_size, test_size=test_size):
        trains = []
        ratings_train = []
        ratings_test = []
        ratings_valid = []
        for n in range(1, n_users+1):
            ratings_by_user = get_ratings_by_user(n, ratings)
            train, test = train_test_split(ratings_by_user, test_size=test_size, random_state=42)
            trains.extend(train)
            ratings_test.extend(test)
            sub_train, valid= train_test_split(train, test_size=valid_size, random_state=42)
            ratings_train.extend(sub_train)
            ratings_valid.extend(valid)
        return np.array(trains), np.array(ratings_train), np.array(ratings_valid), np.array(ratings_test)
    
    return train_valid_test(ratings)
