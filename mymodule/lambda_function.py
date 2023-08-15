from selenium import webdriver
import boto3
import os
import time

def lambda_handler(event, context):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-application-cache")
    options.add_argument("--disable-infobars")
    options.add_argument("--hide-scrollbars")
    options.add_argument("--single-process")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--window-size=1500x1250")
    options.add_argument("--no-sandbox")
    options.add_argument("--homedir=/tmp")
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36') # user-agent設定
    options.binary_location = "/opt/python/bin/headless-chromium"

    bucket = os.environ.get("S3BUCKET", "")
    s3 = boto3.client('s3')
    
    browser = webdriver.Chrome(
        "/opt/python/bin/chromedriver",
        options=options
    )

    URL = os.environ.get("URL")
    browser.get(URL)
    title = browser.title
    
    page_width = browser.execute_script('return document.body.scrollWidth')
    page_height = browser.execute_script('return document.body.scrollHeight')
    browser.set_window_size(page_width, page_height)
    
    time.sleep(15)
    browser.save_screenshot("/tmp/shot.png")
    browser.close()

    s3.upload_file(Filename="/tmp/shot.png",
                   Bucket=bucket,
                   Key="screenshot/" + "screenshot001.png")


    return title
