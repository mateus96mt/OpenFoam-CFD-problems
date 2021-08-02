#!/bin/bash

foamCleanTutorials
blockMesh | tee log.blockMesh
checkMesh | tee log.checkMesh
simpleFoam | tee log.simpleFoam

