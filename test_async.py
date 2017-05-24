from asyncit import Asyncit
import requests
import json
from time import sleep


@Asyncit.wait
def get_json1(url):
    response = requests.get(url)
    if (response.status_code != 200):
        raise Exception("Invalid response code!: " + str(response.status_code))
    return response.json()

@Asyncit.nowait
def get_json2(url):
    sleep(5)
    response = requests.get(url)
    if (response.status_code != 200):
        raise Exception("Invalid response code!: " + str(response.status_code))
    return response.json()

def process(j, subreddit):
    for i in j['data']['children']:
        score = i['data']['score']
        title = i['data']['title']
        link = i['data']['url']
        print(str(score) + ': ' + title + ' (' + link + ')')
    print('DONE:', subreddit + '\n')

def get_reddit_top_wait(subreddit):  
    j = get_json1('https://www.reddit.com/r/' + subreddit + '/top.json?sort=top&t=day&limit=5')
    process(j, subreddit)
    for i in range(1, 6):
        print(i)
        sleep(1)

def get_reddit_top_nowait(subreddit):
    callback = get_json2('https://www.reddit.com/r/' + subreddit + '/top.json?sort=top&t=day&limit=5')
    callback(lambda j: process(j, subreddit))
    for i in range(1, 6):
        print(i)
        sleep(1)

print("--------------wait-------------")
get_reddit_top_wait("programming")
print("-------------nowait------------")
get_reddit_top_nowait("programming")
