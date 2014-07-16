% Load the data from the mine database
% The text file has mine data in the following format, in the order of
% columns
% Object type: 0:APM, 1:ATM, 2:UXO, 3:CLUT (mine-like objects)
% Size : small-(2,13], medium-(13,24], large-(24-40], extra-large-(>40)
% Depth: Surface, shallow-burried, burried, deep-burried
% Shape: Cylinder, Box, Sphere, Long-slender, Irregular
% Metal-content: No-metal, low-metal, high-metal

data = load('mine_database.txt');

% Change the type as mine (0) and not mine (1)
% Objects that are clutter are not mines
% Mark object that are not clutter mine (1)
data(data(:,1) ~= 3, 1) = 1;
% Mark the clutter as not mine (0)
data(data(:,1) == 3, 1) = 0;
data = data(1:4); % We don't need the metal content information

% Create the biasian network
nodes = size(data, 2);
dag = zeros(nodes, nodes);
type_n = 1;
depth_n = 2;
size_n = 3;
shape_n = 4;
% Create the network connections
dag(type_n, [depth_n size_n shape_n]) = 1;
dag(depth_n, [size_n shape_n]) = 1;
dag(size_n, shape_n) = 1;

ncases = size(data, 1); % Number of cases in the database
cases = cell(5, ncases);