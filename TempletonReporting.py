#%%
import os
import pandas as pd

from YoutubeReporting import service, get_ids, get_views_as_of, get_comments

#%%
programs = pd.read_csv("TempletonPrograms.csv")
recent_programs = programs.loc[programs['Release Date'] >= "2024-06-30"]
all_big_ideas_programs = get_ids()

#%%
for end_date in ["2022-01-01", "2024-01-01", "2024-09-30"]:
    print(f"BI total views as of {end_date}: {get_views_as_of(all_big_ideas_programs, service, end_date)}")
    emw = 0
    for id in all_big_ideas_programs:
        try:
            emw +=  service.reports().query(
                metrics='estimatedMinutesWatched', 
                ids='channel==MINE', 
                filters='video==' + id, 
                startDate="2008-01-01", 
                endDate=end_date
                ).execute()['rows'][0][0]
        except:
            print(f"Error with {id}")
    print(f"BI total minutes watched as of {end_date}: {emw}")

#%%
v = 0
for id in programs.ID:
        try:
            v +=  service.reports().query(
                metrics='views', 
                ids='channel==MINE', 
                filters='video==' + id, 
                startDate="2008-01-01", 
                endDate="2024-09-30"
                ).execute()['rows'][0][0]
        except:
            print(f"Error with {id}")
print(f"All grant period programs views as of 2024-09-30: {v}")

v = 0
for id in recent_programs.ID:
        try:
            v +=  service.reports().query(
                metrics='views', 
                ids='channel==MINE', 
                filters='video==' + id, 
                startDate="2008-01-01", 
                endDate="2024-09-30"
                ).execute()['rows'][0][0]
        except:
            print(f"Error with {id}")
print(f"All recent programs views as of 2024-09-30: {v}")

#%%
files = os.listdir("BigIdeasComments")
for _, program in programs.iterrows():
    if program.Title + ".txt" in files:
        print(f"Skipping {program.Title}")
        continue
    else:
        print(f"Getting {program.Title}")
        comments = get_comments(service, program.ID)
        with open("BigIdeasComments" + os.sep + program.Title + ".txt", "w") as f:
            for comment in comments:
                f.write(comment)
                f.write("\n")

# %%
