#!/usr/bin/python

# Import dependencies
import pickle
import feedparser
import smtplib
import mimetypes
import email
import email.mime.application

# Set up variables
pickleAddress = "/location/to/your/postLinks.p"
fromAddress = "youremail@gmail.com"
fromPassword = "y0urP@ssw0rd"
toAddress = "youremail@gmail.com"
rss = "http://www.yourRssFeed.com/rss"

# Load previous feed entries
postLinks = pickle.load(open(pickleAddress, "rb"))
newPostLinks = []
feed = feedparser.parse(rss)

# Iterate through all feed entries, and compare to what we received previously
for post in feed.entries:

        #If post.link doesn't already exist in postLinks
        if not any(post.link in l for l in postLinks):

            #Create a plain text message
            msg = email.mime.Multipart.MIMEMultipart()
            msg['Subject'] = """[RSS] """ + post.title
            msg['From'] = fromAddress
            msg['To'] = toAddress

            # Main body
            body = email.mime.Text.MIMEText("""<a href = '""" + post.guid + """'>""" + post.guid + """</a><br/><br/>"$
            msg.attach(body)

            # Send via Gmail server
            send = smtplib.SMTP('smtp.gmail.com:587')
            send.starttls()
            send.login(fromAddress, fromPassword)
            send.sendmail(toAddress, [toAddress], msg.as_string())
            send.quit()

        newPostLinks.append(post.link)

# Export our current list of unique IDs
pickle.dump(newPostLinks, open(pickleAddress, "wb"))