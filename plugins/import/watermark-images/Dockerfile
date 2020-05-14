ARG SLY_LIB_PATH
ARG REGISTRY
ARG TAG
FROM ${REGISTRY}/base-py:${TAG}

############### copy code ###############
ARG MODULE_PATH
COPY $MODULE_PATH /workdir
COPY $SLY_LIB_PATH /workdir/supervisely_lib
##### Fonts for watermarking #####
COPY fonts /workdir/fonts
##### FSOCO JSON template meta file #####
COPY meta.json /workdir/src

ENV PYTHONPATH /workdir:/workdir/src:/workdir/supervisely_lib/worker_proto:$PYTHONPATH
WORKDIR /workdir/src
