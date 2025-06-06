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
import re
import requests
import matplotlib.pyplot as plt
import pickle
import urllib

#%%
from bs4 import BeautifulSoup
from datetime import datetime
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow

# from gspread_pandas import Client

from YoutubeConfig import (
    API,
    VIDSTATS,
    VIDSTATSTITLES,
    CHANNELSTATS,
    DATA_DIRECTORY,
    WSFID,
    COOL_JOBS,
    CJID,
    YDEID,
    BIG_IDEAS_URL,
    KAVLI_URL,
    # GOOGLE_SHEET,
    BI19,
    BI21,
    BI61300,
    BI62375,
    LIVE22
)

CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = [
    "https://www.googleapis.com/auth/yt-analytics.readonly",
    "https://www.googleapis.com/auth/youtube.readonly",
]
API_SERVICE_NAME = "youtubeAnalytics"
API_VERSION = "v2"

#%%
def get_authenticated_service():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_console()
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)


#%% Not getting all of them...
def get_all_videos_in_channel():
    username = "worldsciencefestival"
    url = f"https://www.youtube.com/user/{username}/videos"
    page = requests.get(url).content
    data = str(page).split(" ")
    item = 'href="/watch?'
    vids = [
        line.replace('href="/watch?v=', "")[:-1] for line in data if item in line
    ]  # list of all videos listed twice

    return vids


def get_titles_from_wsf_html(filename):
    with open(filename) as f:
        soup = BeautifulSoup(f, "html.parser")
    return [x.getText() for x in soup.find_all(attrs={"class: video-title"})]


def get_yt_id_from_title(title):
    html = urllib.request.urlopen(
        f"https://www.youtube.com/results?search_query={urllib.parse.quote_plus(title)}"
    )
    return re.findall(r"watch\?v=(\S{11})", html.read().decode())


#%%
def get_vid_data(vidID, start, end, service):
    itst = (
        service.reports()
        .query(
            ids="channel==" + WSFID,
            startDate=start,
            endDate=end,
            metrics="views",
            dimensions="insightTrafficSourceType",
            filters="video=={}".format(vidID),
        )
        .execute()
    )

    views = 0
    for r in itst["rows"]:
        views += r[1]

    data_dict = {r[0]: r[1] for r in itst["rows"]}
    data_dict["Views"] = views

    # df = pd.DataFrame.from_dict(itst, orient='index', columns=vidID)
    # views = df.views.sum()
    # channel_views = df.loc['YT_CHANNEL', 'views']
    # notifications = df.loc['NOTIFICATION', 'views']
    # suggested = itst['RELATED_VIDEO']

    sub_deets = (
        service.reports()
        .query(
            ids="channel==" + WSFID,
            startDate=start,
            endDate=end,
            metrics="views",
            sort="-views",
            dimensions="insightTrafficSourceDetail",
            filters="video=={};insightTrafficSourceType==SUBSCRIBER".format(vidID),
            maxResults=25,
        )
        .execute()
    )
    for r in sub_deets["rows"]:
        data_dict[r[0]] = r[1]
    df = pd.DataFrame(data_dict, index=[vidID])

    return df


#%%
def get_social_data(vidID, start, end, service):
    externals = (
        service.reports()
        .query(
            ids="channel==" + WSFID,
            startDate=start,
            endDate=end,
            metrics="views",
            sort="-views",
            dimensions="insightTrafficSourceDetail",
            filters="video=={};insightTrafficSourceType==EXT_URL".format(vidID),
            maxResults=25,
        )
        .execute()
    )
    fb = 0
    insta = 0
    twitter = 0
    for r in externals["rows"]:
        if "facebook" in r[0].lower():
            fb += r[1]
        elif "insta" in r[0].lower():
            insta += r[1]
        elif "twitter" in r[0].lower():
            twitter += r[1]

    return pd.DataFrame(
        index=[vidID], data={"Facebook": fb, "Instagram": insta, "Twitter": twitter}
    )


