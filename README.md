# 1. Provisioning

## create layer
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

## environment

```
S3BUCKET=<YOUR_S3BUCKET>
S3BUCKET_PUBLICACCESS=<YOUR_S3BUCKET_PUBLICACCESS>
S3KEY=
VALIDATORS=
VALIDATORS_INFO=
```


# 2. deploy lambda(ValidatorTaxTable)

`cloudformation/ValidatorTaxTable/cf-lambda-[dev|prod].yaml`

```
set up CONFIDENTIAL parameters
```


### lambda_function

```
cd mymodul
cp lambda_function_ValidatorTaxTable.py lambda_function.py && \
    zip -r lf_ValidatorTaxTable.zip lambda_function.py && \
    rm lambda_function.py
aws s3 cp lf_ValidatorTaxTable.zip s3://<YOUR_S3BUCKET>/cloudformation/lambda/lf_ValidatorTaxTable.zip
```

### cloudFormation

#### 2-1 web3-selenium-headless-dev

```
###### direct deploy
$ cd mymodule
$ aws lambda update-function-code --function-name web3-selenium-headless-dev --zip-file fileb://lf_ValidatorTaxTable.zip

###### cloudformation
$ cd cloudformation/ValidatorTaxTable
$ aws s3 cp cf-lambda-ValidatorTaxTable-dev.yaml s3://<YOUR_S3BUCKET>/cloudformation/lambda/cf-lambda-ValidatorTaxTable-dev.yaml
$ aws cloudformation create-stack \
    --stack-name cf-lambda-web3-selenium-headless-dev \
    --template-url https://<YOUR_S3BUCKET>.s3.ap-northeast-1.amazonaws.com/cloudformation/lambda/cf-lambda-ValidatorTaxTable-dev.yaml
```



#### 2-2 web3-selenium-headless-prod

```
##### direct deploy
$ cd mymodule
$ aws lambda update-function-code \
    --function-name web3-selenium-headless-prod \
    --zip-file fileb://lf_ValidatorTaxTable.zip

##### cloudformation
$ cd cloudformation/ValidatorTaxTable
$ aws s3 cp cf-lambda-ValidatorTaxTable-prod.yaml s3://<YOUR_S3BUCKET>/cloudformation/lambda/cf-lambda-ValidatorTaxTable-prod.yaml
$ aws cloudformation create-stack \
    --stack-name cf-lambda-web3-selenium-headless-prod \
    --template-url https://<YOUR_S3BUCKET>.s3.ap-northeast-1.amazonaws.com/cloudformation/lambda/cf-lambda-ValidatorTaxTable-prod.yaml
```


# 3. deploy lambda(PostSlack)

`cloudformation/PostSlack/cf-lambda-[dev|prod].yaml`

```
set up CONFIDENTIAL parameters
```


### lambda_function

```
$ cd mymodul
$ cp lambda_function_PostSlack.py lambda_function.py && \
    zip -r lf_PostSlack.zip lambda_function.py && \
    rm lambda_function.py
$ aws s3 cp lf_PostSlack.zip s3://<YOUR_S3BUCKET>/cloudformation/lambda/lf_PostSlack.zip
```

### cloudFormation

#### 3-1 web3-selenium-PostSlack-dev

```
###### direct deploy
$ cd mymodule
$ aws lambda update-function-code \
    --function-name web3-selenium-PostSlack-dev \
    --zip-file fileb://lf_PostSlack.zip

###### cloudformation
$ cd cloudformation/PostSlack
$ aws s3 cp cf-lambda-PostSlack-dev.yaml s3://<YOUR_S3BUCKET>/cloudformation/lambda/cf-lambda-PostSlack-dev.yaml
$ aws cloudformation create-stack \
    --stack-name cf-lambda-web3-selenium-PostSlack-dev \
    --template-url https://<YOUR_S3BUCKET>.s3.ap-northeast-1.amazonaws.com/cloudformation/lambda/cf-lambda-PostSlack-dev.yaml
```




#### 3-2 web3-selenium-PostSlack-prod

```
##### direct deploy
$ cd mymodule
$ aws lambda update-function-code \
    --function-name web3-selenium-PostSlack-prod \
    --zip-file fileb://lf_ValidatorTaxTable.zip

##### cloudformation
$ cd cloudformation/ValidatorTaxTable
$ aws s3 cp cf-lambda-PostSlack-prod.yaml s3://<YOUR_S3BUCKET>/cloudformation/lambda/cf-lambda-PostSlack-prod.yaml
$ aws cloudformation create-stack \
    --stack-name cf-lambda-web3-selenium-PostSlack-prod \
    --template-url https://<YOUR_S3BUCKET>.s3.ap-northeast-1.amazonaws.com/cloudformation/lambda/cf-lambda-PostSlack-prod.yaml
```s