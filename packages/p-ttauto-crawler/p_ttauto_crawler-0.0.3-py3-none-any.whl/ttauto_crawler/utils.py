import subprocess
import os
import sys
import time
import oss2
import http.client
import json
import logging
import calendar
from pathlib import Path
import shutil
import zipfile
import platform
import requests
import hashlib
import ftplib
from PIL import Image
from io import BytesIO

def getOssResource(rootDir, url, md5, name):
    localFile = os.path.join(rootDir, name)
    localFileIsRemote = False
    if os.path.exists(localFile):
        with open(localFile, 'rb') as fp:
                file_data = fp.read()
        file_md5 = hashlib.md5(file_data).hexdigest()
        if file_md5 == md5:
            localFileIsRemote = True

    if localFileIsRemote == False: #download
        if os.path.exists(localFile):
            os.remove(localFile)
        s = requests.session()
        s.keep_alive = False
        print(f"download {url} ")
        file = s.get(url, verify=False)
        with open(localFile, "wb") as c:
            c.write(file.content)
        s.close()
        fname = name[0:name.index(".")]
        fext = name[name.index("."):]
        unzipDir = os.path.join(rootDir, fname)
        if os.path.exists(unzipDir):
            shutil.rmtree(unzipDir)
        print(f"unzip {url} -> {unzipDir}")

def updateBin(rootDir):
    getOssResource(rootDir, "http://template-m.2tianxin.com/res/ffmpeg.zip", "a9e6b05ac70f6416d5629c07793b4fcf", "ffmpeg.zip.py")
    for root,dirs,files in os.walk(rootDir):
        for file in files:
            if file.find(".") <= 0:
                continue
            name = file[0:file.index(".")]
            ext = file[file.index("."):]
            if ext == ".zip.py" and os.path.exists(os.path.join(root, name)) == False:
                print(f"unzip {os.path.join(root, name)}")
                with zipfile.ZipFile(os.path.join(root, file), "r") as zipf:
                    zipf.extractall(os.path.join(root, name))
        if root != files:
            break

def videoInfo(file):
    w = 0
    h = 0
    bitrate = 0
    fps = 0

    ffmpeg = ffmpegBinary()
    command = f'{ffmpeg} -i {file}'
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, shell=True)
        str = ""
        if result.returncode == 0:
            str = result.stdout.decode(encoding="utf8", errors="ignore")
        else:
            str = result.stderr.decode(encoding="utf8", errors="ignore")
        if str.find("yuv420p") > 0 and str.find("fps") > 0:
            s1 = str[str.find("yuv420p"):str.find("fps")+3].replace(' ', "")
            s1_split = s1.split(",")
            for s1_it in s1_split:
                s2 = s1_it
                if s2.find("[") > 0:
                    s2 = s2[0:s2.find("[")]
                if s2.find("(") > 0:
                    s2 = s2[0:s2.find("[")]
                if s2.find("x") > 0:
                    sizes = s2.split("x")
                    if len(sizes) > 1:
                        w = sizes[0]
                        h = sizes[1]
                if s2.find("kb/s") > 0:
                    bitrate = s2[0:s2.find("kb/s")]
                if s2.find("fps") > 0:
                    fps = s2[0:s2.find("fps")]
    except subprocess.CalledProcessError as e:
        print("====================== process error ======================")
        print(e)
        print("======================      end      ======================")
    return float(w),float(h),float(bitrate),float(fps)

