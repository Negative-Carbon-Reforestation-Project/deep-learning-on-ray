FROM rayproject/ray:latest
USER root
ADD https://raw.githubusercontent.com/Negative-Carbon-Reforestation-Project/deep-learning-on-ray/main/environment.yml $HOME/deps/
RUN conda env create -f /home/ray/deps/environment.yml
RUN conda init bash
