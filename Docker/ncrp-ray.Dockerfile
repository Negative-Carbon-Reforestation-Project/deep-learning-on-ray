FROM rayproject/ray:latest
USER root
RUN pip install --no-input tensorflow
RUN pip install --no-input pyproj
RUN mkdir $HOME/models
RUN mkdir $HOME/resources
ADD https://raw.githubusercontent.com/Negative-Carbon-Reforestation-Project/deep-learning-on-ray/main/models/ncrp_reforestation_alpha.h5 $HOME/models/
ADD https://gist.githubusercontent.com/liamstar97/f2bf19b7af973a9e826d919cb8a648f6/raw/0e9a685c483b408fd91342bbc98b80001e2ff70e/arcGIS.cred $HOME/resources/