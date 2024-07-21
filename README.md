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
* Run `eval "$(tools/miniconda/bin/conda shell.bash hook)"` then `conda activate base` in the `llm-for-cpu` directory

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

## Converting Models to GGML
* For the pre-converted model, download the file here https://drive.google.com/file/d/18AMelftxunpJeBbbfbJq2O5E_OoZMNV-/view?usp=sharing and place it in `llm-for-cpu/tools/bert.cpp/models`
* Otherwise, run `git clone https://huggingface.co/distilbert/distilbert-base-uncased-finetuned-sst-2-english` in the `llm-for-cpu/tools/bert.cpp/models` directory
* Run `./run_conversions.sh distilbert-base-uncased-finetuned-sst-2-english` in the `llm-for-cpu/tools/bert.cpp/models` directory
* NOTE: This can be used to convert a wide range of language models to GGML, but you'll have to modify `convert-to-ggml.py` and `bert.cpp` to properly convert and read-in the model
  * Both `convert-to-ggml.py` and `bert.cpp` contain a commented out example of how to convert and run MiniLM
    * https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
    * https://huggingface.co/sentence-transformers/multi-qa-MiniLM-L6-cos-v1

## Generating Input Parameter Batches
* Run `python sample_params.py <num_batches> <num_samples_per_batch>` in the `llm-for-cpu/tools/bert.cpp/input_params` directory
  * The batches will be created in `llm-for-cpu/tools/bert.cpp/input_params/batches`

## Enabling Simulation Warmup
* Run `scons build/x86/out/m5` in `llm-for-cpu/util/m5`
* Change the absolute path on line 28 in `llm-for-cpu/tools/bert.cpp/examples/CMakeLists.txt` to your own path
* Re-build the `fp16_dot` binary

## Simulating with Input Parameter Batches
* Run `./run_batches <num_batches> <batch_size>` in the `llm-for-cpu` directory
 * NOTE: `batch_size` is formatted as multiples of 1000
 * This will by default read from `tools/bert.cpp/input_params/batches`, so either make sure the files are located there or modify `run_batches` to point to your input data directory

## Simulating Entire Inference Binary
* Change the `params.model` variable at the beginning of main in `tools/bert.cpp/examples/main.cpp` to your local path to `distilbert-base-uncased-finetuned-sst-2-english/ggml-model-f16.bin`
 * Use `ggml-model-f32.bin` to run with 32-bit weights
* Replace the paths in the following `target_link_libraries` with your local `libm5.a` path:
 * `tools/bert.cpp/CMakeLists.txt` line 208
 * `tools/bert.cpp/example/CMakeLists.txt` lines 28, 31
 * `tools/bert.cpp/ggml/src/CMakeLists.txt` lines 277, 279, 287, 310, 319
* Run `build/X86/gem5.opt --outdir=<output/output_dir> scripts/simple.py` to see how far you can get into execution

## Running Bert SST in C++
* Run `cmake .. -DBUILD_SHARED_LIBS=OFF -DCMAKE_BUILD_TYPE=Release` in the `llm-for-cpu/tools/bert.cpp/build` directory
* Run `make` in the `llm-for-cpu/tools/bert.cpp/build` directory
* Run `./main` in the `llm-for-cpu/tools/bert.cpp/build/bin` directory
* This will also create `fp16_dot` in `llm-for-cpu/tools/bert.cpp/build/bin` which will only run the dot product trace
