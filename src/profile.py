from typing import List, Dict

class AccountProfile(object):
    class post:
        comment_num = int
        likes = int
        url_link = str
    followers = int
    followings = int
    post_num = int
    posts = List[post]

def profile_parser() -> AccountProfile:
    pass