#%%
def get_demo_data(vidID, start, end, service):
    demographics = (
        service.reports()
        .query(
            ids="channel==" + WSFID,
            startDate=start,
            endDate=end,
            metrics="viewerPercentage",
            dimensions="ageGroup,gender",
            filters="video=={}".format(vidID),
            maxResults=25,
        )
        .execute()
    )

    data_dict = {r[0] + r[1]: r[2] for r in demographics["rows"]}
    df = pd.DataFrame(data_dict, index=[vidID])

    return df


#%%
def yt_data_from_wsf(playlist, pages):
    views = 0
    for i in range(pages):
        url = f"https://www.worldsciencefestival.com/video/video-library/page/{i+1}/?topic&playlist={playlist}&meta"
        soup = BeautifulSoup(requests.get(url).content, "html.parser")
        big_ideas = soup.find_all(attrs={"class": "video-category-duration"})
        for div in big_ideas:
            s = div.getText().split(" ")[0].replace(",", "")
            if ":" not in s and len(s) > 0:
                views += int(s)

    return views


def fetch_all_data():
    views = {}
    v = 0
    bi = get_ids(BIG_IDEAS_URL)
    for id in bi:
        vid = service.reports().query(metrics='views', ids='channel==MINE', filters='video==' + id, startDate="2008-02-01", endDate=datetime.today().strftime("%Y-%m-%d")).execute()['rows'][0][0]
        v += vid
    views["Big Ideas"] = v

    v = 0 
    k = get_ids(KAVLI_URL)
    for id in k:
        vid = service.reports().query(metrics='views', ids='channel==MINE', filters='video==' + id, startDate="2008-02-01", endDate=datetime.today().strftime("%Y-%m-%d")).execute()['rows'][0][0]
        v += vid
    views["Kavli"] = v
    # views["Big Ideas"] = yt_data_from_wsf(45075, 6)
    # views['Cool Jobs'] = yt_data_from_wsf(64848, 2)
    # views["Your Daily Equation"] = yt_data_from_wsf(64767, 2)
    # views["Kavli"] = yt_data_from_wsf(34438, 1)

    #views["Big Ideas 2019"] = 0
    #for div in BeautifulSoup(
    #    requests.get(
    #        "https://www.worldsciencefestival.com/video/video-library/page/1/?topic&playlist=45075&meta"
    #    ).content,
    #    "html.parser",
    #).find_all(attrs={"class": "video-category-duration"})[:18]:
    #    views["Big Ideas 2019"] += int(div.getText().split(" ")[0].replace(",", ""))

    # with open("youtube.pkl", "rb") as f:
    #    yt = pickle.load(f)

    #views["Your Daily Equation"] = get_yt_views(YDEID, yt)
    #views["Cool Jobs"] = get_yt_views(CJID, yt)

    return views


#%%
def get_yt_views(playlistId, service):
    """ vids = service.reports().query(
        ids="channel==" + WSFID,
        startDate="2008-01-01",
        endDate=datetime.today().strftime("%Y-%m-%d"),
        metrics="views,estimatedMinutesWatched",
        playlist="PLKy-B3Qf_RDVL6Z_CmgKf0tAbpXTua9mV",
    ) """
    res = (
        service.playlistItems()
        .list(part="snippet", playlistId=playlistId, maxResults="50")
        .execute()
    )

    nextPageToken = res.get("nextPageToken")
    while "nextPageToken" in res:
        nextPage = (
            service.playlistItems()
            .list(part="snippet", playlistId=playlistId, maxResults="50", pageToken=nextPageToken)
            .execute()
        )
        res["items"] = res["items"] + nextPage["items"]

        if "nextPageToken" not in nextPage:
            res.pop("nextPageToken", None)
        else:
            nextPageToken = nextPage["nextPageToken"]

    ids = []
    for item in res["items"]:
        ids.append(item["snippet"]["resourceId"]["videoId"])

    views = 0
    vids = service.videos().list(part="statistics", id=ids).execute()
    for vid in vids["items"]:
        views += int(vid["statistics"]["viewCount"])

    return views

