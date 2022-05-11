import streamlit as st
import pandas as pd 
#import os


ratings=pd.read_csv('ratings.csv')
movies=pd.read_csv('movies.csv')
links=pd.read_csv('links.csv')
tags=pd.read_csv('tags.csv')


matrix = pd.merge(ratings,movies, how ="inner", on = ["movieId"])

matrix= pd.merge(matrix,tags, how ="inner", on = ["movieId"])


st.title("WBSFLIX")
 
st.write("""
### Recommender Systems
""")

# Popularity based
st.text("Choose the Genres")
genres = st.selectbox(
    ' ',
     (matrix['genres'].unique()))
def popularity_based_recommender_gen(data: pd.DataFrame, genres: str):
    return (
        matrix
        .groupby(['movieId', 'title',  'genres'])
        .agg(

            movie_rating_mean = ('rating', 'mean'),
            movie_rating_count = ('rating', 'count')
        )
        .reset_index()
        .sort_values(['movie_rating_count'], ascending=False)
        .query('genres == @genres')
        .head(5)
        )
most_popular = popularity_based_recommender_gen(matrix.copy(),genres)
st.text("Popular Movies based On Genre")
matrix_1 = most_popular.filter(['title'])
st.dataframe(matrix_1)
 
        

# Sorting data
newdf= (
    matrix
    .filter(['userId_x', 'title', 'rating'])
    .groupby(['userId_x'])
    .head(5))

(newdf
    .groupby(['userId_x'])
    .agg(
        mean_rating = ('rating', 'mean'),
        count_rating = ('rating', 'count')
    )
    .reset_index()
    .sort_values('mean_rating', ascending=False))

newdf.set_index('userId_x')

newdf1 = newdf.drop_duplicates()

# # Iteam Based Movie
st.text("Choose the Movie name")
movie_name = st.selectbox(
    ' ',
     (matrix['title'].unique()))
# py function get sparse matrix
def get_sparse_matrix(newdf1: pd.DataFrame): 
    return(
    newdf1
        .pivot(index='userId_x', columns='title', values='rating')
    ) 
    
if(movie_name != ''):
    def item_based_recommender(dense_matrix: pd.DataFrame, title: str, n: int=5): 
        try:
            sparse_matrix = get_sparse_matrix(newdf1)
            return( sparse_matrix
             .corrwith(sparse_matrix[title])
             .sort_values(ascending=False)
             .index
             .to_list()[1:n+1]
            )
        except:
            return st.text("Given movie in not present in the data it shows error try another movie please")

    matrix_2 = item_based_recommender(newdf1, movie_name)
    
    st.text("Movies recommended based on the given Input")
    
    st.dataframe(matrix_2)
else:
    st.write("""
    Enter the movie name
    """)
    
## User Based
st.text("Choose the UserId")
user_pref = st.selectbox(
    ' ',
     (matrix['userId_x'].unique()))
user_pref1 = int(user_pref)
if(user_pref > 0):
    def get_user_prefered_item(newdf1: pd.DataFrame, userId_x: int):
        data=newdf1.copy()
        return(data
        .query('userId_x == @userId_x') 
        .sort_values('rating', ascending=False)
        ['title'].to_list()[:6]
        )
    get_user_prefered_item(newdf1,user_pref1)
    
    st.text("Movies recommended based on the User ID")
    
    matrix_3 =  get_user_prefered_item(newdf1,user_pref1)
    
    st.dataframe(matrix_3)
else:
    st.write("""
    Enter the user number
    """)
