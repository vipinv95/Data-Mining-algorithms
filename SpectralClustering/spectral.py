import sys
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

# Spectral Clustering Algorithm for Graph Node Clustering

inputs = sys.argv[1]
k = int(sys.argv[2])
outputs = sys.argv[3]

data = open(inputs,"r")
G = nx.Graph()

edge_list = []
for line in data:
    edge_list.append(tuple(map(int,line.replace("\n","").split(" "))))
G.add_edges_from(edge_list)
f,s = zip(*edge_list)
nodes1 = np.unique(f+s)
dim = len(nodes1)
D = np.zeros(dim)
for i in range(len(D)):
    D[i] = G.degree(nodes1[i])
L = np.identity(dim)*D
for i in range(dim):
    for j in range(i+1):
        if G.has_edge(nodes1[i], nodes1[j]):
            L[i,j] = -1
            L[j,i] = -1

eigval, eigvec = np.linalg.eig(L)
idx = idx = np.where(eigval == np.unique(eigval)[1])[0][0]
eigval = eigval[idx]
eigvec = eigvec[:,idx]
pval = []
nval = []
for ev in range(len(eigvec)):
    if eigvec[ev] >= 0:
        pval.append(nodes1[ev])
    else:
        nval.append(nodes1[ev])
clusters = []
clusters.append(pval)
clusters.append(nval)
if k > 2:
    for iter in range(k-2):
        Glocal = G
        index = int(np.argmax([len(ci) for ci in clusters]))
        current = clusters[index]
        for cs in range(len(clusters)):
            if cs != index:
                Glocal.remove_nodes_from(clusters[cs])
        nodes1 = list(Glocal.nodes)
        dim = len(nodes1)
        D = np.zeros(dim)
        for i in range(len(D)):
            D[i] = Glocal.degree(nodes1[i])
        L = np.identity(dim)*D
        for i in range(dim):
            for j in range(i+1):
                if Glocal.has_edge(nodes1[i], nodes1[j]):
                    L[i,j] = -1
                    L[j,i] = -1
        
        eigval, eigvec = np.linalg.eig(L)
        if len(np.unique(eigval)) < 2:
            break
        idx = np.where(eigval == np.unique(eigval)[1])[0][0]
        eigval = eigval[idx]
        eigvec = eigvec[:,idx]
        pval = []
        nval = []
        for ev in range(len(eigvec)):
            if eigvec[ev] >= 0:
                pval.append(nodes1[ev])
            else:
                nval.append(nodes1[ev])
        clusters.pop(index)
        clusters.append(pval)
        clusters.append(nval)

out = open(outputs,"w+")
for c in clusters:
    csort = sorted(c)
    for ci in range(len(c)):
        if ci != len(c)-1:
            out.write(str(csort[ci])+",")
        else:
            out.write(str(csort[ci]))
    out.write("\n")