def get_views_after_release(service, video, days=30):
    youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=API)
    snippet = youtube.videos().list(part='snippet', id=video).execute()
    published = snippet['items'][0]['snippet']['publishedAt'][:10]
    end = (pd.to_datetime(published) + pd.Timedelta(days=days)).strftime('%Y-%m-%d')
    views = service.reports().query(metrics='views', ids='channel==MINE', dimensions='day', filters='video==' + video, startDate=published, endDate=end).execute()
    
    return views['rows']



#%%
def load_data(directory):
    data = pd.DataFrame(columns=["date", "video_title"])
    files = os.listdir(directory)
    for file in files:
        for stat in VIDSTATSTITLES:
            if re.search(".*chart_{}.csv".format(stat), file):
                data = data.merge(
                    pd.read_csv(directory + os.sep + file), how="outer", on=["date", "video_title"]
                )
        if re.search(".*VidPub.csv", file):
            dates = pd.read_csv(directory + os.sep + file)
            dates["date"] = (
                dates["date"].apply(lambda x: pd.to_datetime(x).strftime("%Y-%m-%d")).astype("str")
            )

    return data, dates


def graph_vid(df, dates, var):
    g = sns.lineplot(x="date", y=var, data=df, hue="video_title")
    labels = df.date.unique()
    labels = [
        str(dates[dates["date"].str.contains(d)]["name"])[2:]
        if dates["date"].str.contains(d).any()
        else ""
        for d in labels
    ]
    for _, d in dates.iterrows():
        g.axvline(d["date"])
    with sns.plotting_context(font_scale=0.5):
        g.set_xticklabels(labels, rotation=90)
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.0)
    plt.show()


def main():
    campaigns = []
    vid_ids = []
    campaign = input("Enter campaign ID: ")
    while campaign != "":
        campaigns.append(campaign)
        vid_ids.append(input("Enter video ID: "))
        campaign = input("Enter campaign ID: ")

    start = mc_times.max()
    end = start + pd.Timedelta(days=14)
    if end > pd.Timestamp.today():
        end = pd.Timestamp.today()
        start = end - pd.Timedelta(days=14)
    start = start.strftime("%Y-%m-%d")
    end = end.strftime("%Y-%m-%d")

    youtube_analytics = get_authenticated_service()
    new_vids = pd.DataFrame()
    social = pd.DataFrame()
    demos = pd.DataFrame()
    for vid in vid_ids:
        new_vids = pd.concat([new_vids, get_vid_data(vid, youtube_analytics)])
        social = pd.concat([social, get_social_data(vid, youtube_analytics)])
        demos = pd.concat([demos, get_demo_data(vid, youtube_analytics)])

    new_vids = new_vids.rename(
        {
            "/my_subscriptions": "Subscribers",
            "YT_CHANNEL": "Channel Page",
            "NOTIFICATION": "Notifications",
            "SUBSCRIBER": "Views from Home",
            "RELATED_VIDEO": "Suggested Videos",
        },
        axis=1,
    )
    new_vids = new_vids.drop(
        [
            "my-history",
            "ANNOTATION",
            "END_SCREEN",
            "EXT_URL",
            "NO_LINK_OTHER",
            "PLAYLIST",
            "PP",
            "YT_OTHER_PAGE",
            "YT_PLAYLIST_PAGE",
            "YT_SEARCH",
            "trend",
            "watch-later",
            "what-to-watch",
        ],
        axis=1,
    )

    top5 = (
        youtube_analytics.reports()
        .query(
            dimensions="video",
            metrics="views",
            ids="channel==UCShHFwKyhcDo3g7hr4f1R8A",
            maxResults=5,
            sort="-views",
            startDate=start,
            endDate=end,
        )
        .execute()["rows"]
    )
    top5 = pd.DataFrame(top5, columns=["id", "views"])
    top5 = top5.set_index("id")
    top5demos = pd.DataFrame()
    top5soc = pd.DataFrame()
    for vid in top5.index:
        df = get_vid_data(vid, start, end, youtube_analytics)
        df["id"] = vid
        top5 = top5.combine_first(df)
        top5demos = pd.concat([top5demos, get_demo_data(vid, start, end, youtube_analytics)])
        top5soc = pd.concat([top5soc, get_social_data(vid, start, end, youtube_analytics)])

    top5 = top5.rename(
        {
            "/my_subscriptions": "Subscribers",
            "YT_CHANNEL": "Channel Page",
            "NOTIFICATION": "Notifications",
            "SUBSCRIBER": "Views from Home",
            "RELATED_VIDEO": "Suggested Videos",
        },
        axis=1,
    )
    top5 = top5.drop(
        [
            "my-history",
            "ANNOTATION",
            "END_SCREEN",
            "EXT_URL",
            "NO_LINK_OTHER",
            "PLAYLIST",
            "PP",
            "YT_OTHER_PAGE",
            "YT_PLAYLIST_PAGE",
            "YT_SEARCH",
            "trend",
            "watch-later",
            "what-to-watch",
            "id",
        ],
        axis=1,
    )

    gsp_client = Client()
    sheet = gsp_client.open(GOOGLE_SHEET)
    template = sheet.sheet_to_df(sheet="Template")
    today = pd.Timestamp.today().strftime("%B %d, %Y")
    sheet.df_to_sheet(template, sheet=today)
    sheet.df_to_sheet(mcdf.T, sheet=today, start=(2, 6), index=False)
    sheet.df_to_sheet(social.T, sheet=today, start=(2, 17), index=False)
    sheet.df_to_sheet(new_vids.T, sheet=today, start=(2, 21), index=False)
    sheet.df_to_sheet(top5soc.T, sheet=today, start=(7, 17), index=False)
    sheet.df_to_sheet(top5.T, sheet=today, start=(7, 21), index=False)
    sheet.df_to_sheet(top5demos.T, sheet=today, start=(7, 28), index=False)


