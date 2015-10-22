### Thursday Oct 22, 2015:
* changes to JSON naming scheme.  An import one to notice is the change from ``time_end`` to ``time_stop``.  I think this will improve readability when using ``sort_keys=True`` in ``json.dump``.  Also made the change in the TCM ``info*.csv`` files.
* changed how I write TCM JSON files.  Now following ``wind_noaa_dirs.py`` technique by making a dictionary ``meta`` once and then just writing using ``json.dump(meta, json_fname, sort_keys=True, indent-4).
* in ``info*.csv``, to express units without getting messy when writing ``README*.json``, adding extra fields to hold units (e.g. ``depth`` will now also get ``depth_units``)
* for ``ctd_ullman_dirs.py`` script, added function to extract time from ``.cnv`` files.
* beginning a module with useful functions for this project.  First function: ``nbriso_db.csv_to_dict``

- [x] Look into creating the metadata dictionary automatically from the ``info*.csv``, else write own function to do this
_______________________________________________
### Wednesday Oct 21, 2015:
* created ``_naming_scheme.md``

###### TO DO:
- [ ] figure best way to deal with incremented handles (i.e. no SN) to make sure the reference number never changes.  ``adcp_2014_moored_04`` should always have the same name no matter how many other ADCP datasets get added for that year.  It would seem preferably if the incremeneting was related to start time but I think it is more important that the handle stay constant.

_______________________________________________
### Monday Oct 19, 2015:
* finished proposal [for Cynthia's class]
* renamed repository to NBRISO_db (from NBRIS_db)
* made a first logo
* began learning some SQL

_______________________________________________
### Friday Oct 16, 2015:
* first commit of scripts to download multi-year NOAA wind data and save to Matlab variables

_______________________________________________
### Thursday Oct 15, 2015:
* began daily_updates.md file
* made further changes to the ``info_tcm_*.csv`` files.  Will now be using yyyy-mm-dd HH:MM:SS format for times instead of Matlab datenum.  Figured this change would improve human readability as well as cross-platform machine readability.  For 2014, I also went through and updated time_end to reflect recovery date. 

###### TO DO:
- [ ] choose naming scheme for adcp data (make sure to account for moored vs. underway)
