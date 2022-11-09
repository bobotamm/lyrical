import requests

def recoginize(file_name):
    data = {
    'return': 'apple_music,spotify',
    'api_token': 'test'
    }
    files = {
        'file': open(file_name, 'rb'),
    }
    result = requests.post('https://api.audd.io/', data=data, files=files)
    return result

print(recoginize("test.mp3").json()['result']['title'])