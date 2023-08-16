from selenium import webdriver
from selenium.webdriver.common.by import By
import boto3
import os
import time
import datetime
import glob
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
    key = os.environ.get("S3KEY")
    s3 = boto3.client('s3')
    
    ### env setting
    validators = os.environ.get("VALIDATORS")
    URL = generate_url(validators)
    print("URL: ",URL)

    
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
    browser.save_screenshot("/tmp/shot.png")
    
    ### put S3
    s3.upload_file(Filename="/tmp/shot.png",
                Bucket=bucket,
                Key=key + "/" + "validators_tax_table.png")
    s3.put_object(ACL='private',
                Bucket=bucket,
                Body=URL,
                Key=key + "/" + "URL.txt",
                ContentType='text/plain')
    
    '''
    ### get CSV
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
            
        s3.upload_file(Filename=download_fileName,
                    Bucket=bucket,
                    Key="csv/" + "csv001.csv")
    else:
        print("Button NOT found.")
    '''    
    
    
    ### close ##########################################
    browser.close()
    #browser.quit()

    return title


def generate_url(validators):
    utcnow = datetime.datetime.utcnow()
    start_of_month = utcnow.replace(day=1, hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(hours=-9)
    
    start = int(start_of_month.timestamp())
    end = int(utcnow.timestamp())
    
    url = f"https://beaconcha.in/rewards?validators={validators}&currency=jpy&days={start}-{end}"
    return url

