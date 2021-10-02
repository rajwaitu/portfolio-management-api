 
import pymongo
import requests
import feedparser
import datetime
import random

def __fetch_feed_links_for_site(site):
        mongoClient = pymongo.MongoClient("mongodb://localhost:27017/")
        newsdb = mongoClient["news-db"]
        feedLinksCollection = newsdb["rss-feed-links"]
        allLinks = []

        for link in feedLinksCollection.find({"site" : site},{ "_id": 0, "site": 1, "links": 1,"image": 1 }):
         allLinks.append(link)
        return allLinks


def find_feeds(url,site,image):
        allFeeds = []

        r = requests.get(url)
        d = feedparser.parse(r.content)

        # d.entries is a list of dict
        #print('total number of entries in feed for url : ' + url)
        #print(len(d.entries))

        '''
        if(site == 'zeebiz'):
            print(d.entries[0])
        '''

        #print(len(d.entries))
        
        #print(r.content)


        if(len(d.entries) > 0):
          for entry in d.entries:
            feed = {}
            feed['site'] = site
            feed['title'] = entry.title
            feed['link'] = entry.link
            feed['summary'] = entry.summary

            if entry.has_key('media_content'):
             feed['image'] = entry.media_content[0]['url']
            elif(image is not None):
              feed['image'] = image

            allFeeds.append(feed)
        return allFeeds

# get feeds on the fly
def get_current_feeds(site):
        allLinks =  __fetch_feed_links_for_site(site)
        feeds = []

        for eachLink in allLinks:
            site = eachLink.get('site')
            links = eachLink.get('links')
            image = eachLink.get('image')

            if(len(links) > 1):
                for link in links:
                    feed = find_feeds(link,site,image)
                    if len(feed) > 0 : feeds.extend(feed)

            else:
                feeds = find_feeds(links[0],site,image)

        #random.shuffle(feeds)
        return {"allFeeds" : feeds}