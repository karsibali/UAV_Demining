function [ smi, zmi ] = SensorMeasurement( H, si, zi )
%SENSORMEASUREMENT Deteriorate the sensor size and shape
%   The size and shape of the target is deteriorated to reflect the
%   randomness in the sensor measurements based on the sensor mode.

sres = H * 0.0015; % Sensor resolution
if (zi >= 8*sres)
    shp_err = 0.4;
    B = 6;
    sigma = 6;
elseif (zi >= 5*sres && zi < 8*sres)
    shp_err = 0.5;
    B = 8;
    sigma = 8;
elseif (zi >= 3*sres && zi < 5*sres)
    shp_err = 0.6;
    B = 10;
    sigma = 10;
else
    shp_err = 0.7;
    B = 12;
    sigma = 12;
end

luck_factor = unifrnd(0,1);

if luck_factor > shp_err
    smi = si;
elseif 0.4 < shp_err - luck_factor <= 0.6
    smi = mod(si + 3, 5);
elseif 0.2 < shp_err - luck_factor <= 0.4
    smi = mod(si + 2, 5);
elseif shp_err - luck_factor <= 0.2
    smi = mod(si + 1, 5);
end

zmi = zi + 0.1 * (B + sigma * unifrnd(0, 1));
end

