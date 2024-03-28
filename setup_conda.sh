#!/bin/bash

conda install -y gcc_linux-64==11.2.0
wait
conda install -y gxx_linux-64==11.2.0
wait
conda install -y scons
wait
conda install -y pytorch
wait
conda install -y transformers
wait
conda install -y pandas
wait
conda install -y cmake
wait
conda install -y pybind11
wait
cd ..
chmod -R 777 llm-for-cpu
cd llm-for-cpu