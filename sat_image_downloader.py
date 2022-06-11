import argparse
import json
import math
import ast

import requests
import os

parser = argparse.ArgumentParser(description="Download satellite images from arcGIS")
parser.add_argument('credentials', type=str, help='path to credential file for OAuth2.0')
parser.add_argument('data', type=str, help='path to file of json objects representing images')
parser.add_argument('path', type=str, help='path to save images to')
parser.add_argument('extent', type=int, help='extent of image from center point, recalculates image size based on distance')
args = parser.parse_args()

def get_token(id, secret):
    params = {
        'client_id': id,
        'client_secret': secret,
        'grant_type': 'client_credentials'
    }
    request = requests.get('https://www.arcgis.com/sharing/rest/oauth2/token',
                           params=params)
    response = request.json()
    token = response["access_token"]
    return token


def expand_window(meter_length, geometry):
    return [geometry[0] - (meter_length / 2), geometry[1] + (meter_length / 2),
            geometry[2] + (meter_length / 2), geometry[3] - (meter_length / 2)]


def download_image(token, bbox, size):
    params = {
        'bbox': f'{bbox[0]}, {bbox[1]}, {bbox[2]}, {bbox[3]}',
        'bboxSR': '102039',
        'size': f'{size}, {size}',
        'imageSR': '102039',
        'format': 'png',
        'transparent': 'false',
        'mapScale': '0',
        'f': 'image'
    }
    headers = {'Authorization': f'Bearer {token}'}
    request = requests.get('https://tiledbasemaps.arcgis.com/arcgis/rest/services/World_Imagery/MapServer/export',
                           params=params,
                           headers=headers)
    return request


if not os.path.exists(args.path):
    print('Creating folder at ', args.path)
    os.makedirs(args.path)

bearer_token = ''
with open(args.credentials, 'r') as creds:
    cred_dict = json.load(creds)
    bearer_token = get_token(cred_dict['id'], cred_dict['secret'])

with open(args.data, 'r') as images:
    length = 30000
    count = 1
    for image in images:
        print(f'\rDownloading Image {count}/{length}', end=' ')
        image_json = ast.literal_eval(image)
        window_size = args.extent
        image_size = math.floor(window_size / 0.3)
        geometry = expand_window(window_size, image_json['geo'])
        file = open(f'{args.path}/{image_json["ident"]}_{image_json["value"]}.png', 'wb')
        request = download_image(bearer_token, geometry, image_size)
        file.write(request.content)
        file.close()
        count += 1
