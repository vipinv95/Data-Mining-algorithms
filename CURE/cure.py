import numpy as np
import sys

# Clustering Using Representatives (CURE) Algorithm

sample = sys.argv[1]
data = sys.argv[2]
k = int(sys.argv[3])
n = int(sys.argv[4])
p = float(sys.argv[5])
output = sys.argv[6]

lines = open(sample, "r")
sample_list = []

for line in lines:
    sample_list.append([list(map(float,line.split(",")))])

dist_mat = np.zeros((len(sample_list),len(sample_list)))
dist_mat.fill(float('inf'))
for li in range(len(sample_list)-1):
    for li1 in range(li+1,len(sample_list)):
        dist_mat[li,li1] = float(np.sqrt(np.sum(np.square(np.array(sample_list[li])-np.array(sample_list[li1])))))
        dist_mat[li1,li] = dist_mat[li][li1]
while (len(sample_list) > k):
    r,c = np.unravel_index(np.argmin(dist_mat), dist_mat.shape)
    if r < c:
        dist_mat = np.delete(dist_mat, r, 0)
        dist_mat = np.delete(dist_mat, r, 1)
        dist_mat = np.delete(dist_mat, c-1, 0)
        dist_mat = np.delete(dist_mat, c-1, 1)
    else:
        dist_mat = np.delete(dist_mat, r, 0)
        dist_mat = np.delete(dist_mat, r, 1)
        dist_mat = np.delete(dist_mat, c, 0)
        dist_mat = np.delete(dist_mat, c, 1)
    dist_mat = np.concatenate((dist_mat,np.zeros((1,dist_mat.shape[1]))),axis=0)
    dist_mat = np.concatenate((dist_mat,np.zeros((dist_mat.shape[0],1))),axis=1)
    dist_mat[dist_mat.shape[0]-1,:] = float('inf')
    dist_mat[:,dist_mat.shape[0]-1] = float('inf')

    for slc in sample_list[c]:
        sample_list[r].append(slc)
    sample_list.append(sample_list[r])
    if r < c:
        sample_list.pop(r)
        sample_list.pop(c-1)
    elif r > c:
        sample_list.pop(r)
        sample_list.pop(c)
    for li in sample_list[len(sample_list)-1]:
        for li1 in range(len(sample_list)-1):
            for li2 in range(len(sample_list[li1])):
                d = float(np.sqrt(np.sum(np.square(np.array(li)-np.array(sample_list[li1][li2])))))
                if dist_mat[len(sample_list)-1][li1] > d:
                    dist_mat[len(sample_list)-1][li1] = d
                    dist_mat[li1][len(sample_list)-1] = d

rep_points = []
for s in sample_list:
    s_arr = np.array(s)
    s_selected = s_arr[np.where(s_arr[:,0] == np.amin(s_arr,axis=0)[0])]
    rep_points.append([list(s_selected[np.argmin(s_selected,axis=0)[1]])])
flat_rep = [rj for ri in rep_points for rj in ri]
sample_minus_rep = [[sj for sj in si if sj not in flat_rep] for si in sample_list]
for si in range(len(sample_minus_rep)):
    while len(rep_points[si]) < n: 
        pmax = None
        ps = []
        for si1 in range(len(sample_minus_rep[si])):
            d = float('inf')
            for rps in rep_points[si]:
                if float(np.sqrt(np.sum(np.square(np.array(rps)-np.array(sample_minus_rep[si][si1]))))) < d and (sample_minus_rep[si][si1] not in flat_rep):
                    d = float(np.sqrt(np.sum(np.square(np.array(rps)-np.array(sample_minus_rep[si][si1])))))
            if (sample_minus_rep[si][si1] not in flat_rep):
                ps.append(d)
            else:
                ps.append(float('-inf'))
        pmax = int(np.argmax(np.array(ps)))
        rep_points[si].append(sample_minus_rep[si][pmax])
        flat_rep.append(sample_minus_rep[si][pmax])
        if len(rep_points[si]) >= len(sample_minus_rep[si]):
            break
for rp in rep_points:
    print(rp)
for si in range(len(sample_list)):
    centroid = []
    centroid = np.sum(np.array(sample_list[si]),axis=0)/len(sample_list[si])
    rep_points[si] = list(np.array(rep_points[si])-(p*(np.array(rep_points[si])-centroid)))

lines.close()
lines = open(data, "r")
out = open(output, "w")
data_list = []
for line in lines:
    data_list.append(list(map(float,line.split(","))))
out_list = []
for dl in data_list:
    min_clust = []
    for ri in range(len(rep_points)):
        min_clust.append(float(np.amin(np.sqrt(np.sum(np.square(np.array(rep_points[ri])-np.array(dl)),axis=1)))))
    out_list.append(str(dl[0])+","+str(dl[1])+","+str(min_clust.index(min(min_clust)))+"\n")
for o in out_list:
    out.write(o)
out.close()
