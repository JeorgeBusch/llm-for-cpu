#!/bin/bash

conda install -y gcc_linux-64==11.2.0
wait
conda install -y gxx_linux-64==11.2.0
wait
conda install -y scons
wait
conda install pytorch
wait
conda install transformer
wait
conda install pandas
wait
conda install cmake
wait
cd ..
chmod -R 777 llm-for-cpu
cd llm-for-cpu