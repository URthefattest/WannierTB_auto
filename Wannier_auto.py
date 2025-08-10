import numpy as np
import matplotlib.pyplot as plt
import os
import math


# ======================================================================================================================
# readme: 需要Ef，TDOS，pband，原子数
with open('../DOSCAR') as doscar:
    data_doscar = doscar.readlines()
Ef = float(data_doscar[5].strip().split()[3])
print('============================================')
print("费米能 EF = ", Ef, ' eV')

# 设置超出Ef的范围
bias = 2
print('设定最低小能窗高于EF bias: ', bias, 'eV')

# ======================================================================================================================
#选投影子，确定大能窗范围
EF = Ef
thresh_weight = 0.03
dos = np.loadtxt('../TDOS_SOC.dat')
bandrange = []
flag = 0
bandleft = 0
bandright = 0
for ii in range(len(dos)):
    if abs(dos[ii, 1]) > 0.0 and flag == 0:
        flag = 1
        bandleft = dos[ii - 1, 0]
    if abs(dos[ii, 1]) <= 0.0 and flag == 1:
        bandright = dos[ii, 0]
        bandrange.append([bandleft, bandright])
        flag = 0
print('从DOS分析得到能带范围：')
print(bandrange)
for ii in range(len(bandrange)-1, -1, -1):
     if bandrange[ii][0] < 0 and bandrange[ii][0]-bandrange[ii-1][1] > 1:
          #print(bands[ii][0])
          froz_wind_dn = bandrange[ii][0]
          break

froz_wind_dn += EF
froz_wind_up = EF + bias


#轨道权重数据
files = os.listdir("../eb/pband_dir/")
for ii in range(len(files)-1, -1, -1):
    if 'pb' not in files[ii]:
        del files[ii]
#先按元素排序
files.sort()
elems = []
for file in files:
    elems.append(file.split('_')[0])
elems = list(set(elems))

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

#读取nkpts和nbands
with open("../eb/pband_dir/" + files[0], 'r') as file_pband:
    data_pband = file_pband.readlines()
nkpts = int(data_pband[1].strip().split(':')[1].split()[0])
nbands = int(data_pband[1].strip().split(':')[1].split()[1])
# print(nkpts, nbands)


#计算小能窗内各轨道总权重
weight_orbs = []
for file in files:
    bandsdata = np.loadtxt("../eb/pband_dir/"+file)
    weight = 0
    for jj in range(len(bandsdata)):
        if bandsdata[jj, 1] >= froz_wind_dn and bandsdata[jj, 1] < froz_wind_up: #设置小能窗范围内
            weight += bandsdata[jj, 2]
    weight_orbs.append([file, weight])

#所有轨道总权重
sumweght = 0
for ii in range(len(weight_orbs)):
    sumweght += weight_orbs[ii][1]

#各轨道占比
print('--------------------------------------------')
print("%-15s %10s %6s" % ('轨道', '总权重', '占比'))
weight_orbs_ratio = []
temp = weight_orbs[0][0].split('_')[0]
for ii in range(len(weight_orbs)):
    weight_orbs_ratio.append([weight_orbs[ii][0], weight_orbs[ii][1]/sumweght, '{:.1%}'.format(weight_orbs[ii][1]/sumweght)])
    if weight_orbs[ii][0].split('_')[0] != temp:
        print(' ')
        temp = weight_orbs[ii][0].split('_')[0]
    print("%-20s %10s %8s" % (weight_orbs[ii][0], '{:.2f}'.format(weight_orbs[ii][1]), '{:.1%}'.format(weight_orbs[ii][1]/sumweght)))
print('--------------------------------------------')
#根据轨道占比确定投影子
print('轨道选取阈值：', thresh_weight)
projectors = []
for ii in range(len(weight_orbs_ratio)):
    if weight_orbs_ratio[ii][1] >= thresh_weight:
        projectors.append(weight_orbs_ratio[ii][0])


