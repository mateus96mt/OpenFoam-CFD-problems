## README Translation
- [English](README.md)
- [Portuguese](README-pt.md)

# Instructions

## To use this repository it is necessary to install OpenFoam on your machine as well as the TOPUS, FSFL, SDPUS-C1 and EPUS schemas.

Please follow the following tutorial for installing OpenFoam and Flow Limiters before proceeding: [Tutorial] (https://github.com/mateus96mt/openFoamFluxLimiters)

After following the tutorial above and with OpenFoam installed and the TOPUS, FSFL, SDPUS-C1 and EPUS flow limiters, proceed to the next steps.

The commands must be run inside the root in any 'TOPUS', 'FSFL', 'SDPUS' or 'EPUS' folder.

To run the problems just two steps:

### 1. Mesh generation using the ```blockMesh``` command

### 2. Execution of the solver

- Cavity problem: ```icoFoam```
- Poisuelli problem ```simpleFoam```
- ```simpleFoam``` step problem

From the results it is possible to generate the files ".VTK"

Just run the command ```foamToVTK```