#%%
#service = get_authenticated_service()

#%%
def get_ids(url=BIG_IDEAS_URL):
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    pages = [x.contents[0]['href'] for x in soup.find_all(attrs={"class": "video-title"})]
    ids = []
    for page in pages:
        soup = BeautifulSoup(requests.get(page).content, "html.parser")
        try:
            id = soup.find_all("meta", attrs={"property":"og:video"})[0]["content"].split("/")[-1]
        except:
            print(page)
            continue
        ids.append(id)
    
    return ids
# %%
def update_grant_level_data():
    today = pd.Timestamp.today().strftime("%Y-%m-%d")
    bi21 = pd.DataFrame()
    for v in BI21:
        print(v)
        sn = service.reports().query(metrics='views', dimensions='day', ids='channel==MINE', filters='video=='+v, startDate='2008-01-01', endDate=today).execute()
        bi21 = pd.concat([bi21, pd.DataFrame({BI21[v]: [x[1] for x in sn['rows']]})], axis=1)

    bi21.to_csv('BI21.csv', index=False)

    bi61300 = pd.DataFrame()
    for v in BI61300:
        sn = service.reports().query(metrics='views', dimensions='day', ids='channel==MINE', filters='video=='+v, startDate='2008-01-01', endDate=today).execute()
        bi61300 = pd.concat([bi61300, pd.DataFrame({BI61300[v]: [x[1] for x in sn['rows']]})], axis=1)

    bi61300.to_csv('BI61300.csv', index=False)

    bi62375 = pd.DataFrame()
    for v in BI62375:
        sn = service.reports().query(metrics='views', dimensions='day', ids='channel==MINE', filters='video=='+v, startDate='2008-01-01', endDate=today).execute()
        bi62375 = pd.concat([bi62375, pd.DataFrame({BI62375[v]: [x[1] for x in sn['rows']]})], axis=1)

    bi62375.to_csv('BI62375.csv', index=False)


    live22 = pd.DataFrame()
    for v in LIVE22:
        sn = service.reports().query(metrics='views', dimensions='day', ids='channel==MINE', filters='video=='+v, startDate='2008-01-01', endDate=today).execute()
        live22 = pd.concat([live22, pd.DataFrame({LIVE22[v]: [x[1] for x in sn['rows']]})], axis=1)
    live22.to_csv('live22.csv', index=False)


    bi19 = pd.DataFrame()
    for v in BI19:
        sn = service.reports().query(metrics='views', dimensions='day', ids='channel==MINE', filters='video=='+v, startDate='2008-01-01', endDate=today).execute()
        bi19 = pd.concat([bi19, pd.DataFrame({BI19[v]: [x[1] for x in sn['rows']]})], axis=1)

    bi19_top8 = bi19[['Beyond Higgs', 'Rethinking Thinking', 'The Richness of Time', 'Intelligence Without Brains', 'Physics in the Dark', 'The Reality of Reality', 'Revealing the Mind', 'Loose Ends']].copy()
    bi19_top8['Beyond Higgs'] = bi19_top8['Beyond Higgs'].shift(-4)
    bi19_top8['Rethinking Thinking'] = bi19_top8['Rethinking Thinking'].shift(-9)
    bi19_top8['The Richness of Time'] = bi19_top8['The Richness of Time'].shift(-8)
    bi19_top8['Intelligence Without Brains'] = bi19_top8['Intelligence Without Brains'].shift(-10)
    bi19_top8['Physics in the Dark'] = bi19_top8['Physics in the Dark'].shift(-2)
    bi19_top8['The Reality of Reality'] = bi19_top8['The Reality of Reality'].shift(-9)
    bi19_top8['Loose Ends'] = bi19_top8['Loose Ends'].shift(-12)
    bi19_top8.to_csv("bi19_top8.csv")

    #avgView31 = bi21.iloc[31].dropna().sum() / bi21.iloc[31].dropna().shape[0]
    #avgView5 = bi21.iloc[5].dropna().sum() / bi21.iloc[5].dropna().shape[0]


    bi212 = pd.DataFrame()
    for v in BI21:
        sn = service.reports().query(metrics='estimatedMinutesWatched', dimensions='day', ids='channel==MINE', filters='video=='+v, startDate='2008-01-01', endDate=today).execute()
        bi212 = pd.concat([bi212, pd.DataFrame({f'{BI21[v]} minutes': [x[1] for x in sn['rows']]})], axis=1)

