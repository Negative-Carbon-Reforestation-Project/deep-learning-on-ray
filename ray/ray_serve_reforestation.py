from pyproj import Proj, transform

import ray
import time
import json
import requests
import tensorflow as tf
import numpy as np
import io

from PIL import Image
from ray import serve

@serve.deployment(route_prefix="/opportunity")
class ReforestationModel:
    def __init__(self):
        import json
        import requests
        import tensorflow as tf
        import numpy as np
        import io

        from PIL import Image
        from pyproj import Proj, transform

    async def __call__(self, starlette_request):
        request = await starlette_request.body()
        longitude = float(request['longitude'])
        latitude = float(request['latitude'])

        with open('.resources/arcGIS.cred', 'r') as creds:
            cred_dict = json.load(creds)
            print(cred_dict)
            params = {
                'client_id': cred_dict['id'],
                'client_secret': cred_dict['secret'],
                'grant_type': 'client_credentials'
            }
            request = requests.get('https://www.arcgis.com/sharing/rest/oauth2/token',
                                   params=params)
            response = request.json()
            token = response["access_token"]

        inProj = Proj(init='epsg:4326')
        outProj = Proj(init='epsg:5070')
        long, lat = transform(inProj, outProj, long, lat)
        bbox = [long, lat,
                long + 210, lat - 210]

        params = {
            'bbox': f'{bbox[0]}, {bbox[1]}, {bbox[2]}, {bbox[3]}',
            'bboxSR': '102039',
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
        image = np.array(Image.open(io.BytesIO(request.content)))

        image = np.divide(image, 255)
        image = image.reshape(1, 300, 300)
        model = tf.keras.models.load_model('./models/ncrp_reforestation_alpha.h5')
        prediction = model(image)
        prediction.numpy().argmax() * 0.1
        return {"prediction": prediction.numpy().argmax() * 0.1}




ray.init('ray://ray-ray-head:10001')
serve.start(http_options={'host': '0.0.0.0'})
ReforestationModel.deploy()

while True:
    time.sleep(5)
    print(serve.list_deployments())
