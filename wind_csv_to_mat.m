% This script will read the wind csv files and convert wind direction and
% speed into u and v components.  I will save the variables in a .mat file

clear
all_wind_dir    = '/Users/kevinrosa/GSO/NBRISO_db/wind/';
years_dirs      = dir(all_wind_dir);
years = [];
for i = 1:length(years_dirs)
    % make sure directory has a 4 digit name beginning with 1 or 2:
    if length(years_dirs(i).name) == 4 & ...
            ((years_dirs(i).name(1) == '2')|(years_dirs(i).name(1) == '1'))
        years = [years, {years_dirs(i).name}];
    end
end

for y = 1:length(years)
    stations_dirs = dir([all_wind_dir, '/', years{y}, '/wind*']);
    handles = [];  % 'wind_2000_12345'
    for i = 1:length(stations_dirs)
        handles = [handles, {stations_dirs(i).name}];
    end
    
    for s = 1:length(handles)  % within each year, iterate through each station
        save_dir = [all_wind_dir, years{y}, '/', handles{s}, '/'];
        fname = [save_dir, handles{s}, '.csv'];
        fid = fopen(fname);
        
        C = textscan(fid, '%{yyyy-MM-dd HH:mm}D %f32 %f32 %*[^\n]',...
            'Delimiter',',', 'EmptyValue', NaN);
        
        time    = datenum(C{1});
        speed   = C{2};
        direction = C{3};  % direction from
        eastward    = -sind(direction).*speed;
        northward   = -sind(direction).*speed;
        parts = strsplit(handles{s}, '_');
        station_id  = parts(end);
        
        save([save_dir, handles{s}, '.mat'], 'time', 'eastward', 'northward');
        clearvars C time speed direction eastward northward
    end
end
