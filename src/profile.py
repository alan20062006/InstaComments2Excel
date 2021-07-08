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

def profile_parser(username, profile_graphql) -> AccountProfile:
    n_posts = profile_graphql.get('graphql').get('user').get('edge_owner_to_timeline_media').get('count')
    n_followers = profile_graphql.get('graphql').get('user').get('edge_followed_by').get('count')
    n_following = profile_graphql.get('graphql').get('user').get('edge_follow').get('count')

    print(f"user: {username}, followers: {n_followers}, following: {n_following},\npost_likes: {n_likes}\nn_comments{n_comments}")

def get_post_link(profile_graphql):
    pass