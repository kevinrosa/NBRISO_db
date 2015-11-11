% Writing NBFSMN buoy data .mat files in NetCDF following CF Conventions
% 1.6
%     qh = 'quarter-hourly', i.e. the raw data values
%     hrmn = 'hourly mean'
%     hrss = 'hourly subsampled', only the samples that fell 'on the hour' (no averaging)
%     lp12 = low-passed: 25-hour half-width triangle-weight average (subsampled to 12 hours)
%     dymn = 'daily mean'
%     lp8d = low-passed: 8d cutoff
%     wb = "weather-band", this is "lp12" minus "lp8d" (variations b/w timescales of 12 hr and 8day)
%
%    In each of these structures, the variable "dnest" refers to "datenum eastern standard time"
%    The variable 'locn' shows you the lat/lon, bathymetric depth, and sensor depths.
% Updates:
%   - at Dave Ullman's suggestion, making time variable double precision.
%   - also changed 'depth_level' to type 'NC_BYTE' (Matlab class int8)

nc_filename = '/Users/kevinrosa/GSO/BayCirculation/NBFSMN_through2014_lp12_rosa_v02.nc';
if exist(nc_filename)
    delete(nc_filename);  % couldn't get 'CLOBBER' and 'NETCDF4' simultaneously
end
ncid = netcdf.create(nc_filename, 'NETCDF4');

% GLOBAL ATTRIBUTES
varid = netcdf.getConstant('NC_GLOBAL');  % for global attributes
netcdf.putAtt(ncid, varid, 'uuid', char(java.util.UUID.randomUUID()));
netcdf.putAtt(ncid, varid, 'temporal_characteristic', ...
    'lp12: low-passed: 25-hour half-width triangle-weight average (subsampled to 12 hours)');

data_dir = '/Users/kevinrosa/GSO/BayCirculation/NBFSMN_ProcessedJune2015_CorrectedAllStnsAllYearsThrough2014/';
mat_file = dir([data_dir, '*.mat'])

t_start = Inf;
t_end   = 0;
for i = 1:length(mat_file)
    clearvars locn lp12 qh  % make sure previous 
    load(fullfile(data_dir, mat_file(i).name))
    
    t_start = min(lp12.dnest(1), t_start);
    t_end   = max(lp12.dnest(end), t_end);
end
dt  = lp12.dnest(2) - lp12.dnest(1);
T   = [t_start:dt:t_end] + datenum(0000,00,00,5,0,0); % EST to UTC !!

dimid_stat  = netcdf.defDim(ncid, 'station', length(mat_file));
dimid_time  = netcdf.defDim(ncid, 'time', length(T));
dimid_depth = netcdf.defDim(ncid, 'depth_level', 2);
dimid_code  = netcdf.defDim(ncid, 'station_code_length', 4);

fillvalue   = -999;
M   = ones(length(mat_file), length(T), 2) * fillvalue;  % initial 3-d matrix

% initializing variables:
[lat, lon, zbathy] = deal(ones(length(mat_file),1)*fillvalue);  
[temp, sal, domgl] = deal(M);
chl = squeeze(M(:,:,1));
site_code = repmat('*', length(mat_file), 4);

for i = 1:length(mat_file)
    clearvars locn lp12 qh  % make sure previous load is overwritten
    load(fullfile(data_dir, mat_file(i).name))
        
    lat(i)  = locn.lat;
    lon(i)  = locn.lon;    
    zbathy(i)   = locn.zbathy;
    zsh     = locn.zsh;
    zdp     = locn.zdp;
    locn.zbathy
    site_code(i,:)  = locn.code
   % site_name   = locn.name;
   % site_abrv   = locn.abrv;
    
    % EST to UTC:
    time    = lp12.dnest + datenum(0000,00,00,5,0,0);
    
    index   = find(ismember(T, time));
    
    temp(i, index, 1)   = lp12.sh.temp;
    temp(i, index, 2)   = lp12.dp.temp;
    sal(i, index, 1)    = lp12.sh.sal;
    sal(i, index, 2)    = lp12.dp.sal;
    domgl(i, index, 1)  = lp12.sh.domgl;
    domgl(i, index, 2)  = lp12.dp.domgl;
    chl(i,index)        = lp12.sh.chl;
end

temp(isnan(temp))   = fillvalue;
sal(isnan(sal))     = fillvalue;
domgl(isnan(domgl)) = fillvalue;
chl(isnan(chl))     = fillvalue;

