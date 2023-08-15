
# get JP-font & make lambda-layer

```
cd font
wget https://moji.or.jp/wp-content/ipafont/IPAexfont/IPAexfont00401.zip
unzip IPAexfont00401.zip 
mkdir .fonts
mv IPAexfont00401/ipaexg.ttf .fonts/
mv IPAexfont00401/ipaexm.ttf .fonts/
zip -r font_layer.zip .fonts
aws s3 cp font_layer.zip s3://********
```

# environment

```
S3BUCKET=*********
```


# deploy lambda

```
cd mymodule
zip -r lf.zip lambda_function.py
aws lambda update-function-code --function-name web3-selenium-headless --zip-file fileb://lf.zip
```
