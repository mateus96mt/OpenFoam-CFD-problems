#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 13:38:52 2021

@author: mateus
"""

import pyvista as vtki
import numpy as np
import matplotlib.pyplot as plt

def readReferenceData():
    
    fileVelX = open('referencia/vel_x_all_reynolds.txt', 'r')
    fileVelY = open('referencia/vel_y_all_reynolds.txt', 'r')
    
    linesVelX = [line.split('\n')[0] for line in fileVelX.readlines()]
    linesVelY = [line.split('\n')[0] for line in fileVelY.readlines()]
        
    columnsVelX = np.array([[float(value) for value in line.split(' ')] for line in linesVelX[1:]])
    columnsVelY = np.array([[float(value) for value in line.split(' ')] for line in linesVelY[1:]])
        
    headersVelX = linesVelX[0].split(' ')
    headersVelY = linesVelY[0].split(' ')    
    
    velX = {headersVelX[i]:list(columnsVelX[:,i]) for i in range(len(headersVelX))}
    velY = {headersVelY[i]:list(columnsVelY[:,i]) for i in range(len(headersVelY))}
    
    
#    print(test['2500'])
    
#    velX = {header for header in headersVelX}
#    velY = {header for header in headersVelY}
#    
#    print(velX)
#    print(velY)
    
    return velX, velY

def velAtCenter(fileName = 'VTK/linear_38000.vtk'):
    
    ## grid is the central object in VTK where every field is added on to grid
    grid = vtki.UnstructuredGrid(fileName)

    ## point-wise information of geometry is contained
    #print("grid.points:\n\n", grid.points, "\n\n")
    #
    ### get a dictionary contains all cell/point informationfile
    #print("grid.cell_arrays:\n\n", grid.cell_arrays, "\n\n") # note that cell-based and point-based are in different size
    #print("grid.point_arrays:\n\n", grid.point_arrays, "\n\n") # 
    #
    #print("\n\ngrid['p']\n", type(grid['p']), "\n", "shape:", grid['p'].shape, "\n", grid['p'])
    #
    #print("\n\ngrid['U']\n", type(grid['U']), "\n", "shape:", grid['U'].shape, "\n", grid['U'])
        
    domx = domy = [0.0, 1.0]
    
    tam = grid['p'].shape[0]
    
    ny = nx = int(np.sqrt(tam))
    
    vel_x = grid['U'][:, 0]
    vel_y = grid['U'][:, 1]
    
    vel_y_center = vel_y[int(tam/2):int(tam/2) + nx]
    vel_x_center = []
    
    count = 0
    for i in range(tam):
        
        if i % int(nx/2) == 0 and i % int(nx) != 0:
        
            vel_x_center.append(vel_x[i])
        
        count = count + 1
    
#    print(len(vel_x_center))
    
    #print("\n\nvel_x:\n", vel_x)
    #print("\n\nvel_x:\n", vel_y)
    
    x_axes = np.linspace(domx[0], domx[1], nx)
    y_axes = np.linspace(domy[0], domy[1], ny)
     
    return x_axes, y_axes, vel_x_center, vel_y_center

def error(y_num, y_referencia):
    
    n = len(y_referencia)
    m = len(y_num)
        
    erro = 0.0
    sum_exata = 0.0
    
    for i in range(n):

        er_min = 999999999999

        for j in range(m):
            
            er = (y_referencia[i] - y_num[j])**2
            
            if er < er_min:
                
                er_min = er
        
        sum_exata = sum_exata + (y_referencia[i]**2)
        erro = erro + er_min
        
    return np.sqrt(erro/sum_exata)

def lastVTKname(malha = '32x32'):
    
    if malha == '32x32':
        return '9000'
    
    if malha == '64x64':
        return '19000'
    
    if malha == '128x128':
        return '38000'

def run():
    #scheme_nameS = ['linear', 'TOPUS', 'FSFL', 'SDPUS', 'EPUS']
    scheme_nameS = ['TOPUS', 'FSFL', 'SDPUS', 'EPUS']
#    scheme_nameS = ['linear']
    ReS = [1000, 7500]
    
    malhas = ['32x32', '64x64', '128x128']
    
    plt.figure(figsize=(8,8))
    
    label_font_size = 12
    
    for scheme_name in scheme_nameS:
        
        print("\n\nscheme_name = " + scheme_name)
        
        for Re in ReS:
            
            for malha in malhas:
        
                path = 'Reynolds/' + str(Re) + '/malhas/' + malha + '/' + scheme_name
            
                if scheme_name == 'linear':
                    
                    path = 'linear'
            
                vtkFileName = path + '/VTK/' + scheme_name + '_' + lastVTKname(malha) + '.vtk'
            
                x_axes, y_axes, vel_x_center, vel_y_center = velAtCenter(fileName = vtkFileName)
                
#                y_axes_ref, vel_U_ref = readOutPut('referencia/referencia_U_Re_' + str(Re) + '_128x128.txt')
#                x_axes_ref, vel_V_ref = readOutPut('referencia/referencia_V_Re_' + str(Re) + '_128x128.txt')
                
                velX, velY = readReferenceData()
                y_axes_ref, vel_U_ref = velX['y'], velX[str(Re)]
                x_axes_ref, vel_V_ref = velY['x'], velY[str(Re)]
                
                plt.plot(y_axes, vel_x_center, label = 'Solução numérica', marker = '+')
                plt.plot(y_axes_ref, vel_U_ref, 'v', label = 'Referência')
                plt.grid(True, linestyle='--')
    #            plt.title(scheme_name)
                plt.legend(loc="best")
                plt.xlabel(r'$y$', fontsize=label_font_size)
                plt.ylabel(r'$U_x$', fontsize=label_font_size, rotation=0)
                plt.tight_layout()
                plt.savefig(scheme_name + '_Re=' + str(Re) + '_' + malha + '_vel_x' + '.png', dpi = 200)
                plt.cla()
                plt.clf()
                
                plt.plot(x_axes, vel_y_center, label = 'Solução numérica', marker = '+')
                plt.plot(x_axes_ref, vel_V_ref, 'v', label = 'Referência')
                plt.grid(True, linestyle='--')
    #            plt.title(scheme_name)
                plt.legend(loc="best")
                plt.xlabel(r'$x$', fontsize=label_font_size)
                plt.ylabel(r'$U_y$', fontsize=label_font_size, rotation=0)
                plt.tight_layout()
                plt.savefig(scheme_name + '_Re=' + str(Re) + '_' + malha + '_vel_y' + '.png', dpi = 200)
                plt.cla()
                plt.clf()
    
                print("Re = " + str(Re) + "  malha: " + malha)
                print("erro Ux: " + str("%.5f" % error(vel_x_center, vel_U_ref)))
                print("erro Uy: " + str("%.5f" % error(vel_y_center, vel_V_ref)) + "\n")

def run2():
    #scheme_nameS = ['linear', 'TOPUS', 'FSFL', 'SDPUS', 'EPUS']
    scheme_nameS = ['TOPUS', 'FSFL', 'SDPUS', 'EPUS']
#    scheme_nameS = ['linear']
    ReS = [1000, 7500]
    
    malhas = ['32x32', '64x64', '128x128']
    
    vels = ['_vel_x', '_vel_y']
    
    plt.figure(figsize=(8,8))
    
    label_font_size = 12
    
    for scheme_name in scheme_nameS:
        
        print("\n\nscheme_name = " + scheme_name)
        
        for Re in ReS:
            
            for vel in vels:
            
                plot_analy = True
                
                for malha in malhas:
                    
                    path = 'Reynolds/' + str(Re) + '/malhas/' + malha + '/' + scheme_name
            
                    if scheme_name == 'linear':
                        
                        path = 'linear'
            
                    vtkFileName = path + '/VTK/' + scheme_name + '_' + lastVTKname(malha) + '.vtk'
                
                    x_axes, y_axes, vel_x_center, vel_y_center = velAtCenter(fileName = vtkFileName)
                    
#                    y_axes_ref, vel_U_ref = readOutPut('referencia/referencia_U_Re_' + str(Re) + '_128x128.txt')
#                    x_axes_ref, vel_V_ref = readOutPut('referencia/referencia_V_Re_' + str(Re) + '_128x128.txt')
                    
                    velX, velY = readReferenceData()
                    y_axes_ref, vel_U_ref = velX['y'], velX[str(Re)]
                    x_axes_ref, vel_V_ref = velY['x'], velY[str(Re)]
                    
                    if vel == '_vel_x':
                        
                        if plot_analy:
                            plt.plot(y_axes_ref, vel_U_ref, 'v', label = 'Referência')
                            plot_analy = False
                        
                        plt.plot(y_axes, vel_x_center, label = malha, marker = '')
#                        plt.plot(y_axes_ref, vel_U_ref, 'v', label = malha)
                        plt.grid(True, linestyle='--')
            #            plt.title(scheme_name)
                        plt.legend(loc="best")
                        plt.xlabel(r'$y$', fontsize=label_font_size)
                        plt.ylabel(r'$U_x$', fontsize=label_font_size, rotation=0)
                        plt.tight_layout()
                    else:
                        
                        if plot_analy:
                            plt.plot(x_axes_ref, vel_V_ref, 'v', label = 'Referência')
                            plot_analy = False
                            
                        plt.plot(x_axes, vel_y_center, label = malha, marker = '')
#                        plt.plot(x_axes_ref, vel_V_ref, 'v', label = malha)
                        plt.grid(True, linestyle='--')
            #            plt.title(scheme_name)
                        plt.legend(loc="best")
                        plt.xlabel(r'$x$', fontsize=label_font_size)
                        plt.ylabel(r'$U_y$', fontsize=label_font_size, rotation=0)
                        plt.tight_layout()
            
                    print("Re = " + str(Re) + "  malha: " + malha)
                    print("erro Ux: " + str("%.5f" % error(vel_x_center, vel_U_ref)))
                    print("erro Uy: " + str("%.5f" % error(vel_y_center, vel_V_ref)) + "\n")
                        
                if vel == '_vel_x':
                    plt.savefig(scheme_name + '_Re=' + str(Re) + '_' + 'MALHAS' + '_vel_x' + '.png', dpi = 200)
                    plt.cla()
                    plt.clf()
                else:
                    plt.savefig(scheme_name + '_Re=' + str(Re) + '_' + 'MALHAS' + '_vel_y' + '.png', dpi = 200)
                    plt.cla()
                    plt.clf()

def run3():
    #scheme_nameS = ['linear', 'TOPUS', 'FSFL', 'SDPUS', 'EPUS']
    scheme_nameS = ['TOPUS', 'FSFL', 'SDPUS', 'EPUS']
#    scheme_nameS = ['linear']
    ReS = ["1000", "2500", "5000", "7500", "10000", "12500", "15000", "17500", "20000", "21000"]
    
#    malhas = ['32x32', '64x64', '128x128']
    malha = '128x128'
    
    vels = ['_vel_x', '_vel_y']
    
    plt.figure(figsize=(8,8))
    
    label_font_size = 12
    
    for vel in vels:
    
        for scheme_name in scheme_nameS:
                        
            for Re in ReS:
                
                path = 'Reynolds/' + str(Re) + '/malhas/' + malha + '/' + scheme_name
                
                vtkFileName = path + '/VTK/' + scheme_name + '_' + lastVTKname(malha) + '.vtk'
                
#                print(str(vel) + ' Re: ' + str(Re) + ' ' + str(scheme_name))
                
                plot_analy = True
                
                if scheme_name == 'linear':
                    
                    path = 'linear'
            
                x_axes, y_axes, vel_x_center, vel_y_center = velAtCenter(fileName = vtkFileName)
                
    #                    y_axes_ref, vel_U_ref = readOutPut('referencia/referencia_U_Re_' + str(Re) + '_128x128.txt')
    #                    x_axes_ref, vel_V_ref = readOutPut('referencia/referencia_V_Re_' + str(Re) + '_128x128.txt')
                
                velX, velY = readReferenceData()
                y_axes_ref, vel_U_ref = velX['y'], velX[str(Re)]
                x_axes_ref, vel_V_ref = velY['x'], velY[str(Re)]
                
#                print(velX)
#                print(velY)
#                print('\n\n\n')
#                
                if vel == '_vel_x':
                    
                    if plot_analy:
                        plt.plot(y_axes_ref, vel_U_ref, 'v', label = 'Referência')
                        plot_analy = False
                    
                    plt.plot(y_axes, vel_x_center, label = malha, marker = '')
    #                        plt.plot(y_axes_ref, vel_U_ref, 'v', label = malha)
                    plt.grid(True, linestyle='--')
        #            plt.title(scheme_name)
                    plt.legend(loc="best")
                    plt.xlabel(r'$y$', fontsize=label_font_size)
                    plt.ylabel(r'$U_x$', fontsize=label_font_size, rotation=0)
                    plt.tight_layout()
                    plt.savefig(scheme_name + '_Re=' + str(Re) + '_' + 'MALHAS' + '_vel_x' + '.png', dpi = 200)
                    plt.cla()
                    plt.clf()
                else:
                    
                    if plot_analy:
                        plt.plot(x_axes_ref, vel_V_ref, 'v', label = 'Referência')
                        plot_analy = False
                        
                    plt.plot(x_axes, vel_y_center, label = malha, marker = '')
    #                        plt.plot(x_axes_ref, vel_V_ref, 'v', label = malha)
                    plt.grid(True, linestyle='--')
        #            plt.title(scheme_name)
                    plt.legend(loc="best")
                    plt.xlabel(r'$x$', fontsize=label_font_size)
                    plt.ylabel(r'$U_y$', fontsize=label_font_size, rotation=0)
                    plt.tight_layout()
                    plt.savefig(scheme_name + '_Re=' + str(Re) + '_' + 'MALHAS' + '_vel_y' + '.png', dpi = 200)
                    plt.cla()
                    plt.clf()
        
                print("Re = " + str(Re) + "  malha: " + malha)
                print("erro Ux: " + str("%.5f" % error(vel_x_center, vel_U_ref)))
                print("erro Uy: " + str("%.5f" % error(vel_y_center, vel_V_ref)) + "\n")


def run4():
    #scheme_nameS = ['linear', 'TOPUS', 'FSFL', 'SDPUS', 'EPUS']
    scheme_nameS = ['TOPUS', 'FSFL', 'SDPUS', 'EPUS']
    markers = ['v', 's', '+', '*']
#    scheme_nameS = ['linear']
    ReS = [1000, 2500, 5000, 7500, 10000, 12500, 15000, 17500, 20000, 21000]
    
#    malhas = ['32x32', '64x64', '128x128']
    malha = '128x128'
    
    vels = ['_vel_x', '_vel_y']
    
    plt.figure(figsize=(8,8))
    
    label_font_size = 12
    
    for vel in vels:
    
        scheme_index = 0
        for scheme_name in scheme_nameS:
                        
            errosVelX = []
            errosVelY = []
            
            for Re in ReS:
                
                path = 'Reynolds/' + str(Re) + '/malhas/' + malha + '/' + scheme_name
                
                vtkFileName = path + '/VTK/' + scheme_name + '_' + lastVTKname(malha) + '.vtk'
                
#                print(str(vel) + ' Re: ' + str(Re) + ' ' + str(scheme_name))
                
#                plot_analy = True
                
                if scheme_name == 'linear':
                    
                    path = 'linear'
            
                x_axes, y_axes, vel_x_center, vel_y_center = velAtCenter(fileName = vtkFileName)
                
    #                    y_axes_ref, vel_U_ref = readOutPut('referencia/referencia_U_Re_' + str(Re) + '_128x128.txt')
    #                    x_axes_ref, vel_V_ref = readOutPut('referencia/referencia_V_Re_' + str(Re) + '_128x128.txt')
                
                velX, velY = readReferenceData()
                y_axes_ref, vel_U_ref = velX['y'], velX[str(Re)]
                x_axes_ref, vel_V_ref = velY['x'], velY[str(Re)]
                
#                print(velX)
#                print(velY)
#                print('\n\n\n')
#                
                erroVelx = error(vel_x_center, vel_U_ref)
                erroVely = error(vel_y_center, vel_V_ref)
                
                print("Re = " + str(Re) + "  malha: " + malha)
                print("erro Ux: " + str("%.5f" % erroVelx))
                print("erro Uy: " + str("%.5f" % erroVely) + "\n")
                
                errosVelX.append(erroVelx)
                errosVelY.append(erroVely)
            
            reys = [float(re/1000.0) for re in ReS]
            
            plt.xticks(reys, reys)
            
            if vel == '_vel_x':
                plt.plot(reys, errosVelX, label = scheme_name, marker = markers[scheme_index])
            
            else:
                plt.plot(reys, errosVelY, label = scheme_name, marker = markers[scheme_index])
            
            scheme_index = scheme_index + 1;
            
        plt.grid(True, linestyle='--')
#            plt.title(scheme_name)
        plt.legend(loc="best")
        plt.xlabel('Reynolds x 1000', fontsize=label_font_size)
        plt.ylabel(r'$||E||_2$', fontsize=label_font_size, rotation=0)
        plt.tight_layout()
        
        plt.savefig('_Reynolds_variable' + '_' + str(vel) + '.png', dpi = 200)
        
        plt.cla()
        plt.clf()

def run5():
    #scheme_nameS = ['linear', 'TOPUS', 'FSFL', 'SDPUS', 'EPUS']
    scheme_nameS = ['TOPUS', 'FSFL', 'SDPUS', 'EPUS']
    markers = ['v', 's', '+', '*']
#    scheme_nameS = ['linear']
    ReS = [1000, 7500]
    
    malhas = ['32x32', '64x64', '128x128']
    
    mesh = [32, 64, 128]
    
    vels = ['_vel_x', '_vel_y']
    
    plt.figure(figsize=(8,8))
    
    label_font_size = 12
    
    for Re in ReS:
        
        print("\n\Re = " + str(Re))
        
        for vel in vels:
        
            markerIndex = 0
            for scheme_name in scheme_nameS:
                
                errosVelx = []
                errosVely = []
                
                for malha in malhas:
                    
                    path = 'Reynolds/' + str(Re) + '/malhas/' + malha + '/' + scheme_name
            
                    if scheme_name == 'linear':
                        
                        path = 'linear'
            
                    vtkFileName = path + '/VTK/' + scheme_name + '_' + lastVTKname(malha) + '.vtk'
                
                    x_axes, y_axes, vel_x_center, vel_y_center = velAtCenter(fileName = vtkFileName)
                    
#                    y_axes_ref, vel_U_ref = readOutPut('referencia/referencia_U_Re_' + str(Re) + '_128x128.txt')
#                    x_axes_ref, vel_V_ref = readOutPut('referencia/referencia_V_Re_' + str(Re) + '_128x128.txt')
                    
                    velX, velY = readReferenceData()
                    y_axes_ref, vel_U_ref = velX['y'], velX[str(Re)]
                    x_axes_ref, vel_V_ref = velY['x'], velY[str(Re)]
            
                    errX = error(vel_x_center, vel_U_ref)
                    errY = error(vel_y_center, vel_V_ref)
            
                    print("Re = " + str(Re) + "  malha: " + malha)
                    print("erro Ux: " + str("%.5f" % errX))
                    print("erro Uy: " + str("%.5f" % errY) + "\n")
                    
                    errosVelx.append(errX)
                    errosVely.append(errY)
                                        
                        
                if vel == '_vel_x':
                    plt.xticks(mesh, mesh)
                    plt.plot(mesh, errosVelx, label = scheme_name, marker = markers[markerIndex])
                    
                else:
                    plt.xticks(mesh, mesh)
                    plt.plot(mesh, errosVely, label = scheme_name, marker = markers[markerIndex])
                    
                plt.grid(True, linestyle='--')
    #            plt.title(scheme_name)
                plt.legend(loc="best")
                plt.xlabel('Malha', fontsize=label_font_size)
                plt.ylabel(r'$||E||_2$', fontsize=label_font_size, rotation=0)
                plt.tight_layout()
                
                
                markerIndex = markerIndex + 1
                
            plt.savefig('error_meshes' + '_Re=' + str(Re) + '_' + 'MALHAS' + str(vel) + '.png', dpi = 200)
            plt.cla()
            plt.clf()

run4()
run5()

#print(velX)
#print(velY)

#run3()

#run2()

#x_axes_ref, vel_U_ref = readOutPut('referencia/referencia_U_Re_1000_128x128.txt')
#
#plt.plot(x_axes_ref, vel_U_ref)

### get a field in numpy array
#p_cell = grid.cell_arrays['p']
#
### create a new cell field of pressure^2
#p2_cell = p_cell**2
#grid._add_cell_scalar(p2_cell, 'p2')
#
### remember to save the modified vtk
#grid.save('./VTK/c1_1000_shaowu.vtk')
