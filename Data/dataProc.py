
import pandas as pd
import numpy as np
import os
import pickle

Density="2.5"
EnergyType=5
input_path="5plus5_SingleSource/"
dump_path = "Cache/"
output_path="ans.csv"
#detection type
dt=["SGS","STGS4EB","STGS4ER","STGS8EB","STGS8ER"]

def Import(DetectionType):
    fin=open(input_path+Density+"_"+DetectionType+".txt")
    try:
        all_lines = fin.readlines()
    finally:
        fin.close()

    df=pd.DataFrame(columns=("Radius","Density","DetectionType",
                             0,1,2,5,"total"))

    i=0
    for line in all_lines:
        line=line.split()
        nums=[2.5*i,#radius
        float(line[1]),
        DetectionType,
        float(line[2]),
        float(line[3]),
        float(line[4]),
        float(line[5]),
        float(line[6])]
        df.loc[i]=pd.Series(nums,index=df.columns)
        i+=1
    return df

def get_df(Density):
    frames=[Import(dt[0]),
        Import(dt[1]),
        Import(dt[2]),
        Import(dt[3]),
        Import(dt[4])]
    df=pd.concat(frames,ignore_index=True)#ignore_index or index will repeat
    return df

#get all data where density equal xxx
df=get_df("0.5")
'''
if os.path.exists(dump_path):
    ans = pickle.load(open(dump_path))
else:
    ans=pd.DataFrame(columns=("Density","EnergyType","Max.","Min.","RMS"))
'''
ans=pd.DataFrame(columns=("Density","EnergyType","Max.","Min.","RMS"))


def get_y(DetectionType):
    #df[(df["Density"]==Density) & (df["DetectionType"]==DetectionType)][EnergyType]/10000000.0-1
    y=df[df["DetectionType"]==DetectionType][EnergyType]/100000.0-100#percent,%
    new=pd.DataFrame( {"Density":Density,"EnergyType":EnergyType,
            "Max.":"%.2f" % y.max(),
            "Min.":"%.2f" % y.min(),
            "RMS":"%.2f" % np.sqrt((y**2).mean()) },
        index=[0])
    global ans#change global variable need statement ahead
    ans=ans.append(new,ignore_index=True)

    return y

def get_all_y(e):
    return [get_y(dt[0]),get_y(dt[1]),get_y(dt[2]),get_y(dt[3]),get_y(dt[4])]



y=get_all_y(0)
print ans
pickle.dump(ans, open(dump_path+Density+"_"+str(EnergyType)+".pkl", 'w'))

def paint():
    import matplotlib.pyplot as plt
    x = 2.5*np.arange(14)

    ax = plt.subplot(111) #注意:一般都在ax中设置,不再plot中设置
    plt.plot(x,y[0],",-",label=dt[0])
    plt.plot(x,y[1],".-",label="STGS4EA")
    plt.plot(x,y[2],"s-",label=dt[2])
    plt.plot(x,y[3],"v-",label="STGS8EA")
    plt.plot(x,y[4],"x-",label=dt[4])
    plt.legend()
    plt.xlim(0,35)

    #y-axis format into percent(%) style
    import matplotlib.ticker as mtick
    fmt='%.0f%%'
    yticks = mtick.FormatStrFormatter(fmt)
    ax.yaxis.set_major_formatter(yticks)
    
    ax.yaxis.grid(True)
    ax.set_xlabel("r(cm)")
    ax.set_ylabel("Det")

    #plt.title("0.5")
    plt.show()

paint()

def output_all():
    result=pd.DataFrame(columns=("Density","EnergyType","Max.","Min.","RMS"))
    for parent,dirnames,filenames in os.walk(dump_path):
        #print filenames
        for index,item in enumerate(filenames):
            #print filenames[index]
            result=result.append(pickle.load(open(dump_path+filenames[index])))
    result.to_csv(output_path,index=False,index_label=False)

output_all()