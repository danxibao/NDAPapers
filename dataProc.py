
import pandas as pd
import numpy as np

path="Data\\5plus5_SingleSource\\"
#detection type
dt=["SGS","STGS4EB","STGS4ER","STGS8EB","STGS8ER"]

def Import(Density,DetectionType):
    fin=open(path+Density+"_"+DetectionType+".txt")
    try:
        all_lines = fin.readlines()
    finally:
        fin.close()

    df=pd.DataFrame()  
    df["Radius"]=None
    df["Density"]=None
    df["DetectionType"]=None
    df[0]=None
    df[1]=None
    df[2]=None
    df[5]=None
    df["total"]=None

    i=0
    for line in all_lines:
        line=line.split()
        nums=[]
        nums.append(2.5*i)#radius
        nums.append(float(line[1]))
        nums.append(DetectionType)
        nums.append(float(line[2]))
        nums.append(float(line[3]))
        nums.append(float(line[4]))
        nums.append(float(line[5]))
        nums.append(float(line[6]))
        df.loc[i]=pd.Series(nums,index=df.columns)
        i+=1
    return df

def get_df(Density):
    frames=[Import(Density,dt[0]),
        Import(Density,dt[1]),
        Import(Density,dt[2]),
        Import(Density,dt[3]),
        Import(Density,dt[4])]
    df=pd.concat(frames)
    return df

#get all data where density equal xxx
df=get_df("0.5")

def get_y(DetectionType,EnergyType):
    #df[(df["Density"]==Density) & (df["DetectionType"]==DetectionType)][EnergyType]/10000000.0-1
    return df[df["DetectionType"]==DetectionType][EnergyType]/100000.0-100#percent,%

def get_all_y(e):
    return [get_y(dt[0],e),get_y(dt[1],e),get_y(dt[2],e),get_y(dt[3],e),get_y(dt[4],e)]




import matplotlib.pyplot as plt

x = 2.5*np.arange(14)

y=get_all_y(0)
   

ax = plt.subplot(111) #注意:一般都在ax中设置,不再plot中设置
plt.plot(x,y[0],"+-",label=dt[0])
plt.plot(x,y[1],".-",label=dt[1])
plt.plot(x,y[2],"s-",label=dt[2])
plt.plot(x,y[3],"v-",label=dt[3])
plt.plot(x,y[4],"x-",label=dt[4])
plt.legend()

#y-axis format into percent(%) style
import matplotlib.ticker as mtick
fmt='%.0f%%'
yticks = mtick.FormatStrFormatter(fmt)
ax.yaxis.set_major_formatter(yticks)
ax.set_xlabel("r(cm)")
ax.set_ylabel("Det")

#plt.title("0.5")
plt.show()