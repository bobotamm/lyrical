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

print(recognize("Rihanna_Diamonds.mp3", "d1e1b6a951741d66e855f5d73e0b2315").json())