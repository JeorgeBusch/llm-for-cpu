# llm-for-cpu

## Gem5 Compilation
* Run scons build/X86/gem5.opt -j <num_cores> CC=<GCC_dir> CXX=<G++_dir> --ignore-style
* You can exclude the CC= and CXX= arguments if you want to build with your native C and C++
* I recommend just doing 1 core for testing purposes since it compiles faster

## Running Bert SST in python
* CD into scripts directory and run python3 bert_sst.py
* Install all missing dependencies
* Make sure the execution completes with out errors
* You can confirm this if at the end of execution, you'll see the TPR, FPR, and Accuracy printed to console

## Running Bert SST in C++
* Once bert_sst.py is running, you should be able to build and run the c++ implementation using cmake in the embed_python directory
* In test.cpp, change the line sys.attr("path").attr("append")("/home/jeorgebusch/.local/lib/python3.8/site-packages"); to your local python module path
* You can get your local python module path by opening the linux shell, run python, import numpy, print(numpy.__path__)
* Next, change the line auto df = pd.attr("read_csv")("/mnt/c/Users/aej45/Desktop/gem5/gem5-21.2.1.1/scripts/embed_python/build/dev.tsv", py::arg("sep")="\t"); to the absoloute path to dev.tsv
* Open CMakeList.txt and comment out the linse set(CMAKE_C_COMPILER /usr/bin/gcc-10) and set(CMAKE_CXX_COMPILER /usr/bin/g++-10)
* Run ./embed_interpreter.sh
* This might also have some unresolved dependencies that you'll have to figure out as well
* Once ./embed_interpreter.sh executes without error, you'll have a new directory called build in which is the binary called "example"
* To execute, all you have to run is ./example and it should produce the same or similar results to bert_sst.py

## Running Bert SST in Gem5
* This is still ongoing, so it will error out if you do this, but that's not a problem
* Run build/X86/gem5.opt --outdir=<output_dir> scripts/simple.py too see how far you can get into execution before fatal error
* This will take a few hours
