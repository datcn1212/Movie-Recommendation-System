# Movie Recommendation System
</p>

## Introduction
</p>
The rapid growth of data collection has led to a new era of information. Data is being used to create more efficient systems and this is where Recommendation Systems come into play. Recommendation Systems improve the quality of search results and provides items that are more relevant to the search item or are realted to the search history of the user. </p>
</p>
There are basically three types of recommender systems: </p>
</p>
Demographic Filtering- They offer generalized recommendations to every user, based on movie popularity and/or genre. The System recommends the same movies to users with similar demographic features. Since each user is different , this approach is considered to be too simple. The basic idea behind this system is that movies that are more popular and critically acclaimed will have a higher probability of being liked by the average audience. </p>
Content Based Filtering- They suggest similar items based on a particular item. This system uses item metadata, such as genre, director, description, actors, etc. for movies, to make these recommendations. The general idea behind these recommender systems is that if a person liked a particular item, he or she will also like an item that is similar to it.</p>
Collaborative Filtering- This system matches persons with similar interests and provides recommendations based on this matching. Collaborative filters do not require item metadata like its content-based counterparts. </p>
</p>
In this project, we use TMDB 5000 Movie Dataset and The MoviLens Dataset to deploy Content Based Filtering and Collaborative Filtering. </p>
</p>

## Data source
</p>
https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata </p>
https://grouplens.org/datasets/movielens/100k/ </p>

## Library
</p>
Install: numpy, pandas, sklearn, nltk, requests, bs4, scipy, matplotlib, seaborn </p>

## About ipynb
</p>
- Content_based_TMDB5000.ipynb : Content-based Filtering on TMDB 5000 Movie Dataset </p>
- Content_based_MovieLens.ipynb: Content-based Filtering on The MovieLens Dataset </p>
- Neighborhood_Based_Collaborative_Filtering.ipynb: Neighborhood-Based Collaborative Filtering with KNN </p>
- Matrix_Factorization_Collaborative_Filtering.ipynb: Matrix Factorization Collaborative Filtering with SGD </p>



