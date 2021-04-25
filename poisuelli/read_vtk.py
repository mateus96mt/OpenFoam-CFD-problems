#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 13:38:52 2021

@author: mateus
"""

import pyvista as vtki
import numpy as np
import matplotlib.pyplot as plt

#def analitic(Nt, Re, t, y):
#    
#    soma = 0.0
#    
#    for n in range(Nt):
#        
#        soma = soma + ((2.0*n+1.0)**3)*np.sin(np.pi*y*(2.0*n+1.0))*np.exp(-(1.0/Re)*((2.0*n+1.0)**2)*(np.pi**2)*t)
#        
#    
#    return (-4.0*y*(y-1.0)) - (32.0/(np.pi**3))*soma

def analitic(D, U_c, y):

    return 4*U_c*(y/D)*(1.0 - (y/D))

def readOutPut(fileName):
    
    x_axes = []
    vel = []
    
    file = open(fileName, 'r')
    
    str_file = file.readlines()
        
    for i in range(len(str_file)):
    
        str_lines = str_file[i].split('\n')
        str_lines = str_lines[0].split(' ')
                
        x_axes.append(float(str_lines[0]))
        vel.append(float(str_lines[1]))
    
    return x_axes, vel

def velInCanal(nx, ny, fileName = 'VTK/poisuelli_400.vtk'):
    
    ## grid is the central object in VTK where every field is added on to grid
    grid = vtki.UnstructuredGrid(fileName)

    ## point-wise information of geometry is contained
#    print("grid.points:\n\n", grid.points, "\n\n")
    #
    ### get a dictionary contains all cell/point information
#    print("grid.cell_arrays:\n\n", grid.cell_arrays, "\n\n") # note that cell-based and point-based are in different size
#    print("grid.point_arrays:\n\n", grid.point_arrays, "\n\n") # 
    #
    #print("\n\ngrid['p']\n", type(grid['p']), "\n", "shape:", grid['p'].shape, "\n", grid['p'])
    #
    #print("\n\ngrid['U']\n", type(grid['U']), "\n", "shape:", grid['U'].shape, "\n", grid['U'])
        
    domx = [0.0, 5.0]
    
    domy = [0.0, 1.0]
    
            
    vel_x = grid['U'][:, 0]
    
    vel_x_canal = []
    
    tam = grid['p'].shape[0]
    
    count = 0
    for i in range(tam):
        
        if i == int(nx/2) + count*nx:
            
            vel_x_canal.append(vel_x[i])
            
            count = count + 1
        
    
    MAX_VEL = max(vel_x_canal)
    vel_x_canal[:] = vel_x_canal[:] / MAX_VEL
    
#    print(len(vel_x_center))
    
    #print("\n\nvel_x:\n", vel_x)
    #print("\n\nvel_x:\n", vel_y)
    
    y_axes = np.linspace(domy[0], domy[1], ny)
     
    return y_axes, vel_x_canal, MAX_VEL

#scheme_nameS = ['linear', 'TOPUS', 'FSFL', 'SDPUS', 'EPUS']
#scheme_nameS = ['TOPUS', 'FSFL', 'SDPUS', 'EPUS']
#ReS = [1000]
#
#plt.figure(figsize=(8,8))
#
#label_font_size = 12
#
#for scheme_name in scheme_nameS:
#
#    for Re in ReS:
#    
#        path = 'Reynolds/' + str(Re) + '/' + scheme_name
#    
#        if scheme_name == 'linear':
#            
#            path = 'linear'
#    
#        x_axes, y_axes, vel_x_center, vel_y_center = velAtCenter(fileName = path + '/VTK/' + scheme_name + '_38000.vtk')
#        
#        x_axes_ref, vel_U_ref = readOutPut('referencia/referencia_U_Re_' + str(Re) + '_128x128.txt')
#        x_axes_ref, vel_V_ref = readOutPut('referencia/referencia_V_Re_' + str(Re) + '_128x128.txt')
#        
#        
#        plt.plot(y_axes, vel_x_center, label = 'Solução numérica', marker = '+')
#        plt.plot(x_axes_ref, vel_U_ref, 'v', label = 'Dados experimentais')
#        plt.grid(True, linestyle='--')
#        plt.title(scheme_name)
#        plt.legend(loc="best")
#        plt.xlabel(r'$y$', fontsize=label_font_size)
#        plt.ylabel(r'$U_x$', fontsize=label_font_size, rotation=0)
#        plt.tight_layout()
#        plt.savefig(scheme_name + '_Re=' + str(Re) + '_vel_x' + '.png', dpi = 200)
#        plt.cla()
#        plt.clf()
#        
#        plt.plot(x_axes, vel_y_center, label = 'Solução numérica', marker = '+')
#        plt.plot(x_axes_ref, vel_V_ref, 'v', label = 'Dados experimentais')
#        plt.grid(True, linestyle='--')
#        plt.title(scheme_name)
#        plt.legend(loc="best")
#        plt.xlabel(r'$x$', fontsize=label_font_size)
#        plt.ylabel(r'$U_y$', fontsize=label_font_size, rotation=0)
#        plt.tight_layout()
#        plt.savefig(scheme_name + '_Re=' + str(Re) + '_vel_y' + '.png', dpi = 200)
#        plt.cla()
#        plt.clf()



### get a field in numpy array
#p_cell = grid.cell_arrays['p']
#
### create a new cell field of pressure^2
#p2_cell = p_cell**2
#grid._add_cell_scalar(p2_cell, 'p2')
#
### remember to save the modified vtk
#grid.save('./VTK/c1_1000_shaowu.vtk')

plt.figure(figsize=(8,6))

label_font_size = 12

D = 1.0

Re = 100#500

scheme_name = 'linear'

y_axes, vel_x_canal, MAX_VEL = velInCanal(100, 10, fileName = 'VTK/poisuelli_400.vtk')

vel = [analitic(D, 1.0, y) for y in y_axes]

plt.plot(y_axes, vel_x_canal, '+', label = 'Solução numérica')
plt.plot(y_axes, vel, label = 'Solução analítica')
plt.grid(True, linestyle='--')
plt.title(scheme_name)
plt.legend(loc="best")
plt.xlabel(r'$y$', fontsize=label_font_size)
plt.ylabel(r'$U_x$', fontsize=label_font_size, rotation=0, labelpad = 10)
plt.tight_layout()
plt.savefig(scheme_name + '_Re=' + str(Re) + '_vel_x' + '.png', dpi = 200)
plt.cla()
plt.clf()

#y_axes = np.linspace(0.0, 1.0, 100)
#
#vel = [analitic(1000, 0.01, 0.000157, y) for y in y_axes]
#
#plt.plot(y_axes, vel)

