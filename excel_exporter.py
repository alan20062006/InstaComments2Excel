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


def export(ids, types, names, comments, likes, replies):
    fname = 'instaComments.xlsx'
    if os.path.isfile(fname):
        saved = pd.read_excel(fname)
        temp_ids.extend(saved['id'])
        temp_types.extend(saved['type'])
        temp_names.extend(saved['name'])
        temp_comments.extend(saved['comment'])
        temp_likes.extend(saved['likes'])
        temp_replies.extend(saved['replies'])
    temp_ids.extend(ids)
    temp_types.extend(types)
    temp_names.extend(names)
    temp_comments.extend(comments)
    temp_likes.extend(likes)
    temp_replies.extend(replies)
    temp.update({'id': temp_ids, 'type': temp_types, 'name': temp_names, 'comment': temp_comments, 'likes': temp_likes,
                 'replies': temp_replies})
    df = pd.DataFrame(temp)
    writer = ExcelWriter(fname)
    df.to_excel(writer, 'ridwan kamil', index=False)
    writer.save()
    print(f"Saving Excel sheet to: {os.getcwd()}/{fname}")
