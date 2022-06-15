FROM rayproject/ray:latest
USER root
RUN pip install --no-input tensorflow
RUN pip install --no-input pyproj
RUN mkdir $HOME/models
RUN mkdir $HOME/resources
COPY ncrp-reforestation_alpha.h5 $HOME/models/
ADD https://pastebin.com/jX3CFUi4 $HOME/resources/