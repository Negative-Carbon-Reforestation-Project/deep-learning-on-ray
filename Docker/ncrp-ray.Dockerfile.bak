FROM rayproject/ray:latest
USER root
RUN pip install --no-input tensorflow
RUN conda install fiona
RUN conda install rasterio
RUN conda install -c conda-forge rvlib
RUN pip install --no-input georasters
RUN mkdir $HOME/models
ADD https://raw.githubusercontent.com/Negative-Carbon-Reforestation-Project/deep-learning-on-ray/main/models/mnist_model.h5 $HOME/models/