import numpy as np
import matplotlib.pyplot as plt
import os


path = './'
files = os.listdir(path+"pband_dir/")
for ii in range(len(files)-1, -1, -1):
    if 'pb' not in files[ii]:
        del files[ii]
#先按元素排序
files.sort()
elems = []
for file in files:
    elems.append(file.split('_')[0])
elems = list(set(elems))
if len(elems) > 4:
    print('元素超过4种，请设置线型或颜色！')

#对轨道排序
filesorb = []
for file in files:
    elem = file.split('_')[0]
    orb = file.split('_')[1].split('-')[0]
    orb = int(orb) + 10 * elems.index(elem)
    filesorb.append([orb, file])
filesorbsort = sorted(filesorb, key=lambda x: x[0])
filesorbsort = np.array(filesorbsort)
files = filesorbsort[:, 1]

#设置不同原子的线型
linestyles = ['solid', 'dashed', 'dotted', 'dashdot' ]
#设置不同轨道的颜色
orbs = ['1', '2', '5', '10']
orbcolors = [ 'blue', 'green', 'orange', 'red']

#读取nkpts和nbands
with open(path+"pband_dir/" + files[0], 'r') as file_pband:
    data_pband = file_pband.readlines()
nkpts = int(data_pband[1].strip().split(':')[1].split()[0])
nbands = int(data_pband[1].strip().split(':')[1].split()[1])
# print(nkpts, nbands)

height_label = 0
plt.figure(figsize=(16, 9))
for file in files:
    bandsdata = np.loadtxt(path+"pband_dir/"+file)

    enmax = max(bandsdata[:, 1])
    enmin = min(bandsdata[:, 1])

    weight_E = []
    nn = 200
    for ii in range(nn):
        dEl = enmin + ii * (enmax - enmin)/nn
        dEr = enmin + (ii+1) * (enmax -enmin)/nn
        weight = 0
        for jj in range(len(bandsdata)):
            if bandsdata[jj, 1] >=dEl and bandsdata[jj, 1] < dEr:
                weight += bandsdata[jj, 2]
        weight_E.append([dEl, weight])

    weight_E = np.array(weight_E)

    elem = file.split('_')[0]
    linesty = linestyles[elems.index(elem)]
    orb = file.split('_')[1].split('-')[0]
    orbcolor = orbcolors[orbs.index(orb)]
    plt.plot(weight_E[:, 0], weight_E[:, 1], label=file, linestyle=linesty, color=orbcolor)


    bandleftrange = []
    bandrightrange = []
    flag = 0
    bandleft = 0
    bandright = 0
    for ii in range(len(weight_E)):
        if abs(weight_E[ii, 1]) > 0.0 and flag == 0:
            flag = 1
            bandleft = weight_E[ii - 1, 0]
            bandleftrange.append(bandleft)
        if abs(weight_E[ii, 1]) <= 0.0 and flag == 1:
            bandright = weight_E[ii, 0]
            bandrightrange.append(bandright)
            flag = 0

    if len(bandleftrange) > 0:
        edges = []
        for edge in bandleftrange:
            break_flag = False
            for ii in range(nbands):
                for jj in range(nkpts):
                    if bandsdata[ii * nkpts + jj, 1] - edge > 0.0:
                        edge_band = ii + 1
                        # print(ii)
                        edges.append([edge, edge_band])
                        break_flag = True
                        break
                if break_flag:
                    break
            #print('能窗下限带指标: ', edge_band)

        for edge in bandrightrange:
            break_flag = False
            for ii in range(nbands):
                for jj in range(nkpts):
                    if bandsdata[ii * nkpts + jj, 1] - edge > 0.0:
                        edge_band = ii
                        # print(ii)
                        edges.append([edge, edge_band])
                        break_flag = True
                        break
                if break_flag:
                    break

        edges = np.array(edges)

        bandslab = edges[:, 1]
        bandslab = bandslab.astype(int)
        bandslab = bandslab.astype(str)
        for kk in range(len(bandslab)):
            plt.text(edges[kk, 0], 500+height_label, bandslab[kk])

    height_label += 50


plt.legend()
plt.xticks(range((int(enmin)//2)*2, (int(enmax)//2)*2, 2))
#plt.show()
plt.savefig(path+"sumofweightforpbands.png", dpi=300)


