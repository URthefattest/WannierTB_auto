with open('PROCAR', 'r') as procar:
    data = procar.readlines()
kps = int(data[1].split('#')[1].split(':')[1].strip())
bands = int(data[1].split('#')[2].split(':')[1].strip())
ions = int(data[1].split('#')[3].split(':')[1].strip())

#print(kps, bands, ions)

with open('POSCAR', 'r') as poscar:
    datapos = poscar.readlines()
elems = datapos[5].split()
elemnums = list(map(int,datapos[6].split()))

projdata = []
for ii in range(len(data)):
    if data[ii].strip() == '':
        continue 
    if data[ii].split()[0]=='k-point':
        kid = int(data[ii].split()[1])
        kcoor = data[ii].split()[3:6]
        bandsdata = []
        for jj in range(ii+1, len(data)):
            if data[jj].strip() == '':
                continue
            if data[jj].split()[0]=='k-point':
                break
            if data[jj].split()[0]=='band':
                bandid = int(data[jj].split()[1])
                energy = data[jj].split()[4]

                for kk in range(jj, len(data)):
                    if data[kk].strip() == '':
                        continue
                    # 每条带的每个k点的数据
                    if data[kk].split()[0]=='ion':
                        weights = [] #所有元素、轨道的权重
                        # 轨道数量
                        if len(data[kk].split())-2 == 9:
                            orbs = [1, 3, 5]
                        elif len(data[kk].split())-2 == 16:
                            orbs = [1, 3, 5, 7]
                        elif len(data[kk].split())-2 == 4:
                            orbs = [1, 3]
                        # 元素
                        for elemid in range(len(elems)):
                            weightorbs = []
                            # 轨道
                            for orbid in range(len(orbs)):
                                orbsum = 0
                                orbtemp = 1+sum(orbs[:orbid])
                                for orb in range(orbs[orbid]): # 分轨道求和
                                    orbtemp += 1
                                    atomstemp = sum(elemnums[:elemid])
                                    for atomid in range(elemnums[elemid]): # 同元素原子求和
                                        atomstemp += 1
                                        orbsum += float(data[kk+atomstemp].split()[orbtemp-1])
                                weightorbs.append(orbsum) 
                            weights.append([elems[elemid], weightorbs])
                        break
                bandsdata.append([bandid, energy, weights])
        projdata.append([kid, kcoor, bandsdata])
#print(projdata[0][2][0])
for elem in range(len(elems)):
    for orb in range(len(orbs)):
        lines = []
        lines.append('#K-Path          Energy      Orbital-Weight\n')
        lines.append('# NKPTS & NBANDS: '+str(kps)+' '+str(bands)+'\n')
        for bandid in range(bands):
            lines.append('#band '+str(bandid+1)+'\n')
            for kid in range(kps):
                lines.append( str(kid) + '  ' + projdata[kid][2][bandid][1] + '  ' + str(projdata[kid][2][bandid][2][elem][1][orb]) +'\n')
        if orbs[orb] == 1:
            orblabel = '1'
        elif orbs[orb] == 3:
            orblabel = '2-4' 
        elif orbs[orb] == 5:
            orblabel = '5-9'
        elif orbs[orb] == 7:
            orblabel = '10-16'
        with open('pband_dir/'+elems[elem] + '_' + orblabel + '_pb.dat', 'w') as output:
            output.writelines(lines)

