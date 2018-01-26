import os
import sys
import tempfile
import webbrowser
import time
import datetime

# urllib compatibility
from pip._vendor.requests.packages.urllib3.connectionpool import xrange
py_version = sys.version_info.major
if py_version == 2:
    import urllib2
    from bs4 import BeautifulSoup
elif py_version == 3:
    import urllib.request
    from bs4 import BeautifulSoup

from shutil import copyfile
from sys import platform

# Free to use to gather post feeds
# Add twitter profiles to static_twitter_profiles
# just like how the two example profiles are
# 
# To run:
# python ./scrape.py

save_scrapping = "false"
profilesPerPage = 8
number_of_posts = 8
defaultDomain = 'https://twitter.com/'
# static_twitter_profiles = []
static_twitter_profiles = ['CNN', 'BBCNews']

profilesCount = len(static_twitter_profiles)
print("Scrapping " + str(profilesCount) + " Profiles")

# Generate Temp File then copy extra files to temp
tmp = tempfile.NamedTemporaryFile(delete=False)
path = str(tmp.name + '.html')
print('\ntmp file: {0}\npath file: {1}\ntmp.name: {2}'.format(tmp,path,tmp.name))
os.rename(tmp.name, path)
current_running_dir = os.path.dirname(os.path.realpath(__file__))

def custom_headers():
    current_running_dir = os.path.dirname(os.path.realpath(__file__))
    css_file_path = js_file_path = current_running_dir + "/"
    if platform == "linux" or platform == "linux2":
        # linux
        css_tmp_path = js_tmp_file_path = "/tmp/"
    elif platform == "darwin":
        # OS X
        css_tmp_path = js_tmp_file_path = "/tmp/"
    elif platform == "win32":
        css_tmp_path = js_tmp_file_path = "%TEMP%/"

    # Handle local CSS to Temp Dir
    css_file = css_file_path + "style.css"
    css_tmp_path = css_tmp_path + "style.css"
    if os.path.isfile(css_file):
        copyfile(css_file, css_tmp_path)

    # Handle local JS to Temp Dir
    js_file = js_file_path + "customJS.js"
    js_tmp_file_path = js_tmp_file_path + "customJS.js"
    if os.path.isfile(js_file):
        copyfile(js_file, js_tmp_file_path)

    f.write("""
    <meta http-equiv='Content-Type' content='text/html; charset=utf-8'>
    <meta http-equiv='Content-Type' content='text/html; charset=shift_jis'>
    <link rel='stylesheet' href='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css'>
    <script src='https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js'></script>
    <script src='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js'></script>
    <link href='""" + str(css_tmp_path) + """' rel='stylesheet' type='text/css'>
    <script src='""" + str(js_tmp_file_path) + """' type='text/javascript'></script>""")


# Gather Contents returns body of url > profile
def contact_twitter(url):
    print("Contacting: " + url)
    if py_version == 2:
        http_response = urllib2.urlopen(url)
    elif py_version == 3:
        http_response = urllib.request.urlopen(url)
    return BeautifulSoup(http_response, "html.parser")


# This will parse out only the posts DOM Objects from Scrapped content (.tweet)
def pull_tweets(soup_response, post_index):
    cards_all = soup_response.find_all('div', class_="tweet")
    return cards_all[post_index]


# Prints each post in one calls group
def print_tweet(id, profile, name, showNumberOfPosts):
    title_txt = "<button type='button' id='profileTitle' data-parent='#title' data-toggle='collapse' " \
                "data-target=\"#slot-" + id + "\"><strong>" + name + "</strong></button>"
    f.write(str("<div id=\"title\" class=\"panel panel-default\">" + title_txt + "</div>"))
    f.write("<div id=\"slot-" + id + "\" class='collapse panel-body'>")
    f.write("<div class='slot'>")
    for x0 in xrange(showNumberOfPosts):
            f.write(str(pull_tweets(soup_response=profile, post_index=x0)))

    f.write("</div>")
    f.write("</div>")


