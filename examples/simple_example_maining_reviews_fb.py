# File: examples/simple_example_maining_reviews_fb

from selenium import webdriver
import time


def getting_reviews(browser, pg):
    url = "https://www.facebook.com/pg/%s/reviews/" % pg
    browser.get(url)
    # Setting time of pause for scroll
    scroll_pause_time = 1
    last_height = browser.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(scroll_pause_time)

        # Calculate new scroll height and compare with last scroll height
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    # Getting the list of reviews as elements by id
    blocks = browser.find_elements_by_css_selector('.fbUserContent')

    content_str = ""
    for block in blocks:
        try:
            name_block = block.find_element_by_css_selector("span.fwb a.profileLink")
            # Getting the text inside the attributes
            name = name_block.text
            profile = name_block.get_attribute('href')
        except:
            # print("ERROR")
            name_block = block.find_element_by_css_selector("span.fwb span.profileLink")
            # Getting the text inside the attributes
            name = name_block.text
            profile = "No_url_PRIVATE_PROFILE=)"
        rating = block.find_element_by_css_selector("h5 .fcg i u")
        content = block.find_element_by_css_selector(".userContent")
        content_str += name + "\n"
        content_str += profile + "\n"
        content_str += content.text + "\n"
        content_str += rating.text + "\n"
        content_str += "###" + "\n"
    return content_str


browser = webdriver.Firefox()
# browser.implicitly_wait(3)
try:
    with open("reviews_csatucu.txt", "w", encoding="utf-8") as file_write:
        file_write.write(getting_reviews(browser, "csatucu"))
finally:
    browser.close()
