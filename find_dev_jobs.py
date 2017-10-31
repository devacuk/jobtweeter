#!/usr/bin/python

# Martin Hamilton <martin.hamilton@jisc.ac.uk> for dev.ac.uk

import feedparser					# RSS fetcher / parser
import requests						# curl equivalent
import re						# regex processing
from lxml.html.soupparser import fromstring     	# the most lenient parser?
from lxml.etree import tostring				# turn HTML parser object back into text string

LOG = "job_url_log.txt"					# file recording job listing URLs we've processed
JARGON = "DEV_JARGON.txt"				# words and phrases that suggest it's a developer job
RECALL = [ ]						# in memory copy of job listing URLs we've processed
REMATCH = [ ]						# in memory copy of developer jargon

# URLs we'll be looking at
URLs = {
  "http://www.jobs.ac.uk/jobs/academic-research/?format=rss",
  "http://www.jobs.ac.uk/jobs/professional-managerial/?format=rss",
  "http://www.jobs.ac.uk/jobs/technical/?format=rss",
}

# Other jobs.ac.uk RSS feeds
# "http://www.jobs.ac.uk/jobs/clerical/?format=rss",
# "http://www.jobs.ac.uk/jobs/craft-manual/?format=rss",
# "http://www.jobs.ac.uk/jobs/masters/?format=rss",
# "http://www.jobs.ac.uk/jobs/phd/?format=rss",

# words to match that might signify that a job listing is for a developer
j = open(JARGON, "r")
for k in j.readlines():
  REMATCH.append(k.rstrip())				# strip trailing newline and then stash away for checking later
j.close()

# read in jobs.ac.uk job listing URLs we've seen already
r = open(LOG, "r")
for l in r.readlines():
  RECALL.append(l.rstrip())				# strip trailing newline and then stash away for checking later
r.close()

# now let's reopen our job listing URL log file in append mode
w = open(LOG, "a+")

# finally, fetch each RSS feed and the individul job listing URLs
for URL in URLs:
  print "# {0}".format(URL) 				# this is the RSS feed we are looking at
  feed = feedparser.parse(URL)				# fetch and parse it

  for e in feed.entries:				# loop through the entries in the RSS feed

    if e.id in RECALL:					# have we seen it already?
      #print "Skipping - seen this one already"
      continue						# if so, skip

    RECALL.append(e.id)					# note that we have now seen this job listing URL

    #print "Not seen this one before - processing"
    w.write("{0}\n".format(e.id))			# make a note that we've seen this job listing URL

    # fetch the page at this URL and keep a copy of the text that we can search
    h = requests.get(e.id)				# returns the raw HTML text of the job listing page
    t = fromstring(h.content)				# parse with the BeautifulSoup parser
    l = t.find('.//*[@id="layout"]/*')			# we want the "layout" section
    m = tostring(l)					# now turn it back from lxml object into text string

    # search for common coding terminology
    n = re.compile("(" + "|".join(REMATCH) + ")")	# join the words in REMATCH together as a regex
    
    # drop out if we don't spot developer jargon
    if not n.search(m):					# is there a match for our "developer words" regex?
      continue

    print e.id						# this is the jobs.ac.uk URL of the job listing

w.close()


