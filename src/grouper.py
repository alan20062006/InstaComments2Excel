import os.path
import pandas as pd
import numpy as np
import exporter


c_ids = []
c_types = []
c_names = []
c_comments = []
c_likes = []
c_replies = []
c_key_words = []
c_themes = []

stats = {}

PATH_TO_DATA_FILE = r'/src/data/instaComments.xlsx'
PATH_TO_GROUPINGS_FILE = r'/src/data/groupings.xlsx'


def initialize():
    global i_df, g_df, g_df_columns
    i_df = pd.read_excel(os.getcwd() + PATH_TO_DATA_FILE)
    g_df = pd.read_excel(os.getcwd() + PATH_TO_GROUPINGS_FILE)

    g_df.replace(r'\s+|^$', np.nan, regex=True)
    g_df_columns = g_df.columns.values

    for i in range(len(g_df_columns)):
        stats.update({g_df_columns[i]: [0, 0, 0]})


def iterate_sheet():
    for i_index, i_row in i_df.iterrows():
        key_words = None
        themes = None
        likes = i_row['likes']
        replies = i_row['replies']
        comment = i_row["comment"]
        for g_index, g_row in g_df.iterrows():
            for i in range(len(g_df_columns)):
                current_column_theme = g_df_columns[i]
                current_column_word = g_row[g_df_columns[i]]

                if pd.isna(current_column_word):
                    continue

                if current_column_word.upper() in comment.upper():
                    if key_words is None:
                        key_words = current_column_word
                    else:
                        key_words += ", " + current_column_word

                    if themes is None:
                        themes = current_column_theme
                        stats.get(current_column_theme)[0] += 1
                    elif current_column_theme not in themes:
                        themes += ", " + current_column_theme
                        stats.get(current_column_theme)[0] += 1
                    stats.get(current_column_theme)[1] += likes
                    if replies == "['Hide', 'replies']":
                        replies = 0
                    stats.get(current_column_theme)[2] += replies

        c_ids.append(i_row['id'])
        c_types.append(i_row['type'])
        c_names.append(i_row['name'])
        c_comments.append(i_row['comment'])
        c_likes.append(i_row['likes'])
        c_replies.append(i_row['replies'])
        c_key_words.append(key_words)
        c_themes.append(themes)


def export():
    print('\n', stats, '\n')
    exporter.export_comments(c_ids, c_types, c_names, c_comments, c_likes, c_replies, c_key_words, c_themes)
    exporter.export_stats(stats, True)


def start():
    initialize()
    iterate_sheet()
    export()


start()
