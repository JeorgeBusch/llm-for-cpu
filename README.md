# llm-for-cpu
## Building Miniconda
* Download the file here https://drive.google.com/file/d/1dscF494qws0R5bMBqsBkIA1vrcUk-eZc/view?usp=sharing
* Drop the file in `llm-for-cpu/tools` and CD into it
* Run `chmod 777 Miniconda3-py39_24.1.2-0-Linux-x86_64.sh`
* Run `./Miniconda3-py39_24.1.2-0-Linux-x86_64.sh`
* Go through license agreement and enter `yes`
* When it prompts you for a directory name, enter `miniconda`
* When it asks you to initialize conda, type `no`

## Starting Miniconda
* EVERY TIME you start a new terminal or hprc job, you will have to initialize and activate the Miniconda environment
* Run `source start_conda` to activate your local conda base environment

## Setting Up Enviornment
* This only needs to be done once
* Run `./setup_conda.sh` in the `llm-for-cpu` directory
* Next, run the following commands in the `llm-for-cpu/tools/miniconda/bin` directory
* `ln -s x86_64-conda-linux-gnu-c++ c++`
* `ln -s x86_64-conda-linux-gnu-cc cc`
* `ln -s x86_64-conda-linux-gnu-g++ g++`
* `ln -s x86_64-conda-linux-gnu-gcc gcc`

## Building Gem5 Binary
* Run `scons build/X86/gem5.opt -j <num_cores> CC=tools/miniconda/bin/gcc CXX=tools/miniconda/bin/g++ --ignore-style` in the `llm-for-cpu` directory
* If the compilation finishes without errors, you'll use `llm-for-cpu/build/X86/gem5.out` to run the simulator
* If you want to build the simulator with a different instruction set architecture, run `scons build/<arm/mips/riscv/etc.>/gem5.opt -j <num_cores> CC=tools/miniconda/bin/gcc CXX=tools/miniconda/bin/g++ --ignore-style` 

## Enabling M5 Utils
* Run `scons build/x86/out/m5` in `llm-for-cpu/util/m5`
* Re-build the `main` binary

## Running Bert SST
* Run `cmake .. -DBUILD_SHARED_LIBS=OFF -DCMAKE_BUILD_TYPE=Release` in the `llm-for-cpu/tools/bert.cpp/build` directory
  * Create `llm-for-cpu/tools/bert.cpp/build` if it doesn't exist
* Run `make` in the `llm-for-cpu/tools/bert.cpp/build` directory
* This will also create `main` in `llm-for-cpu/tools/bert.cpp/build/bin` which will run the entire model inference with the input "test prompt" if not otherwise changed

## Simulating Entire BERT Inference Binary
* Run `build/X86/gem5.opt --outdir=<output/output_dir> scripts/simple_caches.py`

## Running Qwen2 Decoder
* Run `cmake -B build` then `cmake --build build --config Release` in `tools/llama.cpp`
  * For re-building in the future, you can simply run `make` in `tools/llama.cpp/build`
* Download the Qwen2 decoder model here: https://drive.google.com/file/d/1WZS0ewshRx_FDy85NTCV_y1-uyEj0bJW/view?usp=sharing and place it in `tools/llama.cpp/models`
  * Create `tools/llama.cpp/models` if it doesn't already exist
* In `scripts/simple_caches.py`, replace the line `binary=` with `tools/llama.cpp/build/bin/llama-cli` then run `build/X86/gem5.opt --outdir=<output/output_dir> scripts/simple_caches.py` to simulate

## Converting Models to GGML
* For the pre-converted model, download the file here https://drive.google.com/file/d/18AMelftxunpJeBbbfbJq2O5E_OoZMNV-/view?usp=sharing and place it in `llm-for-cpu/tools/bert.cpp/models`
* Otherwise, run `git clone https://huggingface.co/distilbert/distilbert-base-uncased-finetuned-sst-2-english` in the `llm-for-cpu/tools/bert.cpp/models` directory
* Run `./run_conversions.sh distilbert-base-uncased-finetuned-sst-2-english` in the `llm-for-cpu/tools/bert.cpp/models` directory
* NOTE: This can be used to convert a wide range of language models to GGML, but you'll have to modify `convert-to-ggml.py` and `bert.cpp` to properly convert and read-in the model
  * Both `convert-to-ggml.py` and `bert.cpp` contain a commented out example of how to convert and run MiniLM
    * https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
    * https://huggingface.co/sentence-transformers/multi-qa-MiniLM-L6-cos-v1
