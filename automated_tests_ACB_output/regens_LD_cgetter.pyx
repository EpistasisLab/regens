import numpy
cimport numpy
cimport cython
@cython.boundscheck(False) # turn off bounds-checking for entire function
@cython.wraparound(False)  # turn off negative index wrapping for entire function

def open_LD_file(str path_to_LD_file):
    LD_file = (open(path_to_LD_file, "r").readlines())[1:]
    cdef long num_lines = len(LD_file)
    cdef long i
    cdef numpy.ndarray[double, ndim=1] r2 = numpy.zeros(num_lines, dtype = numpy.float)
    cdef numpy.ndarray[double, ndim=1] second_SNP_maf = numpy.zeros(num_lines, dtype = numpy.float)
    cdef numpy.ndarray second_SNP_ID = numpy.zeros(num_lines, dtype = 'U30')
    cdef numpy.ndarray[long, ndim=1] second_SNP_distance = numpy.zeros(num_lines, dtype = numpy.int)
    cdef numpy.ndarray[long, ndim=1] chromosome = numpy.zeros(num_lines, dtype = numpy.int)
    cdef numpy.ndarray[double, ndim=1] first_SNP_maf = numpy.zeros(num_lines, dtype = numpy.float)
    cdef numpy.ndarray first_SNP_ID = numpy.zeros(num_lines, dtype = 'U30')
    cdef numpy.ndarray[long, ndim=1] first_SNP_distance = numpy.zeros(num_lines, dtype = numpy.int)
    print("loading LD file")
    for i in range(num_lines):
        if i%5000000 == 0:
            print(str(i) + " out of " + str(num_lines) + " lines have been read from the LD file.")
        values = (LD_file[i]).split()
        r2[i] = float(values.pop())
        second_SNP_maf[i] = float(values.pop())
        second_SNP_ID[i] = values.pop()
        second_SNP_distance[i] = int(values.pop())
        chromosome[i] = int(values.pop())
        first_SNP_maf[i] = float(values.pop())
        first_SNP_ID[i] = values.pop()
        first_SNP_distance[i] = int(values.pop())
    return r2, second_SNP_maf, second_SNP_ID, second_SNP_distance, chromosome, first_SNP_maf, first_SNP_ID, first_SNP_distance

def open_r_file(str path_to_LD_file):
    content = open(path_to_LD_file, "r").readlines()
    return [float(i.strip()) for i in content]

def binner(long[:] values_to_bin, long num_unique_values):
    cdef long current_value, value_index, unique_value_index, i
    output = [[] for i in range(num_unique_values)]
    unique_value_index = 0
    value_index = 0
    current_value = values_to_bin[0]
    for value in values_to_bin:
        if current_value == value:
            output[unique_value_index].append(value_index)
            value_index = value_index + 1
        else: 
            current_value = value
            unique_value_index = unique_value_index + 1
            output[unique_value_index].append(value_index)
            value_index = value_index + 1
    return(output)

            