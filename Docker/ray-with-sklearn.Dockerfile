FROM rayproject/ray:latest
USER root
RUN pip install --no-input sklearn
RUN pip install --no-input tensorflow