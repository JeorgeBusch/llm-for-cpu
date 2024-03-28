$Env:CONDA_EXE = "/scratch/user/averyjohnson/llm-for-cpu/tools/miniconda/bin/conda"
$Env:_CE_M = ""
$Env:_CE_CONDA = ""
$Env:_CONDA_ROOT = "/scratch/user/averyjohnson/llm-for-cpu/tools/miniconda"
$Env:_CONDA_EXE = "/scratch/user/averyjohnson/llm-for-cpu/tools/miniconda/bin/conda"
$CondaModuleArgs = @{ChangePs1 = $True}
Import-Module "$Env:_CONDA_ROOT\shell\condabin\Conda.psm1" -ArgumentList $CondaModuleArgs

Remove-Variable CondaModuleArgs