# jobtweeter
Look for developer oriented jobs on jobs.ac.uk and Tweet / Slack about them

## How to use it:

1. Install any dependencies you don't already have, e.g. "pip install feedparser", Selenium driver for Chrome etc
2. Create Twitter app and put secrets, key, access token into "config.py" (see config.py.example for file format)
3. "touch job_url_log.txt" - we keep a record here of job listing URLs we've seen
4. Run "find_dev_jobs.py" and it should produce a list of RSS feeds checked and URLs that look like they are for dev jobs
5. Run "tweet_job.py URL" where URL is one of the job listing URLs previously output

## Notes:

find_dev_jobs.py has a hard coded list of jobs.ac.uk RSS feed URLs, and knows a little bit about the structure of a jobs.ac.uk job listing, so that it can pull out just the content of the job listing to check for key words (like SQL, Ruby, Erlang etc). This isn't generalised code that would work with lots of different sites - it really is just for jobs.ac.uk (for now...)

tweet_job.py uses Soupparser to sloppily match key fields from the job listing, Selenium to screenshot the job listing as it appears in the browser, PIL to crop the image to just the bits we're interested in, and Tweepy + SlackClient to tweet and Slack(?) all of this. It doesn't cope well with updates that are more than 140 characters, or job listing pages that don't follow the normal jobs.ac.uk template, but the results it produces are useful and interesting

## TODO: [[ hint: you could help with this! ]]

- Error checking!
- Support for a wider range of job listing sources / sites - or maybe we keep this to just ac.uk related jobs ?
- Ability to run headless - some clues here: https://duo.com/blog/driving-headless-chrome-with-python ?
- Hard coded file names, e.g. "screenshot.png" - could put these in the config file ?
- Smarts to truncate e.g. text in brackets if it's making our Tweet too long
- More developer jargon for our list :-)
