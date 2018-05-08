import sys
import re
import os
from itertools import combinations
from collections import Counter
filepath = sys.argv[1]
a = int(sys.argv[2])
b = int(sys.argv[3])
N = int(sys.argv[4])
s = int(sys.argv[5])
output_dir = sys.argv[6]

f = open(filepath,'r')
basket = []
item_lists = []
count_table = Counter()
freq_count_table = {}
all_item_pairs = []
hash_freq_bucket_table = {}
freq_itemsets = {}
candidate_txt = []
for line in f:
    items = line.split(",")
    for i in items:
        item_lists.append(int(i))
    basket.append(list(map(int, items)))
def hashf(i,j):
    return (a*i+b*j)%N
count_table = Counter(item_lists)
for k,v in count_table.most_common(): #Get only frequent 1-items > s from count table 
    if v >= s:
        freq_count_table[k] = v 
freq_itemsets = freq_count_table
for k in count_table:
    for k1 in count_table:
        if (k != k1) and (((k,k1) not in all_item_pairs) and ((k1,k) not in all_item_pairs)): 
            pair_count = 0
            for bi in basket:
                if (k in bi) and (k1 in bi):
                    pair_count = pair_count + 1
            if k > k1:
                if hash_freq_bucket_table.get(hashf(k1, k)) is None:
                    hash_freq_bucket_table[hashf(k1, k)] = pair_count
                else:
                    hash_freq_bucket_table[hashf(k1, k)] = hash_freq_bucket_table[hashf(k1, k)] + pair_count
                all_item_pairs.append((k1,k))
            else:
                if hash_freq_bucket_table.get(hashf(k, k1)) is None:
                    hash_freq_bucket_table[hashf(k, k1)] = pair_count
                else:
                    hash_freq_bucket_table[hashf(k, k1)] = hash_freq_bucket_table[hashf(k, k1)] + pair_count
                all_item_pairs.append((k,k1))
hash_freq_bucket_table = { k : v for k,v in hash_freq_bucket_table.items() if v >= s}
total_candidates = 0
fp = 0
for k in count_table:
    for k1 in count_table:
        if (k < k1) and (hash_freq_bucket_table.get(hashf(k, k1)) is not None) and (freq_count_table.get(k) is not None) and (freq_count_table.get(k1) is not None):
            pair_count = 0
            total_candidates = total_candidates + 1
            for bi in basket:
                if (k in bi) and (k1 in bi):
                    pair_count = pair_count + 1
            if pair_count >= s:
                freq_itemsets[(k,k1)] = pair_count
            else:
                fp = fp + 1
        elif (k < k1) and (hash_freq_bucket_table.get(hashf(k, k1)) is None) and (freq_count_table.get(k) is not None) and (freq_count_table.get(k1) is not None):
            candidate_txt.append((k,k1))
int_list = []
tuple_list = []
for ki in freq_itemsets.keys():
    if not isinstance(ki, tuple):
        int_list.append(ki)
    else:
        tuple_list.append(ki)
freq_itemset_list = sorted(int_list)
for se in sorted(tuple_list):
    freq_itemset_list.append(se)
if not os.path.exists(output_dir):
	os.makedirs(output_dir)
f_freq = open(os.path.join(output_dir,"frequentset.txt"),"w")
for fil in freq_itemset_list:
    f_freq.write(str(fil).replace(" ", "")+"\n")
candidate_txt.sort()
f_cand = open(os.path.join(output_dir,"candidates.txt"),"w")
for fc in candidate_txt:
    f_cand.write(str(fc).replace(" ", "")+"\n")
f.close()
f_freq.close()
f_cand.close()
if (total_candidates != 0):
    print("False positive rate: "+str(round(float(fp/total_candidates),3)))
else:
    print("False positive rate: "+str(0))
