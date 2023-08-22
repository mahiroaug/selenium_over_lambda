from selenium import webdriver
from selenium.webdriver.common.by import By
import boto3
import os
import time
import datetime
import glob
import json
from pathlib import Path

def lambda_handler(event, context):
    
    #### SETTING ####################################
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-application-cache")
    options.add_argument("--disable-infobars")
    options.add_argument("--hide-scrollbars")
    options.add_argument("--single-process")
    options.add_argument("--enable-logging")
    options.add_argument("--log-level=INFO")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--window-size=1500x1250")
    options.add_argument("--no-sandbox")
    options.add_argument("--homedir=/tmp")
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36') # user-agent設定
    options.binary_location = "/opt/python/bin/headless-chromium"
    
    ### download directory
    tmp_dir = Path(Path.cwd(), "tmp") # lambdaの場合：/var/task/tmp
    prefs = {'download.default_directory' : "/tmp" }
    options.add_experimental_option('prefs',prefs)

    ### s3 setting
    bucket = os.environ.get("S3BUCKET", "")
    bucket_publicaccess = os.environ.get("S3BUCKET_PUBLICACCESS")
    key = os.environ.get("S3KEY")
    s3client = boto3.client('s3')
    s3resource = boto3.resource('s3')
    
    ### env setting
    validators = os.environ.get("VALIDATORS")
    info = os.environ.get("VALIDATORS_INFO")
    URL = generate_url(validators)
    print("URL: ",URL)

    #get date
    current = datetime.datetime.now()
    current_formed = current.strftime('%Y-%m-%d') 
    
    
    ### HEADLESS BROWSER(selenium) ########################
    browser = webdriver.Chrome(
        "/opt/python/bin/chromedriver",
        options=options
    )
    browser.get(URL)
    title = browser.title
    
    ### resize
    page_width = browser.execute_script('return document.body.scrollWidth')
    page_height = browser.execute_script('return document.body.scrollHeight')
    browser.set_window_size(page_width, page_height)
    
    time.sleep(10)
    
    ### get screenshot ###########################
    file_name = "/tmp/shot.png"
    browser.save_screenshot(file_name)
    
    ### put S3
    full_key = f"{key}/png/any-url_{current_formed}.png"
    s3client.upload_file(Filename=file_name,
                        Bucket=bucket_publicaccess,
                        Key=full_key)
    image_url = f"https://{bucket_publicaccess}.s3.ap-northeast-1.amazonaws.com/{full_key}"
     
    
    ### close ##########################################
    browser.close()
    #browser.quit()
    
    attachments = [
        {
            "pretext": f"<!channel> ({current_formed}現在) sample",
            "color": "#FFA500",
            "author_name": "author_name",
            "title": "title(info)",
            "title_link": URL,
            "text": "text(sample)",
            "image_url": image_url,
            "footer": "powered by headless-chromium",
            "ts": int(time.time())
        }
    ]
    
    attachments_json = json.dumps(attachments).encode('utf-8')

    # push bucket
    s3client.put_object(
                        Bucket=bucket,
                        ACL='private',
                        Body=attachments_json,
                        Key=key + "/json/" + "attachments" + ".json",
                        ContentType='application/json'
                        )



    return title


def generate_url(validators):  
    url = "https://beaconcha.in/charts"
    return url

