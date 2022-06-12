import ray
from ray import serve
import time

ray.init("ray://ray-ray-head:10001")

# This will start Ray locally and start Serve on top of it.
serve.start()

@serve.deployment
def my_func(request):
  return "hello"

my_func.deploy()

# Serve will be shut down once the script exits, so keep it alive manually.
while True:
    time.sleep(5)
    print(serve.list_deployments())

