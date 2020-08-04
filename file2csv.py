#  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  
#                       Converts flat file(s) to a .csv file                     #
#  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  
##
##      Author: Jake Nelson
##      Credits: [Danny Wilde]
##      Version: 1.0.0
##      GitHub: https://github.com/couldbejake

import argparse

#  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  
import os
import sys
import time
import csv

def convertToCSV( input_filenames, output_filename, lines_to_convert ):
    
    f_out = open( output_filename, " w " )
    f_out.write( ' , ' . join( map( str, input_filenames ) ) + " \n " )

    csv_data = { }

    for file_name in input_filenames:
        column_name = file_name

        column_data = { }

        i = 0
        for line in open( file_name, "r" ):
            column_data[ i ] = " \" " + line.replace( " \\ ", "" ) + " \" "
            i += 1

        csv_data[ column_name ] = column_data

    if( lines_to_convert == -1 ):
        first_column = input_filenames[ 0 ]
        line_count = len( csv_data[ first_column ] )
    else:
        line_count = lines_to_convert

    for i in range( line_count ):

        line_data = []
        
        for column_name in input_filenames:
            line_data.append( csv_data[ column_name ][ i ].replace( "\n", "" ) )

        f_out.write( ','.join( map( str, line_data ) ) + "\n" )

    f_out.close()

    return line_count

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument( '--input', nargs = '*', metavar=( 'input file name(s)'), help='A list of input file names.', required = True)
    parser.add_argument( '--linecount', nargs = 1, metavar=( 'lines to convert'), help='The amount of lines that should be converted.' )
    parser.add_argument( '--output', nargs = 1, metavar=( 'output file name'), help='The file the converter should output to.' )

    args = parser.parse_args()

    proc_start = time.time()

    input_filenames = args.input

    if( args.output != None ):
        output_filename = args.output[ 0 ]
    else:
        output_filename = "output.csv"
    
    lines_to_convert = - 1

    input_files_exist = True

    for input_filename in input_filenames:
        if( not os.path.exists( input_filename ) ):
            input_files_exist = False

    if( not input_files_exist ):
        print("One or more of the files you have specified in the arguments do not exist!")
        sys.exit()

    if( args.linecount != None ):
        try:
            lines_to_convert = int( args.linecount[ 0 ] )
            
            if( lines_to_convert < 0 ):
                
                print("Lines to convert must be a positive integer!")
                
        except ValueError:
            
            print( "Line count must be an integer!" )
            
            sys.exit()

    print( "Loading data from input files '" + ', '.join( map( str, input_filenames ) )+ "' into '" + output_filename + "'" )
    
    converted_line_count = convertToCSV( input_filenames, output_filename, lines_to_convert )

    print("(Succesfully converted "+str( converted_line_count ) + " lines in " + str( " {0:.2f} ".format( time.time() - proc_start ) ) + " seconds! )")
