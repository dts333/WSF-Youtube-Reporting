#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 11:40:20 2019

@author: DannySwift
"""
#%%
import googleapiclient
import google.oauth2.credentials
import google_auth_oauthlib.flow
import os
import pandas as pd
import pygsheets
import re
import matplotlib.pyplot as plt
import seaborn as sns
import sys

#%%
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow

#%%
from YoutubeConfig import VIDSTATS, VIDSTATSTITLES, CHANNELSTATS, DATA_DIRECTORY, WSFID, SCOPES

#%%
CLIENT_SECRETS_FILE = 'client_secret.json'
API_SERVICE_NAME = 'youtubeAnalytics'
API_VERSION = 'v2'

#%%
def get_authenticated_service():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_console()
    return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

#%%
def get_vid_data(vidIDs, start, end, client):
    itst = client.reports().query(
            ids='channel==' + WSFID,
            startDate=start,
            endDate=end,
            metrics='views',
            dimensions='insightTrafficSourceType',
            filters='video=={}'.format(vidID)
            ).execute()
    
    views=0
    for r in itst['rows']: views += r[1]
    
    data_dict = {r[0]: r[1] for r in itst['rows']}
    
    df = pd.DataFrame.from_dict(itst, orient='index', columns=vidID)
    views = df.views.sum()
    channel_views = df.loc['YT_CHANNEL', 'views']
    notifications = df.loc['NOTIFICATION', 'views']
    suggested = itst['RELATED_VIDEO']
    
    sub_deets = client.reports().query(
            ids='channel==' + WSFID,
            startDate=start,
            endDate=end,
            metrics='views',
            dimensions='insightTrafficSourceDetail',
            filters='video=={};insightTrafficSourceType==SUBSCRIBER'.format(','.join(vidIDs)),
            maxResults=10
            ).execute()
    for r in sub_deets['rows']: data_dict[r[0]] = r[1]
    home = sub_deets['what-to-watch']
    subscriptions = sub_deets['/my_subscriptions']

#%%
def get_dates_titles(ids, client):
    response = client.videos().list(
        part='snippet',
        id=ids
    ).execute()['items']
    df = pd.DataFrame(np.array([
        vid['id'], 
        vid['snippet']['title'], 
        vid['snippet']['publishedAt'][:10]] 
        for vid in response
        ],
        columns=['id', 'title', 'start']
        ))
    df = df.set_index('id')
    
    return df

#%%
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

#%%
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
    args = sys.argv[1:]
    client = get_authenticated_service()
    new_vids = get_dates_titles(args, client)
    new_vids['start'] = pd.to_datetime(new_vids['start'], format='%Y-%b-%d')
    new_vids['end'] = new_vids['start'] + pd.DateOffset(weeks=2)
    start = new_vids['start'].min()
    end = new_vids['end'].min()

    top5 = client.reports().query(
            dimensions='video',
            metrics='views',
            ids='channel==' + WSFID,
            maxResults=5,
            sort='-views',
            startDate=start,
            endDate=end).execute()['rows']
    top5 = pd.DataFrame(top5, columns['id', 'views'])
    top5names = get_dates_titles(top5.id.values(), client)
    top5['names'] = top5names['names']
    top5['start'], top5['end'] = start, end
    top5 = top5.set_index('id')

    #Todo: Get Mailchimp data, form full df

    pgsc = pygsheets.authorize(service_file=CLIENT_SECRET_FILE)
    #make title
    spreadsheet = pgsc.create(title, template=TEMPLATE, folder=GFOLDER)
    spreadsheet[0].set_dataframe(df, (1,20))


if __name__ == '__main__':
    main()

#%%
