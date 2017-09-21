##OAuth2 HOWTO

新浪微博API OAuth 2 Python客户端

最新源码
https://github.com/michaelliao/sinaweibopy/blob/master/weibo.py
使用简介

注册微博App后，可以获得app key和app secret，然后定义网站回调地址：

```python
from weibo import APIClient

APP_KEY = '1234567' # app key
APP_SECRET = 'abcdefghijklmn' # app secret
CALLBACK_URL = 'http://www.example.com/callback' # callback url
```

在网站放置“使用微博账号登录”的链接，当用户点击链接后，引导用户跳转至如下地址：

```python
client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
url = client.get_authorize_url()
# TODO: redirect to url
```

用户授权后，将跳转至网站回调地址，并附加参数code=abcd1234：

```python
# 获取URL参数code:
code = your.web.framework.request.get('code')
client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
r = client.request_access_token(code)
access_token = r.access_token # 新浪返回的token，类似abc123xyz456
expires_in = r.expires_in # token过期的UNIX时间：http://zh.wikipedia.org/wiki/UNIX%E6%97%B6%E9%97%B4
# TODO: 在此可保存access token
client.set_access_token(access_token, expires_in)
```

然后，可调用任意API：

```python
print client.statuses.user_timeline.get()
print client.statuses.update.post(status=u'测试OAuth 2.0发微博')
print client.statuses.upload.post(status=u'测试OAuth 2.0带图片发微博', pic=open('/Users/michael/test.png'))
```

## API调用规则

首先查看新浪微博API文档，例如：

> API：statuses/user_timeline

> 请求格式：GET

> 请求参数：

> source：string，采用OAuth授权方式不需要此参数，其他授权方式为必填参数，数值为应用的AppKey?。

> access_token：string，采用OAuth授权方式为必填参数，其他授权方式不需要此参数，OAuth授权后获得。

> uid：int64，需要查询的用户ID。

> screen_name：string，需要查询的用户昵称。

> （其它可选参数略）

> 调用方法：将API的“/”变为“.”，根据请求格式是GET或POST，调用get ()或post()并传入关键字参数，但不包括source和access_token参数：

```python
r = client.statuses.user_timeline.get(uid=123456)
for st in r.statuses:
    print st.text
```

> 若为POST调用，则示例代码如下：

```python
r = client.statuses.update.post(status=u'测试OAuth 2.0发微博')
```

> 若需要上传文件，传入file-like object参数，示例代码如下：

```python
f = open('/Users/michael/test.png', 'rb')
r = client.statuses.upload.post(status=u'测试OAuth 2.0带图片发微博', pic=f)
f.close() # APIClient不会自动关闭文件，需要手动关闭
```

> 请注意：上传的文件必须是file-like object，不能是str，因为无法区分一个str是文件还是字段。可以通过StringIO把一个str包装成file-like object。
站内应用

**站内应用授权不能作URL跳转，而是由新浪微博POST用户信息至iFrame，需要在iFrame的页面中处理用户信息。**

假定iFrame的入口地址是http://app.example.com/index，则新浪微博会POST数据至该URL。

第一步，获取POST数据：

```python
signed_request ＝ your.web.framework.get('signed_request')
client = APIClient(APP_ID, APP_SECRET, 'http://app.example.com/callback')
data = client.parse_signed_request(signed_request)
```

第二步，判断用户是否授权，如未授权，返回授权页面：

```python
user_id = data.get('uid', '')
auth_token = data.get('oauth_token', '')
if not user_id or not auth_token:
    return Template('auth.html')
```

授权页auth.html可以是静态页面，需要调用新浪的JS：

```html
<html>
<head>
    <title>未授权时的页面</title>
    <script src="http://tjs.sjs.sinajs.cn/t35/apps/opent/js/frames/client.js"></script>
</head>
<script>
function authLoad() {
    App.AuthDialog.show({
        client_id: 'YOUR_CLIENT_ID',
        redirect_uri: 'http://apps.weibo.com/YOUR_APP_ID',
        height: 40});
}
</script>
<body onload="authLoad();"></body>
</html>
```

第三步，如果用户已授权，则可直接获得OAuth token：

```python
user_id = data.get('uid', '')
auth_token = data.get('oauth_token', '')
if not user_id or not auth_token:
    return Template('auth.html')
expires = data.expires
client.set_access_token(auth_token, expires)
```

现在，已获取到用户的auth_token和expires，可以按照API进行正常调用。
使用限制

**仅支持Web方式调用，不支持口令方式验证。**

补充说明

所有API调用均为动态调用，支持**链式调用**，需要根据新浪API文档由HTTP调用方式（GET，POST）决定APIClient的链式方法名（如statuses.user_timeline）和最后调用的方法是get()还是post()，以及关键字参数。

若调用出错，会抛出APIError异常，该异常包含error_code，error和request三个字段，与新浪返回的出错json对应。具体错误原因请查询新浪文档。

若HTTP响应出错（例如404），会抛出urllib2.HTTPError异常。