#%%)
def get_average_view_duration(vids, duration, service):
    youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=API)
    v = 0
    emw = 0
    for video in vids:
        snippet = youtube.videos().list(part='snippet', id=video).execute()
        published = snippet['items'][0]['snippet']['publishedAt'][:10]
        end = (pd.to_datetime(published) + pd.Timedelta(days=duration)).strftime('%Y-%m-%d')
        response = service.reports().query(metrics='views,estimatedMinutesWatched', ids='channel==MINE', filters='video==' + video, startDate=published, endDate=end).execute()
        v += response['rows'][0][0]
        emw += response['rows'][0][1]
    
    return emw / v
# %%
def get_agg_geo_views(vids, service, start='2008-01-01', end=None):
    if not end:
        end = pd.Timestamp.today().strftime("%Y-%m-%d")
    agg = {}
    for vid in vids:
        r = service.reports().query(
            metrics='views', 
            dimensions='country', 
            ids='channel==MINE', 
            filters='video=='+vid, 
            startDate=start, 
            endDate=end
            ).execute()
        for row in r['rows']:
            agg.setdefault(row[0], 0)
            agg[row[0]] += int(row[1])
    df = pd.DataFrame({'country': agg.keys(), 'views': agg.values()})
    total = df.views.sum()
    df['percent'] = df.views / total * 100
    
    return df.sort_values('views')

