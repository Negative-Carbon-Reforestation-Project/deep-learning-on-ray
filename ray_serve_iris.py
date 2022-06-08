import time

from sklearn.datasets import load_iris
from sklearn.ensemble import GradientBoostingClassifier

from ray import serve

serve.start()

# Train model.
iris_dataset = load_iris()
model = GradientBoostingClassifier()
model.fit(iris_dataset["data"], iris_dataset["target"])


@serve.deployment(route_prefix="/iris")
class BoostingModel:
    def __init__(self, model):
        self.model = model
        self.label_list = iris_dataset["target_names"].tolist()

    async def __call__(self, request):
        payload = await request.json()
        print(f"Received flask request with data {payload}")

        prediction = self.model.predict([payload["vector"]])[0]
        human_name = self.label_list[prediction]
        return {"result": human_name}


# Deploy model.
BoostingModel.deploy(model)

while True:
    time.sleep(5)
    print(serve.list_deployments())

