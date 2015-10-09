__author__ = 'kevinrosa'

# I want to make a directory for each 2014 TCM using the naming format: TCM_year_serialnumber.
# Inside each of these directories I will have the raw .txt file data, the .cfg config file, the .mat matlab output
# variable output, and the README with metadata.

import os
import glob  # for finding pathnames according to the rules used by the Unix shell
import shutil  # I will use for moving files

def main():
    database_dir = '/Users/kevinrosa/GSO/NBRIS_db/'
    instrument = 'tcm'
    year = '2014'
    path = database_dir + instrument + '/' + year + '/'

    files_txt = glob.glob(path + '*.txt')  # list of strings of the .txt filenames (raw data)
    files_mat = glob.glob(path + '*.mat')
    files_cfg = glob.glob(path + '*.cfg')


    for txt in files_txt:
        serial = txt.split('/')[-1].split('_')[0]
        # name = file.split('/')[-1]  would return the part after the path and...
        # serl = name.split('_')[0]  would return the part before the first underscore
        handle = instrument + '_' + year + '_sn' + serial

        new_dir = path + handle + '/'  # name of new directory
        os.makedirs(new_dir, exist_ok=True)  # makes the directory
        shutil.copyfile(txt, new_dir+handle+'.txt')
        
        for i in range(0, len([f for f in files_mat if serial in f])):
            shutil.copyfile(str([f for f in files_mat if serial in f][i]), new_dir+handle+'.mat')
        for i in range(0, len([f for f in files_cfg if serial in f])):
            shutil.copyfile(str([f for f in files_cfg if serial in f][i]), new_dir+handle+'.cfg')

        make_README(new_dir, instrument, year, serial)


# The function to write the README:
def make_README(new_dir, instrument, year, serial):
    sn = list(map(str, [10175303, 10175307, 10175311, 10175312, 10175308, 10175306, 10175331, 9784975, 10175296, 2333586,
          2039045, 9784980, 9714529, 10175327, 10175324, 10175299, 10175323, 2006622, 2333584, 2006627,
          9714526, 9721595, 10175298, 9714531, 9714522, 9784979, 9714524, 9714532, 2333585, 9721594]))

    depth = list(map(str, [3.048, 3.6576, 2.7432, 2.4384, 3.048, 2.6993, 2.9992, 7.0104, 5.1816, 4.8768,
             4.8768, 4.572, 4.572, 5.4864, 5.4864, 2.7432, 5.4864, 7.0104, 6.4008, 6.096,
             4.572, 9.7536, 6.096, 6.4008, 6.096, 4.572, 3.6576, 7.62, 11.5824, 7.0104]))  # in meters

    y_ax = list(map(str, [245, 300, 275, 335, 260, 185, 125, 45, 145, 345, 145, 175, 145, 175, 195,
            120, 160, 165, 145, 175, 45, 265, 45, 15, 355, 305, 65, 70, 210, 235]))  # degrees clockwise of true N

    length = list(map(str, [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 1, 1, 1, 1, 1, 1, 1, 1, 1,
              1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 3]))  # tcm length (in meters)

    lon = list(map(str, [-71.3844, -71.3827, -71.3823, -71.3829, -71.3231, -71.3313, -71.3489, -71.3586,
                         -71.3565, -71.3609, -71.3461, -71.3128, -71.3258, -71.3261, -71.3116, -71.3066,
                         -71.321, -71.3088, -71.321, -71.3319, -71.3434, -71.288, -71.3752, -71.3671,
                         -71.3678, -71.3504, -71.3369, -71.3212, -71.308, -71.255]))  # decimal degrees east

    lat = list(map(str, [41.7628, 41.7619, 41.7595, 41.7584, 41.7202, 41.7196, 41.7092, 41.6786, 41.701, 41.6957,
                         41.7014, 41.7196, 41.7147, 41.7091, 41.7074, 41.6997, 41.6859, 41.688, 41.6859, 41.685,
                         41.6687, 41.6303, 41.6669, 41.6617, 41.6532, 41.6639, 41.6563, 41.6556, 41.6551, 41.6403]))
    timezone = 'UTC'
    investigators = 'Chris Kincaid, Christelle Balt, Christina King Wertman, Sara Szwaja, Kevin Rosa, Tucker Sylvia'
    project = 'SCOL 2014 (Study of Current on Ohio Ledge'
    velocity_units = 'cm/s'

    # Now let's write the README:
    if serial in sn:
        i = sn.index(serial)
        file = open(new_dir+'README'+'_'+handle+'.txt', 'w')
        file.write('SN: '+sn[i]+'\n')
        file.write('Depth: '+depth[i]+'\n')
        file.write('Y-axis: '+y_ax[i]+'\n')
        file.write('Length: '+length[i]+'\n')
        file.write('Lon: '+lon[i]+'\n')
        file.write('Lat: '+lat[i]+'\n')
        file.write('Timezone: '+timezone+'\n')
        file.write('Velocity units: '+velocity_units+'\n')
        file.write('Investigators: '+investigators+'\n')
        file.write('Project name: '+project+'\n')
        file.close()

    else:
        file = open(new_dir+'README_ERROR.txt')

    return

if __name__ == '__main__':
    main()