#设置大能窗左边排除带
excludebands = 10000
break_flag = False
for ii in range(nbands):
    for jj in range(nkpts):
        if bandsdata[ii * nkpts + jj, 1] - froz_wind_dn > 0.0:
            # print(ii)
            excludebands = ii
            break_flag = True
            break
    if break_flag:
        break

print('投影子   所有左带边')
for projector in projectors:
    # if projector != 'Pt_5-9_pb.dat':
    #     continue
    bandsdata = np.loadtxt("../eb/pband_dir/"+projector)

    enmax = max(bandsdata[:, 1])
    enmin = min(bandsdata[:, 1])
    weight_E = []
    nn = 200
    for ii in range(-1, nn): #能量小区间
        dEl = enmin + ii * (enmax - enmin)/nn
        dEr = enmin + (ii+1) * (enmax - enmin)/nn
        weight = 0
        for jj in range(len(bandsdata)): #能量小区间内的k点的轨道的权重求和
            if bandsdata[jj, 1] >=dEl and bandsdata[jj, 1] < dEr:
                weight += bandsdata[jj, 2]
        weight_E.append([dEl, weight])
    weight_E = np.array(weight_E)

    elem = projector.split('_')[0]
    orbsym = projector.split('_')[1].split('-')[0]

    projleftrange = []
    projrightrange = []
    flag = 0
    projleft = 0
    projright = 0
    for ii in range(len(weight_E)):
        if abs(weight_E[ii, 1]) > 0.0 and flag == 0:
            flag = 1
            projleft = weight_E[ii - 1, 0]
            #projleftrange.append(projleft)
        if abs(weight_E[ii, 1]) <= 0.0 and flag == 1:
            projright = weight_E[ii, 0]
            #计算能带区间内的权重是否可忽略
            weightsum = 0
            for jj in range(len(weight_E)):
                if weight_E[jj, 0] >= projleft and weight_E[jj, 0] < projright:
                    weightsum += weight_E[jj, 1]
            if weightsum > 100:
                #如果能带不可忽略则计入左右带边
                projleftrange.append(projleft)
                projrightrange.append(projright)
            flag = 0

    if len(projleftrange) > 0:
        leftedges = [] #投影子所有左边界带指标
        for edge in projleftrange:
            break_flag = False
            for ii in range(nbands):
                for jj in range(nkpts):
                    if bandsdata[ii * nkpts + jj, 1] - edge > 0.0:
                        edge_band = ii + 1
                        # print(ii)
                        leftedges.append(edge_band)
                        break_flag = True
                        break
                if break_flag:
                    break
            #print('能窗下限带指标: ', edge_band)

        rightedges = [] #投影子所有右边界带指标
        for edge in projrightrange:
            break_flag = False
            for ii in range(nbands):
                for jj in range(nkpts):
                    if bandsdata[ii * nkpts + jj, 1] - edge > 0.0:
                        edge_band = ii
                        # print(ii)
                        rightedges.append(edge_band)
                        break_flag = True
                        break
                if break_flag:
                    break

        excludeproj = min(leftedges) - 1
        excludebands = min(excludebands, excludeproj)
        print(projector, '  ', leftedges)
print('--------------------------------------------')


window_down_band = excludebands + 1



# ======================================================================================================================
# 计算wannier轨道数
orbs_elem = {}
for ii in elems:
    num = 0
    for jj in projectors:
        if jj.split('_')[0] == ii:
            if jj.split('_')[1] == '1':
                num += 1
            elif jj.split('_')[1] == '2-4':
                num += 3
            elif jj.split('_')[1] == '5-9':
                num += 5
            elif jj.split('_')[1] == '10-16':
                num += 7
    orbs_elem[ii] = num
# print('元素轨道种数: ', orbs_elem)

with open('./POSCAR', 'r') as poscar:
    data_poscar = poscar.readlines()
