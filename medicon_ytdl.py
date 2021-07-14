import os
import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from google.cloud import storage
import shutil


gsheet = "REQ-481"
config = "/home/cred.json"
bucket =  "medicon-req-481"

def download_vids(gsheet, config, bucket):
    #Configurations
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = config
    scope = ['https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(config, scope)
    client = gspread.authorize(creds)
    sheet = client.open(gsheet).sheet1
    #importing excel sheet
    sr = sheet.col_values(1)
    sk = len(sr) + 1
    stat = sheet.col_values(7)
    #For loop to iterate the links in the sheet.
    for r in range(2,sk):
        row = sheet.row_values(r)
        link = row[0]
        dur = row[1]
        dl = r
        print(dl)
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
        if link in stat:
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
            dl_vds = 'imgs'
            #To download the frames or vidoes from the link
            if not os.path.exists('imgs'):
                os.makedirs('imgs')
            #downloading frames directly from youtube
            command = 'ffmpeg -ss {} -t {} -i "$(youtube-dl -f best --get-url {})" -vf fps=2 imgs/{}/img%04d.png'.format(start, dur, link, link)
            #command = 'youtube-dl -ciw -o "downloaded_videos/%(id)s.%(epoch)s.%(ext)s" --external-downloader ffmpeg --external-downloader-args  "-ss '+ start +' -t ' + dur + '"'" -f best " + '"' + link + '"' #command that will download the videos
            os.system(command)
            print(command)
            r = str(r)

            #update the sheet
            sheet.update_acell('G'+ r , link)

            storage_client = storage.Client()
            #function for upload the files to bucket
            def upload_to_bucket(blob_name, file_path, bucket_name):
                try:
                    bucket = storage_client.get_bucket(bucket_name)
                    blob = bucket.blob(blob_name)
                    blob.upload_from_filename(file_path)
                    return True
                except Exception as e:
                    print(e)
                    return False  


            # upload images to bucket    
            imgs = "imgs"    
            img_path = os.listdir("imgs")
            for dirs in img_path:   
                print(dirs) 
                wd = os.path.join(imgs, dirs) 
                dirst = os.listdir(wd)
                #print(dirst)
                for file in dirst:
                    #print(file) 
                    up = 'imgs/' + dirs + '/' + file
                    file_name = 'imgs/' + dirs + '/' + file
                    upload_to_bucket(file_name, up, bucket )

            shutil.rmtree(imgs)

download_vids(gsheet, config, bucket)