<h1>Python Script to download youtube videos based on data retrieved from google sheets and upload the videos to Cloud Storage.</h1>

Requirements: Python 3.6 or more and pip.<br>
Dependencies: youtube-dl, gspread, re, google_cloud_storage can be installed through pip.<br>
External dependecies: ffmpeg to process the videos need to be installed manually follow the instruction in the link https://www.wikihow.com/Install-FFmpeg-on-Windows. <br>
GCP requirement: Enable Google Drive Api and cloud storage api. Use the gmail adrress or google account in which the source spreadsheet is situated. <br>
		 Create a storage bucket before running the code. <br>
		 After enabling the APIs create a service account and download the json file. <br>
		 Copy the credentials in the json file and paste it in the config.json file.<br>
		 Change the gsheet name and the bucket name also in the config.json file.<br>

Note: In some cases due to resource restrictions the youtube videos will get downloaded but may not get uploaded in that case just rerun the script the videos will not download again but it will get uploaded to the storage.


