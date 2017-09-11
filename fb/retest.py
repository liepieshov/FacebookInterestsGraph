import json
import datetime
import csv
import time
import requests

app_id = "182309148958301"
app_secret = "57ab18c8ab5cbeedb1dab2eedf341115"
page_id = "1889640824624912"

access_token = app_id + "|" + app_secret


def request_until_succeded(url):
    print(
        url)
    response = requests.request("GET", url)
    # success = False
    # while success is False:
    #     try:
    #         response = urllib2.urlopen(req)
    #         if response.getcode() == 200:
    #             success = True
    #     except Exception as e:
    #         print(e)
    #         time.sleep(5)
    #
    #         print("Error for URL %s: %s" % (url, datetime.datetime.now()))
    #         print(
    #         "Retrying.")
    # encoding = response.headers.get_content_charset()
    encoding = None
    if encoding is None:
        print("Error")
        encoding = "utf-8"
    return response.text.decode(encoding)


def getFacebookPageFeedData(page_id, access_token, num_statuses):
    base = "https://graph.facebook.com/v2.9"
    node = "/%s/posts" % page_id
    fields = "/?fields=message,likes{hometown, name}"
    parameters = "&limit=%s&access_token=%s" % (num_statuses, access_token)

    url = base + node + fields + parameters

    data = json.loads(request_until_succeded(url))

    return data


if __name__ == "__main__":
    print(
        getFacebookPageFeedData(page_id, access_token, 5))
