from selenium import webdriver
from selenium.webdriver.common.by import By
import boto3
import os
import time
import glob
from pathlib import Path

def lambda_handler(event, context):
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
    
    tmp_dir = Path(Path.cwd(), "tmp") # lambdaの場合：/var/task/tmp
    prefs = {'download.default_directory' : "/tmp" }
    options.add_experimental_option('prefs',prefs)

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
    s3.upload_file(Filename="/tmp/shot.png",
                Bucket=bucket,
                Key="screenshot/" + "screenshot001.png")
        
    # get CSV
    xpath = "//*[@id='tax-table_wrapper']/div[1]/button[2]"
    object_button = browser.find_elements(by=By.XPATH, value=xpath)
    if object_button:
        print("Button found. object_button[0]=", object_button[0])
        object_button[0].click()
        
        time.sleep(5)
        
        download_fileName = glob.glob(str(tmp_dir) + f"*.*")    
        print("download_filename: ",download_fileName)
        download_fileName2 = glob.glob(f'/tmp/*')    
        print("download_filename2: ",download_fileName2)
        
    else:
        print("Button NOT found.")
    
    
    #browser.close()
    browser.quit()
    
    
    s3.upload_file(Filename=download_fileName,
                   Bucket=bucket,
                   Key="csv/" + "csv001.csv")

    return title
