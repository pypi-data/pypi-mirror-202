import requests
import json

def send_message(webhook_url, message, username=None, avatar_url=None, custom_id=None, default=None, label=None, max_length=None, min_length=None, placeholder=None, required=None, style=None, type=None, value=None):
    payload = {'content': message}
    if username:
        payload['username'] = username
    if avatar_url:
payload['avatar_url'] = avatar_url
    if custom_id:
        payload['custom_id'] = custom_id
    if default:
        payload['default'] = default
    if label:
        payload['label'] = label
    if max_length:
        payload['max_length'] = max_length
    if min_length:
        payload['min_length'] = min_length
    if placeholder:
        payload['placeholder'] = placeholder
    if required:
        payload['required'] = required
    if style:
        payload['style']  = style
    if type:
        payload['type'] = type
    if value:
        payload['value'] = value
    headers = {'Content-Type': 'application/json'}
    response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)
    if response.status_code != 204:
        print('Request failed with status code', response.status_code)

def send_embed(webhook_url, embed, username=None, avatar_url=None):
    payload = {'embeds': [embed.to_dict()]}
    if username:
        payload['username'] = username
    if avatar_url:
        payload['avatar_url'] = avatar_url
      
    headers = {'Content-Type': 'application/json'}
    response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)
    if response.status_code != 204:
        print('Request failed with status code', response.status_code)

def send_file(webhook_url, file, username=None, avatar_url=None):
    files = {'file': file}
    data = {}
    if username:
        data['username'] = username
    if avatar_url:
        data['avatar_url'] = avatar_url
    response = requests.post(webhook_url, data=data, files=files)
    if response.status_code != 204:
        print('Request failed with status code', response.status_code)