#!/usr/bin/env python
"""
A script allowing to run ntcplot tool.

Use the --help option to see the available options.

Author: Alexandre PAPADOPOULOS, 2024
"""
import os
import argparse
import sys
from PyQt6.QtWidgets import (QApplication)
from .ihm import Window
from .netcdf_functions import ncdump_fuction, nc_variables

def setup_args():
    """
    Setup the arguments for the script
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('nc_file', type=str, help='NetCDF file')
    parser.add_argument('-help', action="help",
    help="python3 test_ntcplot.py some_nc_file.nc")
    res = parser.parse_args()
    return res

def main():
    """
    Main function
    """
    args = setup_args()
    print_args(args)

    if not os.path.isfile(args.nc_file):
        raise ValueError("NetCDF file does not exist")

    # input file
    ntc_file = args.nc_file

    # cla..ssic ncdump -h
    dump_str = ncdump_fuction(ntc_file)
    # dictionary with variables of netcdf
    var_dict = nc_variables(ntc_file)
    app = QApplication(sys.argv)


    windowInstance = Window()
    windowInstance.class_args(var_dict, dump_str, ntc_file)
    windowInstance.show()
    sys.exit(app.exec())


def print_args(args):
    """
    Print the arguments
    """
    print("Arguments:")
    for arg in vars(args):
        print("    {:20} {}".format(str(arg) + ":", getattr(args, arg)))
    print("")


if __name__ == '__main__':
    main()

