import os, sys
import ROOT
import matplotlib.pyplot as plt
import numpy as np
import pandas
import plotly.graph_objects as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

def GetNumpyArray(inPandaTable, ncol: int):
    ## Transforms columns in np.array
    return np.array(inPandaTable.iloc[:, [ncol]])[:, 0]

if (len(sys.argv) < 1):
	print("Please specify the output file")
	sys.exit(1)

outputfile = sys.argv[1]

file = ROOT.TFile.Open(outputfile)

tree = file.Get("myTree;3")

# Read using PANDAS
channelmap = pandas.read_table("optical_mapping.txt", delimiter=' ')

xpds= GetNumpyArray(channelmap, 1)
ypds= GetNumpyArray(channelmap, 2)
zpds= GetNumpyArray(channelmap, 3)

##print(xpds)

event=29187 ## Example: one photon origin from event 29187

tree.GetEntry(event)

numberPDS=tree.GetLeaf("numberDevices").GetValue()

leaf_hits = tree.GetLeaf("VUV_hits")
leaf_x = tree.GetLeaf("X")
leaf_y = tree.GetLeaf("Y")
leaf_z = tree.GetLeaf("Z")

hits=[]

for i in range(int(numberPDS)):
        
    hits.append(leaf_hits.GetValue(i))
    
hits=np.array(hits)

xorigin= leaf_x.GetValue()
yorigin= leaf_y.GetValue()
zorigin= leaf_z.GetValue()

xorigin=np.array(xorigin)
yorigin=np.array(yorigin)
zorigin=np.array(zorigin)


trace = go.Scatter3d(x=xpds,
                     y=ypds,
                     z=zpds,
                     mode='markers',
                     marker=dict(size=1.5, color=hits, colorscale= 'viridis', colorbar=dict(thickness=20, title='Number of Hits')),
                     hovertext = ['Hits=%d' % (hits[j]) for j in range(len(hits))],
					 showlegend=False
					 )
    
fig = go.Figure(data=[trace])


fig.add_trace(go.Scatter3d(
    x=xorigin,
    y=yorigin,
    z=zorigin,
    mode='markers',
    marker=dict(size=3., color='red', opacity=0.8),
	showlegend=False
))


fig.update_layout(
    scene = dict(
        xaxis = dict(nticks=10, range=[-700,700],title='X (cm)'),
        yaxis = dict(nticks=10, range=[-600,600],title='Y (cm)'),
        zaxis = dict(nticks=20, range=[0,5800],title='Z (cm)')), 
        scene_aspectmode='manual',
        scene_aspectratio=dict(x=0.3, y=0.3, z=1),
        title_text="VUV photons in Anode", title_x=0.5)
        
fig.show()
