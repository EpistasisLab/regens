subpops = ['ACB', 'GBR']

for pop in subpops:
    file = open("correctness_testing_" + pop + "/regens_automated_tests_optional_part2_LD_getter_" + pop + ".sh", "w")
    file.write("#!/bin/bash\n")
    file.write("#BSUB -J automated_tests_part2_" + pop + "\n")
    file.write("#BSUB -o automated_tests_part2_" + pop + ".out\n")
    file.write("#BSUB -e automated_tests_part2_" + pop + ".err\n")
    file.write('#BSUB -R "rusage[mem=50000MB]"\n')
    file.write("#BSUB -M 50000MB\n")
    file.write("source activate PyTriadsim\n")
    file.write("module load plink/1.90Beta6.18\n\n")

    for chr in range(1,23):
        file.write("plink --bfile ../input_files/" + pop + " --chr " + str(chr))
        file.write(" --make-bed --out " + pop + "_chr" + str(chr) + "\n")
    file.write("\n")
    
    for chr in range(1,23):
        file.write("plink --bfile " + pop + "_chr" + str(chr))
        file.write(" --r --keep-allele-order --ld-window-kb 200 --ld-window 1000000 --with-freqs --ld-window-r2 0")
        file.write(" --out " + pop + "_chr" + str(chr) + "\n")
    file.write("\n")

    for chr in range(1,23):
        file.write("plink --bfile " + pop + "_simulated_chr" + str(chr))
        file.write(" --r --keep-allele-order --ld-window-kb 200 --ld-window 1000000 --with-freqs --ld-window-r2 0")
        file.write(" --out " + pop + "_simulated_chr" + str(chr) + "\n")
    file.write("\n")

    file.write("python regens_LD_getter.py --ref " + pop + " --sim " + pop + "_simulated")

    file.write("\n\n")
    for chr in range(1,23):
        file.write("rm " + pop + "_simulated_chr" + str(chr) + ".ld\n")
        file.write("rm " + pop + "_simulated_chr" + str(chr) + ".log\n")
        for end in [".bed\n", ".bim\n", ".fam\n", ".log\n", ".ld\n"]:
            file.write("rm " + pop + "_chr" + str(chr) + end)


    file.close()