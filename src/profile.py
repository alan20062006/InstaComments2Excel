from typing import List, Dict
import re

NUM_RECENT_POSTS = 12

class AccountProfile(object):
    self.n_followers = int
    self.n_following = int
    self.n_posts = int

    # post fields
    self.n_comments = List[int]
    self.n_likes = List[int]
    self.captions = List[str]
    self.hashtags = List[List[str]]
    self.url_codes = List[str]


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
        profile.captions.append(json_posts.get('edges')[i].get('node').get('edge_media_to_caption').get('edges')[0].get('node').get('text'))
        profile.hashtags.append(re.findall(r"#(\w+)", post.caption))
        profile.url_codes.append(json_posts.get('edges')[i].get('node').get('shortcode'))

    print(profile)

    return profile



def get_post_link(profile_graphql):
    pass