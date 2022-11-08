import requests

    # r = requests.post('http://httpbin.org/post', files={'report.xls': f})
data = {
'return': 'apple_music,spotify',
'api_token': 'test'
}
files = {
    'file': open('test.mp3', 'rb'),
}
result = requests.post('https://api.audd.io/', data=data, files=files)
print(result.text)