elems_poscar = data_poscar[5].strip().split()
num_elems_poscar = list(map(int, data_poscar[6].strip().split()))
atoms_elem = {}
for ii in range(len(elems_poscar)):
    atoms_elem[elems_poscar[ii]] = num_elems_poscar[ii]
# print(atoms_elem)
# atoms_elem = {'Mn': 4, 'Nb': 4, 'P': 4}
num_wann = 0
for ii in orbs_elem:
    num_wann += orbs_elem[ii] * atoms_elem[ii]
num_wann *= 2
print('wannier轨道数: ', num_wann)




# print('==========================Final==================================')

print('小能窗上限超过Ef：', froz_wind_up - Ef)
print('小能窗下限低于Ef：', Ef - froz_wind_dn)
print('============================================')
proj = []
for ii in elems_poscar:
    temp_list = []
    temp_list.append(ii)
    temp_dic = {}
    for jj in projectors:
        if jj.split('_')[0] == ii:
            if jj.split('_')[1] == '1':
                # temp_list.append('s')
                temp_dic['0'] = 's'
            elif jj.split('_')[1] == '2-4':
                # temp_list.append('p')
                temp_dic['1'] = 'p'
            elif jj.split('_')[1] == '5-9':
                # temp_list.append('d')
                temp_dic['2'] = 'd'
            elif jj.split('_')[1] == '10-16':
                # temp_list.append('f')
                temp_dic['3'] = 'f'
    if temp_dic == {}:
        continue
    for jj in sorted(temp_dic):
        temp_list.append(temp_dic[jj])
    proj.append(temp_list)

for ii in range(len(proj)):
    proj[ii] = proj[ii][0] + ': ' + '; '.join(proj[ii][1:]) + '\n'

with open('./wannierjob.sh', 'r') as job:
    data_job = job.readlines()
ncore = int(data_job[2].split()[2])
nbands_incar = excludebands + 2 * num_wann
nbands_incar = math.ceil(nbands_incar / ncore) * ncore

with open('./INCAR', 'r') as incar:
    data_incar = incar.readlines()
data_incar[5] = 'NBANDS = ' + str(nbands_incar) + '\n'
with open('./INCAR', 'w') as incar:
    incar.writelines(data_incar)

#with open('./INCAR', 'r') as incar:
#    data_incar = incar.readlines()
#for ii in data_incar:
#    if ii[:8] == 'NBANDS =':
#        nbands_incar = int(ii.strip().split()[2])

if excludebands == 0 or excludebands == 1:
    strexcludedn = ''
else:
    strexcludedn = '1-' + str(excludebands) + ', '

win = ['#体系相关部分\n',
       'num_bands = ' + str(nbands_incar - window_down_band + 1 - 4) + ' #考虑进去的DFT能带数，等于DFT总能带数减去exclude_bands中的能带数\n',
       'num_wann = ' + str(num_wann) + ' #Wannier轨道数，需要考虑spinor\n',
       'dis_froz_max = ' + str(froz_wind_up) + '  #小能窗上限\n',
       'dis_froz_min = ' + str(froz_wind_dn) + ' #小能窗下限\n',
       'exclude_bands: ' + strexcludedn + str(nbands_incar - 4 + 1) + '-' + str(
           nbands_incar) + '\n',
       'begin projections\n',
       'end projections\n',
       '################\n',
       'dis_num_iter = 2000 #解纠缠的最大迭代步数\n',
       'dis_mix_ratio = 1 #解纠缠迭代时的mix程度\n',
       'iprint = 2 #控制输出文件内容的多少\n',
       'num_iter = 0 #完成解纠缠后最局域化过程的迭代次数,一般解纠缠步骤已经满足要求了\n',
       'num_print_cycles = 100\n',
       'conv_window = 3\n',
       '#write_hr = T\n\n']

for ii in range(len(proj)):
    win.insert(7 + ii, proj[ii])
# print(win)
with open('wannier90.win', 'w') as file_win:
    file_win.writelines(win)

#for ii in win:
#    print(ii)
