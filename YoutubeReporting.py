#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 11:40:20 2019

@author: DannySwift
"""

import googleapiclient
import google.oauth2.credentials
import google_auth_oauthlib.flow
import os
import pandas as pd
import re
import matplotlib.pyplot as plt
import seaborn as sns

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow

from YoutubeConfig import VIDSTATS, VIDSTATSTITLES, CHANNELSTATS, DATA_DIRECTORY, WSFID

CLIENT_SECRETS_FILE = 'client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/yt-analytics.readonly',
          'https://www.googleapis.com/auth/youtube.readonly']
API_SERVICE_NAME = 'youtubeAnalytics'
API_VERSION = 'v2'

def get_authenticated_service():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_console()
    return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

def get_vid_data(vidID, start, end, service):
    itst = service.reports().query(
            ids='channel==' + WSFID,
            startDate=start,
            endDate=end,
            metrics='views',
            dimensions='insightTrafficSourceType',
            filters='video=={}'.format(vidID)
            ).execute()
    itst = {r[0]: r[1] for r in itst['rows']}
    
    df = pd.DataFrame.from_dict(itst, orient='index', columns='views')
    views = df.views.sum()
    channel_views = df.loc['YT_CHANNEL', 'views']
    notifications = df.loc['NOTIFICATION', 'views']
    suggested = itst['RELATED_VIDEO']
    
    sub_deets = service.reports().query(
            ids='channel==' + WSFID,
            startDate=start,
            endDate=end,
            metrics='views',
            dimensions='insightTrafficSourceDetail',
            filters='video=={};insightTrafficSourceType==SUBSCRIBER'.format(vidID),
            maxResults=10
            ).execute()
    sub_deets = {r[0]: r[1] for r in sub_deets['rows']}
    home = sub_deets['what-to-watch']
    subscritions = sub_deets['/my_subscriptions']
    


def load_data(directory):
    data = pd.DataFrame(columns=['date', 'video_title'])
    files = os.listdir(directory)
    for file in files:
        for stat in VIDSTATSTITLES:
            if re.search('.*chart_{}.csv'.format(stat), file):
                data = data.merge(pd.read_csv(directory + os.sep + file), 
                                  how='outer', on=['date', 'video_title'])
        if re.search('.*VidPub.csv', file):
            dates = pd.read_csv(directory + os.sep + file)
            dates['date'] = dates['date'].apply(lambda x: pd.to_datetime(x).strftime('%Y-%m-%d')).astype('str')
    
    return data, dates

def graph_vid(df, dates, var):
    g = sns.lineplot(x='date', y=var, data=df, hue='video_title')
    labels = df.date.unique()
    labels = [str(dates[dates['date'].str.contains(d)]['name'])[2:] if 
              dates['date'].str.contains(d).any() else '' for d in labels]
    for _, d in dates.iterrows():
        g.axvline(d['date'])
    with sns.plotting_context(font_scale=0.5):
        g.set_xticklabels(labels, rotation=90)
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.show()


def main():
    directory = input("Enter the folder containing the reporting data: ")
    directory = DATA_DIRECTORY + os.sep + directory
    data, dates = load_data(directory)
    for var in VIDSTATS:
        graph_vid(data, dates, var)

def main2():
    youtube_analytics = get_authenticated_service()


if __name__ == '__main__':
    main()