from selenium import webdriver

def lambda_handler(event, context, is_lambda=True):

    URL = "https://news.yahoo.co.jp/"

    options = webdriver.ChromeOptions()

    # Lambdaから呼び出した場合
    if is_lambda:
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--hide-scrollbars")
        options.add_argument("--single-process")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--window-size=880x996")
        options.add_argument("--no-sandbox")
        options.add_argument("--homedir=/tmp")
        options.binary_location = "/opt/python/bin/headless-chromium"

        browser = webdriver.Chrome("/opt/python/bin/chromedriver", options=options)

    # 直接呼び出した場合
    else:
        from webdriver_manager.chrome import ChromeDriverManager

        browser = webdriver.Chrome(ChromeDriverManager().install())

    browser.get(URL)
    title = browser.title
    browser.close()

    return title

if __name__ == "__main__": 
    result = lambda_handler(event=None, context=None, is_lambda=False)
    print(result)
