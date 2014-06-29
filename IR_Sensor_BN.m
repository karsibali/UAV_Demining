addpath(genpath('~/MATLAB/bnt')) % Add BNT to the path

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
zmi = 10;    % Measured size
smi = 11;    % Mueasured shape

node_sizes = [2 50 3 3 3 4 4 5 3 4 5];

DAG(Vir, [smi zmi]) = 1;
DAG(w, [smi zmi]) = 1;
DAG(g, sr) = 1;
DAG(i, sr) = 1;
DAG(sr, [smi zmi]) = 1;
DAG(di, [zi si]) = 1;
DAG(zi, [si zmi]) = 1;
DAG(si, smi) = 1;
DAG(yi, [di zi si]) = 1;

bnet = mk_bnet(DAG, node_sizes, 'discrete', 1:N);

%G = bnet.dag;
%draw_graph(G);

% Define the CPDs
bnet.CPD{yi} = tabular_CPD(bnet, yi);
bnet.CPD{di} = tabular_CPD(bnet, di);
bnet.CPD{zi} = tabular_CPD(bnet, zi);
bnet.CPD{si} = tabular_CPD(bnet, si);
bnet.CPD{Vir} = tabular_CPD(bnet, Vir);
bnet.CPD{w} = tabular_CPD(bnet, w);
bnet.CPD{g} = tabular_CPD(bnet, g);
bnet.CPD{i} = tabular_CPD(bnet, i);
bnet.CPD{sr} = tabular_CPD(bnet, sr);
bnet.CPD{zmi} = tabular_CPD(bnet, zmi);
bnet.CPD{smi} = tabular_CPD(bnet, smi);

% Load the training database
samples = load('BN_training_db.txt');
% Separate the data as training, test, and cross-validation
tr_size = int16(size(samples,1) * 0.6);
test_size = int16(size(samples,1) * 0.2);
cv_size = int16(size(samples,1) * 0.2);
tr_db = samples(1:tr_size, :);
test_db = samples(tr_size+1:tr_size+test_size, :);
cv_db = samples(tr_size + test_size + 1:end, :);

%tr_cases = cell(N, tr_size);
tr_cases = num2cell(tr_db');

% Learn the parameters
bnet = learn_params(bnet, tr_cases);