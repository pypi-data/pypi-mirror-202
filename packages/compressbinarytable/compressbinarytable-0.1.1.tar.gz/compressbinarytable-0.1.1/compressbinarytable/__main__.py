#!/usr/bin/env python3

import pandas as pd
import numpy as np
import argparse
import sys
import os

# Compresses the binary table
def compression_algorithm(input_file):

    if input_file.endswith(".csv"):
        df = pd.read_csv(input_file, sep=",", dtype={"name/position": str, "outcome": int, "*": int})
        print("CSV")
    elif input_file.endswith(".tsv"):
        df = pd.read_csv(input_file, sep="\t", dtype={"name/position": str, "outcome": int, "*": int})
        print("TSV")
    else:
        return -1

    columns = df.columns.to_list()
    #print(columns)
    array = df.to_numpy()

    #will be add select 1 as a option too
    selection = 1

    dictionary_of_strains_data = {}

    for strain in array:
        strain_list = strain.tolist()
        strain_name = strain_list[0]
        index_counter = 0
        temp_list = []
        for elem in strain_list[1:]:
            if elem == selection or elem == str(selection):
                temp_list.append(index_counter)
            
            index_counter += 1
        
        dictionary_of_strains_data[strain_name] = temp_list

    
    return dictionary_of_strains_data, columns, selection


# Writes compressed file into outfile 
def compressed_file_writer(outfile, dictionary_of_strains_data, columns, selection):

    with open(outfile, "w") as compressed_file:
        compressed_file.write(str(selection))
        for col in columns[1:]:
            compressed_file.write(";" + str(col))
        compressed_file.write("\n")

        for key in dictionary_of_strains_data.keys():
            compressed_file.write(str(key))
            for index in dictionary_of_strains_data[key]:
                compressed_file.write(";" + str(index))
            
            compressed_file.write("\n")


# Decompresses the compressed file
def decompress_file(compressed_file):

    # Check if given file is properly formatted

    if not compressed_file.endswiht(".cbt"):
        print("Given file is not cbt format")
        return -1

    with open(compressed_file) as infile:
        lines = infile.readlines()

    default_value = str(lines[0].split(";")[0])

    # Checks if it is binary matrix

    if default_value not in ["0" ,"1"]:
        print("Given table is not binary")
        return -1
    
    all_the_strains = []

    # Set the value which will printed to indexes
    
    if default_value == "0":
        indexed_value = "1"
    else:
        indexed_value = "0"
    
    columns = lines[0][1:]

    first_line = []

    first_line.append("name/position")
    columns_split = columns.split(";")
    for col in columns_split:
        first_line.append(col)

    all_the_strains.append(first_line)

    for line in lines[1:]:
        splitted = line.split(";")
        strain_name = splitted[0]
        temp_list = [default_value for _ in range(len(columns.split(";"))+1)]
        temp_list[0] = strain_name
        for index in splitted[1:]:
            temp_list[index] = indexed_value

        all_the_strains.append(temp_list)


    return all_the_strains


# Prints decompressed file to given file name
def decompress_file_printer(outfile_name, all_the_strains, outfile_type):

    seperator = None

    if outfile_type == "tsv":
        seperator = "\t"
    elif outfile_type == "csv":
        seperator = ","
    else:
        print("Outfile type can be only csv or tsv")
        return -1

    with open(outfile_name + ".%s" %outfile_type , "w") as ofile:

        for line in all_the_strains:
            ofile.write(str(line[0]))
            for elem in line[1:]:
                ofile.write(seperator + str(elem))
            
            ofile.write("\n")
    
    return 0


def cbt_to_array(compressed_file):

    # Check if given file is properly formatted

    if not compressed_file.endswiht(".cbt"):
        print("Given file is not cbt format")
        return -1

    with open(compressed_file) as infile:
        lines = infile.readlines()

    default_value = str(lines[0].split(";")[0])

    # Checks if it is binary matrix

    if default_value not in ["0" ,"1"]:
        print("Given table is not binary")
        return -1
    
    all_the_strains = []

    # Set the value which will printed to indexes
    
    if default_value == "0":
        indexed_value = "1"
    else:
        indexed_value = "0"
    
    columns = lines[0][1:]

    for line in lines[1:]:
        splitted = line.split(";")
        strain_name = splitted[0]
        temp_list = [default_value for _ in range(len(columns.split(";"))+1)]
        temp_list[0] = strain_name
        for index in splitted[1:]:
            temp_list[index] = indexed_value

        all_the_strains.append(temp_list)

    return_array = np.array(all_the_strains)

    return return_array


def cbt_columns(compressed_file):

    # Check if given file is properly formatted

    if not compressed_file.endswiht(".cbt"):
        print("Given file is not cbt format")
        return -1

    with open(compressed_file) as infile:
        lines = infile.readlines()

    default_value = str(lines[0].split(";")[0])

    # Checks if it is binary matrix

    if default_value not in ["0" ,"1"]:
        print("Given table is not binary")
        return -1
    
    columns = lines[0][1:]

    return_array = np.array(columns)

    return return_array 


def main(args):

    # Main function to call from command line

    parser = argparse.ArgumentParser(description='Compression of Binary Mutation Tables')

    parser.add_argument("-c", help="Compression flag", action="store_true")

    parser.add_argument("-d", help="Decompression flag", action="store_true")

    parser.add_argument("-i", help="Path of input file", required=True)

    parser.add_argument("-o", help="Path of output file", required=True)

    parser.add_argument("-t", help="Type of output file, either csv or tsv", default="tsv")

    parser.add_argument("--override", help="If output file exist and want to override", action="store_true")

    args = parser.parse_args()

    print(args)

    if not os.path.exists(args.i):
        print("Input file is not exist, please provide input file")
        exit()

    if os.path.exists(args.o):
        if not args.override:
            print("Output file is already exist, use --override if you want to override")
            print("Warning : The old file will be overriden!")
            exit()

    if args.c and args.d:

        print("You need to select either Compression -c or Decompression -d")
        exit()

    if args.c:

        print("Compression starting")

        # Maybe add randomized movie quotes here 

        dictionary, columns, sel = compression_algorithm(args.i)
        compressed_file_writer(args.o, dictionary, columns, sel)

        print("Compression ended, compressed file can be found at %s" % args.o)

        print("Have a nice day!")

        exit()

    if args.d:

        print("Decompression starting")

        decompress_file_printer(args.o, decompress_file(args.i), args.t)

        print("Decompression ended, decompressed file can be found at %s" % args.o)

        print("Have a nice day!")

        exit()
    
    else:
        print("You need to select either Compression -c or Decompression -d")
        exit()




if __name__ == "__main__":

    main(sys.argv[1:])
