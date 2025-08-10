Automatically generate input files for Wannier90 software to construct Wannier tight-binding models; Generate projected electronic band structures from the PROCAR file; Plot projected density of states.


code list:
Wannier_auto.py  自动生成合适的Wannier90软件的输入文件"wannier90.win"
wannier90.win  Wannier90软件的输入文件模板
projbands.py  自动生成投影能带结构数据，并存放于pband_dir目录下
sumofweightforpbands.py  计算投影能带权重，并生成图片方便用户直观了解投影能带权重分布以及对应的能带指标范围


建议目录架构：（注：同一目录下的文件和目录用{}包围）
如果按照此目录架构部署，所有.py程序可直接运行，否则需要更改.py中的文件路径

材料(自洽计算目录)
       |                          
{ DOSCAR(态密度文件), PROCAR(投影能带数据文件), TDOS_SOC.dat(总的态密度文件，可以用vaspkit生成),       eb(能带计算目录),                      wann_cal(构建wannier模型目录), ... }
                                                                                                     |                                            |
                                                  { projbands.py, pband_dir(投影能带计算目录), sumofweightforpbands.py,... }       { Wannier_auto.py, wannier90.win,... }