# Arrow Keys, carasoul dots, Search, Checkbox's
def write_navigation(carousal_name, item_page_count):
    f.write("<div id=\"pageMarker\">")
    f.write("<ol class=\"carousel-indicators\">")
    for x in xrange(item_page_count):
        if x == 0:
            f.write("<li data-target=\"#" + carousal_name + "\" data-slide-to=\"0\" class=\"active\"></li>")
        elif x == itemPageCount:
            f.write(
                "<li data-target=\"#" + carousal_name + "\" data-slide-to=\"" + str((item_page_count + 1)) + "\"></li>")
        else:
            f.write("<li data-target=\"#" + carousal_name + "\" data-slide-to=\"" + str(x) + "\"></li>")
    f.write("</ol>")
    f.write("</div>")

    # Arrow Keys
    f.write("""<a class='left carousel-control' href='#""" + carousal_name + """' data-slide='prev'>
            <span class='glyphicon glyphicon-chevron-left'></span>
            <span class='sr-only'\>Previous</span>
            </a>
            <a class='right carousel-control' href='#""" + carousal_name + """' data-slide=\"next\">
            <span class='glyphicon glyphicon-chevron-right'></span>
            <span class='sr-only'>Next</span>
            </a>
            </div>""")


# Create & Print out
if 'html' not in path:
    path = str(path+'.html')
    print('Path did not have html: {}'.format(path))
else:
    path = path
f = open(path, 'w')
f.write("""<!DOCTYPE html><head>""")

# CDN - BootStrap & jQuery plus custom CSS
custom_headers()

# Override CSS
f.write("""<style>
    .carousel-indicators { bottom: 0; left: 50%; list-style: outside none none; margin-left: -30%; margin-top: 18px;  
                        padding-left: 0; position: relative; text-align: center; width: 60%;  z-index: 15;}
    </style>
    </head>
    <body>
    <div id='myCarousel' class='carousel slide' data-ride='carousel' data-interval='false'>
    <div class='carousel-inner'>""")

# Contact Twitter based on current profile
# Loop through and write content out as appropriate
isFirstPage = "true"
carousalInnerPage = 0
itemPageCount = 0
clock = datetime.datetime.now()
for x, currentProfile in enumerate(static_twitter_profiles):
    current_url = str(defaultDomain + currentProfile)
    twitter_content = contact_twitter(current_url)
    if (carousalInnerPage == 0) & (isFirstPage == "true"):
        isFirstPage = "false"
        f.write("<div class='item active'>")
    elif carousalInnerPage == profilesPerPage:
        carousalInnerPage = 0
        itemPageCount = itemPageCount + 1
        f.write("</div><div class='item'>")
    elif (carousalInnerPage == 0) & (isFirstPage == "false"):
        f.write("<div class='item'>")
    carousalInnerPage = carousalInnerPage + 1
    print_tweet(id=str(x), profile=twitter_content, name=currentProfile, showNumberOfPosts=number_of_posts)

stop_time = datetime.datetime.now() - clock
print("End Time > " + str(stop_time))
f.write("</div></div>")

# Carousal Arrows & Dots
write_navigation("myCarousel", itemPageCount)

f.write("""</div>
        <div id='footer' class='row'>
        <div class='col-sm-2'>
        Profile Count: """ + str(profilesCount) +
        "<br />End Time: " + str(stop_time) +
        """<br />
        </div>
        <div class='col-md-3'>
        <input type='text' class='search-form' placeholder='Search'>
        </div>

        <script>
        lookupTweet('.search-form','.item','.collapse');
        </script>
        </body></html>""")
f.close()
webbrowser.open('file://' + path)
time.sleep(99)

# Clean Tmp Dir
if (os.path.exists(path)) & (save_scrapping == "false"):
    os.remove(path)

exit()
