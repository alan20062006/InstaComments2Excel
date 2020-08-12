import os.path
import pandas as pd
import numpy as np
import exporter


insta_df = pd.read_excel(os.getcwd() + r'/src/data/instaComments.xlsx')
insta_df_columns = insta_df.columns.values
group_df = pd.read_excel(os.getcwd() + r'/src/data/groupings.xlsx')
group_df.replace(r'\s+|^$', np.nan, regex=True)
group_df_columns = group_df.columns.values

stats = {}

for i in range(len(group_df_columns)):
    stats.update({group_df_columns[i]: 0})

# print(groupings_counter)
# print(group_df)

c_ids = []
c_types = []
c_names = []
c_comments = []
c_likes = []
c_replies = []
c_key_words = []
c_themes = []

for i_index, i_row in insta_df.iterrows():
    key_words = None
    themes = None
    comment = i_row["comment"]
    for g_index, g_row in group_df.iterrows():
        for i in range(len(group_df_columns)):
            current_column_theme = group_df_columns[i]
            current_column_word = g_row[group_df_columns[i]]

            if pd.isna(current_column_word):
                continue

            if current_column_word.upper() in comment.upper():
                if key_words is None:
                    key_words = current_column_word
                else:
                    key_words += ", " + current_column_word

                if themes is None:
                    themes = current_column_theme
                    stats[current_column_theme] += 1
                elif current_column_theme not in themes:
                    themes += ", " + current_column_theme
                    stats[current_column_theme] += 1

    c_ids.append(i_row['id'])
    c_types.append(i_row['type'])
    c_names.append(i_row['name'])
    c_comments.append(i_row['comment'])
    c_likes.append(i_row['likes'])
    c_replies.append(i_row['replies'])
    c_key_words.append(key_words)
    c_themes.append(themes)

print(stats)

exporter.export_comments(c_ids, c_types, c_names, c_comments, c_likes, c_replies, c_key_words, c_themes)
exporter.export_stats(stats)
