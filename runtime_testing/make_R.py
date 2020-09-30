import pdb

next_r_file_content = open("triadsim1.R", "r").read()
for i in range(2,11):
    next_r_file_content = next_r_file_content[:418] + str(i) + next_r_file_content[(419 + len(str(i-1)) - 1):]
    next_r_file = open("triadsim" + str(i) + ".R", "w")
    next_r_file.write(next_r_file_content)
    next_r_file.close()
    
next_sh_file_content = open("triadsim1.sh", "r").read()
for i in range(2,11):
    next_sh_file_content = next_sh_file_content[:164] + str(9 + i) + next_sh_file_content[166:-(3 + len(str(i - 1)) -  1)] + str(i) + ".R" 
    next_sh_file = open("triadsim" + str(i) + ".sh", "w")
    next_sh_file.write(next_sh_file_content)
    next_sh_file.close()

next_sh_file_content = open("regens1.sh", "r").read()
for i in range(2,11):
    next_sh_file_content = next_sh_file_content[:155] + str(9 + i) + next_sh_file_content[157:] 
    next_sh_file_content = next_sh_file_content[:278] + str(i) + next_sh_file_content[279:]
    next_sh_file = open("regens" + str(i) + ".sh", "w")
    next_sh_file.write(next_sh_file_content)
    next_sh_file.close()
