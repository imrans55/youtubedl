import os
from core import CLI, CVAT_API_V1
from definition import parser
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import requests
import json

gsheet = "REQ-481"
config = "/home/cred.json"
user = "req481"
pwd = "admin481"

mount = "/home/mounts/req-481"
host = "91.227.139.201"
port = "8050"



def upload_task(gsheet, config, user, pwd, mount, host, port):
    
    files = os.listdir(mount)
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = config
    scope = ['https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(config, scope)
    client = gspread.authorize(creds)
    sheet = client.open(gsheet).sheet1
    stat = sheet.col_values(8)
    #print(stat)
    def my_join(tpl):
        return ' imgs/{}/'.format(dirs).join(x if isinstance(x, str) else my_join(x) for x in tpl)
    
    count = 2
    for dirs in files:
        
        if dirs in stat:
            print("Already Added to CVAT")
        else:
            disk = 'imgs/' + dirs
            fol = os.listdir(disk)
            k = my_join(fol)
            #print(k)
            l = 'imgs/' + dirs + '/' + k
            #print(l)
            command  = "python cli.py --server-host {} --server-port {} --auth {}:{} create {}  --labels /home/mounts/req-481/labels.json share {}" .format(host, port, user, pwd, dirs, l)
            #print(command)
            os.system(command)
            
            cnt = str(count)
            
            count = count + 1
            credns = [user, pwd]
            with requests.Session() as session:
                api = CVAT_API_V1('%s:%s' % (host, port), False)
                cli = CLI(session, api, credns)
                f = CLI.tasks_list(cli, False)
            l = json.dumps(f)
            q = json.loads(l)
            y = str(l[56])
            k = str(l[57])
            e = str(l[58])
            e1 = str(l[59])
            e2 = str(l[60])
            e3 = str(l[61])
            u = y + k + e + e1 + e2 + e3
            cell = "Task Created Task Id:" + u 
            print(cell)
            sheet.update_acell('H'+ cnt, file)
            sheet.update_acell('I'+ cnt , cell)
            #print (u)

   
upload_task(gsheet, config, user, pwd, mount, host, port)