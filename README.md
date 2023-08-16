# create layer
### selenium 

`layer/selenium/README.md`

### headless-chromium

```
$ mkdir -p python/bin/
$ curl -SL https://github.com/adieuadieu/serverless-chrome/releases/download/v1.0.0-37/stable-headless-chromium-amazonlinux-2017-03.zip > headless-chromium.zip
$ unzip headless-chromium.zip -d python/bin/
$ rm headless-chromium.zip
```

### chromedriver 

```
$ curl -SL https://chromedriver.storage.googleapis.com/2.37/chromedriver_linux64.zip > chromedriver.zip
$ unzip chromedriver.zip -d python/bin/
$ rm chromedriver.zip
```

### slack-sdk

`layer/slack-sdk/README.md`


### JP-font

```
cd font
wget https://moji.or.jp/wp-content/ipafont/IPAexfont/IPAexfont00401.zip
unzip IPAexfont00401.zip 
mkdir .fonts
mv IPAexfont00401/ipaexg.ttf .fonts/
mv IPAexfont00401/ipaexm.ttf .fonts/
zip -r font_layer.zip .fonts
```

# environment

```
S3BUCKET=<YOUR_S3BUCKET>
S3KEY=screenshot-dev
VALIDATORS=<YOUR_VALIDATOR_ID>
```


`cloudformation/cf-lambda-[dev|prod].yaml`

```
VALIDATORS: "<YOUR_VALIDATOR_ID>" ### confidential
```



# deploy lambda

```
cp mymodule/lambda_function_ValidatorTaxTable.py mymodule/lambda_function.py
zip -r mymodule/lf_ValidatorTaxTable.zip mymodule/lambda_function.py
aws s3 cp mymodule/lf_ValidatorTaxTable.zip s3://<YOUR_S3BUCKET>/cloudformation/lambda/lf_ValidatorTaxTable.zip
```


```
###### web3-selenium-headless-dev

# direct deploy
aws lambda update-function-code --function-name web3-selenium-headless-dev --zip-file fileb://mymodule/lf_ValidatorTaxTable.zip

# cloudformation
aws s3 cp cloudformation/cf-lambda-dev.yaml s3://<YOUR_S3BUCKET>/cloudformation/lambda/cf-lambda-dev.yaml

aws cloudformation create-stack --stack-name cf-lambda-web3-selenium-headless-dev --template-url https://<YOUR_S3BUCKET>.s3.ap-northeast-1.amazonaws.com/cloudformation/lambda/cf-lambda-dev.yaml

```


```
###### web3-selenium-headless-prod

# direct deploy
aws lambda update-function-code --function-name web3-selenium-headless-prod --zip-file fileb://mymodule/lf_ValidatorTaxTable.zip

# cloudformation
aws s3 cp cloudformation/cf-lambda-prod.yaml s3://<YOUR_S3BUCKET>/cloudformation/lambda/cf-lambda-prod.yaml

aws cloudformation create-stack --stack-name cf-lambda-web3-selenium-headless-prod --template-url https://<YOUR_S3BUCKET>.s3.ap-northeast-1.amazonaws.com/cloudformation/lambda/cf-lambda-prod.yaml

```