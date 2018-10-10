# 0.0 coding:utf-8 0.0
import networkx as nx

from openpyxl import load_workbook
from get_data import get_data

#201 1为节点编号  2位节点流量
#202 1为管段编号  2为管段流量  3，4分别为管段首尾的节点编号
filename1 = '201.xlsx'
filename2 = '202.xlsx'

d1 = get_data(filename2,3)
d2 = get_data(filename2,4)
d3 = get_data(filename2,2)
print("管网节点：",d1)
print(d2)
print(d3)

d4 = get_data(filename1,1)
d5 = get_data(filename1,2)
print(d5)
print(d4)

G = nx.DiGraph()
print(d1.__len__())

i = 0
while i <d1.__len__():
    G.add_edge(d1[i],d2[i],pipline_gpm = d3[i])
    G.add_node(d4[i],node_gpm = d5[i])
    i = i+1

print(G.edges())
print(nx.get_edge_attributes(G,"pipline_gpm"))
print(nx.get_node_attributes(G,"node_gpm"))

for (u,v,d) in G.edges(data="pipline_gpm"):
    print(u,v,d)

print("节点个数为:",G.number_of_nodes())
print("边个数为:",G.number_of_edges())
print("节点:",G.nodes())
print("边:",G.edges())
#print("节点6的邻居为:",G.neighbors(6)) #有错误
#for n,nbrs in G.adjacency():
#    for nbr,eatter in nbrs.items():
#        data = eatter['pipline_gpm']
#        print('(%d,%d,%.3f)'% (n,nbr,data))

#print(G.out_degree(97)) #计算节点的出度
#print(G.out_degree(97,weight='pipline_gpm')) #计算节点出度之和
#print("显示节点的继承者:",G.successors(97))
#print("显示节点的邻居:",G.neighbors(97))
m=15
n=17
listBFS = list(nx.bfs_tree(G,m).edges())
listBFS1 = list(nx.bfs_edges(G,m))
print(listBFS1)
#print(listBFS[0])
x=0
for i in listBFS:
    print(i)