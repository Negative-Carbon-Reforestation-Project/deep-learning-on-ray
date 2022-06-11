FROM rayproject/ray:latest
USER root
RUN pip install --no-input sklearn
RUN pip install --no-input tensorflow
RUN mkdir $HOME/models
ADD https://raw.githubusercontent.com/Negative-Carbon-Reforestation-Project/deep-learning-on-ray/main/models/mnist_model.h5 $HOME/models/