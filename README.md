# llm-for-cpu
## Building Miniconda
* Download the file here https://drive.google.com/file/d/1dscF494qws0R5bMBqsBkIA1vrcUk-eZc/view?usp=sharing
* Drop the file in `llm-for-cpu/tools` and CD into it
* Run `Chmod 777 Miniconda3-py39_24.1.2-0-Linux-x86_64.sh`
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
* I recommend just doing 1 core for testing purposes since it compiles faster
* If the compilation finishes without errors, you'll use `llm-for-cpu/build/X86/gem5.out` to run the simulator
* If you want to build the simulator with a different instruction set architecture, run `scons build/<arm/mips/riscv/etc.>/gem5.opt -j <num_cores> CC=tools/miniconda/bin/gcc CXX=tools/miniconda/bin/g++ --ignore-style` 

## Running Bert SST in python
* Run `python3 bert_sst.py` in `llm-for-cpu/scripts`
* Install all missing dependencies
* Make sure the execution completes without errors
* You can confirm this if, at the end of execution, you see the TPR, FPR, and Accuracy printed to the console

## Running Bert SST in C++
* Once `bert_sst.py` is running, you should be able to build and run the c++ implementation using cmake in `llm-for-cpu/scripts/embed_python`
* In `llm-for-cpu/scripts/embed_python/bert_sst.cpp`, change the line `sys.attr("path").attr("append")("<path_to_local_python_modules>")` to your local python module path
* You can get your local python module path by opening the linux shell and running the following commands: `python3`, `import numpy`, `print(numpy.__path__)`
* Next, change the line `auto df = pd.attr("read_csv")("<path_to_dev_tsv>", py::arg("sep")="\t")` to the absoloute path to `dev.tsv`
* If you built your Gem5 binary with the default C and C++ on linux, open `CMakeList.txt` and comment out the lines `set(CMAKE_C_COMPILER <path_to_gcc>)` and `set(CMAKE_CXX_COMPILER <path_to_g++>)`
* Otherwise, put your gcc and g++ paths in `CMakeList.txt`
* Run `./embed_interpreter.sh`
* This might also have some unresolved dependencies that you'll have to figure out as well
* Once `./embed_interpreter.sh` executes without error, you'll have a new directory called `build` with the binary `example`
* To execute, all you have to run is `./bert_sst` in `llm-for-cpu/scripts/embed_python/build` and it should produce the same or similar results to `bert_sst.py`

## Running Bert SST in Gem5
* This is still ongoing, so it will error out if you do this, but that's not a problem
* Run `build/X86/gem5.opt --outdir=<output_dir> scripts/simple.py` to see how far you can get into execution before fatal error
* This will take a few hours
* At this point, i have nothing else, so just get familiar with the source code in `llm-for-cpu/src`
* I'm currently working on `llm-for-cpu/src/arch/x86/linux/syscall_tbl64.cc`, `llm-for-cpu/src/sim/syscall_emul.hh`, and `llm-for-cpu/src/sim/syscall_emul.cc` to implement the `sendmmsgFunc` system call
* You can google the name of any syscall and find the linux manual page for it as well as information on usage
