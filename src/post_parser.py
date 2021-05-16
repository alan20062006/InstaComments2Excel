import requests

def post_json_parser(self, logging_page_id: str) -> None:
    """
    logging_page_id: the post json string
    """
    image_urls = []
    video_urls = []
    try:
        """Taking Gallery Photos or Videos"""
        for log_pages in logging_page_id['graphql']['shortcode_media']['edge_sidecar_to_children']['edges']:
            description = log_pages['node']['accessibility_caption']
            video = log_pages['node']['is_video']
            if video:
                videos_url = log_pages['node']['video_url']
                video_urls.append(videos_url)
            else:
                images_url = log_pages['node']['display_url']
                image_urls.append(images_url)

    except KeyError:
        """Unique photo or Video"""
        description = logging_page_id['graphql']['shortcode_media']['accessibility_caption']
        image_url = logging_page_id['graphql']['shortcode_media']['display_url']
        image_urls.append(image_url)

        if logging_page_id['graphql']['shortcode_media']['is_video']:
            video_url = logging_page_id['graphql']['shortcode_media']['video_url']
            video_urls.append(video_url)

if __name__ == "__main__":
    # for unitest
    http_base = requests.Session()
    # test single picture post
    post_json_parser(http_base.get('https://www.instagram.com/p/COyhuiaKZop/?__a=1').json())
    # test multiple pictures post
    post_json_parser(http_base.get('https://www.instagram.com/p/CN37zCdsmAF/?__a=1').json())
    # test single video post
    post_json_parser(http_base.get('https://www.instagram.com/p/COSkTGfgW3f/?__a=1').json())
    # test multiple videos post
    post_json_parser(http_base.get('https://www.instagram.com/p/CO6HZFvLGUM/?__a=1').json())

    