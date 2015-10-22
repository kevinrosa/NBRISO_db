__author__ = 'kevinrosa'

# Will make a directory for each TCM deployment using the naming format: TCM_year_serialnumber.
# Inside each of these directories I will have the raw data .txt file, the .cfg config file, the .mat matlab output,
# the .dat file, and the metadata in JSON.

import os
import glob  # for finding pathnames according to the rules used by the Unix shell
import shutil  # I will use for moving files
import json
from collections import OrderedDict
import csv
import nbriso_db_module as db

def main():
    database_dir = '/Users/kevinrosa/GSO/NBRISO_db/'
    instrument = 'tcm'
    year = '2012'
    path = database_dir + instrument + '/' + year + '/'
    dump = path + 'dump/'

    files_txt = glob.glob(dump+'*.txt')  # list of strings of the .txt filenames (raw data)
    files_mat = glob.glob(dump+'*.mat')
    files_cfg = glob.glob(dump+'*.cfg')
    files_dat = glob.glob(dump+'*.dat')

    for txt in files_txt:
        serial = get_sn(txt, year)  # extract serial number from file name

        handle = '_'.join([instrument, year, 'sn']) + serial  # 'tcm_2000_sn12345'
        new_dir = path + handle + '/'  # name of new directory
        os.makedirs(new_dir, exist_ok=True)  # makes the directory
        shutil.copyfile(txt, new_dir+handle+'.txt')

        for i in range(0, len([f for f in files_mat if serial in f])):
            shutil.copyfile(str([f for f in files_mat if serial in f][i]), new_dir+handle+'.mat')
        for i in range(0, len([f for f in files_cfg if serial in f])):
            shutil.copyfile(str([f for f in files_cfg if serial in f][i]), new_dir+handle+'.cfg')
        for i in range(0, len([f for f in files_dat if serial in f])):
            shutil.copyfile(str([f for f in files_dat if serial in f][i]), new_dir+handle+'.dat')

        make_README_json(dump, new_dir, serial, handle)
    return

# To handle different file naming formats for different years:
def get_sn(fname, year):
    if year == '2012':
        serial = fname.split('/')[-1].split('_')[-1].split('.')[0]
    elif year == '2014':
        serial = fname.split('/')[-1].split('_')[0]
    else:
        raise ValueError("ERROR: Not a supported year yet.  Alternatively: make sure year is a string")

    return serial

# The function to write the README:
def make_README_json(dump, new_dir, serial, handle):

    csv_fname = dump+'info_'+handle.split('_sn')[0]+'.csv'
    dictionary = db.csv_to_dict(csv_fname)
    metadata = dictionary[serial]

    with open(new_dir+'README'+'_'+handle+'.json', 'w') as outfile:
        json.dump(metadata, outfile, sort_keys=True, indent=4)

    return

if __name__ == '__main__':
    main()