def ffmpegBinary():
    binDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bin")
    updateBin(binDir)
    binaryFile = ""
    if sys.platform == "win32":
        binaryFile = os.path.join(binDir, "ffmpeg", "win", "ffmpeg.exe")
    elif sys.platform == "linux":
        machine = platform.machine().lower()
        if machine == "x86_64" or machine == "amd64":
            machine = "amd64"
        else:
            machine = "arm64"
        binaryFile = os.path.join(binDir, "ffmpeg", "linux", machine, "ffmpeg")
    elif sys.platform == "darwin":
        binaryFile = os.path.join(binDir, "ffmpeg", "darwin", "ffmpeg")
    
    if len(binaryFile) > 0 and sys.platform != "win32":
        cmd = subprocess.Popen(f"chmod 755 {binaryFile}", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        while cmd.poll() is None:
            print(cmd.stdout.readline().rstrip().decode('utf-8'))
        
    return binaryFile
    
def processMoov(file):
    tmpPath = f"{file}.mp4"
    binary = ffmpegBinary()
    command = f'{binary} -i {file} -movflags faststart -y {tmpPath}'
    logging.info(f"ffmpegProcess: {command}")
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, shell=True)
        if result.returncode == 0:
            logging.info(result.stdout.decode(encoding="utf8", errors="ignore"))
            os.remove(file)
            os.rename(tmpPath, file)
        else:
            logging.error("====================== ffmpeg error ======================")
            logging.error(result.stderr.decode(encoding="utf8", errors="ignore"))
            logging.error("======================     end      ======================")
    except subprocess.CalledProcessError as e:
        logging.error("====================== process error ======================")
        logging.error(e)
        logging.error("======================      end      ======================")

def ffmpegTest():
    binDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bin")
    testImage = os.path.join(binDir, "ffmpeg", "test.jpg")
    ffmpegProcess(f"-i {testImage}")
    
def ffmpegProcess(args):
    binary = ffmpegBinary()
    command = f'{binary} {args}'
    logging.info(f"ffmpegProcess: {command}")
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, shell=True)
        if result.returncode == 0:
            logging.info(result.stdout.decode(encoding="utf8", errors="ignore"))
        else:
            logging.error("====================== ffmpeg error ======================")
            logging.error(result.stderr.decode(encoding="utf8", errors="ignore"))
            logging.error("======================     end      ======================")
    except subprocess.CalledProcessError as e:
        logging.error("====================== process error ======================")
        logging.error(e)
        logging.error("======================      end      ======================")

def getOssImageSize(p):
    try:
        s = requests.session()
        s.keep_alive = False
        res = s.get(p)
        image = Image.open(BytesIO(res.content), "r")
        s.close()
        return image.size
    except:
        return 0, 0

def getLocalImageSize(p):
    try:
        image = Image.open(BytesIO(p), "r")
        return image.size
    except:
        return 0, 0

def deepFtpUpload(file, ftp, remote_dir=''):
    append_dir = f'{remote_dir}'
    if len(remote_dir) > 0:
        remote_path = f'1TB01/data/video/{append_dir}/'
        try:
            ftp.cwd(remote_path)
        except ftplib.error_perm as e:
            if e.args[0].startswith('550'):
                # 如果远程目录不存在，则创建它
                ftp.mkd(remote_path)
                ftp.cwd(remote_path)

    s = []
    if os.path.isfile(file):
        with open(file, 'rb') as f:
            ftp.storbinary(f'STOR {os.path.basename(file)}', f)
        s.append(f"http://192.168.3.220/01/video/{append_dir}{os.path.basename(file)}")
    elif os.path.isdir(file):
        for filename in os.listdir(file):
            local_file = os.path.join(file, filename)
            if os.path.isfile(local_file):
                with open(local_file, 'rb', encoding='UTF-8') as file:
                    ftp.storbinary(f'STOR {filename}', file)
                s.append(f"http://192.168.3.220/01/video/{append_dir}{filename}")
            elif os.path.isdir(local_file):
                subdir = os.path.join(remote_dir, filename)
                s.append(ftpUpload(local_file, ftp, subdir))
    return s

def ftpUpload(file, ftp = None):
    if not ftp:
        ftp = ftplib.FTP('192.168.3.220')
        ftp.login('xinyu100', 'xinyu100.com')

    remote_path = f'1TB01/data/video/'
    try:
        ftp.cwd(remote_path)
    except ftplib.error_perm as e:
        if e.args[0].startswith('550'):
            # 如果远程目录不存在，则创建它
            ftp.mkd(remote_path)
            ftp.cwd(remote_path)

    s = deepFtpUpload(file, ftp, "")
    ftp.quit()
    return s