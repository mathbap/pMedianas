#!/usr/bin/env python
# coding: utf-8

# # <ins>Problema das P-Medianas</ins>

# <div style="text-align: justify"> No Problema das P-Medianas busca-se encontrar o nó de uma rede que apresenta a menor distância entre todos os outros.  </div> 

# ### 1) Base de Dados

# In[ ]:


import pandas as pd
import time
from gurobipy import *

start_01 = time.time()
#-----------------------
tb = pd.read_csv("nodes.csv", sep = ";")
#-------------------------------------------------------------------------
m = Model("pMedianas")
nodes = list(range(1, max(tb.iloc[:, 0].max(), tb.iloc[:, 1].max()) + 1))
links = [(tb.iloc[i, 0], tb.iloc[i, 1]) for i in range(len(tb))]
dist = dict(zip(links, tb.iloc[:, 2]))
#-----------------------
end_01 = time.time()
print(end_01 - start_01)


# \begin{equation}
# x_{ij}, y_{i} \in \{0,1\}
# \end{equation}

# In[ ]:


start_02 = time.time()
#-----------------------
x = m.addVars(nodes, nodes, vtype = GRB.BINARY, name = "x")
y = m.addVars(nodes, vtype = GRB.BINARY, name = "y")
print("vars.ok")
#-----------------------
end_02 = time.time()
print(end_02 - start_02)


# \begin{equation}
# min \sum_{i \in N} \sum_{j \in N}d_{ij}x_{ij}
# \end{equation}

# In[ ]:


start_03 = time.time()
#-----------------------
m.setObjective(sum(sum(dist[i,j] * x[i,j] for i in nodes) for j in nodes), GRB.MINIMIZE)
print("obj.ok")
#-----------------------
end_03 = time.time()
print(end_03 - start_03)


# \begin{equation}
# \sum_{j \in N}x_{ij} = 1 \hspace{0.5cm}  \forall i \in  N
# \end{equation}

# In[ ]:


start_04 = time.time()
#-----------------------
r1 = m.addConstrs( (sum(x[i,j] for j in nodes) == 1 for i in nodes), name = "R1")
print("r1.ok")
#-----------------------
end_04 = time.time()
print(end_04 - start_04)


# \begin{equation}
# \sum_{j \in N}y_{j} = P \hspace{0.5cm}
# \end{equation}

# In[ ]:


start_05 = time.time()
#-----------------------
r2 = m.addConstr( (sum(y[i] for i in nodes) == 1 ), name = "R2")
print("r2.ok")
#-----------------------
end_05 = time.time()
print(end_05 - start_05)


# \begin{equation}
# x_{ij} \leq y_{j} \hspace{0.5cm}  \forall i,j \in  N
# \end{equation}

# In[ ]:


start_06 = time.time()
#-----------------------
r3 = m.addConstrs( (x[i,j] <=  y[j] for i in nodes for j in nodes), name = "R3")
print("r3.ok")
#-----------------------
end_06 = time.time()
print(end_06 - start_06)


# In[ ]:


start_07 = time.time()
#-----------------------
#m.write("pMedianas.lp")
m.optimize()
m.write("pMedianas.sol")
#-----------------------
end_07 = time.time()
print(end_07 - start_07)


# In[ ]:


print("Total Time:", end_07 - start_01)

