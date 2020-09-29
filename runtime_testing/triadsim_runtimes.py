import numpy as np
import pdb

def get_run_info(runtimes_info_path):
    runtimes_info = open(runtimes_info_path, "r").read()
    max_index = len(runtimes_info) -1
    next_index = 0
    runtime_vals = []
    max_ram_vals = []
    while next_index <= max_index:
        try:
            pos_before_index = runtimes_info.index("CPU time :", next_index)
            pos_after_index = runtimes_info.index(" sec.", pos_before_index) 
            runtime_val = runtimes_info[(pos_after_index - 9):pos_after_index]
            if runtime_val[0] == " ":
                runtime_vals.append(float(runtime_val[1:]))
            else: 
                print("ERROR: runtime much longer than expected")
                exit()
        
            pos_before_index = runtimes_info.index("Max Memory :", next_index)
            pos_after_index = runtimes_info.index(" MB", pos_before_index) 
            max_ram_val = runtimes_info[(pos_after_index - 9):pos_after_index]
            if runtime_val[0] == " ":
                max_ram_vals.append(int(max_ram_val[1:]))
            else: 
                print("ERROR: max_ram much longer than expected")
                exit()

            next_index = pos_after_index
        except: 
            next_index = max_index + 1

    return(np.array(runtime_vals), np.array(max_ram_vals))

def bootstrap_improvement_ratio(triadsim_vals, regens_vals, N):
    resampled_vals_triadsim = triadsim_vals[(np.random.rand(N, len(triadsim_vals))*len(triadsim_vals)).astype(np.int)]
    resampled_vals_regens = regens_vals[(np.random.rand(N, len(regens_vals))*len(regens_vals)).astype(np.int)]
    resampled_improvement_ratios = np.mean(resampled_vals_triadsim, axis = 1)/np.mean(resampled_vals_regens, axis = 1)
    mean = np.mean(triadsim_vals)/np.mean(regens_vals)
    low = np.percentile(resampled_improvement_ratios, 2.5)
    high = np.percentile(resampled_improvement_ratios, 97.5)
    return([low, mean, high])

triadsim_runtimes, triadsim_max_rams = get_run_info("triadsim_runtimes.out")
regens_runtimes, regens_max_rams = get_run_info("regens_runtime.out")
print(bootstrap_improvement_ratio(triadsim_runtimes, regens_runtimes, 1000000))
print(bootstrap_improvement_ratio(triadsim_max_rams, regens_max_rams, 1000000))
