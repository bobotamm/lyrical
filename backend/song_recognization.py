import requests

def recognize(file_name, api_token):
    data = {
    'return': 'apple_music,spotify',
    'api_token': api_token
    }
    files = {
        'file': open(file_name, 'rb'),
    }
    result = requests.post('https://api.audd.io/', data=data, files=files)
    return result