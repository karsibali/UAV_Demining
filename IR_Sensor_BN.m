% Create the IR sensor BN and learn the parameters (CPTs) from sample data
clc;clear;
addpath(genpath('~/MATLAB/bnt')) % Add BNT to the path

%% Create the BN structure
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

node_sizes = [2 4 4 5 50 3 3 3 3 4 5];

DAG(yi, [di zi si]) = 1;
DAG(Vir, [zmi smi]) = 1;
DAG(w, [zmi smi]) = 1;
DAG(g, sr) = 1;
DAG(i, sr) = 1;
DAG(sr, [zmi smi]) = 1;
DAG(di, [zi si]) = 1;
DAG(zi, [si zmi]) = 1;
DAG(si, smi) = 1;

observed = [zmi smi];
bnet = mk_bnet(DAG, node_sizes);

%G = bnet.dag;
%draw_graph(G);

% Define the CPDs
bnet.CPD{yi} = tabular_CPD(bnet, yi, 'prior_type', 'dirichlet', 'dirichlet_weight', 0);
bnet.CPD{di} = tabular_CPD(bnet, di, 'prior_type', 'dirichlet', 'dirichlet_weight', 0);
bnet.CPD{zi} = tabular_CPD(bnet, zi, 'prior_type', 'dirichlet', 'dirichlet_weight', 0);
bnet.CPD{si} = tabular_CPD(bnet, si, 'prior_type', 'dirichlet', 'dirichlet_weight', 0);
bnet.CPD{Vir} = tabular_CPD(bnet, Vir, 'prior_type', 'dirichlet', 'dirichlet_weight', 0);
bnet.CPD{w} = tabular_CPD(bnet, w, 'prior_type', 'dirichlet', 'dirichlet_weight', 0);
bnet.CPD{g} = tabular_CPD(bnet, g, 'prior_type', 'dirichlet', 'dirichlet_weight', 0);
bnet.CPD{i} = tabular_CPD(bnet, i, 'prior_type', 'dirichlet', 'dirichlet_weight', 0);
bnet.CPD{sr} = tabular_CPD(bnet, sr, 'prior_type', 'dirichlet', 'dirichlet_weight', 0);
bnet.CPD{zmi} = tabular_CPD(bnet, zmi, 'prior_type', 'dirichlet', 'dirichlet_weight', 0);
bnet.CPD{smi} = tabular_CPD(bnet, smi, 'prior_type', 'dirichlet', 'dirichlet_weight', 0);

CPT = cell(1,N);
for i=1:N
  s=struct(bnet.CPD{i});  % violate object privacy
  CPT{i}=s.CPT;
  dispcpt(CPT{i})
end

%% Load the training database
samples = load('BN_training_db.txt');
samples = samples + 1; % Start classes from 1 instead of 0

% Separate the data as training, test, and cross-validation
tr_size = int16(size(samples,1) * 0.6);
test_size = int16(size(samples,1) * 0.2);
cv_size = int16(size(samples,1) * 0.2);
tr_db = samples(1:tr_size, :);
test_db = samples(tr_size+1:tr_size+test_size, :);
cv_db = samples(tr_size + test_size + 1:end, :);

%tr_cases = cell(N, tr_size);
%tr_cases = num2cell(tr_db');

% Learn the parameters
bnet2 = learn_params(bnet, tr_db');

%% Display learned CPTs
CPT3 = cell(1,N);
for i=1:N
  s=struct(bnet2.CPD{i});  % violate object privacy
  CPT3{i}=s.CPT;
  dispcpt(CPT{i})
end

%%
engine = jtree_inf_engine(bnet2);

evidence = cell(size(test_db,1),N);
evidence(:,2:end) = num2cell(test_db(:,2:end));
[engine, loglik] = enter_evidence(engine, evidence);
marg = marginal_nodes(engine, yi);

