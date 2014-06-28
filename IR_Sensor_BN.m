addpath(genpathKPM('~/MATLAB/bnt')) % Add BNT to the path

N = 11; % Number of variables

DAG = zeros(N, N);

% Variables in the topological order
yi  = 1;     % Target classification
di  = 2;     % Depth
zi  = 3;     % Size
si  = 4;     % Shape
Vir = 5;     % Sensor mode
w   = 6;     % Weather
g   = 7;     % Vegetation
i   = 8;     % Illumination
sr  = 9;     % Soil moisture
smi = 10;    % Mueasured shape
zmi = 11;    % Measured size

node_sizes = [2 50 3 3 3 4 4 5 3 5 4];

DAG(Vir, [smi zmi]) = 1;
DAG(w, [smi zmi]) = 1;
DAG(g, sr) = 1;
DAG(i, sr) = 1;
DAG(sr, [smi zmi]) = 1;
DAG(di, [zi si]) = 1;
DAG(zi, [si zmi]) = 1;
DAG(si, smi) = 1;
DAG(yi, [di zi si]) = 1;

onodes = 
bnet = mk_bnet(DAG, node_sizes, 'observed', onodes);

%G = bnet.dag;
%draw_graph(G);

% Load the training database
samples = load('BN_training_db.mat');
% Separate the data as training, test, and cross-validation
tr_size = size(samples,1) * 0.6;
test_size = size(samples,1) * 0.2;
cv_size = size(samples,1) * 0.2;
tr_db = samples(1:tr_size, :);
test_db = samples(tr_size+1:tr_size+test_size, :);
cv_db = samples(tr_size + test_size + 1:end, :);