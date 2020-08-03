import os.path
import pandas as pd
from pandas import ExcelWriter

temp = {}
temps = []
temp_ids = []
temp_types = []
temp_names = []
temp_comments = []
temp_likes = []
temp_replies = []
temp_key_words = []
temp_themes = []


def export(ids, types, names, comments, likes, replies, key_words=None, themes=None):
    if key_words is not None:
        fname = 'src/data/instaCommentsGrouped.xlsx'
    else:
        fname = 'src/data/instaComments.xlsx'
    if os.path.isfile(fname):
        saved = pd.read_excel(fname)
        temp_ids.extend(saved['id'])
        temp_types.extend(saved['type'])
        temp_names.extend(saved['name'])
        temp_comments.extend(saved['comment'])
        temp_likes.extend(saved['likes'])
        temp_replies.extend(saved['replies'])
        if key_words is not None:
            temp_key_words.extend(saved['key words'])
            temp_themes.extend(saved['themes'])
    temp_ids.extend(ids)
    temp_types.extend(types)
    temp_names.extend(names)
    temp_comments.extend(comments)
    temp_likes.extend(likes)
    temp_replies.extend(replies)
    if key_words is not None:
        temp_key_words.extend(key_words)
        temp_themes.extend(themes)
        temp.update(
            {'id': temp_ids, 'type': temp_types, 'name': temp_names, 'comment': temp_comments, 'likes': temp_likes,
             'replies': temp_replies, 'key words': temp_key_words, 'themes': temp_themes})
    else:
        temp.update(
            {'id': temp_ids, 'type': temp_types, 'name': temp_names, 'comment': temp_comments, 'likes': temp_likes,
             'replies': temp_replies})
    df = pd.DataFrame(temp)
    writer = ExcelWriter(fname)
    df.to_excel(writer, 'Instagram Comments', index=False)
    writer.save()
    print(f"Saving extracted data to: {os.getcwd()}/{fname}")
