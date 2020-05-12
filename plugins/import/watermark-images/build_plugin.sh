#!/usr/bin/env bash

REGISTRY=$1
OWN_REGISTRY=$2
MODULE_PATH=$3
SLY_LIB_PATH=$4

VERSION_FILE=$(cat "${MODULE_PATH}/VERSION")
IMAGE_NAME=${VERSION_FILE%:*}
OWN_TAG=${VERSION_FILE#*:}

DOCKER_IMAGE=${OWN_REGISTRY}/${IMAGE_NAME}:${OWN_TAG}


MODES_ARR=()
for mode in main train inference deploy deploy_smart; do
	[[ -f "${MODULE_PATH}/src/${mode}.py" ]] && MODES_ARR+=( ${mode} )
done
MODES=${MODES_ARR[@]}

function get_file_content () {
	[[ -f "$1" ]] && echo $(base64 $1 | tr -d \\n) || echo ""
}

docker build \
	--label "VERSION=${DOCKER_IMAGE}" \
	--label "INFO=$(get_file_content "${MODULE_PATH}/plugin_info.json")" \
	--label "MODES=${MODES}" \
	--label "README=$(get_file_content "${MODULE_PATH}/README.md")" \
	--label "CONFIGS=$(get_file_content "${MODULE_PATH}/predefined_run_configs.json")" \
	--build-arg "MODULE_PATH=${MODULE_PATH}" \
	--build-arg "REGISTRY=${REGISTRY}" \
	--build-arg "TAG=latest" \
	--build-arg "SLY_LIB_PATH=~/github-repos/supervisely/supervisely_lib" \
	-f "${MODULE_PATH}/Dockerfile" \
	-t ${DOCKER_IMAGE} \
	.

echo "---------------------------------------------"
echo ${DOCKER_IMAGE}
