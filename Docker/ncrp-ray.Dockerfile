FROM rayproject/ray:latest
USER root
RUN pip install --no-input tensorflow
RUN pip install --no-input pyproj
RUN mkdir $HOME/models
RUN mkdir $HOME/resources
ADD https://raw.githubusercontent.com/Negative-Carbon-Reforestation-Project/deep-learning-on-ray/main/models/ncrp_reforestation_alpha.h5 $HOME/models/
ADD https://pastebin.com/jX3CFUi4 $HOME/resources/