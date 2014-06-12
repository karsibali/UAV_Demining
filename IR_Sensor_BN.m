addpath(genpathKPM('~/bnt'))
N = 11;

DAG = zeros(N, N);

yi  = 1;     % Target classification
Vir = 2;     % Sensor mode
w   = 3;     % Weather
g   = 4;     % Vegetation
i   = 5;     % Illumination
di  = 6;     % Depth
zi  = 7;     % Size
si  = 8;     % Shape
sr  = 9;     % Soil moisture
smi = 10;    % Mueasured shape
zmi = 11;    % Measured size

node_sizes = [2 10 3 3 3 4 4 5 3 5 4];

DAG(Vir, [smi zmi]) = 1;
DAG(w, [smi zmi]) = 1;
DAG(g, sr) = 1;
DAG(i, sr) = 1;
DAG(sr, [smi zmi]) = 1;
DAG(di, [zi si]) = 1;
DAG(zi, [si zmi]) = 1;
DAG(si, smi) = 1;
DAG(yi, [di zi si]) = 1;

onodes = 1;
bnet = mk_bnet(DAG, node_sizes, 'observed', onodes);

G = bnet.dag;
draw_graph(G);