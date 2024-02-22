#include <iostream>
#include <vector>
#include <pybind11/embed.h> // everything needed for embedding

using namespace std;
namespace py = pybind11;

// Run Vtune 
// . /opt/intel/oneapi/setvars.sh
// vtune -collect hotspots ./example
// vtune -report hotspots -r r001hs -report-output hotspot_results

// vtune -collect performance-snapshot ./example
// vtune -report performance-snapshot -r r000ps -report-output performance_snapshot_results

int main() {
	
	cout << endl << "Starting Interpreter..." << endl;
    py::scoped_interpreter guard{};
	cout << "Interpreter Started Successfully!" << endl << endl;
	
	// Add local packages to system path
	py::module sys = py::module::import("sys");
	sys.attr("path").attr("append")("/home/jeorgebusch/.local/lib/python3.8/site-packages");
	
	// Set OpenBLAS thread limit enviornment variable if null
	if (const char* env_p = std::getenv("OPENBLAS_NUM_THREADS"))
        std::cout << "OPENBLAS_NUM_THREADS is: " << env_p << '\n';
	else{
		putenv("OPENBLAS_NUM_THREADS=1");
		std::cout << "OPENBLAS_NUM_THREADS is: " << std::getenv("OPENBLAS_NUM_THREADS") << '\n';
	}
	
	cout << endl << "Importing Modules..." << endl << endl;
	
	// Import transformers
	cout << endl << "Importing Transformers..." << endl; 
	auto transformers = py::module::import("transformers");
	cout << "Loaded Transformers Successfully!" << endl;
	cout << "Path: " << transformers.attr("__file__").cast<std::string>() << endl << endl;
	
	// Import DistilBert tokenizer
	cout << endl << "Importing DistilBertTokenizer..." << endl; 
    auto DistilBertTokenizer =  transformers.attr("DistilBertTokenizer");
	cout << "Loaded DistilBertTokenizer from Transformers Successfully!" << endl << endl;
	
	// Retrieve DistilBert tokenizer
	cout << endl << "Retrieving Tokenizer: distilbert-base-uncased-finetuned-sst-2-english" << endl; 
	auto tokenizer = DistilBertTokenizer.attr("from_pretrained")("/mnt/c/Users/aej45/Desktop/llm-for-cpu/scripts/embed_python/distilbert-base-uncased-finetuned-sst-2-english");
	//auto tokenizer = DistilBertTokenizer.attr("from_pretrained")(py::arg("tokenizer_file")="/mnt/c/Users/aej45/Desktop/llm-for-cpu/scripts/embed_python/distilbert-base-uncased-finetuned-sst-2-english");
	cout << "Tokenizer Retrieved SUccessfully!" << endl << endl;
	
	// Import DistilBert model
	cout << endl << "Importing DistilBertForSequenceClassification..." << endl;
	auto DistilBertForSequenceClassification =  transformers.attr("DistilBertForSequenceClassification");
	cout << "Loaded DistilBertForSequenceClassification from Transformers Successfully!" << endl << endl;
	
	// Retrieve DistilBert model
	cout << endl << "Retrieving Model: distilbert-base-uncased-finetuned-sst-2-english" << endl;
	auto model = DistilBertForSequenceClassification.attr("from_pretrained")("/mnt/c/Users/aej45/Desktop/llm-for-cpu/scripts/embed_python/distilbert-base-uncased-finetuned-sst-2-english");
	//auto model = DistilBertTokenizer.attr("from_pretrained")(py::arg("tokenizer_file")="/mnt/c/Users/aej45/Desktop/llm-for-cpu/scripts/embed_python/distilbert-base-uncased-finetuned-sst-2-english");
	cout << "Model Retrieved Successfully!" << endl << endl;
	
	cout << endl << "Importing Numpy" << endl;
	auto np = py::module::import("numpy");
	cout << "Path: " << np.attr("__file__").cast<std::string>() << endl << endl;
	cout << "Loaded NumPy Successfully!" << endl << endl;
	
	cout << endl << "Importing Pandas" << endl;
	auto pd = py::module::import("pandas");
	cout << "Loaded Pandas Successfully!" << endl;
	cout << "Path: " << pd.attr("__file__").cast<std::string>() << endl << endl;
	
	cout << endl << "Importing Torch..." << endl;
	py::module torch = py::module::import("torch");
	cout << "Loaded Torch Successfully!" << endl;
	cout << "Path: " << torch.attr("__file__").cast<std::string>() << endl << endl;	
	
	
	// Import transformers
	
	// Import DistilBert tokenizer
	
	// Import DistilBert model

	
	cout << "All Modules Loaded Successfully!" << endl << endl;
	
	// Retrieve DistilBert tokeinzer and model
	// Retrieve DistilBert tokenizer
	
	// Retrieve DistilBert model

	
	// Reading tsv file as
	auto df = pd.attr("read_csv")("/mnt/c/Users/aej45/Desktop/gem5/gem5-21.2.1.1/scripts/embed_python/build/dev.tsv", py::arg("sep")="\t");
	auto features = df["sentence"];
	auto labels = df["label"];
	
	// Converting pandas dataframes into python lists then std::vectors 
	// THERE HAS TO BE A BETTER WAY TO DO THIS
	py::list f = features.attr("tolist")();
	py::list l = labels.attr("tolist")();
	vector<string> features_vec;
	for (py::handle obj : f) {
		features_vec.push_back(obj.attr("__str__")().cast<std::string>());
    }
	vector<string> labels_vec;
	for (py::handle obj : l) {
		labels_vec.push_back(obj.attr("__str__")().cast<std::string>());
    }
	
	float correct = 0;
	float num = 0;
	float tp = 0;
	float fp = 0;
	float tn = 0;
	float fn = 0;
	
	for (int i = 0; i < features_vec.size(); i ++){
		auto inputs = tokenizer(features_vec.at(i), py::arg("return_tensors") = "pt");
		
		int preds = model(py::arg("input_ids") = inputs["input_ids"]).attr("logits").attr("argmax")().attr("item")().cast<int>();
		
		if (stoi(labels_vec.at(i)) == 0 && preds == 0)
			tn += 1;
		if (stoi(labels_vec.at(i)) == 0 && preds == 1)
			fp += 1;
		if (stoi(labels_vec.at(i)) == 1 && preds == 0)
			fn += 1;
		if (stoi(labels_vec.at(i)) == 1 && preds == 1)
			tp += 1;
	}
	
	float acc = ((tp + tn) / (tp + fp + tn + fn)) * 100;
	float tpr = (tp / (tp + fn)) * 100;
	float fpr = (fp / (fp + tn)) * 100;
	
	cout << "Accuracy: " << acc << endl;
	cout << "TPR: " << tpr << endl;
	cout << "FPR: " << fpr << endl;
	
}