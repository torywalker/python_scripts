#!/usr/bin/python

# Import dependencies
import argparse
import pickle
import feedparser
import smtplib
import mimetypes
import email.mime.application

# Set up arguments
parser = argparse.ArgumentParser()
parser.add_argument('--fromEmail', help='The email address that updates will be sent from')
parser.add_argument('--fromPassword', help='The password for the from address')
parser.add_argument('--toEmail', help='The email address that updates will be sent to')
parser.add_argument('--rssUrl', help='The email address that updates will be sent to')
args = parser.parse_args()

# Load previous feed entries
pickleAddress = 'postLinks.pickle'
try:
    postLinks = pickle.load(open(pickleAddress, 'rb'))
except (OSError, IOError) as e:
    postLinks = []
    pickle.dump(postLinks, open(pickleAddress, 'wb'))
newPostLinks = []
feed = feedparser.parse(args.rssUrl)

# Iterate through all feed entries, and compare to what we received previously
for post in feed.entries:

        #If post.link doesn't already exist in postLinks
        if not any(post.link in l for l in postLinks):

            #Create a plain text message
            msg = email.mime.Multipart.MIMEMultipart()
            msg['Subject'] = '[RSS] ' + post.title
            msg['From'] = args.fromEmail
            msg['To'] = args.toEmail

            # Main body
            bodyContent = '<a href = \'' + post.guid + '\'>' + post.guid + '</a><br/><br/>' + post.description
            body = email.mime.Text.MIMEText(bodyContent, 'html')
            msg.attach(body)

            # Send via Gmail server
            send = smtplib.SMTP('smtp.gmail.com:587')
            send.starttls()
            send.login(args.fromEmail, args.fromPassword)
            send.sendmail(args.toEmail, [args.toEmail], msg.as_string())
            send.quit()

        newPostLinks.append(post.link)

# Export our current list of unique IDs
pickle.dump(newPostLinks, open(pickleAddress, "wb"))