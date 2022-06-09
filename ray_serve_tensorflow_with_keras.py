import ray
from ray import serve

import os
import time
import numpy as np

@serve.deployment(route_prefix="/mnist")
class TFMnistModel:
    def __init__(self, model_path):
        import tensorflow as tf

        self.model_path = model_path
        self.model = tf.keras.models.load_model(model_path)

    async def __call__(self, starlette_request):
        # Step 1: transform HTTP request -> tensorflow input
        # Here we define the request schema to be a json array.
        input_array = np.array((await starlette_request.json())["array"])
        reshaped_array = input_array.reshape((1, 28, 28))

        # Step 2: tensorflow input -> tensorflow output
        prediction = self.model(reshaped_array)

        # Step 3: tensorflow output -> web output
        return {"prediction": prediction.numpy().tolist(), "file": self.model_path}


ray.init('ray://ray-ray-head:10001')
serve.start()
TFMnistModel.deploy('./models/mnist_model.h5')

while True:
    time.sleep(5)
    print(serve.list_deployments())