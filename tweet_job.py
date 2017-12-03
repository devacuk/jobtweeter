#!/usr/bin/python

# Martin Hamilton <martin.hamilton@jisc.ac.uk> for dev.ac.uk

from lxml.html.soupparser import fromstring	# the most lenient parser?
from slackclient import SlackClient		# Slack API
from selenium import webdriver 			# remote control browser, take screenshots
from PIL import Image 				# image manipulation
import requests					# URL fetcher
import tweepy 					# Twitter API
import time					# needed for sleep
import sys					# needed to change default text encoding to UTF-8 + access arguments
import config as cfg				# top secret Twitter API keys

reload(sys)
sys.setdefaultencoding('utf8')			# Danger Will Robinson!

# URL we'll be looking at today
URL = sys.argv[1]

# Chrome remote control code
DRIVER="chromedriver";

# fetch the page at this URL and keep a copy of the text that we can search
r = requests.get(URL)
t = fromstring(r.content)			# parse with the BeautifulSoup parser

# XPATH routes to the relevant bits of the jobs.ac.uk HTML - found via Chrome Developer Tools
role = t.findtext('.//*[@id="layout"]/div[1]/h1')
institution = t.findtext('.//*[@id="layout"]/div[1]/h3/strong')
ft = t.findtext('.//*[@id="layout"]/div[1]/div[2]/table[1]/tr[4]/td[2]')
#salary = t.findtext('.//*[@id="layout"]/div[1]/div[2]/table[1]/tr[2]/td[2]') # XXX needs more work to find this info reliably

# remote control Chrome to fetch the URL
driver = webdriver.Chrome(DRIVER)
driver.get(URL)

# scroll to the bit we are interested in, and take a screenshot
element = driver.find_element_by_id('layout')	# we want the content tagged with "layout"
location = element.location_once_scrolled_into_view
driver.save_screenshot('screenshot.png')	# saves screenshot of entire page
driver.quit()

# crop screenshot to just the main content
im = Image.open('screenshot.png')		# uses PIL library to open image in memory
left = int(location['x'])
top = int(location['y'])
right = 700					# hard coded to match jobs.ac.uk content area
bottom = 670					# hard coded to match jobs.ac.uk content area
im = im.crop((left, top, right, bottom))	# defines crop points
im.save('screenshot.png')			# saves new cropped image

# Line up a tweet about this job
tweet_text = "Job opportunity: {0} at {1}, {2} {3} #devacuk via @jobsacuk".format(role, institution, ft, URL)
if len(tweet_text) > 280:
  tweet_text = "Job opportunity: {0} at {1}, {2} #devacuk via @jobsacuk".format(role, institution, URL)
if len(tweet_text) > 280:
  tweet_text = "Job opportunity: {0} {1} #devacuk via @jobsacuk".format(role, URL)
if len(tweet_text) > 280:
  tweet_text = "Job opportunity: {0} {1} #devacuk @jobsacuk".format(role, URL)
print "Tweet: " + tweet_text

# Line up a Slack post about this job
slack_text = "{0} at {1}, {2} {3}".format(role, institution, ft, URL)
slack_headline = "{0}".format(role)
print "Slack headline: " + slack_headline
print "Slack: " + slack_text

time.sleep(5)					# in case it screws up horribly and we're frantically hitting ^C

# Post it on Twitter
auth = tweepy.OAuthHandler(cfg.CONSUMER_KEY, cfg.CONSUMER_SECRET)
auth.set_access_token(cfg.ACCESS_TOKEN, cfg.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)
api.update_with_media('screenshot.png', tweet_text)

# And post it on the #jobs channel on our devacuk Slack instance
sc = SlackClient(cfg.SLACK_VERIFICATION_TOKEN)
sc.api_call(
  'files.upload', 
  channels='jobs', 
  title=slack_headline,
  is_public=True,
  initial_comment=slack_text,
  file=open('screenshot.png', 'rb'),
)


