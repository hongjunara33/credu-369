import requests
import datetime
import argparse
import http.client
import httplib2
import os
import random
import time
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow

from isodate import parse_duration

from django.conf import settings
from django.shortcuts import render
from videolist.models import Videoinfo
from videolist.models import Categoryinfo
from videolist.models import Mylearninginfo


# Create your views here.
def index(request):
    videos = []

    if request.method == 'POST':
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'

        search_params = {
            'part' : 'snippet',
            'q' : request.POST['search'],
            'key' : settings.YOUTUBE_DATA_API_KEY,
            'maxResults' : 30,
            'type' : 'video'
        }

        video_ids = []
        r = requests.get(search_url, params=search_params)

        results = r.json()['items']

        for result in results:
            video_ids.append(result['id']['videoId'])

        video_params = {
            'key' : settings.YOUTUBE_DATA_API_KEY,
            'part' : 'snippet,contentDetails',
            'id' : ','.join(video_ids),
            'maxResults' : 30
            }

        r = requests.get(video_url, params=video_params)

        results = r.json()['items']

        for result in results:
            video_data = {
            'title' : result['snippet']['title'],
            'id' : result['id'],
            'url' : f'https://www.youtube.com/watch?v={ result["id"] }',
            'duration' : int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
            'thumbnail' : result['snippet']['thumbnails']['high']['url'],
            'description' : result['snippet']['description'][:600]
            }

            videos.append(video_data)

    context = {
        'videos' : videos
    }

    return render(request, 'videolist/index.html', context)

def CreateCategoryinfo(request):

    vids = []
    videos = []

    if request.method == 'POST':
        vids = request.POST.getlist("chkbox")

        video_url = 'https://www.googleapis.com/youtube/v3/videos'
        video_params = {
            'key' : settings.YOUTUBE_DATA_API_KEY,
            'part' : 'snippet,contentDetails',
            'id' : ','.join(vids),
            'maxResults' : 30
            }

        r = requests.get(video_url, params=video_params)

        results = r.json()['items']

        for result in results:
            video_data = {
            'title' : result['snippet']['title'],
            'id' : result['id'],
            'url' : f'https://www.youtube.com/watch?v={ result["id"] }',
            'duration' : int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
            'thumbnail' : result['snippet']['thumbnails']['high']['url'],
            'description' : result['snippet']['description']
            }

            vid = video_data['id']
            title = video_data['title']
            thumbnailurl = video_data['thumbnail']
            videourl = video_data['url']
            duration = video_data['duration']
            description = video_data['description']

            videos.append(video_data)

            if Videoinfo.objects.filter(vid=vid).exists():
                print("The Videoid already exists : %s" % vid)
            else:
                Videoinfo(vid=vid, title=title, thumbnailurl=thumbnailurl, videourl=videourl, duration=duration, description=description).save()

    context = {
         'videos' : videos
    }
    return render(request, 'videolist/createcategory.html', context)

def Mycategoryview(request):
    categorys = []
    mycategorys = []
    vinfo = []

    qs = Mylearninginfo.objects.filter(userid='tag2')
    categorys = qs.values()

    i = 0
    while i < len(categorys):
        vid=categorys[i]['videoid']

        if(i > 0 and (categorys[i-1]['categoryname']==categorys[i]['categoryname'])):
            cname = ""
        else:
            cname=categorys[i]['categoryname']

        cid = categorys[i]['categoryid']
        qs1 = Videoinfo.objects.filter(vid=vid)
        vinfo = qs1.values()

        if(vinfo is None):
            i = i + 1
        else:
            mycategory_data = {
               'categoryname' : cname,
               'categoryid' : cid,
               'videoid' : vid,
               'videotitle' : vinfo[0]['title'],
               'thumbnailurl' : vinfo[0]['thumbnailurl'],
               'videourl' : vinfo[0]['videourl']
            }
            mycategorys.append(mycategory_data)
            i = i + 1

    context = {
                'mycategorys' : mycategorys
            }

    return render(request, 'videolist/mycategoryview.html', context)


