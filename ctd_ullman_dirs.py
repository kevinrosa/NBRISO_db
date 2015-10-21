__author__ = 'kevinrosa'

# There are a list of CTD data ascii files and a single txt file with the locations and depths of each station.
# This script will organize those CTD records into directories by year and then a directory for each profile
# along with a JSON file with metadata for each profile
import os
import glob
import shutil
import json

database_dir = '/Users/kevinrosa/GSO/NBRISO_db/'
instrument = 'ctd'
dump = os.path.join(database_dir, instrument, 'dump', '')  # note this time dump is not in any particular year
subdump = os.path.join(dump, 'CTD_ullman', '')  # the extra '' is for a trailing slash (OS independent)
trips = [n for n in os.listdir(subdump) if '20' in n and os.path.isdir(os.path.join(subdump, n))]

for n in trips:
        d = os.path.join(subdump, n)  # d is the full path, n is the 'sep2009' part
        year = ''.join([c for c in n if c.isdigit()])
        year_dir = os.path.join(database_dir, instrument, year, '')

        if not os.path.exists(year_dir):
            os.makedirs(year_dir)

        txt_meta = [f for f in glob.glob(os.path.join(subdump, n, '*.txt')) if 'Final' in f][0]
        sta_dict = {}
        with open(txt_meta) as f:
            f.readline()  # to skip the header line
            for line in f:
                data = line.split()
                sta = data[0]
                sta_dict[sta] = {'lat': data[1],
                                 'lon': data[2],
                                 'depth': data[-1]}

        cnv_files = [f for f in glob.glob(os.path.join(subdump, n, '*.cnv'))]
        for cnv_file in cnv_files:
            profile = cnv_file.split('/')[-1]  # e.g. 's42_avg.cnv'
            sta = ''.join([c for c in profile if c.isdigit()])  # only the numeric part of ctd profile name
            # the handle will include an index calculate based on the other handles in that year.
            # this protects from double-naming but adds a weakness where running this script repeatedly without
            # deleting files will just add duplicates.
            handles = [x for x in os.listdir(year_dir)]
            if not handles:  # if the directory is empty
                index = 1
            else:
                index = max(map(int, [h.split('_')[-1] for h in handles])) + 1

            handle = '_'.join([instrument, year, str(index).zfill(4)])  # index will be 4 characters long
            handle_dir = os.path.join(year_dir, handle, '')
            os.makedirs(handle_dir)  # make directory from handle

            shutil.copyfile(cnv_file, handle_dir+handle+'.cnv')

            with open(handle_dir + '_'.join(['README', handle]) + '.json', 'w') as outfile:
                meta = {}
                meta['instrument'] = instrument
                meta['handle'] = handle
                meta['lat'] = sta_dict[sta]['lat']
                meta['lon'] = sta_dict[sta]['lon']
                meta['depth'] = sta_dict[sta]['depth']
               # meta['time_start'] = year + '-01-01 00:00:00'
               # meta['time_end'] = year + '-12-31 23:54:00'
               # meta['source'] = url
                json.dump(meta, outfile, sort_keys=True, indent=4)
