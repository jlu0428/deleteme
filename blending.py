# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 18:22:01 2018

@author: cindylu
"""


from gurobipy import *

m= Model("Blending")
m.ModelSense=GRB.MAXIMIZE
m.setParam('TimeLimit',7200)

o1g=m.addVar(vtype=GRB.CONTINUOUS,name='o1g',lb=0.0)
o1h=m.addVar(vtype=GRB.CONTINUOUS,name='o1h',lb=0.0)
o2g=m.addVar(vtype=GRB.CONTINUOUS,name='o2g',lb=0.0)
o2h=m.addVar(vtype=GRB.CONTINUOUS,name='o2h',lb=0.0)

m.update()


m.addConstr(o1g+o1h,GRB.LESS_EQUAL,5000.0,"Oil1_usage")
m.addConstr(o2g+o2h,GRB.LESS_EQUAL,10000.0,"Oil2_usage")
m.addConstr(o1g*10.0+o2g*5.0,GRB.GREATER_EQUAL,(o1g+o2g)*8.0,"GasolineQuantityLevel")
m.addConstr(o1h*10.0+o2h*5.0,GRB.GREATER_EQUAL,(o1h+o2h)*6.0,"HeatingQuantityLevel")

m.setObjective((o1g+o2g)*75.0+(o1h+o2h)*60.0+(5000.0-o1g-o1h)*65.0+(10000-o2g-o2h)*50.0,GRB.MAXIMIZE)


m.update()

m.optimize()


for var in m.getVars():
    print("Variable Name = %s, Optimal Value = %s, Lower Bound = %s, Upper Bound = %s" % (var.varName, var.x,var.lb,var.ub))
max_revenue=(o1g.x+o2g.x)*75.0+(o1h.x+o2h.x)*60.0+(5000.0-o1g.x-o1h.x)*65.0+(10000-o2g.x-o2h.x)*50.0
print("The optimized max revenue is $", max_revenue,'when put',o1g.x,'and',o1h.x,'barrels of crude oil 1 into Gasoline and heating oil',',',o2g.x,'and',o2h.x,'barrels of crude oil 2 into gasoline and heating oil.')
print('Analysis:Chanlder should sell more heating oil than gasoline to meet its optimal production level. Since this solution used up all inputes, there were no leftover to sell. ')

print('From the chart, we can see that revenue stays $950000 when gasoline selling price in range $40~$60. Total revenue keeps increasing after gasoline price exceeded $60, this might indicate that Chandler can try to keep increasing gasoline price to reach a higher level revenue' )
price_level=(100-40)//5
gasoline_price=35
gasoline_price_list=[]
revenue_list=[]


for i in range(price_level+1):
    gasoline_price=gasoline_price + 5
    m.setObjective((o1g+o2g)*gasoline_price+(o1h+o2h)*60.0+(5000.0-o1g-o1h)*65.0+(10000-o2g-o2h)*50.0,GRB.MAXIMIZE)
    m.update()
    m.optimize()
    

    gasoline_price_list.append(gasoline_price)
    revenue=(o1g.x+o2g.x)*gasoline_price+(o1h.x+o2h.x)*60.0+(5000.0-o1g.x-o1h.x)*65.0+(10000-o2g.x-o2h.x)*50.0
    revenue_list.append(revenue)
for p in range (len(gasoline_price_list)):
    print('The maximum revenue is ','${:,.2f}'.format(revenue_list[p]),'when gasoline price is','${:,.2f}'.format(gasoline_price_list[p] ))
    
    

import matplotlib.pyplot as plt
plt.plot(gasoline_price_list,revenue_list)
plt.title("selling price VS revenue")
plt.xlabel('selling price $')
plt.ylabel('revenue $')

 