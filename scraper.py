from selenium import webdriver
import time
import sys
import excel_exporter

c_ids = []
c_types = []
c_names = []
c_comments = []
c_likes = []
c_replies = []


def start():
    driver = initialize_driver(sys.argv[1])
    close_sign_in_popup(driver)
    load_all_comments(driver)
    comment_iterator(driver)
    excel_exporter.export(c_ids, c_types, c_names, c_comments, c_likes, c_replies)
    driver.close()


def initialize_driver(url):
    driver = webdriver.Firefox()
    driver.get(url)
    time.sleep(2)
    return driver


def close_sign_in_popup(driver):
    try:
        close_button = driver.find_element_by_class_name('xqRnw')
        close_button.click()
        return True
    except Exception as e:
        print(e)
        return False


def load_all_comments(driver):
    times_loaded = 0
    try:
        load_comment_button = driver.find_element_by_css_selector('.MGdpg > button:nth-child(1)')
        while load_comment_button.is_displayed():
            load_comment_button.click()
            time.sleep(1.0)
            load_comment_button = driver.find_element_by_css_selector('.MGdpg > button:nth-child(1)')
            times_loaded += 1
            if (times_loaded + 1) % 10:
                print(f"Times loaded main comments: {times_loaded} [Loading...]")
    except Exception as e:
        print(f"Times loaded main comments: {times_loaded} [Finished]")
        pass


def comment_iterator(driver):
    comment_containers = driver.find_elements_by_class_name('Mr508')
    index = 0
    for comment_container in comment_containers:
        name, comment, likes, replies = extract_comment(comment_container)
        append_comment(index, 'Main', name, comment, likes, replies)
        try:
            reply_container = load_reply_comments(comment_container)
            reply_container = reply_container.find_elements_by_class_name('ZyFrc')
            for reply_comment_container in reply_container:
                name, comment, likes, replies = extract_comment(reply_comment_container)
                append_comment(index, 'Reply', name, comment, likes, replies)
        except Exception as e:
            pass
        index = index + 1


def extract_comment(comment_container):
    container = comment_container.find_element_by_class_name('C4VMK')
    name = container.find_element_by_class_name('_6lAjh').text
    comment = container.find_element_by_tag_name('span').text
    comment = comment.replace('\n', ' ').strip().rstrip()
    button_container = container.find_element_by_class_name('_7UhW9')
    buttons = button_container.find_elements_by_class_name('FH9sR')
    likes = 0
    for button in buttons:
        if "likes" in button.text or "like" in button.text:
            likes = button.text.split()
            likes = int(likes[0].replace(',', ''))
    replies = define_replies_amount(comment_container)
    return name, comment, likes, replies


def define_replies_amount(comment_container):
    replies = 0
    try:
        reply_container = comment_container.find_element_by_class_name('TCSYW')
        replies = reply_container.find_element_by_tag_name('span').text
        replies = replies.split()
        replies = int(replies[2].replace('(', '').replace(')', ''))
    except Exception as e:
        pass
    return replies


def load_reply_comments(comment_container, times_loaded):
    reply_container = comment_container.find_element_by_class_name('TCSYW')
    show_replies_button = comment_container.find_element_by_class_name('sqdOP.yWX7d.y3zKF')
    while show_replies_button.is_displayed():
        show_replies_button.click()
        time.sleep(0.3)
        show_replies_button = comment_container.find_element_by_class_name('sqdOP.yWX7d.y3zKF')
        button_text = reply_container.find_element_by_tag_name('span').text
        times_loaded += times_loaded + 1
        if (times_loaded + 1) % 10:
            print(f"Times loaded reply comments: {times_loaded} [Loading...]")
        if button_text == "Hide replies":
            print(f"Times loaded reply comments: {times_loaded} [Loading...]")
            reply_container = comment_container.find_element_by_class_name('TCSYW')
            break
    return reply_container


def append_comment(index, category, name, comment, likes, replies):
    c_ids.append(index)
    c_types.append(category)
    c_names.append(name)
    c_comments.append(comment)
    c_likes.append(likes)
    c_replies.append(replies)


start()