% TIME:
varid   = netcdf.defVar(ncid, 'time', 'double', [dimid_time]);
netcdf.defVarFill(ncid, varid, false, fillvalue);
netcdf.putVar(ncid, varid, T);
netcdf.putAtt(ncid, varid, 'long_name', 'datenum');
netcdf.putAtt(ncid, varid, 'units', 'days since 0000-01-00 00:00:00');
netcdf.putAtt(ncid, varid, 'time_zone', 'UTC');

% LAT:
varid   = netcdf.defVar(ncid, 'lat', 'float', [dimid_stat]);
netcdf.defVarFill(ncid, varid, false, fillvalue);
netcdf.putVar(ncid, varid, lat);
netcdf.putAtt(ncid, varid, 'standard_name', 'latitude');
netcdf.putAtt(ncid, varid, 'units', 'degree_north');

% LON:
varid   = netcdf.defVar(ncid, 'lon', 'float', [dimid_stat]);
netcdf.defVarFill(ncid, varid, false, fillvalue);
netcdf.putVar(ncid, varid, lon);
netcdf.putAtt(ncid, varid, 'standard_name', 'longitude');
netcdf.putAtt(ncid, varid, 'units', 'degree_east');

% DEPTH LEVEL:
varid   = netcdf.defVar(ncid, 'depth_level', 'byte', [dimid_depth]);
netcdf.putVar(ncid, varid, [1, 2]);
netcdf.putAtt(ncid, varid, 'long_name', 'Depth Level');
netcdf.putAtt(ncid, varid, 'comment', ['There are two depth levels: ' ...
    '1 m below surface and 0.5 m above bottom.  depth_level==1 ' ...
    'corresponds to the former and depth_level==2 to the latter.']);

% BATHYMETRY:
varid   = netcdf.defVar(ncid, 'zbathy', 'float', [dimid_stat]);
netcdf.defVarFill(ncid, varid, false, fillvalue);
netcdf.putVar(ncid, varid, zbathy);
netcdf.putAtt(ncid, varid, 'standard_name', 'sea_floor_depth_below_sea_level');
netcdf.putAtt(ncid, varid, 'units', 'm');

% TEMPERATURE:
varid   = netcdf.defVar(ncid, 'temp', 'float', [dimid_stat, dimid_time, dimid_depth]);
netcdf.defVarFill(ncid, varid, false, fillvalue);
netcdf.putVar(ncid, varid, temp);
netcdf.putAtt(ncid, varid, 'standard_name', 'sea_water_temperature');
netcdf.putAtt(ncid, varid, 'units', 'degree_C');

% SALINITY:
varid   = netcdf.defVar(ncid, 'sal', 'float', [dimid_stat, dimid_time, dimid_depth]);
netcdf.defVarFill(ncid, varid, false, fillvalue);
netcdf.putVar(ncid, varid, sal);
netcdf.putAtt(ncid, varid, 'standard_name', 'sea_water_salinity');
netcdf.putAtt(ncid, varid, 'units', 'psu');
netcdf.putAtt(ncid, varid, 'comment', ['The unit PSU or practical' ... 
    'salinity unit is no longer used in CF. ' ...
    'This is considered a dimensionless quanity.']);

% DISSOLVED OXYGEN:
varid   = netcdf.defVar(ncid, 'domgl', 'float', [dimid_stat, dimid_time, dimid_depth]);
netcdf.defVarFill(ncid, varid, false, fillvalue);
netcdf.putVar(ncid, varid, domgl);
netcdf.putAtt(ncid, varid, 'standard_name', 'mass_concentration_of_oxygen_in_sea_water');
netcdf.putAtt(ncid, varid, 'long_name', 'Dissolved Oxygen');
netcdf.putAtt(ncid, varid, 'units', 'mg/L')

% CHLOROPHYLL:
varid   = netcdf.defVar(ncid, 'chl', 'float', [dimid_stat, dimid_time]);
netcdf.defVarFill(ncid, varid, false, fillvalue);
netcdf.putVar(ncid, varid, chl);
netcdf.putAtt(ncid, varid, 'standard_name', 'mass_concentration_of_chlorophyll_in_sea_water');
netcdf.putAtt(ncid, varid, 'units', 'ug/L')
netcdf.putAtt(ncid, varid, 'comment', ['Chlorophyll is only measured at ' ...
    'depth_level==1 (near-surface).']);

% SITE CODE:
varid   = netcdf.defVar(ncid, 'site_code', 'char', [dimid_stat, dimid_code]);
netcdf.defVarFill(ncid, varid, false, '*');
netcdf.putVar(ncid, varid, site_code);

netcdf.close(ncid)
