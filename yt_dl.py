#Python script to download youtube videos based on data retrieved from a google spreadsheet and upload the videos to the Google Cloud Storage.

import youtube_dl
import os
import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint 
from google.cloud import storage 
from openpyxl import load_workbook
import json

#Open config file and extract values.
with open('config.json') as config_file:
    data = json.load(config_file)
gsheet = data['gsheet']
bucket = data['bucket']
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'config.json'

#Acess google sheets for data source to download videos.
scope = ['https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('config.json',scope)
client = gspread.authorize(creds)
sheet = client.open(gsheet).sheet1
 #importing excel sheet
sr = sheet.col_values(1)
sk = len(sr) + 1

#function to download videos and write it to the status file.
def download_video(link,start,dur): 
    if not os.path.exists('downloaded_videos'):
        os.makedirs('downloaded_videos')
    command = 'youtube-dl -ciw -o "/downloaded_videos/%(title)s-%(id)s.%(epoch)s.%(ext)s" --external-downloader ffmpeg --external-downloader-args  "-ss '+ start +' -t ' + dur + '"'" -f best " + '"' + link + '"' #command that will download the videos
    os.system(command)
    f.write(link + "\n")
    #print(command)
      
#Defining variables for cloud storage access.
storage_client = storage.Client()
dir(storage_client)
filenames = os.listdir("downloaded_videos")
my_bucket = storage_client.get_bucket(bucket)

#Function to upload the downloaded files.
def upload_to_bucket(blob_name, file_path, bucket_name):
    try:
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(file_path)
        return True
    except Exception as e:
        print(e)
        return False      

#Opening status text file and assigning permissions.
f = open("status.txt", "a")
fr = open("status.txt", "r")
frd = fr.readlines()
frd1 = ''.join(frd)
r = "t="

#For loop to iterate and retrieve values from the google spreadsheet.             
for r in range(2,sk):
    row = sheet.row_values(r)
    #a = r       
    #b = [str(a) for a in r]
    #[link,dur] = b
    link = row[0]
    dur = row[1]
    if ',' in dur:
        dur = dur.replace(',','')
        [mi,se,kt] = dur
        ht = se + kt
        ht = int(ht)
        mi = int(mi)
        mi = mi * 60
        mi = mi + ht
        mi = str(mi)
        dur = mi
    else:
        dur = dur
    if "t=" not in link: link = link + "&?t=0m00s"
    print(link)       
    if link in frd1:
        print("Already Downloaded")
    else: 
        m = link.split('t=')[1]
        q = m.isdigit()
        
        if q == False:
            s = re.findall(r'\d+', m)
            [min,sec] = s
            d = int(min)
            e = int(sec)
            time = d*60+e
            start = str(time)
        else :
            time = m
            start = str(time)
        download_video(link,start,dur)        
                      
#For loop to iterate videos in the directory and upload them to google cloud storage bucket.
file_path = ("downloaded_videos")
try:
    for file_name in filenames:
        upload_to_bucket(file_name, os.path.join(file_path, file_name), bucket )
        #print(file_name)
except:
    print("No Upload")
#file Closing    
f.close()
fr.close()

# End of program