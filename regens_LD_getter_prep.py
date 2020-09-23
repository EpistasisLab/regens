subpops = ['ACB', 'GBR']

for pop in subpops:
    file = open("regens_automated_tests_optional_part2_LD_getter_" + pop + ".sh", "w")
    file.write("#!/bin/bash\n")
    file.write("#BSUB -J automated_tests_part2_" + pop + "\n")
    file.write("#BSUB -o automated_tests_" + pop + "_output/automated_tests_part2_" + pop + ".out\n")
    file.write("#BSUB -e automated_tests_" + pop + "_output/automated_tests_part2_" + pop + ".err\n")
    file.write('#BSUB -R "rusage[mem=50000MB]"\n')
    file.write("#BSUB -M 50000MB\n")
    file.write("source activate PyTriadsim\n")
    file.write("module load plink/1.90Beta6.18\n\n")

    for chr in range(1,23):
        file.write("plink --bfile " + pop + " --chr " + str(chr))
        file.write(" --make-bed --out automated_tests_" + pop + "_output/" + pop + "_chr" + str(chr) + "\n")
    file.write("\n")
    
    for chr in range(1,23):
        file.write("plink --bfile automated_tests_" + pop + "_output/" + pop + "_chr" + str(chr))
        file.write(" --r --keep-allele-order --ld-window-kb 200 --ld-window 1000000 --with-freqs --ld-window-r2 0")
        file.write(" --out automated_tests_" + pop + "_output/" + pop + "_chr" + str(chr) + "\n")
    file.write("\n")

    for chr in range(1,23):
        file.write("plink --bfile automated_tests_" + pop + "_output/" + pop + "_simulated_chr" + str(chr))
        file.write(" --r --keep-allele-order --ld-window-kb 200 --ld-window 1000000 --with-freqs --ld-window-r2 0")
        file.write(" --out automated_tests_" + pop + "_output/" + pop + "_simulated_chr" + str(chr) + "\n")
    file.write("\n")

    file.write("python automated_tests_" + pop + "_output/regens_LD_getter.py --ref automated_tests_" + pop + "_output/" + pop + " --sim automated_tests_" + pop + "_output/" + pop + "_simulated")

    file.write("\n\n")
    for chr in range(1,23):
        file.write("rm automated_tests_" + pop + "_output/" + pop + "_simulated_chr" + str(chr) + ".ld\n")
        for end in [".bed\n", ".bim\n", ".fam\n", ".log\n", ".ld\n"]:
            file.write("rm automated_tests_" + pop + "_output/" + pop + "_chr" + str(chr) + end)


    file.close()