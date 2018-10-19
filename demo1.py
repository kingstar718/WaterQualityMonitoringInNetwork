# 0.0 coding:utf-8 0.0
import networkx as nx
import numpy as np
from openpyxl import load_workbook
from get_data import get_data

# 201 excel中  列1为节点编号  列22位节点流量
# 202 excel中  列1为管段编号  列2为管段流量  列3，4分别为管段首尾的节点编号
node_name = '201.xlsx'
# 当前时段的流量方向和初始管网默认的方向不同,为方便计算,统一将流量改成正值并更改默认管网方向.
pipeline_name = '2022.xlsx'

# 节点
node_num = get_data(node_name,1)
node_data = get_data(node_name,2)
print('管网节点编号： ',node_num)
print('管网节点流量： ',node_data)

# 管段
pipeline_num = get_data(pipeline_name,1)
pipeline_data = get_data(pipeline_name,2)
pipeline_firstnum = get_data(pipeline_name,3)
pipeline_lastnum = get_data(pipeline_name,4)
print('管网管段编号： ',pipeline_num)
print('管网管段流量： ',pipeline_data)
print('管网管段首节点： ',pipeline_firstnum)
print('管网管段末节点： ',pipeline_lastnum)

# 加权图
G = nx.DiGraph()
i = 0
while i<node_num.__len__():
    G.add_edge(pipeline_firstnum[i],pipeline_lastnum[i],pipline_gpm=pipeline_data[i])
    G.add_node(node_num[i],node_gpm=node_data[i])
    i=i+1

print("加权图： ",G.edges())
print("管段及流量：",nx.get_edge_attributes(G,"pipline_gpm"))
print("节点及流量：",nx.get_node_attributes(G,"node_gpm"))

# 直接相连
# 上游节点
m = 15
# 下游节点
n = 5

# 判别函数   1直接相连  -1间接相连  None不相连
def connected(m,n,list):
    i = 0
    while i < list.__len__():
        if(m == list[i][0]):
            if(n == list[i][1]):
                # print("直接相连")
                return 1
                break
        else:
            if(n==list[i][1]):
                #print("间接相连")
                return -1
                break
        i=i+1

# 二维数组初始化以及赋值
listW=np.zeros((node_num.__len__(),node_num.__len__()),dtype=float)
# 多条路径的l
lmore=[]
l21=[]
l22=[]
l31=[]
l4=[]
l41=[]
pp2=[]
indgreelist=[]
for i in node_num:
    for j in node_num:  #谁当下游节点  j为上游 为广度优先搜索的起始节点
        listjBFS=list(nx.bfs_tree(G,j).edges())
        judge=connected(j,i,listjBFS)
        # 直接相连
        if(judge==1):
            p=G.in_degree(i)  #算的是下游节点的入度
            # indgreelist.append(p)
            # pp1=list(nx.all_simple_paths(G,j,i,cutoff=1))
            # pp2.append(pp1[0])
            if(p==1):
                listW[i-1][j-1]=1 #入度为1  直接相连 值设为1
            elif(p==2):
                l2=list(nx.all_simple_paths(G,j,i,cutoff=1))
                l21.append(l2[0])  #入度为2的先存入list  在后面进行计算
            elif(p==3):
                l3=list(nx.all_simple_paths(G,j,i,cutoff=1))
                l31.append(l3[0])   #入度3的同理   这个管网节点入度最大的为3
        elif(judge==-1):   #间接相连
            l=list(nx.all_simple_paths(G,j,i))#起始  结束
            #print(list(nx.all_simple_paths(G,j,i)))
            lmore.append(l)
            #l4.append(l[0])        #间接相连的节点list存l4,后面再计算
        elif(judge==None):
            listW[i-1][j-1]=0  #不相连直接设为0


# 计算入度为2的节点的值  其中l21包含了所有入度为2的节点
l21_num = 0
# 查看任意边的属性，为pipline_gpm[22,32]
pipline_gpm=nx.get_edge_attributes(G,'pipline_gpm')
while(l21_num<len(l21)):
    x=pipline_gpm[l21[l21_num][0],l21[l21_num][1]]    #取上下游节点的管段1流量
    y=pipline_gpm[l21[l21_num+1][0],l21[l21_num+1][1]]  #取上下游节点的管段2流量

    z1=("%.3f"% (x/(x+y))) #保留三位小数
    z2=("%.3f"% (y/(x+y)))

    listW[l21[l21_num][0]-1,l21[l21_num][1]-1]=z1  #矩阵下标从0开始  将值放入矩阵
    listW[l21[l21_num+1][0]-1,l21[l21_num+1][1]-1]=z2
    l21_num=l21_num+2  #下一个入度为2的节点

# 直接相连  入度为3
l31_num=0
while(l31_num<len(l31)):
    x31=pipline_gpm[l31[l31_num][0],l31[l31_num][1]]
    y31=pipline_gpm[l31[l31_num+1][0],l31[l31_num+1][1]]
    z31=pipline_gpm[l31[l31_num+2][0],l31[l31_num+2][1]]
    m31=("%.3f"% (x31/(x31+y31+z31)))
    m32=("%.3f"% (y31/(x31+y31+z31)))
    m33=("%.3f"% (z31/(x31+y31+z31)))
    print(m31,m32,m33)
    listW[l31[l31_num][0]-1,l31[l31_num][1]-1]=m31
    listW[l31[l31_num+1][0]-1,l31[l31_num+1][1]-1]=m32
    listW[l31[l31_num+2][0]-1,l31[l31_num+2][1]-1]=m33
    l31_num = l31_num +3

node_m = nx.get_node_attributes(G,'node_gpm')

# 间接连通的计算函数
def IndirectConnect(list):  #w(i,j) 中 i为下游  j为上游
    i=0
    m=1
    while i<len(list)-1:
        n1=list[i]
        n2=list[i+1]   # 依次取出两个节点
        n3=listW[n2-1,n1-1]  #查找其在矩阵中的值
        m=n3*m   #累乘
        i=i+1
    listW[list[len(list)-1]-1,list[0]-1]=m  #值放入矩阵


# 多路径计算
def IndirectConnect2(list):  #w(i,j) 中 i为下游  j为上游
    i=0
    m=1
    while i<len(list)-1:
        n1=list[i]
        n2=list[i+1]   # 依次取出两个节点
        n3=listW[n2-1,n1-1]  #查找其在矩阵中的值
        m=n3*m   #累乘
        i=i+1
    return m

# 计算间接连通   #其中list l4 存储了两两节点间所有节点
for i in lmore:
    # 一条路径
    if(len(i)==1):
        IndirectConnect(i[0]) #多重嵌套,取第一个
    else:
        sumM = 0
        for j in i:
            #IndirectConnect2(j)
            sumM = sumM + IndirectConnect2(j)
        listW[i[0][len(i[0]) - 1] - 1, i[0][0] - 1] = sumM

def standard(list,c):
    for i in list:
        for j in range(len(i)):
            if(i[j]<c):      #赋值方式：在for循环中直接更改列表中的元素值不会起作用
                i[j]=0
            else:
                i[j]=1
    return list

newList=standard(listW,0.3)


for i in newList:
    print(i)
import codecs

list111=[]
list222=[]
#f = codecs.open("list.txt",'w','utf-8')
#for i in newList:
    #f.write(str(i)+'\r\n')
#f.close()
#for i in node_num:
    #list111.append('"'+str(i)+'"')

#print(list111)
