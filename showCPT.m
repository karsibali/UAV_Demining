function [varargout] = showCPT(bnet,node_rng)

% function [varargout] = showCPT(bnet,node_rng)
% 
% Helper function for displaying the CPT's associated with discrete nodes in bnet (Bayes net)
% Optional argument node_rng must contain a valid range of indices with respect to the
% discrete nodes in bnet (i.e. bnet.dnodes). If it is omitted it defaults to all discrete nodes.
% The BNT function 'dispcpt' is used to pretty print each CPT.
% Cell array of CPT's is returned if an output argument is supplied.
% This can be printed using 'celldisp(outputarg)' if desired.
%
% Jim Rehg, Georgia Tech, 2002.

if nargin == 1
   num_nodes = length(bnet.dnodes);
   node_rng = 1:num_nodes;
else
   num_nodes = length(node_rng);
end
assert(node_rng(1) >= 1 & node_rng(end) <= length(bnet.dnodes), 'Discrete node range out of bounds');

CPT = cell(1,num_nodes);
k = 1;
for i = node_rng,
   s = struct(bnet.CPD{bnet.dnodes(i)});
   fprintf('CPT for dnode %d:\n', i);
   dispcpt(s.CPT);  % Kevin's pretty printer for CPT's
   if nargout > 0
     CPT{k} = s.CPT;
     k = k + 1;
   end
end
%celldisp(CPT)
if nargout > 0
   varargout(1) = {CPT};
end

