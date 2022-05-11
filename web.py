import streamlit as st
import pandas as pd 
#import os


ratings=pd.read_csv(r'Python/Jupyter/Recommender_Systems/ratings.csv')
movies=pd.read_csv(r'Python/Jupyter/Recommender_Systems/movies.csv')
links=pd.read_csv(r'Python/Jupyter/Recommender_Systems/links.csv')
tags=pd.read_csv(r'Python/Jupyter/Recommender_Systems/tags.csv')


matrix = pd.merge(ratings,movies, how ="inner", on = ["movieId"])

matrix= pd.merge(matrix,tags, how ="inner", on = ["movieId"])


st.title("WBSFLIX")
 
st.write("""
### Recommender Systems
Popular Movies
""")

# Popularity based

matrix.dropna()

matrix.drop(['timestamp_x','timestamp_y','userId_y'], axis=1, inplace=True )

def popularity_based_recommender(data: pd.DataFrame, min_n_ratings: int):
    
    return (
        matrix
        .groupby(['movieId', 'title',  'genres'])
        .agg(
           
            movie_rating_mean = ('rating', 'mean'),
            movie_rating_count = ('rating', 'count')
        )
        .reset_index()
        .sort_values('movie_rating_mean')
        .query('movie_rating_count > @min_n_ratings')
        .head(5)
        )

popularity_based_recommender(matrix.copy(), 20)

matrix_1 = popularity_based_recommender(matrix.copy(), 20)
popular_movies = matrix_1.filter(['title'])
    
st.dataframe(popular_movies)

# Sorting data
# newdf= (
#     matrix
#     .filter(['userId_x', 'title', 'rating'])
#     .groupby(['userId_x'])
#     .head(5))

# (newdf
#     .groupby(['userId_x'])
#     .agg(
#         mean_rating = ('rating', 'mean'),
#         count_rating = ('rating', 'count')
#     )
#     .reset_index()
#     .sort_values('mean_rating', ascending=False))

# newdf.set_index('userId_x')

# newdf1 = newdf.drop_duplicates()

# # # Iteam Based Movie

# movie_name = st.sidebar.text_input("Enter the name of a movie")

# py function get sparse matrix
# def get_sparse_matrix(newdf1: pd.DataFrame): 
#     return(
#     newdf1
#         .pivot(index='userId_x', columns='title', values='rating')
#     ) 
    
# if(movie_name != ''):
#     def item_based_recommender(dense_matrix: pd.DataFrame, title: str, n: int=5): 
#         try:
#             sparse_matrix = get_sparse_matrix(newdf1)
#             return( sparse_matrix
#              .corrwith(sparse_matrix[title])
#              .sort_values(ascending=False)
#              .index
#              .to_list()[1:n+1]
#             )
#         except:
#             return 
#                   st.text("given movie in not present in the data")

#     matrix_2 = item_based_recommender(newdf1, movie_name)
    
#     st.text("Movies recommended based on the given Input")
    
#     st.dataframe(matrix_2)
# else:
#     st.write("""
#     Enter the movie name
#     """)
    
## User Based

user_pref = st.sidebar.number_input("Enter user number", value=0, min_value=0, step=1, max_value=999)
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
    Enter the number
    """)
