import ray
import time

from ray import serve


@serve.deployment(route_prefix="/opportunity")
class ReforestationModel:
    def __init__(self):
        import json
        import requests

    async def __call__(self, starlette_request):
        return '{"prediction": 69}'


ray.init('ray://ray-ray-head:10001')
serve.start()
ReforestationModel.deploy()

while True:
    time.sleep(5)
    print(serve.list_deployments())
