cmake -S . -B build
wait
cmake --build build -j 1
wait
cmake --install build
wait
cp ../dev.tsv build/dev.tsv