$Env:CONDA_EXE = "/mnt/c/Users/aej45/Desktop/llm-for-cpu/miniconda/bin/conda"
$Env:_CE_M = ""
$Env:_CE_CONDA = ""
$Env:_CONDA_ROOT = "/mnt/c/Users/aej45/Desktop/llm-for-cpu/miniconda"
$Env:_CONDA_EXE = "/mnt/c/Users/aej45/Desktop/llm-for-cpu/miniconda/bin/conda"
$CondaModuleArgs = @{ChangePs1 = $True}
Import-Module "$Env:_CONDA_ROOT\shell\condabin\Conda.psm1" -ArgumentList $CondaModuleArgs

Remove-Variable CondaModuleArgs