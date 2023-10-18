import json
import re

import joblib
import numpy as np
import pandas as pd
import tensorflow as tf
from keras.callbacks import ModelCheckpoint
from keras.layers import (
    BatchNormalization,
    Concatenate,
    Dense,
    Embedding,
    Flatten,
    Input,
    LeakyReLU,
)
from keras.optimizers import Adam
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder, OrdinalEncoder
from tensorflow import random as tf_random

RANDOM = 202309


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


class AddOne(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X + 1


def prepare_data(users_table, movies_table, ratings_table):
    cached_data_path = 'cached_data'

    df_users = pd.read_csv(f'.\\{cached_data_path}\\{users_table}').rename(
        columns={'id': 'user', 'fav_genres.1': 'favorited_genres'}
    )
    df_movies = pd.read_csv(f'.\\{cached_data_path}\\{movies_table}').rename(
        columns={'id': 'movie_id'}
    )
    df_ratings = pd.read_csv(f'.\\{cached_data_path}\\{ratings_table}').rename(
        columns={'id': 'rate_id', 'movie': 'movie_id'}
    )

    initial_columns_order = [
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
        'rate',
    ]

    new_columns_order_st1 = [
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
        'rate',
    ]

    data = df_ratings.merge(df_movies, how='left', on='movie_id').merge(
        df_users, how='left', on='user'
    )[initial_columns_order]

    data['premiere_date'] = pd.to_datetime(data['premiere_date']).dt.year
    data['favorited_genres'] = data['favorited_genres'].fillna('0')

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

    # Применяем нашу функцию предобработки к данным
    preprocessor_st1 = OrdinalEncoder(
        unknown_value=-1, handle_unknown='use_encoded_value'
    )
    data[id_columns] = preprocessor_st1.fit_transform(data[id_columns])

    # Применение AddOne
    ao = AddOne()
    data[id_columns] = data[id_columns].apply(ao.transform)

    # Применение StringToList
    stl = StringToList()
    stl.fit(data[list_transform_columns])
    data[list_transform_columns] = data[list_transform_columns].apply(
        stl.transform
    )

    # Преобразовываем data в DataFrame с нужным порядком столбцов
    fixed_data = data[new_columns_order_st1]

    preprocessor_st2 = ColumnTransformer(
        transformers=[
            (
                'ohe_features',
                OneHotEncoder(sparse=False, drop='first'),
                ohe_encoding_columns,
            ),
            ('numerical_features', MinMaxScaler(), numerical_encoding_columns),
        ],
        remainder='passthrough',
    )

    preprocessor_st2.fit(fixed_data.drop('rate', axis=1))

    mins = {}
    maxs = {}
    ns = {}
    lens = {}
    for i in [
        'user',
        'movie_id',
        'genres',
        'actors',
        'favorited_genres',
        'directors',
        'countries',
    ]:
        try:
            mins[i] = min(fixed_data[i].apply(lambda x: min(x)))
            maxs[i] = max(fixed_data[i].apply(lambda x: max(x)))
            lens[i] = max(fixed_data[i].apply(len))
        except:
            mins[i] = min(fixed_data[i].tolist())
            maxs[i] = max(fixed_data[i].tolist())

    data_metrics_json = {'min': mins, 'max': maxs, 'n': ns, 'len': lens}

    X_train = pd.DataFrame(
        preprocessor_st2.transform(fixed_data.drop('rate', axis=1))
    )

    train_input_user = np.array(X_train[8].astype(int))
    train_input_movie = np.array(X_train[9].astype(int))
    train_input_gender_0 = np.array(X_train[0].astype(int))
    train_input_gender_1 = np.array(X_train[1].astype(int))
    train_input_age = np.array(X_train[2])
    train_input_imdb = np.array(X_train[3])
    train_input_kinopoisk = np.array(X_train[4])
    train_input_duration = np.array(X_train[5])
    train_input_age_limit = np.array(X_train[6])
    train_input_year = np.array(X_train[7])

    train_input_genres = np.array(
        X_train[10]
        .apply(
            lambda x: x + [0] * (data_metrics_json['len']['genres'] - len(x))
        )
        .values.tolist()
    )

    train_input_actors = np.array(
        X_train[11]
        .apply(
            lambda x: x + [0] * (data_metrics_json['len']['actors'] - len(x))
        )
        .values.tolist()
    )

    train_input_favorited_genres = np.array(
        X_train[12]
        .apply(
            lambda x: x
            + [0] * (data_metrics_json['len']['favorited_genres'] - len(x))
        )
        .values.tolist()
    )

    train_input_directors = np.array(
        X_train[13]
        .apply(
            lambda x: x
            + [0] * (data_metrics_json['len']['directors'] - len(x))
        )
        .values.tolist()
    )

    train_input_countries = np.array(
        X_train[14]
        .apply(
            lambda x: x
            + [0] * (data_metrics_json['len']['countries'] - len(x))
        )
        .values.tolist()
    )

    train_inputs = [
        train_input_user,
        train_input_movie,
        train_input_gender_0,
        train_input_gender_1,
        train_input_age,
        train_input_imdb,
        train_input_kinopoisk,
        train_input_duration,
        train_input_age_limit,
        train_input_year,
        train_input_genres,
        train_input_actors,
        train_input_favorited_genres,
        train_input_directors,
        train_input_countries,
    ]

    joblib.dump(preprocessor_st1, 'stage1preprocessor')
    joblib.dump(preprocessor_st2, 'stage2preprocessor')
    with open('data_metrics.json', 'w') as f:
        json.dump(data_metrics_json, f)

    return (
        [arr.astype(np.float64) for arr in train_inputs],
        fixed_data['rate'],
        data_metrics_json,
    )


def net(
    learning_rate=0.001,
    loss='mean_squared_error',
    layer1_units=10,
    layer2_units=5,
    layer3_units=None,
    layer4_units=None,
    layer5_units=None,
    layer6_units=None,
    layer1_activation='relu',
    layer2_activation='relu',
    layer3_activation='relu',
    layer4_activation='relu',
    layer5_activation='relu',
    layer6_activation='relu',
):
    """
    Компиляция нейронной сети:

    Параметры:
        learning_rate (float): скорость обучения оптимизатора. default: 0.001
        loss (str): функция потерь для компиляции модели. default: mean_squared_error
        layer[n]_units (int): количество нейронов в слое
        layer[n]_activation (str): функция активации слоя

    Вывод:
        model (tf.keras.Model): скомпилированная модель.
    """

    with open('data_metrics.json', 'r') as f:
        data_metrics_json = json.load(f)

    # Фиксация случайных значений для воспроизводимости
    tf_random.set_seed(RANDOM)
    np.random.seed(RANDOM)

    # Оптимизатор
    optimizer = Adam(learning_rate=learning_rate)

    # Входные слои
    layer_user_id = Input(shape=[1], name='user')
    layer_movie_id = Input(shape=[1], name='movie')
    layer_gender0 = Input(shape=[1], name='gender0')
    layer_gender1 = Input(shape=[1], name='gender1')
    layer_age = Input(shape=[1], name='age')
    layer_imdb = Input(shape=[1], name='imdb')
    layer_kinopoisk = Input(shape=[1], name='kinopoisk')
    layer_duration = Input(shape=[1], name='duration')
    layer_age_limit = Input(shape=[1], name='age_limit')
    layer_year = Input(shape=[1], name='year')

    layer_genres = Input(
        shape=[data_metrics_json['len']['genres']], name='genres'
    )
    layer_actors = Input(
        shape=[data_metrics_json['len']['actors']], name='actors'
    )
    layer_favorites = Input(
        shape=[data_metrics_json['len']['favorited_genres']], name='favorites'
    )
    layer_directors = Input(
        shape=[data_metrics_json['len']['directors']], name='directors'
    )
    layer_countries = Input(
        shape=[data_metrics_json['len']['countries']], name='countries'
    )

    # Эмбеддинги для id пользователей
    user_embedding = Embedding(
        output_dim=10,
        input_dim=int(data_metrics_json['max']['user']) + 5,
        input_length=1,
        name='user_embedding',
    )(layer_user_id)
    user_embedding = Flatten()(user_embedding)

    # Эмбеддинги для id фильмов
    movie_embedding = Embedding(
        output_dim=10,
        input_dim=int(data_metrics_json['max']['movie_id']) + 5,
        input_length=1,
        name='movie_embedding',
    )(layer_movie_id)
    movie_embedding = Flatten()(movie_embedding)

    # Эмбеддинги для списочных id жанров
    genres_embedding = Embedding(
        output_dim=5,
        input_dim=data_metrics_json['max']['genres'] + 1,
        input_length=data_metrics_json['len']['genres'],
        mask_zero=True,
    )(layer_genres)
    genres_embedding = Flatten()(genres_embedding)

    # Эмбеддинги для списочных id актеров
    actors_embedding = Embedding(
        output_dim=5,
        input_dim=data_metrics_json['max']['actors'] + 10,
        input_length=data_metrics_json['len']['actors'],
        mask_zero=True,
    )(layer_actors)
    actors_embedding = Flatten()(actors_embedding)

    # Эмбеддинги для списочных id любимых жанров пользователя
    favorites_embedding = Embedding(
        output_dim=5,
        input_dim=data_metrics_json['max']['favorited_genres'] + 1,
        input_length=data_metrics_json['len']['favorited_genres'],
        mask_zero=True,
    )(layer_favorites)
    favorites_embedding = Flatten()(favorites_embedding)

    # Эмбеддинги для списочных id режиссеров
    directors_embedding = Embedding(
        output_dim=5,
        input_dim=data_metrics_json['max']['directors'] + 5,
        input_length=data_metrics_json['len']['directors'],
        mask_zero=True,
    )(layer_directors)
    directors_embedding = Flatten()(directors_embedding)

    # Эмбеддинги для списочных id стран
    countries_embedding = Embedding(
        output_dim=5,
        input_dim=data_metrics_json['max']['countries'] + 1,
        input_length=data_metrics_json['len']['countries'],
        mask_zero=True,
    )(layer_countries)
    countries_embedding = Flatten()(countries_embedding)

    # Объединение всех эмбеддингов
    x = Concatenate()(
        [
            user_embedding,
            movie_embedding,
            layer_gender0,
            layer_gender1,
            layer_age,
            layer_imdb,
            layer_kinopoisk,
            layer_duration,
            layer_age_limit,
            layer_year,
            genres_embedding,
            actors_embedding,
            favorites_embedding,
            directors_embedding,
            countries_embedding,
        ]
    )

    # Полносвязные слои
    x = BatchNormalization()(x)
    x = Dense(
        layer1_units,
        activation=layer1_activation,
        kernel_initializer='he_normal',
    )(x)

    x = BatchNormalization()(x)
    x = Dense(
        layer2_units,
        activation=layer2_activation,
        kernel_initializer='he_normal',
    )(x)

    # Ниже второго слои создаются если в аргументах указано количество нейронов
    # в обратном случае остается 2 полносвязных слоя
    if layer3_units:
        x = BatchNormalization()(x)
        x = Dense(
            layer3_units,
            activation=layer3_activation,
            kernel_initializer='he_normal',
        )(x)

    if layer4_units:
        x = BatchNormalization()(x)
        x = Dense(
            layer4_units,
            activation=layer4_activation,
            kernel_initializer='he_normal',
        )(x)

    if layer5_units:
        x = BatchNormalization()(x)
        x = Dense(
            layer5_units,
            activation=layer5_activation,
            kernel_initializer='he_normal',
        )(x)

    if layer6_units:
        x = BatchNormalization()(x)
        x = Dense(
            layer6_units,
            activation=layer6_activation,
            kernel_initializer='he_normal',
        )(x)

    # Выходной слой
    output = Dense(1, activation='linear')(x)

    # Создание и компиляция модели
    model = tf.keras.Model(
        inputs=[
            layer_user_id,
            layer_movie_id,
            layer_gender0,
            layer_gender1,
            layer_age,
            layer_imdb,
            layer_kinopoisk,
            layer_duration,
            layer_age_limit,
            layer_year,
            layer_genres,
            layer_actors,
            layer_favorites,
            layer_directors,
            layer_countries,
        ],
        outputs=output,
    )
    model.compile(
        optimizer=optimizer, loss=loss, metrics=['mean_absolute_error']
    )

    return model


def train(
    model, X, y, batch_size=100, epochs=100, validation_split=0.2, verbose=0
):
    """
    Функция обучает нейросеть

    Аргументы:
    - model (tf.keras.Model): Модель для обучения
    - X (array-like): Входные признаки для обучения
    - y (array-like): Целевой признак
    - batch_size (int, optional): Размер пакета для одной итерации. default 100.
    - epochs (int, optional): Количество эпох обучения. default 100.
    - validation_split (float, optional): Доля данных, которая будет использована для валидации. default 0.2 (20 %)
    - verbose (int, optional): Режим отображения процесса обучения (0 - не показывать, 1 - показывать прогресс, 2 - подробный прогресс)

    Вывод:
    - dict: Словарь, содержащий обученную модель и историю обучения.
    """

    # Инициализация чекпойнта для сохранения лучшей модели
    checkpoint = ModelCheckpoint("best_model.h5", save_best_only=True)

    # Обучение модели с переданными аргументами и сохранением истории обучения
    history = model.fit(
        X,
        y,
        batch_size=batch_size,
        epochs=epochs,
        validation_split=validation_split,
        verbose=verbose,
        callbacks=[
            checkpoint
        ],  # сохранение состояния сети на лучшей валидации
    )

    return {'model': model, 'history': history}


if __name__ == '__main__':
    model = net(
        learning_rate=0.0025,
        loss='mean_squared_error',
        layer1_units=200,
        layer2_units=150,
        layer3_units=100,
        layer4_units=20,
        layer5_units=8,
        layer6_units=2,
        layer1_activation='relu',
        layer2_activation=LeakyReLU(alpha=0.2),
        layer3_activation='relu',
        layer4_activation=LeakyReLU(alpha=0.2),
        layer5_activation='relu',
        layer6_activation=LeakyReLU(alpha=0.2),
    )

    temporary_data = [
        'User-2023-10-14.csv',
        'Movie-2023-10-14.csv',
        'RatingMovie-2023-10-14.csv',
    ]

    train_data = prepare_data(
        temporary_data[0], temporary_data[1], temporary_data[2]
    )

    train(
        model, train_data[0], train_data[1].values.astype('float64'), 90, 250
    )
