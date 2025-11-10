#!/usr/bin/env bash
export CONTAINERD_ENABLE_DEPRECATED_PULL_SCHEMA_1_IMAGE=1

SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"

# ./build.sh

DOCKER_FILE_SHARE=$(pwd)/output_debug
mkdir -p $DOCKER_FILE_SHARE

# Inference
docker run --cpus=4 --memory=32gb --shm-size=32gb --rm \
        -v $SCRIPTPATH/test/:/input/ \
        -v $DOCKER_FILE_SHARE:/output/ \
        picai_baseline_nnunet_processor

# Validation - Segmentation mask
docker run --rm \
    -v $DOCKER_FILE_SHARE:/output/ \
    -v $SCRIPTPATH/test/:/input/ \
    python:3.10-slim bash -c "pip install -q SimpleITK numpy && python -c \"import sys, numpy as np, SimpleITK as sitk; f1 = sitk.GetArrayFromImage(sitk.ReadImage('/output/images/cspca-detection-map/cspca_detection_map.mha')); f2 = sitk.GetArrayFromImage(sitk.ReadImage('/input/cspca-detection-map/10032_1000032.mha')); diff = np.sum(np.abs(f1-f2)>1e-3); print('N/o voxels more than 1e-3 different between prediction and reference:', diff); sys.exit(int(diff > 10))\""

if [ $? -eq 0 ]; then
    echo "Detection map test successfully passed..."
else
    echo "Expected detection map was not found..."
fi

# Validation - Confidence Score
docker run --rm \
    -v $DOCKER_FILE_SHARE:/output/ \
    -v $SCRIPTPATH/test/:/input/ \
    python:3.10-slim bash -c "pip install -q numpy && python -c \"import sys, json; f1 = json.load(open('/output/cspca-case-level-likelihood.json')); f2 = json.load(open('/input/cspca-detection-map/10032_1000032.json')); print(f'Found case-level prediction {f1}, expected {f2}'); sys.exit(int(abs(f1-f2) > 1e-3))\""


if [ $? -eq 0 ]; then
    echo "Case-level prediction test successfully passed..."
else
    echo "Expected case-level prediction was not found..."
fi
