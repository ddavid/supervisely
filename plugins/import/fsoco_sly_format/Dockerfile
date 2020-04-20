ARG REGISTRY
ARG TAG
FROM ${REGISTRY}/base-py:${TAG}

############### copy code ###############
ARG MODULE_PATH
COPY ${MODULE_PATH} /workdir
##### Fonts for watermarking #####
COPY fonts /workdir/fonts

ENV PYTHONPATH /workdir:/workdir/src:/workdir/supervisely_lib/worker_proto:$PYTHONPATH
WORKDIR /workdir/src