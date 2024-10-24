import os
import io
import pickle
import json
import argparse
import base64
import logging
import re
import time
import platform
from logging.handlers import RotatingFileHandler
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import crypto,uuid
import requests, tempfile
from datetime import datetime, timedelta
from cloudflare import CloudFlareHelper
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(thread)d %(funcName)s %(message)s')
try:
    file_handler = RotatingFileHandler('debug.log', maxBytes=(1024 * 1024 * 128), backupCount=1)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
except:
    pass

class DriverHelper(object):
    def get_file_info_v2(self, idx):
        idx = self.pre_process_link(idx)
        url = f"https://content.googleapis.com/drive/v2beta/files/{idx}?fields=alternateLink%2CcopyRequiresWriterPermission%2CcreatedDate%2Cdescription%2CdriveId%2CfileSize%2CiconLink%2Cid%2Clabels(starred%2C%20trashed)%2ClastViewedByMeDate%2CmodifiedDate%2Cshared%2CteamDriveId%2CvideoMediaMetadata(height%2Cwidth%2CdurationMillis)%2ClabelInfo%2CuserPermission(id%2Cname%2CemailAddress%2Cdomain%2Crole%2CadditionalRoles%2CphotoLink%2Ctype%2CwithLink)%2Cpermissions(id%2Cname%2CemailAddress%2Cdomain%2Crole%2CadditionalRoles%2CphotoLink%2Ctype%2CwithLink)%2Cparents(id)%2Ccapabilities(canMoveItemWithinDrive%2CcanMoveItemOutOfDrive%2CcanMoveItemOutOfTeamDrive%2CcanAddChildren%2CcanEdit%2CcanDownload%2CcanComment%2CcanMoveChildrenWithinDrive%2CcanRename%2CcanRemoveChildren%2CcanMoveItemIntoTeamDrive)%2Ckind&supportsTeamDrives=true&includeBadgedLabels=true&enforceSingleParent=true&key=AIzaSyC1eQ1xj69IdTMeii5r7brs3R90eck-m7k"
        payload = {}
        headers = {
            'authority': 'content.googleapis.com',
            'accept': '*/*',
            'accept-language': 'en',
            'dnt': '1',
            'referer': 'https://content.googleapis.com/static/proxy.html?usegapi=1&jsh=m%3B%2F_%2Fscs%2Fabc-static%2F_%2Fjs%2Fk%3Dgapi.gapi.en.t9z7VPsEMFg.O%2Fd%3D1%2Frs%3DAHpOoo8oD_5FQW3kT3ksWwmXIWvhhqbKdw%2Fm%3D__features__',
            'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
            'x-clientdetails': 'appVersion=5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F104.0.0.0%20Safari%2F537.36&platform=Win32&userAgent=Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F104.0.0.0%20Safari%2F537.36',
            'x-goog-authuser': '0',
            'x-goog-encode-response-if-executable': 'base64',
            'x-javascript-user-agent': 'google-api-javascript-client/1.1.0',
            'x-origin': 'https://drive.google.com',
            'x-referer': 'https://drive.google.com',
            'x-requested-with': 'XMLHttpRequest'
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        return response.text

    def create_driver_config(self, email):
        if not os.path.exists(self.get_dir('cached') + '/driver/email'):
            cred_file = self.get_dir('cached/driver/' + email) + "/cred.json"
            token = self.get_dir('cached/driver/' + email) + "/token.pickle"
            config_file = self.get_dir('cached/driver/' + email) + "/config.json"
            obj = {
                "SCOPES": [
                    "https://www.googleapis.com/auth/drive"
                ],
                "CRED_FILE": cred_file,
                "TOKEN_FILE": token,
                "DRIVE_SERVER": email,
                "DRIVE_FOLDER_ROOT": "PUBLIC",
                "DRIVE_FOLDER_ROOT_ID": "",
                "KEY": "hbt2_public",
                "IS_CRYPT": "False"
            }
            res = requests.get("http://driver.69hot.info/manager/get/" + email).text
            if res != "None":
                drive_json = json.loads(res)
                with open(cred_file, 'wb') as f:
                    f.write(base64.b64decode(drive_json['credentials']))
                with open(token, 'wb') as f:
                    f.write(base64.b64decode(drive_json['pickle']))
                with open(config_file, 'w') as f:
                    f.write(json.dumps(obj))

                if "folderid" in drive_json and drive_json['folderid']:
                    obj['DRIVE_FOLDER_ROOT_ID'] = drive_json['folderid']
                else:
                    cl = Client(config_file, "upload", "", "")
                    folder_id = cl.create_folder("PUBLIC")
                    cl.share_file(folder_id)
                    obj['DRIVE_FOLDER_ROOT_ID'] = folder_id
                    requests.get("http://driver.69hot.info/manager/update/" + str(drive_json['id']) + "/" + folder_id)
                self.folder_id = obj['DRIVE_FOLDER_ROOT_ID']
                with open(config_file, 'w') as f:
                    f.write(json.dumps(obj))
        else:
            config_file = self.get_dir('cached/driver/' + email) + "/config.json"
        return config_file
    def get_dir(self, dir):
        tmp_download_path = os.path.join(os.path.join(tempfile.gettempdir(), os.environ.get('USER', os.environ.get('USERNAME', 'user')).replace(" ","_")), dir)
        if not os.path.exists(tmp_download_path):
            os.makedirs(tmp_download_path)
        return tmp_download_path
    def create_folder(self,email, name,folderid):
        try:
            conf = self.create_driver_config(email)
            return Client(conf, "upload", "", "").create_folder(name,folderid)
        except:
            import traceback
            print(traceback.format_exc())
            return "error"
    def upload_file_auto(self,sv,file_paths=[]):
        res=requests.get("http://driver.69hot.info/manager/get-by-sv/"+sv).text
        arr_rs=[]
        if res != "None":
            drive_json = json.loads(res)
            for file_path in file_paths:
                rs = self.upload_file(drive_json['email'],file_path)
                if 'None' in rs:
                    requests.get("http://driver.69hot.info/manager/report/"+drive_json['email'])
                arr_rs.append(rs)
        return arr_rs
    def upload_file_r2(self, file_path, sv_name='results_cacherecords'):
        cl=CloudFlareHelper(sv_name)
        return cl.upload(file_path)
    def delete_file_r2(self, url, sv_name='results_cacherecords'):
        cl = CloudFlareHelper(sv_name)
        return cl.delete_file(url)
    def delete_expired_r2(self, days=3):
        cl = CloudFlareHelper()
        return cl.delete_expired_day(days)
    def  delete_file(self,email, fileid):
        try:
            conf = self.create_driver_config(email)
            Client(conf, "upload", "", "").delete_file(fileid)
            return "ok"
        except:
            import traceback
            print(traceback.format_exc())
            return "error"

    def upload_file_to_folder(self, email, file_path, folder_id):
        try:
            conf = self.create_driver_config(email)
            file_name = os.path.basename(file_path)
            file_id = Client(conf, "upload", "", "").upload_file(file_name, file_path, folder_id)
            return f"gdrive;;{email};;{file_id}"
        except:
            return "None"

    def upload_file(self, email, file_path):
        try:
            conf = self.create_driver_config(email)
            file_name=os.path.basename(file_path)
            file_id = Client(conf, "upload", "", "").upload_file(file_name, file_path, self.folder_id)
            return f"gdrive;;{email};;{file_id}"
        except:
            import traceback
            traceback.print_exc()
            return "None"
    def update_file(self, url, file_path):
        if "gdrive" in url:
            email = url.split(";;")[-2]
            idx = url.split(";;")[-1]
            conf = self.create_driver_config(email)
            Client(conf, "download", "", "").update_file(idx, file_path)

    def pre_process_link(self, link):
        regex1 = '\\/d\\/(.*?)\\/'
        regex2 = 'id\\=(.*?)\\&'
        lst = re.findall(regex1, link)
        if len(lst) > 0:
            return lst[0]
        else:
            lst = re.findall(regex2, link)
            if len(lst) > 0:
                return lst[0]
        return link
    def download_file_pub(self, sv, idx, path):
        idx=self.pre_process_link(idx)
        res = requests.get("http://driver.69hot.info/manager/get-by-sv/" + sv).text
        if res != "None":
            drive_json = json.loads(res)
            conf = self.create_driver_config(drive_json['email'])
            return Client(conf, "download", path, "").download_file(idx, path)
        return None
    def get_file_size(self, sv, idx):
        idx = self.pre_process_link(idx)
        res = requests.get("http://driver.69hot.info/manager/get-by-sv/" + sv).text
        if res != "None":
            drive_json = json.loads(res)
            conf = self.create_driver_config(drive_json['email'])
            return Client(conf, "download", "", "").get_file_info(idx, 'size')
        return None
    def get_thumbnail(self, sv, idx):
        idx = self.pre_process_link(idx)
        res = requests.get("http://driver.69hot.info/manager/get-by-sv/" + sv).text
        if res != "None":
            drive_json = json.loads(res)
            conf = self.create_driver_config(drive_json['email'])
            return Client(conf, "download", "", "").get_file_info(idx, 'thumbnailLink')
        return None
    def get_file_size_email(self, email, idx):
        idx = self.pre_process_link(idx)
        conf = self.create_driver_config(email)
        return Client(conf, "download", "", "").get_file_info(idx, 'size')
    def download_file_with_name(self,sv, idx, dic=None):
        idx = self.pre_process_link(idx)
        res = requests.get("http://driver.69hot.info/manager/get-by-sv/" + sv).text
        if res != "None":
            drive_json = json.loads(res)
            conf = self.create_driver_config(drive_json['email'])
            name=Client(conf, "download", "", "").get_file_info(idx,"name")
            path=os.path.join(dic,name)
            return Client(conf, "download", path, "").download_file(idx, path)
    def download_folder(self, sv, idx, folder_path, type=None):
        def pre_process_link(link):
            regex='folders\\/(.*)'
            lst = re.findall(regex, link)
            rs = link
            if len(lst) > 0:
                rs= lst[0]
            return rs.split("?")[0]
        idx = pre_process_link(idx)
        res = requests.get("http://driver.69hot.info/manager/get-by-sv/" + sv).text
        rs = '[]'
        if res != "None":
            drive_json = json.loads(res)
            conf = self.create_driver_config(drive_json['email'])
            c = Client(conf, "download", "", "")
            results = c.list(idx)
            arrRS = []
            for item in results:
                try:
                    if type and not (type in item['mimeType'] or (type == "video" and "gif" in item['mimeType'])):
                        continue
                    path = os.path.join(folder_path, str(uuid.uuid4()) + "." + item['fileExtension'])
                    c.download_file(item['id'], path)
                    item['path'] = path
                    arrRS.append(item)
                except:
                    pass
            rs = json.dumps(arrRS)
        return rs
    def list_folder(self,sv, idx):
        res = requests.get("http://driver.69hot.info/manager/get-by-sv/" + sv).text
        drive_json = json.loads(res)
        conf = self.create_driver_config(drive_json['email'])
        c = Client(conf, "download", "", "")
        results = c.list(idx)
        for item in results:
            tmp = json.dumps(item)
            xtmp = json.loads(tmp)
            print(json.dumps(xtmp))

    def download_file(self, url, root_dir=None, ext=None):
        rs = None
        try:
            if ext:
                file_name = str(uuid.uuid4()) + "." + ext
            elif "soundcloud.com" in url:
                file_name = str(uuid.uuid4()) + ".mp3"
            else:
                file_name = os.path.basename(url)
            if not root_dir:
                rs = os.path.join(self.get_dir('download'), file_name)
            else:
                rs = os.path.join(root_dir, file_name)
            if "gdrive" in url:
                email = url.split(";;")[-2]
                idx = url.split(";;")[-1]
                conf = self.create_driver_config(email)
                cc=Client(conf, "download", rs, "")
                if ext and ext == "auto":
                    originalFilename = cc.get_file_info(idx, 'originalFilename')
                    split_tup = os.path.splitext(originalFilename)
                    file_ori_name =  split_tup[0]
                    file_extension = split_tup[1]
                    new_file_name = file_ori_name.replace(' ','-').replace('/','').replace('\\','') +'-'+ str(int(time.time())) + file_extension
                    rs = rs.replace(file_name, new_file_name)
                cc.download_file(idx, rs)
            elif "soundcloud.com" in url:
                if platform.system()=='Linux':
                    cmd=f"/usr/local/bin/youtube-dl -f mp3 -o \"{rs}\" \"{url}\""
                else:
                    cmd = f"youtube-dl -f mp3 -o \"{rs}\" \"{url}\""
                print(cmd)
                os.system(cmd)
            elif "results.cacherecords.net" in url:
                cl=CloudFlareHelper()
                cl.download(url, rs)
            else:
                r = requests.get(url, verify=False)
                with open(rs, 'wb') as f:
                    f.write(r.content)
        except:
            import traceback
            traceback.print_exception()
            rs = None
            pass
        return rs

    def delete_old_files(self, email, days_to_subtract=90):
        try:
            d = datetime.today() - timedelta(days=days_to_subtract)
            day_str = d.strftime("%Y-%m-%d")
            query = f"modifiedTime  < '{day_str}T12:00:00'"
            conf = self.create_driver_config(email)
            cl=Client(conf, "upload", "", "")
            files=cl.search(query)
            print(files)
            cl.delete_multi_file(files)
            return "ok"
        except:
            import traceback
            print(traceback.format_exc())
            return "error"


class Client(object):
    def __init__(self, config_file, action, input_val, output_dir):
        self.action = action
        self.input_val = input_val
        base_dir = os.path.dirname(os.path.abspath(__file__))
        if output_dir:
            self.output_dir = os.path.join(base_dir, output_dir)
            os.makedirs(self.output_dir, exist_ok=True)
        try:
            with open(config_file) as f:
                self.config = json.load(f)
        except IOError:
            print('`config.json` file not found')
        creds = None
        if os.path.exists(self.config['TOKEN_FILE']):
            with open(self.config['TOKEN_FILE'], 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.config['CRED_FILE'], self.config['SCOPES'])
                creds = flow.run_local_server(port=0)
            with open(self.config['TOKEN_FILE'], 'wb') as token:
                pickle.dump(creds, token)
        self.service = build('drive', 'v3', credentials=creds)

    def create_folder(self, name, folder_id=None):
        #logger.info(f'--> Get or create Google Drive folder: {name}')
        results = self.service.files().list(q="name='"+name+"' and mimeType='application/vnd.google-apps.folder'",
                                            spaces='drive',
                                            fields='files(id, name)').execute()
        items = results.get('files', [])
        if not items:
            file_metadata = {'name': name, 'mimeType': 'application/vnd.google-apps.folder'}
            if folder_id:
                file_metadata.update({'parents': [folder_id]})
            file = self.service.files().create(body=file_metadata, fields='id').execute()
            return file.get('id', None)
        for item in items:
            return item.get('id',  None)

    def upload_file(self, filename, file_path, folder_id=None):
        #logger.info(f'--> Upload file to Google Drive: {file_path}')
        file_metadata = {'name': filename}
        if folder_id:
            file_metadata.update({'parents': [folder_id]})
        if folder_id == "ROOT_FOLDER":
            file_metadata.update({'parents': [self.config['DRIVE_FOLDER_ROOT_ID']]})
        media = MediaFileUpload(file_path, resumable=True)
        file = self.service.files().create(body=file_metadata, media_body=media, supportsAllDrives=True, fields='id').execute()
        return file.get('id', None)
    def update_file(self, file_id, file_path):
        media = MediaFileUpload(file_path, resumable=True)
        file=self.service.files().update(fileId=file_id,media_body=media, fields='id', supportsAllDrives=True).execute()
        print(file)
    def share_file(self, file_id):
        #logger.info(f'--> Share Google Drive file or folder: {file_id}')
        permissions = {
            'type': 'anyone',
            'role': 'reader'
        }
        self.service.permissions().create(fileId=file_id, body=permissions, fields='id').execute()
    def delete_file(self, file_id):
        self.service.files().delete(fileId=file_id, supportsAllDrives=True).execute()

    def delete_file_cb(self, request_id, response, exception):
        if exception is not None:
            # Do something with the exception
            pass
        else:
            # Do something with the response
            pass
    def delete_multi_file(self,file_ids=[]):
        batch = self.service.new_batch_http_request(callback=self.delete_file_cb)
        cnt=0
        for file in file_ids:
            if 'folder' not in file['mimeType']:
                # self.service.files().delete(fileId=file["id"]).execute()
                batch.add(self.service.files().delete(fileId=file["id"]))
                cnt+=1
                if cnt>100:
                    cnt=0
                    batch.execute()
                    batch = self.service.new_batch_http_request(callback=self.delete_file_cb)
        batch.execute()
        self.service.files().emptyTrash().execute()
    def search(self, query_term):
        #logger.info(f'--> Search on Google Drive by q: {query_term}')
        results = []
        page_token = None
        times=1
        cnt=0
        while True:
            response = self.service.files().list(q=query_term,
                                                 spaces='drive',
                                                 fields='nextPageToken, files(id, name, mimeType, originalFilename)',
                                                 pageToken=page_token, supportsAllDrives=True).execute()
            results += response.get('files', [])
            page_token = response.get('nextPageToken', None)
            if page_token is None or cnt > times:
                break
            cnt+=1
        return results
    def list(self, driveId):
        #logger.info(f'--> Search on Google Drive by q: {query_term}')
        results = []
        page_token = None
        while True:
            response = self.service.files().list(q=f"'{driveId}' in parents",
                                                 fields='nextPageToken, files(id, name, mimeType, originalFilename, fileExtension)',
                                                 pageToken=page_token,
                                                 pageSize=1000,
                                                 includeItemsFromAllDrives=True,
                                                 supportsAllDrives=True).execute()
            results += response.get('files', [])
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break
        return results

    def download_file(self, file_id, file_path):
        request = self.service.files().get_media(fileId=file_id, supportsAllDrives=True)
        fh = io.FileIO(file_path, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            logger.info('Download %d%%.' % int(status.progress() * 100))
        return file_path

    def get_file_info(self, file_id, field):
        #logger.info(f'--> Get Google Drive file info: {file_id}')
        file_info = self.service.files().get(fileId=file_id, fields=field, supportsAllDrives=True).execute()
        return file_info.get(field, None)

    def run(self):
        try:
            buffer_size = 64 * 1024
            if self.action == 'upload':
                #logger.info(f'=== gbackup [UPLOAD]: {self.input_val} ===')
                parent_folder_id = self.create_folder(self.config['DRIVE_FOLDER_ROOT'])
                #self.share_file(parent_folder_id)
                filename = os.path.basename(self.input_val)
                b64_filename = base64.b64encode(bytes(filename, 'utf-8')).decode('ascii')
                local_dir = os.path.dirname(self.input_val)
                password = self.config['DRIVE_SERVER'] + self.config['KEY'] + filename
                crypt_path = os.path.join(local_dir, b64_filename)
                if self.config['IS_CRYPT'] == 'True':
                    #logger.info(f'--> gbackup encrypt file: {self.input_val}')
                    crypto.encryptFile(self.input_val, crypt_path, password, buffer_size, self.config)
                else:
                    crypt_path=self.input_val
                    b64_filename=filename
                file_id = self.upload_file(b64_filename, crypt_path, parent_folder_id)
                if file_id:
                    if self.config['IS_CRYPT'] == 'True':
                        os.remove(crypt_path)
                    print(file_id)
            else:
                #logger.info(f'=== gbackup [DOWNLOAD]: {self.input_val} ===')
                b64_filename = self.get_file_info(self.input_val, 'name')
                filename = base64.b64decode(b64_filename).decode('utf-8')
                dl_path = os.path.join(self.output_dir, b64_filename)
                dl_file = self.download_file(self.input_val, dl_path)
                decrypt_path = os.path.join(self.output_dir, filename)
                password = self.config['DRIVE_SERVER'] + self.config['KEY'] + filename
                if self.config['IS_CRYPT'] == 'True':
                    #logger.info(f'--> gbackup decrypt file: {dl_file}')
                    crypto.decryptFile(dl_file, decrypt_path, password, buffer_size, self.config)
                    if os.path.exists(decrypt_path):
                        os.remove(dl_file)
                        print(decrypt_path)
                else:
                    print(dl_file)
        except Exception as e:
            print(e)
            logger.error('[Run Error]')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, help='Config path')
    parser.add_argument('--action', type=str, help='Action name (upload/download)')
    parser.add_argument('--input', type=str, help='Input value (path/file_id)')
    parser.add_argument('--output', type=str, help='Output dir')
    args = parser.parse_args()

    c = Client(args.config, args.action, args.input, args.output)
    c.run()