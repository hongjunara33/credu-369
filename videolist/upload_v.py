import requests

from isodate import parse_duration

from django.conf import settings
from django.shortcuts import render
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



# Create your views here.
def upload_v(request):

    httplib2.RETRIES = 1
    MAX_RETRIES = 10
    RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError, http.client.NotConnected,
      http.client.IncompleteRead, http.client.ImproperConnectionState,
      http.client.CannotSendRequest, http.client.CannotSendHeader,
      http.client.ResponseNotReady, http.client.BadStatusLine)

    RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

    CLIENT_SECRETS_FILE = "client_secrets.json"
    YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"

    MISSING_CLIENT_SECRETS_MESSAGE = """
    WARNING: Please configure OAuth 2.0

    To make this sample run you will need to populate the client_secrets.json file
    found at:

       %s

    with information from the API Console
    https://console.developers.google.com/

    For more information about the client_secrets.json file format, please visit:
    https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
    """ % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                       CLIENT_SECRETS_FILE))

    VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")
    print('test-1')

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
            part='.'.join(body.keys()),
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

    if request.method == 'POST':
        video_url = 'https://www.googleapis.com/youtube/v3/videos'

        args = []
        args = ','.join(request.POST['video-file'])
        args = ','.join(request.POST['video-title'])
        args = ','.join(request.POST['video-descirption'])
        args = ','.join('22')
        args = ','.join('test')
        args = ','.join('public')


        if not os.path.exists(request.POST['video-file']):
            exit("Please specify a valid file using the --file= parameter.")

        youtube = get_authenticated_service()
        try:
            initialize_upload(youtube, args)
        except (HttpError, e):
            print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))

        return render(request, 'videolist/upload_vi.html')
