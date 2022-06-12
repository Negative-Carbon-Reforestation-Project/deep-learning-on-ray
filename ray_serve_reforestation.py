import ray
import time
import json
import requests

from ray import serve

def refresh_token():
    with open('./resources/arcGIS.cred', 'r') as creds:
        cred_dict = json.load(creds)
        return get_token(cred_dict['id'], cred_dict['secret'])


def get_token(secret):
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


def download_image(token, bbox):
    params = {
        'bbox': f'{bbox[0]}, {bbox[1]}, {bbox[2]}, {bbox[3]}',
        'bboxSR': '4326',
        'size': f'300, 300',
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
    return request.content


def solve_geometry(long, lat):
    # TODO: return bbox given long and lat
    return [long, lat,
            long + 80, lat + 80]


@serve.deployment(route_prefix="/opportunity")
class ReforestationModel:
    def __init__(self):
        import json
        import requests

    async def __call__(self, starlette_request):
        request = await starlette_request.body()
        longitude = request['longitude']
        latitude = request['latitude']
        token = refresh_token()
        bbox = solve_geometry(longitude, latitude)
        image = download_image(token, bbox)
        # TODO: add prediction from image.
        return "{'prediction': [[1]]}"


ray.init('ray://ray-ray-head:10001')
serve.start()
ReforestationModel.deploy()

while True:
    time.sleep(5)
    print(serve.list_deployments())
