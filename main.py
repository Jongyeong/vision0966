#-*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
from TwitterSearch import *
import requests.packages.urllib3
import base64
from StringIO import StringIO
import cStringIO
import requests
from PIL import Image
from operator import itemgetter
import pygal
from google.appengine.api import memcache
from pygal.style import DefaultStyle

requests.packages.urllib3.disable_warnings()

app = Flask(__name__)

DISCOVERY_URL = 'https://{api}.googleapis.com/$discovery/rest?version={apiVersion}'


# for twitter
access_token = ""
access_token_secret = ""
consumer_key = ""
consumer_secret = ""


max_length = 0


@app.route('/')
def start():
    return render_template('main.html')


@app.route('/user', methods=['POST', 'GET'])
def twu():
    try:
        text = []
        global max_length
        keyword = request.form['user']
        tuo = TwitterUserOrder('%s' % keyword)
        tuo.set_include_entities(True)
        text = search(tuo)
        memcache.set(key=keyword, value=text, time=3600)
        max_length = len(text)
        if len(text) is 0:
            pie_chart = pygal.Pie(no_data_text='No result found',
                                  style=DefaultStyle(no_data_font_size=60))
            return pie_chart.render_response()
        else:
            return render_template('process.html', text=text, max_length=max_length, keyword=keyword)
    except TwitterSearchException as e:
        return render_template('error.html', error=e)


@app.route('/word', methods=['POST', 'GET'])
def tww():
    try:
        text = []
        global max_length
        keyword = request.form['word']
        tso = TwitterSearchOrder()
        tso.set_keywords([keyword])
        tso.set_include_entities(True)
        text = search(tso)
        memcache.set(key=keyword, value=text, time=3600)
        max_length = len(text)
        if len(text) is 0:
            pie_chart = pygal.Pie(no_data_text='No result found',
                                  style=DefaultStyle(no_data_font_size=60))
            return pie_chart.render_response()
        else:
            return render_template('process.html', text=text, max_length=max_length, keyword=keyword)
    except TwitterSearchException as e:
        return render_template('error.html', error=e)


@app.route('/vision', methods=['POST', 'GET'])
def process():
    text = request.form['url']
    response = requests.get(text)
    img = Image.open(StringIO(response.content))
    annotations = logo_finder(img)
    if annotations:
        temp = [a['description'] for a in annotations]
        append(text, temp)
    return '1'


@app.route('/final/<string:keyword>', methods=['POST', 'GET'])
def graph(keyword):
    re = []
    text = memcache.get(key=keyword)
    temp = memcache.get_multi(keys=text)
    for val in temp.values():
        re.append(val)
    result = sort(re)
    key = []
    value = []
    for i in range(0, len(result)):
        key.append(result[i][0])
        value.append(result[i][1])
    title = 'Brand(Logo) in : %s (in percentage)' % keyword
    pie_chart = pygal.Pie(dynamic_print_values=True, style=DefaultStyle)
    pie_chart.title = title
    pie_chart.value_formatter = lambda x: "%.2f" % x
    for i in range(0, len(result)):
        pie_chart.add(key[i], value[i])
    chart = pie_chart.render_data_uri()
    return render_template('result.html', chart=chart)

if __name__ == '__main__':
    app.run()


def logo_finder(image, max_results=1):
    buff = cStringIO.StringIO()
    image.save(buff, format='JPEG')
    batch_request = [{
        'image': {
            'content': base64.b64encode(buff.getvalue()).decode('UTF-8')
        },
        'features': [{
            'type': 'LOGO_DETECTION',
            'maxResults': max_results,
        }]
    }]
    service = get_vision_service()
    req = service.images().annotate(body={
        'requests': batch_request,
    })
    response = req.execute()
    return response['responses'][0].get('logoAnnotations', None)


def get_vision_service():
    credentials = GoogleCredentials.get_application_default()
    return discovery.build('vision', 'v1', credentials=credentials,
                           discoveryServiceUrl=DISCOVERY_URL)


def search(to):
    se = []
    ts = token()
    for tweet in ts.search_tweets_iterable(to):
        if 'media' in tweet['entities']:
            if tweet['entities']['media'][0]['type'] == 'photo':
                se.append(tweet['entities']['media'][0]['media_url'])
            else:
                continue
        else:
            continue
    return se


def token():
    ts = TwitterSearch(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret
    )
    return ts


def sort(k):
    result = {}
    for temp in k:
        if temp in result.keys():
            result[temp] += float(100.0/len(k))
        else:
            result[temp] = float(100.0/len(k))
    result = sorted(result.iteritems(), key=itemgetter(1), reverse=True)
    return result


def append(text, temp):
    for x in temp:
        memcache.set(key=text, value=x, time=3600)
