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

def profile_parser(profile_graphql) -> AccountProfile:
    n_posts = load_and_check.get('graphql').get('user').get('edge_owner_to_timeline_media').get('count')
    n_followers = load_and_check.get('graphql').get('user').get('edge_followed_by').get('count')
    n_following = load_and_check.get('graphql').get('user').get('edge_follow').get('count')