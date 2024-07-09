#include "bert.h"
#include "ggml.h"

#include <gem5/m5ops.h>

#include <unistd.h>
#include <stdio.h>
#include <vector>
#include <iostream>
#include <fstream>
#include <string>
#include <iterator>
#include <sstream>
#include <algorithm>

#define GGML_FP16_TO_FP32(x) ((float) (x))

using namespace std;

typedef double ggml_float;

extern "C" {
	static void ggml_vec_dot_f16(const int n, float *  s, ggml_fp16_t *  x, ggml_fp16_t *  y) {
		
		ggml_float sumf = 0.0;
	
	#if defined(GGML_SIMD)
		const int np = (n & ~(GGML_F16_STEP - 1));
	
		GGML_F16_VEC sum[GGML_F16_ARR] = { GGML_F16_VEC_ZERO };
	
		GGML_F16_VEC ax[GGML_F16_ARR];
		GGML_F16_VEC ay[GGML_F16_ARR];
	
		for (int i = 0; i < np; i += GGML_F16_STEP) {
			for (int j = 0; j < GGML_F16_ARR; j++) {
				ax[j] = GGML_F16_VEC_LOAD(x + i + j*GGML_F16_EPR, j);
				ay[j] = GGML_F16_VEC_LOAD(y + i + j*GGML_F16_EPR, j);
	
				sum[j] = GGML_F16_VEC_FMA(sum[j], ax[j], ay[j]);
			}
		}
	
		// reduce sum0..sum3 to sum0
		GGML_F16_VEC_REDUCE(sumf, sum);
	
		// leftovers
		for (int i = np; i < n; ++i) {
			sumf += (ggml_float)(GGML_FP16_TO_FP32(x[i])*GGML_FP16_TO_FP32(y[i]));
		}
	#else
		for (int i = 0; i < n; ++i) {
			sumf += (ggml_float)(GGML_FP16_TO_FP32(x[i])*GGML_FP16_TO_FP32(y[i]));
		}
	#endif
	
		*s = sumf;
	}
};

int main(int argc, char ** argv) {	
	if (argc == 1){
		cout << "Not enough arguments: Include path to parameter list." << endl;
		return 0;
	}
	ifstream file(argv[1]);
	if (file.fail()){
		cout << "Failed to open file: Check file name." << endl;
		return 0;
	}

	string line; 
	string delimiter = "\t";
	
	int n;
	float s[2];
	ggml_fp16_t x[4];
	ggml_fp16_t y[4];
	int warmup_iter = 0;
	
	printf("Warming Up...\n");
	// WARMUP
    while (getline(file, line) && warmup_iter < 1000) { 
		size_t pos = 0;
		std::string token;
		int count = 0;
		while ((pos = line.find(delimiter)) != std::string::npos) {
			token = line.substr(0, pos);
			line.erase(0, pos + delimiter.length());
			if (count == 0)
				n = stoi(token);

			else if (count == 1){
				istringstream ss( token );
				copy(
					istream_iterator <float> ( ss ),
					istream_iterator <float> (),
					s
					);
			}
			else if (count == 2){
				istringstream ss( token );
				copy(
					istream_iterator <float> ( ss ),
					istream_iterator <float> (),
					x
					);
			}
			count += 1;
		}
		istringstream ss( line );
		copy(
			istream_iterator <float> ( ss ),
			istream_iterator <float> (),
			y
			);
		
		ggml_vec_dot_f16(n, s, x, y);
		warmup_iter += 1;
    } 
	
	file.clear();
	file.seekg(0);
	
	#ifdef GEM5
		m5_reset_stats(0, 0);
	#endif
	
	printf("Running Parameters...\n");
	while (getline(file, line)) { 
		size_t pos = 0;
		std::string token;
		int count = 0;
		while ((pos = line.find(delimiter)) != std::string::npos) {
			token = line.substr(0, pos);
			line.erase(0, pos + delimiter.length());
			if (count == 0)
				n = stoi(token);

			else if (count == 1){
				istringstream ss( token );
				copy(
					istream_iterator <float> ( ss ),
					istream_iterator <float> (),
					s
					);
			}
			else if (count == 2){
				istringstream ss( token );
				copy(
					istream_iterator <float> ( ss ),
					istream_iterator <float> (),
					x
					);
			}
			count += 1;
		}
		istringstream ss( line );
		copy(
			istream_iterator <float> ( ss ),
			istream_iterator <float> (),
			y
			);
		
		ggml_vec_dot_f16(n, s, x, y);
    } 
    file.close();
	
	

    return 0;
}