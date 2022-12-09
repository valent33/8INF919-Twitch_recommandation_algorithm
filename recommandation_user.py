import pandas as pd
import numpy as np
import sys

def similarity(user1, user2):
    # calculate the similarity between two users
    # return the similarity
    return np.dot(user1, user2) / (np.linalg.norm(user1) * np.linalg.norm(user2))

def recommandation(matrix, user):
    # calculate the recommandation for a user
    return np.dot(matrix, user) / np.linalg.norm(user)

def recommand_category(user, df_pivot_category, matrix_category):
    # get the user index
    user_index = df_pivot_category.index.get_loc(user)
    # get the user's categories
    user_categories = df_pivot_category.loc[user]
    user_categories = user_categories[user_categories > 0]
    # get the user
    user_matrix = matrix_category[user_index]
    # calculate the similarity between the user and all the other users
    similarities = []
    for i in range(len(matrix_category)):
        similarities.append(similarity(user_matrix, matrix_category[i]))
    # get the most similar users
    most_similar_users = np.argsort(similarities)[::-1][:10000]
    # naive recommandation system that loops through the most similar users and add the categories to a list
    recommandation = {}
    for i in most_similar_users:
        # get the categories of the user
        categories = df_pivot_category.iloc[i]
        categories = categories[categories > 0]
        # add the categories to the recommandation list
        for category in categories.index:
            # add counts to the category key
            recommandation[category] = recommandation.get(category, 0) + categories[category]
    # filter out the categories that the user already follows
    for category in user_categories.index:
        if category in recommandation:
            del recommandation[category]
    # get the top 10 recommandation
    top_10_recommandation = sorted(recommandation.items(), key=lambda x: x[1], reverse=True)[:10]

    print('Top 10 categories recommandation for ' + user + ' are: ')
    # print the top 10 recommandation
    for i, reco in enumerate(top_10_recommandation):
        print(f'#{i+1} - {reco[0]}')

def recommand_streamer(user, df_pivot_streamer, matrix_streamer):
    # get the user index
    user_index = df_pivot_streamer.index.get_loc(user)
    # retrieve the user's streamers
    user_streamers = df_pivot_streamer.iloc[user_index]
    user_streamers = user_streamers[user_streamers > 0]
    # get the user
    user_matrix = matrix_streamer[user_index]
    # calculate the similarity between the user and all the other users
    similarities = []
    for i in range(len(matrix_streamer)):
        similarities.append(similarity(user_matrix, matrix_streamer[i]))
    # take 10000 randomly out of 100000 most similar users
    most_similar_users = np.argsort(similarities)[::-1][:10000]
    # most_similar_users = np.random.choice(most_similar_users, 10000)
    # naive recommandation system that loops through the most similar users and add the streamers to a list
    recommandation = {}
    for i in most_similar_users:
        # get the streamers of the user
        streamers = df_pivot_streamer.iloc[i]
        streamers = streamers[streamers > 0]
        # add the streamers to the recommandation list
        for streamer in streamers.index:
            # add counts to the streamer key
            recommandation[streamer] = recommandation.get(streamer, 0) + streamers[streamer]
    # filter out the streamers that the user already follows
    for streamer in user_streamers.index:
        if streamer in recommandation:
            del recommandation[streamer]
    # get the top 10 recommandation
    top_10_recommandation = sorted(recommandation.items(), key=lambda x: x[1], reverse=True)[:10]

    print('Top 10 streamers recommandation for ' + user + ' are: ')
    # print the top 10 recommandation
    for i, reco in enumerate(top_10_recommandation):
        print(f'#{i+1} - {reco[0]}')

def main():
    df = pd.read_csv('graph/final_fr.csv')

    # username
    user = sys.argv[1]
    
    # category or streamer
    category_or_streamer = sys.argv[2]

    if category_or_streamer == 'streamer':
        # drop the category column
        df = df.drop(columns=['category'])
        
        grouped = df.groupby('viewers')['streamer'].nunique()
        # filter out the viewers that have only one unique streamer
        filtered = grouped[grouped > 1]
        # filter out the rows that have a viewer that only watches one  but keep user
        filtered_df = df[df['viewers'].isin(filtered.index) | (df['viewers'] == user)]

        # create a pivot table for streamers and addition the counts
        df_pivot_streamer = filtered_df.pivot_table(index='viewers', columns='streamer', values='counts', fill_value=0, aggfunc='sum')
        df_pivot_streamer.fillna(0, inplace=True)

        matrix_streamer = df_pivot_streamer.to_numpy()
        user_streamers = df_pivot_streamer.loc[user]
        user_streamers = user_streamers[user_streamers > 0]

        print("The streamers that " + user + " watches are: ")
        print(user_streamers)
        recommand_streamer(user, df_pivot_streamer, matrix_streamer)

    else :
        # remove the streamer column
        df = df.drop(columns=['streamer'])

        # group by viewers and count the unique categories
        grouped = df.groupby('viewers')['category'].nunique()
        # filter out the viewers that have only one unique category
        filtered = grouped[grouped > 1]
        # filter out the rows that have a viewer that only watches one category but keep user
        filtered_df = df[df['viewers'].isin(filtered.index) | (df['viewers'] == user)]

        # create a pivot table for categories and addition the counts
        df_pivot_category = filtered_df.pivot_table(index='viewers', columns='category', values='counts', fill_value=0, aggfunc='sum')
        df_pivot_category.fillna(0, inplace=True)

        matrix_category = df_pivot_category.to_numpy()
        user_categories = df_pivot_category.loc[user]
        user_categories = user_categories[user_categories > 0]

        print("The categories that " + user + " watches are: ")
        print(user_categories)
        recommand_category(user, df_pivot_category, matrix_category)

main()