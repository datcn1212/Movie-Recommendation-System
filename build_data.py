from utils import *
from url_utils import *
import pandas as pd
import time

def get_details():
    full_links = pd.read_csv("links_full.csv") 
    data = dict({"movie_id":[], "movie_brief": [], "director": [], "writers": [], "casts": []})
    print("Processing")

    for i in range(0, 10):
        print(str(i))
        url = full_links.loc[i, 'movie_url']
        d = get_data_from_webpage(url)
        data['movie_id'].append(i)
        data['movie_brief'].append(d['movie_brief'])
        data['director'].append(d['director'])
        data['writers'].append("|".join(d['writers']))
        data["casts"].append("|".join(d['casts']))
        time.sleep(1)
    pd.DataFrame(data).to_csv("details.csv", index=False)
    print("done")

def get_part_of_details(n_batch, low, high):
    full_links = pd.read_csv("links_full.csv") 
    data = dict({"movie_id":[], "movie_brief": [], "director": [], "writers": [], "casts": []})
    print("Processing")

    file_name = "raw_details/details_" + str(n_batch) + ".csv"
    for i in range(low, high):
        print(str(i))
        url = full_links.loc[i, 'movie_url']
        d = get_data_from_webpage(url)
        data['movie_id'].append(i)
        data['movie_brief'].append(d['movie_brief'])
        data['director'].append(d['director'])
        data['writers'].append("|".join(d['writers']))
        data["casts"].append("|".join(d['casts']))
        # time.sleep(1)
    pd.DataFrame(data).to_csv(file_name, index=False)
    print("done")

def merge_part_of_data():
    file_names = ["details_" + str(i) + ".csv" for i in range(0, 17)]
    l = []
    for file_name in file_names:
        print(file_name)
        file = "raw_details/" + file_name
        df = pd.read_csv(file, sep=",")
        l.append(df)
    df = pd.concat(l)
    df['movie_id'] = df['movie_id'] + 1
    df.to_csv("full_details.csv",index=False)

def build_movies_details():
    movies = get_movies()
    full_details = get_full_details()
    mark_genres(movies)
    movies_features = ["movie_id", "title", "genres"]
    movies = movies[movies_features]
    movies_details = movies.merge(full_details, how="left", left_on="movie_id", right_on="movie_id", suffixes=["", "r"])
    movies_details.to_csv("movies_details.csv", index=False, sep="\t")
    return movies_details