def get_agg_demo_views(vids, service, start='2008-01-01', end=None):
    if not end:
        end = pd.Timestamp.today().strftime("%Y-%m-%d")
    df = pd.DataFrame()
    for vid in vids:
        ndf = get_demo_data(vid, start=start, end=end, service=service)
        ndf *= service.reports().query(metrics='views',ids='channel==MINE', filters='video==' + vid, startDate=start, endDate=end).execute()['rows'][0][0]
        df = pd.concat([df, ndf])
    
    return df

    
def get_views_as_of(vids, service, end, start="2008-02-01"):
    v = 0
    for vid in vids:
        v += service.reports().query(
            metrics='views',
            ids='channel==MINE',
            filters='video==' + vid,
            startDate=start,
            endDate=end
        ).execute()['rows'][0][0]
    
    return v

#%%
def get_all_vids():
    vids = []
    youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=API)
    uploads = youtube.channels().list(part='contentDetails', id=WSFID).execute()['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    res = youtube.playlistItems().list(playlistId=uploads, part='id', maxResults=50).execute()
    nextPageToken = res['nextPageToken']
    for item in res['items']:
        vids.append(item['etag'])    
    while 'nextPageToken' in res:
        res = youtube.playlistItems().list(playlistId=uploads, part='id', maxResults=50, pageToken=nextPageToken).execute()
        print(len(vids))
        for item in res['items']:
            vids.append(item['etag'])
        if len(vids) > 2000:
            break
    
    return vids
# %%
def get_shorts(vids, duration, service):
    youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=API)
    v = []
    for video in vids.values:
        cd = youtube.videos().list(part='contentDetails', id=video[0]).execute()
        dur = cd['items'][0]['contentDetails']['duration'][2:]
        dur = dur.split("M")[0]
        try:
            dur = int(dur)
            if dur < duration:
                v.append(video[0])
        except:
            continue
    
    return v

#%%
# Returns all replies the top-level comment has: 
# topCommentId = it's the id of the top-level comment you want to retrieve its replies.
# replies = array of replies returned by this function. 
# token = the comments.list might return moren than 100 comments, if so, use the nextPageToken for retrieve the next batch of results.
def getAllTopLevelCommentReplies(youtube, topCommentId, replies, token): 
    replies_response=youtube.comments().list(part='snippet',
                                               maxResults=100,
                                               parentId=topCommentId,
                                               pageToken=token).execute()

    for item in replies_response['items']:
        # Append the reply's text to the 
        replies.append(item['snippet']['textDisplay'])

    if "nextPageToken" in replies_response: 
        return getAllTopLevelCommentReplies(topCommentId, replies, replies_response['nextPageToken'])
    else:
        return replies


def get_comments(youtube, video_id, comments=[], token=''):
    youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=API)

    # Stores the total reply count a top level commnet has.
    totalReplyCount = 0
    
    # Replies of the top-level comment might have.
    replies=[]

    video_response=youtube.commentThreads().list(part='snippet',
                                                videoId=video_id,
                                                pageToken=token).execute()
    for item in video_response['items']:
        comment = item['snippet']['topLevelComment']
        text = comment['snippet']['textDisplay']
        comments.append(text)

        # Get the total reply count: 
        totalReplyCount = item['snippet']['totalReplyCount']
        
        # Check if the total reply count is greater than zero, 
        # if so,call the new function "getAllTopLevelCommentReplies(topCommentId, replies, token)" 
        # and extend the "comments" returned list.
        if (totalReplyCount > 0): 
            comments.extend(getAllTopLevelCommentReplies(youtube, comment['id'], replies, None)) 
            
        # Clear variable - just in case - not sure if need due "get_comments" function initializes the variable.
        replies = []

    if "nextPageToken" in video_response: 
        return get_comments(youtube, video_id, comments, video_response['nextPageToken'])
    else:
        return comments
# %%
#service.reports().query(metrics="views", dimensions="liveOrOnDemand", ids="channel==MINE", filters='video==' + "5Iy5mt7F_N4", startDate="2008-01-01", endDate="2023-12-12").execute()
# %%
#fetch_all_data()
# %%
if __name__ == "__main__":
    service = get_authenticated_service()
    print(fetch_all_data())
# %%
