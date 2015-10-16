__author__ = 'kevinrosa'

# Download wind data for NOAA CO-OPS stations.
# 6-minute data is only allowed in up to 31 day intervals so I will download each month and combine into a
# full year of 6-minute data.
# Since Matlab is the most popular language among oceanographers, I will then save the data as .mat file.
# Do not know yet whether I will be able to do this in Python or will have write a separate Matlab
# script for this.

import urllib.request
import os
import csv
import json

instrument = 'wind'
stations = ['8452660', '8452944', '8454000', '8454049', '8452951']
years = [str(i) for i in range(2004, 2014+1)]
months = [str(i).zfill(2) for i in range(1,13)]  # zfill() for leading zero

for station in stations:
    for year in years:
        handle = '_'.join([instrument, year, station])  # wind_2000_12345
        wind_dir = '/'.join(['/Users/kevinrosa/GSO/NBRIS_db', instrument, year, handle]) + '/'
        wind_dir_dump = wind_dir + 'dump/'
        if not os.path.exists(wind_dir_dump):
            os.makedirs(wind_dir_dump)  # making wind_dir_dump will make wind_dir too

        year_fname = wind_dir + handle +'.csv'

        os.remove(year_fname) if os.path.isfile(year_fname) else None  # remove old file so don't append to end of it

        for month in months:
            day1 = '02' if month != '01' else '01'  # start on the 2nd except for January (1st)
            day2 = '01' if month != '12' else '31'  # end on the 1st except December (31st)
            next_month = str(int(month)+1).zfill(2) if month != '12' else month
            url = 'http://tidesandcurrents.noaa.gov/api/datagetter?product=wind&application=NOS.COOPS.TAC.MET&begin_date=' \
                  +year+month+day1+'&end_date='+year+next_month+day2+'&station='+station+'&time_zone=GMT' \
                                                                                   '&units=metric&interval=6&format=csv'
            month_fname = wind_dir_dump + '_'.join([station, year, month])+'.csv'
            urllib.request.urlretrieve(url, month_fname)

            with open(year_fname, 'a') as f_out:
                with open(month_fname, 'r') as f_in:
                    f_in.readline()  # skip the first line
                    for line in f_in:
                        f_out.write(line)

        url_json = url[0:-3] + 'json'  # url for JSON format
        json_fname = wind_dir_dump + '_'.join(['JSON', handle]) + '.json'
        urllib.request.urlretrieve(url_json, json_fname)

        with open(json_fname) as json_file:
            data = json.load(json_file)
            meta = data['metadata']

        with open(wind_dir + '_'.join(['README', handle]) + '.json', 'w') as outfile:
            meta['instrument'] = 'wind'
            meta['time_start'] = year + '-01-01 00:00:00'
            meta['time_end'] = year + '-12-31 23:54:00'
            meta['source'] = url
            json.dump(meta, outfile, sort_keys=True, indent=4)


