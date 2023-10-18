import json
import re

import joblib
import numpy as np
import pandas as pd
from keras.models import load_model
from sklearn.base import BaseEstimator, TransformerMixin

from morec.settings.core import BASE_DIR

UTILITY_PATH = f'{BASE_DIR}/analytics/model/'


class AddOne(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X + 1


class StringToList(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        self.input_features_ = X.columns
        return self

    def transform(self, X, y=None):
        return X.map(self.string_to_list)

    def string_to_list(self, x):
        if pd.isna(x):
            return x
        else:
            return [int(n) for n in re.split(',\s*|\s+', x)]

    def get_feature_names(self, input_features=None):
        return self.input_features_


def user_processing(test_user_slug):

    cached_data_path = 'cached_data'
    users_table = 'User-2023-10-14.csv'
    movies_table = 'Movie-2023-10-14.csv'
    ratings_table = 'RatingMovie-2023-10-14.csv'

    try:
        with open(f'{UTILITY_PATH}data_metrics.json', 'r') as f:
            fitted_metrics = json.load(f)
            process1 = joblib.load(UTILITY_PATH + 'stage1preprocessor')
            process2 = joblib.load(UTILITY_PATH + 'stage2preprocessor')
            df_users = pd.read_csv(UTILITY_PATH + f'{cached_data_path}/{users_table}').rename(
                columns={'id': 'user', 'fav_genres.1': 'favorited_genres'})
            df_movies = pd.read_csv(UTILITY_PATH + f'{cached_data_path}/{movies_table}').rename(columns={'id': 'movie_id'})
            df_ratings = pd.read_csv(UTILITY_PATH + f'{cached_data_path}/{ratings_table}').rename(
                columns={'id': 'rate_id', 'movie': 'movie_id'})

    except FileNotFoundError:
        with open('data_metrics.json', 'r') as f:
            fitted_metrics = json.load(f)
            process1 = joblib.load('stage1preprocessor')
            process2 = joblib.load('stage2preprocessor')
            df_users = pd.read_csv(f'.\\{cached_data_path}\\{users_table}').rename(
                columns={'id': 'user', 'fav_genres.1': 'favorited_genres'})
            df_movies = pd.read_csv(f'.\\{cached_data_path}\\{movies_table}').rename(columns={'id': 'movie_id'})
            df_ratings = pd.read_csv(f'.\\{cached_data_path}\\{ratings_table}').rename(
                columns={'id': 'rate_id', 'movie': 'movie_id'})

    multiplied_test_user = pd.concat([df_users[df_users['user'] == test_user_slug]] * len(df_movies), ignore_index=True)

    df_test_merged = (
        pd.concat(
            [multiplied_test_user, df_movies], axis=1
        )
        .merge(
            df_ratings[df_ratings['user'] == test_user_slug], on=['movie_id', 'user'], how='left'
        )
        [[
            'user',
            'sex',
            'date_of_birth',
            'favorited_genres',
            'movie_id',
            'rate_imdb',
            'rate_kinopoisk',
            'duration_minutes',
            'premiere_date',
            'age_limit',
            'genres',
            'actors',
            'directors',
            'countries',
            'rate'
        ]]
    )

    df_test_merged['premiere_date'] = pd.to_datetime(
        df_test_merged['premiere_date']
    ).dt.year
    df_test_merged['favorited_genres'] = df_test_merged[
        'favorited_genres'
    ].fillna('0')

    if len(df_users[df_users['user'] == test_user_slug]) == 0:
        df_test_merged['date_of_birth'] = df_test_merged[
            'date_of_birth'
        ].fillna(0)

    list_transform_columns = [
        'genres',
        'actors',
        'favorited_genres',
        'directors',
        'countries',
    ]
    ohe_encoding_columns = ['sex']
    id_columns = ['user', 'movie_id']
    numerical_encoding_columns = [
        'date_of_birth',
        'rate_imdb',
        'rate_kinopoisk',
        'duration_minutes',
        'age_limit',
        'premiere_date',
    ]

    df_test_merged[id_columns] = process1.transform(df_test_merged[id_columns])

    # Применение AddOne
    ao = AddOne()
    df_test_merged[id_columns] = df_test_merged[id_columns].apply(ao.transform)

    # Применение StringToList
    stl = StringToList()
    stl.fit(df_test_merged[list_transform_columns])
    df_test_merged[list_transform_columns] = df_test_merged[
        list_transform_columns
    ].apply(stl.transform)

    # Преобразовываем data в DataFrame с нужным порядком столбцов
    fixed_data = df_test_merged[[
        'user',
        'movie_id',
        'genres',
        'actors',
        'favorited_genres',
        'directors',
        'countries',
        'sex',
        'date_of_birth',
        'rate_imdb',
        'rate_kinopoisk',
        'duration_minutes',
        'premiere_date',
        'age_limit',
        'rate'
    ]]

    if len(fixed_data[fixed_data['rate'].isna()]) > 10:
        fixed_data = fixed_data[fixed_data['rate'].isna()]

    X_test_one_user_data = pd.DataFrame(
        process2.transform(
            fixed_data.drop('rate', axis=1)
        )
    )

    one_user_input_user = np.array(X_test_one_user_data[8].astype(int))
    one_user_input_movie = np.array(X_test_one_user_data[9].astype(int))
    one_user_input_gender_0 = np.array(X_test_one_user_data[0].astype(int))
    one_user_input_gender_1 = np.array(X_test_one_user_data[1].astype(int))
    one_user_input_age = np.array(X_test_one_user_data[2])
    one_user_input_imdb = np.array(X_test_one_user_data[3])
    one_user_input_kinopoisk = np.array(X_test_one_user_data[4])
    one_user_input_duration = np.array(X_test_one_user_data[5])
    one_user_input_age_limit = np.array(X_test_one_user_data[6])
    one_user_input_year = np.array(X_test_one_user_data[7])

    one_user_input_genres = np.array(
        X_test_one_user_data[10].apply(
            lambda x: x + [0] * (
                fitted_metrics['len']['genres'] - len(x)
            )).values.tolist()
    )

    one_user_input_actors = np.array(
        X_test_one_user_data[11].apply(
            lambda x: x + [0] * (
                fitted_metrics['len']['actors'] - len(x)
            )).values.tolist()
    )

    one_user_input_favorited_genres = np.array(
        X_test_one_user_data[12].apply(
            lambda x: x + [0] * (
                fitted_metrics['len']['favorited_genres'] - len(x)
            )).values.tolist()
    )

    one_user_input_directors = np.array(
        X_test_one_user_data[13].apply(
            lambda x: x + [0] * (
                fitted_metrics['len']['directors'] - len(x)
            )).values.tolist()
    )

    one_user_input_countries = np.array(
        X_test_one_user_data[14].apply(
            lambda x: x + [0] * (
                fitted_metrics['len']['countries'] - len(x)
            )).values.tolist()
    )

    one_user_inputs = [
        one_user_input_user,
        one_user_input_movie,
        one_user_input_gender_0,
        one_user_input_gender_1,
        one_user_input_age,
        one_user_input_imdb,
        one_user_input_kinopoisk,
        one_user_input_duration,
        one_user_input_age_limit,
        one_user_input_year,
        one_user_input_genres,
        one_user_input_actors,
        one_user_input_favorited_genres,
        one_user_input_directors,
        one_user_input_countries
    ]

    return [arr.astype(np.float64) for arr in one_user_inputs], fixed_data['movie_id']


def get_inference(data) -> list:
    try:
        try:
            model = load_model(UTILITY_PATH + 'best_model.h5')
        except FileNotFoundError:
            model = load_model('best_model.h5')

        one_user_preds = model.predict(data[0]).flatten()

        one_user_results = pd.DataFrame(
            {'movie_id': data[1].astype(int).tolist(),
             'rate': one_user_preds}
        )

        one_user_results_sampler = one_user_results.sort_values(
            'rate', ascending=False
        ).head(20).sample(n=10)

        return_list = one_user_results_sampler['movie_id'].tolist()
        if 0 in return_list:
            try:
                one_best_film = pd.read_csv(
                    UTILITY_PATH + 'cached_data/dflt_movies.csv'
                ).sample()['movie_id'].tolist()
            except FileNotFoundError:
                one_best_film = pd.read_csv(
                    '.\\cached_data\\dflt_movies.csv'
                ).sample()['movie_id'].tolist()
            finally:
                index = return_list.index(0)
                return_list[index] = one_best_film[0]

        return return_list

    except:
        try:
            one_user_results_sampler = pd.read_csv(
                UTILITY_PATH + 'cached_data/dflt_movies.csv'
            ).sample(n=10)
        except FileNotFoundError:
            one_user_results_sampler = pd.read_csv(
                '.\\cached_data\\dflt_movies.csv'
            ).sample(n=10)

        return one_user_results_sampler['movie_id'].tolist()
