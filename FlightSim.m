alts = 500:50:2999;
bin_size = 2.5; % size of one bin in meters

% FOV = 20 x 10 deg with 1.5 mrad
%     = (20 x 0.0175) x (10 x 0.0175) rad
% FOV_M = FOV x H

for idx = 1:50
    fov_h = 20 * 0.0175 * alts(idx);
    fov_v = 10 * 0.0175 * alts(idx);
    bins_x = fov_h / (bin_size * sqrt(2)); % # of bins covered diagonally
    
end    
