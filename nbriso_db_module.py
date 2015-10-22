__author__ = 'kevinrosa'

# A module with some useful functions for the NBRISO database project.

def csv_to_dict(csv_fname, *identifying_field):
    if identifying_field:
        id_field = identifying_field  # this allows flexibility for an instrument with no SN but some other identifying value
    else:
        id_field = 'sn'

    d = {}  # dictionary that will have a dictionary in it for each serial number
    with open(csv_fname) as f:
        fields = f.readline().split(',')
        for line in f:
            line = line.split(',')
            sn = line[fields.index(id_field)]

            d[sn] = dict(zip(fields, line))

    return d

