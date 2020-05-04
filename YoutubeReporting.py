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
from mailchimp3 import Mailchimp
from gspread_pandas import Client

from YoutubeConfig import (
    VIDSTATS,
    VIDSTATSTITLES,
    CHANNELSTATS,
    DATA_DIRECTORY,
    WSFID,
    GOOGLE_SHEET,
)
from Secrets import MC_API

CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = [
    "https://www.googleapis.com/auth/yt-analytics.readonly",
    "https://www.googleapis.com/auth/youtube.readonly",
]
API_SERVICE_NAME = "youtubeAnalytics"
API_VERSION = "v2"


def get_authenticated_service():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_console()
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)


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


def get_mc_data(campaign, client):
    report = client.reports.get(campaign)
    df = pd.DataFrame(
        index=[campaign],
        data={
            "Title": report["campaign_title"],
            "Unsubscribed": report["unsubscribed"],
            "Send Time": report["send_time"],
            "Recipients": report["emails_sent"],
            "Opens": report["opens"].unique_opens,
            "Open Rate": report["opens"].open_rate,
            "Clicks": report["clicks"].clicks_total,
            "Click Rate": report["clicks"].click_rate,
        },
    )

    return df


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
    mc_client = Mailchimp(mc_api=MC_API)
    campaigns = []
    vid_ids = []
    campaign = input("Enter campaign ID: ")
    while campaign != "":
        campaigns.append(campaign)
        vid_ids.append(input("Enter video ID: "))
        campaign = input("Enter campaign ID: ")
    mcdf = pd.DataFrame()
    for campaign in campaigns:
        mcdf = pd.concat([mcdf, get_mc_data(campaign, mc_client)])

    mc_times = pd.to_datetime(mcdf["Send Time"])
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


if __name__ == "__main__":
    main()
