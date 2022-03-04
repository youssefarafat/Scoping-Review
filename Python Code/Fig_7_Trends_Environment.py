import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import urllib.request
from urllib.error import HTTPError, URLError
from scipy import interpolate
from socket import timeout
from numpy import matlib as mb
import logging

import nltk
nltk.download('punkt')

from nltk.tokenize import word_tokenize

#Basic keywords, to be concatenated later concatenate
basicURL                = 'https://www.ncbi.nlm.nih.gov/pubmed/?term='
#allF                    = '%5BAll%20Fields%5D%29' # all fields code

yearsAnalysis = np.arange(2010,2023)
KW_Pathology            =  '%20(pathology)'  
KW_Cancer               =  '%20AND%20(cancer)'
KW_ImageAnalysis        =  '%20AND%20+((image)+OR+(imaging))'
KW_Dates                =  '%20AND%20('+str(yearsAnalysis[0])+':'+str(yearsAnalysis[-1])+'[dp])'

KW_ImageAnalysis

keywords=[ '(Matlab))%20NOT%20((rural)%20AND%20(bangladesh))',
          '(Python)%20NOT%20(snake)%20NOT%20(python%20regius)',
          '(%22R%20project%22)%20OR%20(%22R%20package%22)%20OR%20(Rstudio)%20OR%20(R/Shiny)',
          '(%22C programming%22)%20OR%20(%22C language%22)%20OR%20(%22C package%22)']
    
keywords2=['Matlab','Python','R','C','CellProfiler','Fiji','ICY','ImageJ','QuPath']
numKeywords = len(keywords)
numYears    = len(yearsAnalysis)

entries_per_KW_cancer = np.zeros((numKeywords,len(yearsAnalysis))) # keyword (and total) and year
entries_per_KW_all = np.zeros((numKeywords,len(yearsAnalysis))) # keyword (and total) and year

entries_per_KW_cancer.shape
for index_kw,kw in enumerate(keywords):
    urlAddress          = basicURL+'%20('+str.replace(kw,' ','%20')+')%20AND%20'+KW_Pathology+KW_Cancer+KW_ImageAnalysis+KW_Dates
    #print(urlAddress)
    print(index_kw)
    with urllib.request.urlopen(urlAddress,  timeout=50) as url:
        wholeURL =  url.read().decode('utf-8')

        location_init = wholeURL.index('yearCounts')
        location_fin  = wholeURL.index('startYear')
        years_tokens  = word_tokenize(wholeURL[location_init+14:location_fin-11])
        years_tokens2 = [w for w in years_tokens if not w in '[],']
        years         = years_tokens2[::2]
        num_entries   = years_tokens2[1::2]
        
        
        for index_year, val_year in enumerate(years) :
            entries_per_KW_cancer[index_kw,round(float(val_year))-(yearsAnalysis[0])] = float(num_entries[index_year])
for index_kw,kw in enumerate(keywords):
    urlAddress          = basicURL+'%20('+str.replace(kw,' ','%20')+')%20AND%20'+KW_Dates
    #print(urlAddress)
    print(index_kw)
    with urllib.request.urlopen(urlAddress,  timeout=50) as url:
        wholeURL =  url.read().decode('utf-8')

        location_init = wholeURL.index('yearCounts')
        location_fin  = wholeURL.index('startYear')
        years_tokens  = word_tokenize(wholeURL[location_init+14:location_fin-11])
        years_tokens2 = [w for w in years_tokens if not w in '[],']
        years         = years_tokens2[::2]
        num_entries   = years_tokens2[1::2]
        
        
        for index_year, val_year in enumerate(years) :
            entries_per_KW_all[index_kw,round(float(val_year))-(yearsAnalysis[0])] = float(num_entries[index_year])
allEntries_KW = entries_per_KW_cancer.sum(axis=1)

sortedValues = np.sort(allEntries_KW)
sortedIndex  = np.argsort(allEntries_KW)
temp =[keywords2[i] for i in sortedIndex]


fig = plt.figure( figsize=(8, 4))
ax  = fig.add_subplot(111)
ax.bar(temp[::-1],sortedValues[::-1])
ax.tick_params(axis='x', rotation=270, labelsize=18)
ax.tick_params(axis='y',  labelsize=18)
ax.set_yscale('linear')
ax.grid()

#type_lines=['-','--',':','-.']
fig2 = plt.figure( figsize=(11, 8))

ax2=fig2.gca(projection='3d')
for index_kw,kw in enumerate(keywords):
    ax2.plot3D(yearsAnalysis,index_kw*np.ones(13),(entries_per_KW_cancer[index_kw,:]),linewidth=4)  #/(1+entries_per_KW[numKeywords-1]),label=kw, linestyle='-',linewidth=0.5+0.5*np.mod(index_kw,8))  #,  marker='.', color='b',markersize = 5)
    #plt.plot(yearsAnalysis,entries_per_KW_cancer[index_kw,:]/(1+entries_per_KW_cancer[numKeywords-1]),label=kw, linestyle=type_lines[np.mod(index_kw,4)],linewidth=0.5+0.5*np.mod(index_kw,8))  #,  marker='.', color='b',markersize = 5)

ax2.yaxis.set_ticks(np.arange(0,numKeywords))
ax2.yaxis.set_ticklabels(keywords2)
ax2.tick_params(axis='y', rotation=270, labelsize=10)
ax2.view_init(20, 20)

fig2 = plt.figure( figsize=(11, 8))

ax2=fig2.gca(projection='3d')
for index_kw,kw in enumerate(keywords):
    ax2.plot3D(yearsAnalysis,index_kw*np.ones(13),(entries_per_KW_all[index_kw,:]),linewidth=4)  #/(1+entries_per_KW[numKeywords-1]),label=kw, linestyle='-',linewidth=0.5+0.5*np.mod(index_kw,8))  #,  marker='.', color='b',markersize = 5)
    #plt.plot(yearsAnalysis,entries_per_KW_cancer[index_kw,:]/(1+entries_per_KW_cancer[numKeywords-1]),label=kw, linestyle=type_lines[np.mod(index_kw,4)],linewidth=0.5+0.5*np.mod(index_kw,8))  #,  marker='.', color='b',markersize = 5)

ax2.yaxis.set_ticks(np.arange(0,numKeywords))
ax2.yaxis.set_ticklabels(keywords2)
ax2.tick_params(axis='y', rotation=270, labelsize=10)
ax2.view_init(20, 20)
