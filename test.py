#encoding=utf-8
from urllib import quote
import urllib.request
if __name__ == '__main__':
    url = 'http://api.ltp-cloud.com/analysis/?api_key=M1z3A1v4F4gdjNpwTR0i4BoArpkrTJ8HZYbVUOws&text=我是中国人&pattern=dp&format=plain'
    result = urllib.request.urlopen(quote(url, safe='/:?=&'))
    print(result)