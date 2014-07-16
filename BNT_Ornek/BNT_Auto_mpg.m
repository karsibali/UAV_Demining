%% Prepare the dataset
%# load dataset
D = load('auto-small');

%# filter the rows to keep only two classes
idx = ismember(D.Origin, [1 3]);
D = structfun(@(x)x(idx,:), D, 'UniformOutput',false);
numInst = sum(idx);

%# replace missing values with mean
D.MPG(isnan(D.MPG)) = nanmean(D.MPG);

%# convert discrete attributes to numeric indices 1:mx
[D.Origin,~,gnOrigin] = grp2idx( cellstr(D.Origin) );
[D.Cylinders,~,gnCylinders] = grp2idx( D.Cylinders );
[D.Model_Year,~,gnModel_Year] = grp2idx( D.Model_Year );

%% Create the graphical model for BNT

%# info about the nodes
nodeNames = fieldnames(D);
numNodes = numel(nodeNames);
node = [nodeNames num2cell((1:numNodes)')]';
node = struct(node{:});
dNodes = [node.Origin node.Cylinders node.Model_Year];
cNodes = [node.MPG node.Weight node.Acceleration];
depNodes = [node.MPG node.Cylinders node.Weight ...
            node.Acceleration node.Model_Year];

vals = cell(1,numNodes);
vals(dNodes) = cellfun(@(f) unique(D.(f)), nodeNames(dNodes), 'Uniform',false);
nodeSize = ones(1,numNodes);
nodeSize(dNodes) = cellfun(@numel, vals(dNodes));

%# DAG
dag = false(numNodes);
dag(node.Origin, depNodes) = true;

%# create naive bayes net
bnet = mk_bnet(dag, nodeSize, 'discrete',dNodes, 'names',nodeNames, ...
    'observed',depNodes);
for i=1:numel(dNodes)
    name = nodeNames{dNodes(i)};
    bnet.CPD{dNodes(i)} = tabular_CPD(bnet, node.(name), ...
        'prior_type','dirichlet');
end
for i=1:numel(cNodes)
    name = nodeNames{cNodes(i)};
    bnet.CPD{cNodes(i)} = gaussian_CPD(bnet, node.(name));
end

%# visualize the graph
[~,~,h] = draw_graph(bnet.dag, nodeNames);
hTxt = h(:,1); hNodes = h(:,2);
set(hTxt(node.Origin), 'FontWeight','bold', 'Interpreter','none')
set(hNodes(node.Origin), 'FaceColor','g')
set(hTxt(depNodes), 'Color','k', 'Interpreter','none')
set(hNodes(depNodes), 'FaceColor','y')

%% Now we split the data into training/testing:

%# build samples as cellarray
data = num2cell(cell2mat(struct2cell(D)')');

%# split train/test: 1/3 for testing, 2/3 for training
cv = cvpartition(D.Origin, 'HoldOut',1/3);
trainData = data(:,cv.training);
testData = data(:,cv.test);
testData(1,:) = {[]};    %# remove class

%% Finally we learn the parameters from the training set, and predict the class of the test data:

%# training
bnet = learn_params(bnet, trainData);

%# testing
prob = zeros(nodeSize(node.Origin), sum(cv.test));
engine = jtree_inf_engine(bnet);         %# Inference engine
for i=1:size(testData,2)
    [engine,loglik] = enter_evidence(engine, testData(:,i));
    marg = marginal_nodes(engine, node.Origin);
    prob(:,i) = marg.T;

end
[~,pred] = max(prob);
actual = D.Origin(cv.test)';