def SaveCategoryinfo(request):

    videoids = []

    if request.method == 'POST':
        cname = request.POST.get("category")
        videoids = request.POST.getlist("videoid")
        now = datetime.datetime.now()
        nowDate = now.strftime('%Y%m%d')
        nowDatetime = now.strftime('%Y%m%d%H%M%S')
        categoryid = 'c' + nowDatetime

        for videoid in videoids:
            Mylearninginfo(userid='tag2', videoid=videoid, categoryid=categoryid, categoryname=cname).save()

    return render(request, 'videolist/index.html')

def UpdateCategoryname(request):

    categoryids = []
    categoryinfo = []
    if request.method == 'POST':
        categoryids = request.POST.getlist("chkbox")

        if len(categoryids) == 0:
            categoryid = "NoSel"
            categoryname = "NoSel"
        elif  len(categoryids) >= 2:
            categoryid = "TooMuch"
            categoryname = "TooMuch"
        else:
            categoryid = categoryids[0]
            qs = Mylearninginfo.objects.filter(categoryid=categoryid)
            mlinfo = qs.values()
            categoryname = mlinfo[0]['categoryname']

        category_info = {
            'categoryid' : categoryid,
            'categoryname' : categoryname
            }
        categoryinfo.append(category_info)

    context = {
            'categoryinfo' : categoryinfo
            }

    return render(request, 'videolist/updatecategoryname.html', context)

def UpdateCategoryname1(request):

    if request.method == 'POST':
        categoryname = request.POST.get("categoryname")
        categoryid = request.POST.get("categoryid")

        Mylearninginfo.objects.filter(categoryid=categoryid).update(categoryname=categoryname)

    categorys = []
    vinfo = []
    mycategorys = []
    qs = Mylearninginfo.objects.filter(userid='tag2')
    categorys = qs.values()

    i = 0
    while i < len(categorys):
        vid=categorys[i]['videoid']
        if(i > 0 and (categorys[i-1]['categoryname']==categorys[i]['categoryname'])):
            cname = ""
        else:
            cname=categorys[i]['categoryname']

        cid = categorys[i]['categoryid']
        qs1 = Videoinfo.objects.filter(vid=vid)
        vinfo = qs1.values()
        mycategory_data = {
           'categoryname' : cname,
           'categoryid' : cid,
           'videoid' : vid,
           'videotitle' : vinfo[0]['title'],
           'thumbnailurl' : vinfo[0]['thumbnailurl'],
           'videourl' : vinfo[0]['videourl']
        }
        mycategorys.append(mycategory_data)
        i = i + 1

    context = {
                'mycategorys' : mycategorys
            }

    return render(request, 'videolist/mycategoryview.html', context)

def DeleteCategory(request):
    categorys = []
    mycategorys = []
    vinfo = []

    qs = Mylearninginfo.objects.filter(userid='tag2')
    categorys = qs.values()

    i = 0
    while i < len(categorys):
        vid=categorys[i]['videoid']

        if(i > 0 and (categorys[i-1]['categoryname']==categorys[i]['categoryname'])):
            cname = ""
        else:
            cname=categorys[i]['categoryname']

        cid = categorys[i]['categoryid']
        qs1 = Videoinfo.objects.filter(vid=vid)
        vinfo = qs1.values()

        mycategory_data = {
           'categoryname' : cname,
           'categoryid' : cid,
           'videoid' : vid,
           'videotitle' : vinfo[0]['title'],
           'thumbnailurl' : vinfo[0]['thumbnailurl'],
           'videourl' : vinfo[0]['videourl']
        }
        mycategorys.append(mycategory_data)
        i = i + 1

    context = {
                'mycategorys' : mycategorys
            }
    return render(request, 'videolist/deletecategory.html', context)

