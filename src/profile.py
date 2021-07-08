from typing import List, Dict
import re

NUM_RECENT_POSTS = 12

class AccountProfile(object):
    def __init__(self):
        self.n_followers = 0
        self.n_following = 0
        self.n_posts = 0

        # post fields
        self.n_comments = []
        self.n_likes = []
        self.captions = []
        self.hashtags = []
        self.url_codes = []


def profile_parser(username, profile_graphql) -> AccountProfile:
    profile = AccountProfile()
    # parse number of follower & following
    profile.n_followers = profile_graphql.get('graphql').get('user').get('edge_followed_by').get('count')
    profile.n_following = profile_graphql.get('graphql').get('user').get('edge_follow').get('count')
    
    # parse recent posts
    json_posts = profile_graphql.get('graphql').get('user').get('edge_owner_to_timeline_media')
    profile.n_posts = json_posts.get('count')

    for i in range(NUM_RECENT_POSTS):
        profile.n_comments.append(json_posts.get('edges')[i].get('node').get('edge_media_to_comment').get('count'))
        profile.n_likes.append(json_posts.get('edges')[i].get('node').get('edge_liked_by').get('count'))
        
        caption = json_posts.get('edges')[i].get('node').get('edge_media_to_caption').get('edges')[0].get('node').get('text')
        profile.captions.append(caption)
        profile.hashtags.append(re.findall(r"#(\w+)", caption))
        
        profile.url_codes.append(json_posts.get('edges')[i].get('node').get('shortcode'))

    print(profile)

    return profile



def get_post_link(profile_graphql):
    pass