#!/usr/bin/env python3
import os
import time

import feedparser
import functions_framework
from google.cloud import storage
import requests

# Constants

LOBSTERS_FEED_URL       = 'https://lobste.rs/rss'
LOBSTERS_MINIMUM_SCORE  = 10

# Functions

def fetch_article_score(url):
    response = requests.get(url + '.json')
    return response.json()['score']

def fetch_all_articles(url=LOBSTERS_FEED_URL):
    feed = feedparser.parse(url)

    for entry in feed.entries:
        yield {
            'title'    : entry.title,
            'author'   : entry.author.split('@')[0],
            'link'     : entry.comments,
            'published': entry.published,
            'timestamp': entry.published_parsed,
            'guid'     : entry.guid,
            'score'    : fetch_article_score(entry.comments),
        }

        time.sleep(0.5)   # Work around rate limit

def generate_articles_feed(articles):
    feed = '''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>Lobsters</title>
    <link>https://lobste.rs</link>
    <description></description>'''

    for article in sorted(articles, key=lambda a: a['timestamp'], reverse=True):
        feed += f'''
    <item>
      <title>{article['title']}</title>
      <author>{article['author']}</author>
      <link>{article['link']}</link>
      <guid isPermaLink="false">{article['guid']}</guid>
      <pubDate>{article['published']}</pubDate>
    </item>'''

    feed += '''
  </channel>
</rss>'''

    return feed

def generate_feed_with_limit():
    return generate_articles_feed(
        a for a in fetch_all_articles()
        if a['score'] > LOBSTERS_MINIMUM_SCORE
    )

@functions_framework.cloud_event
def main(cloud_event):
    client = storage.Client()
    bucket_name = os.environ['LOBSTERS_BISQUE_BUCKET_NAME']
    bucket = client.get_bucket(bucket_name)

    feed = generate_feed_with_limit()
    blob = storage.Blob('lobsters.rss', bucket)
    blob.upload_from_string(feed, content_type='application/rss+xml')

    return feed

if __name__ == '__main__':
    print(generate_feed_with_limit())