def DeleteCategory1(request):

    categoryids = []

    if request.method == 'POST':
        categoryids = request.POST.getlist("chkbox")

        for categoryid in categoryids:
            dml = Mylearninginfo.objects.filter(categoryid=categoryid)
            dml.delete()

    categorys = []
    vinfo = []
    mycategorys = []
    qs = Mylearninginfo.objects.filter(userid='tag2')
    categorys = qs.values()

    i = 0
    while i < len(categorys):
        vid=categorys[i]['videoid']
        if(i > 0 and (categorys[i-1]['categoryname']==categorys[i]['categoryname'])):
            cname = ""
        else:
            cname=categorys[i]['categoryname']

        cid = categorys[i]['categoryid']
        qs1 = Videoinfo.objects.filter(vid=vid)
        vinfo = qs1.values()

        mycategory_data = {
           'categoryname' : cname,
           'categoryid' : cid,
           'videoid' : vid,
           'videotitle' : vinfo[0]['title'],
           'thumbnailurl' : vinfo[0]['thumbnailurl'],
           'videourl' : vinfo[0]['videourl']
        }
        mycategorys.append(mycategory_data)
        i = i + 1

    context = {
                'mycategorys' : mycategorys
            }

    return render(request, 'videolist/deletecategory.html', context)


def upload_v(request):
    return render(request, 'videolist/upload_vi.html')

def upload_video(request):
    if request.method == 'POST':
        httplib2.RETRIES = 1
        MAX_RETRIES = 10
        RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError, http.client.NotConnected,
            http.client.IncompleteRead, http.client.ImproperConnectionState,
            http.client.CannotSendRequest, http.client.CannotSendHeader,
            http.client.ResponseNotReady, http.client.BadStatusLine)

        RETRIABLE_STATUS_CODES = [500, 502, 503, 504]
        CLIENT_SECRETS_FILE = 'client_secrets.json'

        SCOPES = 'https://www.googleapis.com/auth/youtube.upload'
        API_SERVICE_NAME = 'youtube'
        API_VERSION = 'v3'

        VALID_PRIVACY_STATUSES = ('public', 'private', 'unlisted')

        def get_authenticated_service():
          flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
          credentials = flow.run_console()
          return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

        def initialize_upload(youtube, options):
          tags = None
          if options.keywords:
             tags = options.keywords.split(',')

          body=dict(
            snippet=dict(
                title=options.title,
                description=options.description,
                tags=tags,
                categoryId=options.category
            ),
            status=dict(
                privacyStatus=options.privacyStatus
            )
            )

          insert_request = youtube.videos().insert(
            part=','.join(body.keys()),
            body=body,
            media_body=MediaFileUpload(options.file, chunksize=-1, resumable=True)
          )

          resumable_upload(insert_request)

        def resumable_upload(request):
          response = None
          error = None
          retry = 0
          while response is None:
            try:
              print ('Uploading file...')
              status, response = request.next_chunk()
              if response is not None:
                if 'id' in response:
                  print ('Video id "%s" was successfully uploaded.' % response['id'])
                else:
                  exit('The upload failed with an unexpected response: %s' % response)
            except (HttpError, e):
              if e.resp.status in RETRIABLE_STATUS_CODES:
                error = 'A retriable HTTP error %d occurred:\n%s' % (e.resp.status,
                                                                     e.content)
              else:
                raise
            except (RETRIABLE_EXCEPTIONS, e):
              error = 'A retriable error occurred: %s' % e

            if error is not None:
              print (error)
              retry += 1
              if retry > MAX_RETRIES:
                exit('No longer attempting to retry.')

              max_sleep = 2 ** retry
              sleep_seconds = random.random() * max_sleep
              print ('Sleeping %f seconds and then retrying...' % sleep_seconds)
              time.sleep(sleep_seconds)


        if request.POST.get("videofile") == "":
            print("Please input video file")
        elif request.POST.get("videotitle") == "":
            print("Please input video title")
        elif request.POST.get("videodescription") == "":
            print("Please input video descirption")
        else:
            video_data = {
            'file' : request.POST.get("videofile"),
            'title' : request.POST.get("videotitle"),
            'description' : request.POST.get("videodescription"),
            'category' : '22',
            'keywords' : 'video upload test',
            'privacyStatus' : 'private'
            }

        youtube = get_authenticated_service()

        try:
            initialize_upload(youtube, video_data)
        except (HttpError, e):
            print ('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))
