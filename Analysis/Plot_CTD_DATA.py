# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

def extract_quantities(line, key):
    fullname = line.partition(': ')[2]
    index = int(line.split(' ')[2])
    return fullname, index

# <codecell>

# function from Jody Klymak
def getSpice(pden,temp,sal):
             
    import seawater as sw
    import numpy as np

    beta = 7.7e-4*1000
    alpha = 2.0e-4*1000
    Sline=np.array([33.2,33.8])
    Tline=np.array([7.75,6.6])
    Sarray = np.arange(30,35,0.01)
    m = (np.diff(Tline)/np.diff(Sline))
    Tarray = m*(Sarray-Sline[0])+Tline[0]
    Pdarray=sw.pden(Sarray,Tarray,100.+0.*Tarray,0.)
    #plot(Pdarray)
    S0 = np.interp(pden,Pdarray,Sarray)
    T0 = m*(S0-Sline[0])+Tline[0]
    dT = -(T0-temp)
    dS = -(S0-sal)
    tau = beta*(dS)+alpha*(dT)
    return tau

# <codecell>

# function from Jody Klymak
def plotTopo():
    topo_datastruct = sio.loadmat('../topo/SouthVIgrid.mat')
    topo_struct = topo_datastruct['SouthVIgrid']
    topo = topo_struct[0,0]
    indx = np.where((np.squeeze(topo['lon'])>-126.4) & (np.squeeze(topo['lon'])<-124.5))[0]
    indy = np.where(np.squeeze(topo['lat']>47.8) & np.squeeze(topo['lat']<48.8))[0]
    
    plt.rcParams['contour.negative_linestyle'] = 'solid'
    x = np.squeeze(topo['lon'])[indx]
    y = np.squeeze(topo['lat'])[indy]
    Z = topo['depth'][indy,:]
    Z = Z[:,indx]
    plt.contourf(x,y,Z)
    plt.contour(x,y,Z,
            np.arange(-200.,0,25.),colors='0.4',linestyles='-',linewidth=0.25)
    plt.contour(x,y,Z,
            [-2000.,-1000.,-200.,-100.],colors='k',linestyles='-',linewidth=1.5)
    plt.contour(x,y,Z,
            np.arange(-2000.,-200.,200.), colors='0.6', linestyles='-', linewidth=0.35)                
    plt.contour(x,y,Z,
            [0.,0.],colors='k',linewidth=3)

# <codecell>

# <codecell>

import os
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio
from matplotlib.backends.backend_pdf import PdfPages

pdf = PdfPages('ctdplots.pdf')

DIRECTORY = '../5_bin'
QUANTITIES = {
    'prDM': 'pressure',
    'sal00': 'salinity1',
    'potemp090C': 'temperature1',
    'potemp190C': 'temperature2',
    'sbeox0ML/L': 'oxygen',
    'CStarTr0': 'transmission',
    'Density [sigma-theta': 'sigma1',
}
            
index = {}
fullname = {}

#filenames = ['FK009A_CTD005_20130820.cnv']
filenames = [f for f in os.listdir(DIRECTORY) if f.startswith('FK')]
for filename in sorted(filenames):
    f = open(os.path.join(DIRECTORY, filename), 'rt')
    for line in f:
        line = line.strip()
        if line.startswith('*'):
            # header line, look for useful info
            if 'Latitude' in line:
                latitude = line.partition(' = ')[2]
            if 'Longitude' in line:
                longitude = line.partition(' = ')[2]
            if 'Time' in line:
                time = line.partition(' = ')[2]
            if 'Station' in line:
                station = line.partition(': ')[2]
            if line == '*END*':
                break
        elif line.startswith('# name'):     
            if int(line.split(' ')[2]) < 22: # this is sad, but don't want the last salinity
            # comment line, look for plotable quantities information
                for key,value in QUANTITIES.items():
                    if key in line:
                        fullname[value], index[value] = extract_quantities(line, key) 
        
    thedata = np.loadtxt(f).transpose()
    
    # calculate "Spice"
    tau = getSpice(1000.+thedata[index['sigma1'],:],
                   thedata[index['temperature1'],:],thedata[index['salinity1'],:])
    
    # type the info
    strone = 'Station: '+station+' at '+latitude+','+longitude
    strtwo = 'On: '+time+'UTC'
    strthree = 'Filename: '+filename

    
    fig = plt.figure(1, figsize=(8.5,11))
    
    axgeo = plt.axes([0.08,0.52,0.42,0.42])    
    plotTopo()
    axgeo.set_aspect(1./np.cos(48.5*np.pi/180.))
    axgeo.set_xlabel('Longitude')
    axgeo.set_ylabel('Latitude')
#   plot station
    value_longitude = -int(longitude.split(' ')[0])-float(longitude.split(' ')[1])/60.
    value_latitude = int(latitude.split(' ')[0])+float(latitude.split(' ')[1])/60.
    
    plt.plot(value_longitude,value_latitude,'rd',markersize=9)
    
    # do the (TS) plot
    ts = plt.axes([0.61,0.61,0.25*11/8.5,0.25])
    ts.annotate(strone, xy=(0.15, 0.97),
                xycoords='figure fraction', horizontalalignment='left',
                verticalalignment='top',fontsize=18)
    ts.annotate(strtwo, xy=(0.15, 0.94),
                xycoords='figure fraction', horizontalalignment='left',
                verticalalignment='top',fontsize=15)
    ts.annotate(strthree, xy=(0.15, 0.91),
                xycoords='figure fraction', horizontalalignment='left',
                verticalalignment='top',fontsize=15)
    ts.plot(thedata[index['salinity1'],:],thedata[index['temperature1'],:],'k')
    ts.set_xlabel(fullname['salinity1'])
    ts.set_ylabel(fullname['temperature1'])
    
    # do the profiles
    ax1 = plt.axes([0.08,0.1,0.25,0.4])
    ax1.plot(thedata[index['salinity1'],:],thedata[index['pressure'],:])
    ax1.invert_yaxis()
    ax1.set_xlabel(fullname['salinity1'])
    ax1.xaxis.label.set_color('blue')
    ax1.set_ylabel(fullname['pressure'])
    ax2 = ax1.twiny()
    ax2.plot(thedata[index['temperature1'],:],thedata[index['pressure'],:],'r')
    ax2.xaxis.label.set_color('red')
    ax2.set_xlabel(fullname['temperature1'])
    
#    ax3 = plt.subplot2grid((2,6),(1,2), colspan=2)
    ax3 = plt.axes([0.39,0.1,0.25,0.4])
    ax3.plot(thedata[index['transmission'],:],thedata[index['pressure'],:],'brown')
    ax3.invert_yaxis()
    ax3.xaxis.label.set_color('brown')
    ax3.set_xlabel(fullname['transmission'])

#    ax4: for fluoresence when I get that figured out

#    ax5 = plt.subplot2grid((2,6),(1,4),colspan=2)
    ax5 = plt.axes([0.70,0.1,0.25,0.4])
    ax5.plot(thedata[index['oxygen'],:], thedata[index['pressure'],:],'teal')
    ax5.invert_yaxis()
    ax5.xaxis.label.set_color('teal')
    ax5.set_xlabel(fullname['oxygen'])
    ax6 = ax5.twiny()
    ax6.plot(tau,thedata[index['pressure'],:],'m')
    ax6.xaxis.label.set_color('magenta')
    ax6.set_xlabel('Spice relative to Eddy [kg/m3]')
    plt.savefig(pdf, format='pdf')
    pdf.close()
    

    




