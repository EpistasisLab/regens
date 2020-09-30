library(TriadSim)
stringsAsFactors=FALSE

m.file <- "input_files/ACB_not_trio_fathers"
f.file <- "input_files/ACB_not_trio_mothers"
k.file <- "input_files/ACB_not_trio_kin"
input.plink.file <- c(m.file, f.file, k.file)
rcmb.rate2 = read.table("input_files/triadsim_rcmb_rate_df.tab", header = TRUE, sep = "\t")

sessionInfo()

TriadSim(input.plink.file, 
         out.put.file = "runtime_testing/triadsim_old_simulated8_chr", 
         fr.desire = 0.05,
         pathways = list(1:4,5:8),
         n.ped = 10000,
         N.brk = 4, 
         target.snp = NA,
         P0 = 0.001,
         is.OR = FALSE,
         risk.exposure = 1,
         risk.pathway.unexposed = c(1.5, 2), 
         risk.pathway.exposed = c(1.5, 2),  
         is.case = TRUE, 
         e.fr = NA,
         pop1.frac = NA, 
         P0.ratio = 1, 
         rcmb.rate = rcmb.rate2, 
         no_cores = 1)
