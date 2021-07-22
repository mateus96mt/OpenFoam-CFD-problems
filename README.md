# Instruções

## Para utilizar este repositório é necessário instalar o OpenFoam em sua máquina bem como os esquemas TOPUS, FSFL, SDPUS-C1 e EPUS.

Siga o tutorial a seguiir para instalação do OpenFoam e dos limitadores de fluxo antes de continuar: [Tutorial] (https://github.com/mateus96mt/openFoamFluxLimiters)

Após seguir o tutorial acima e com o OpenFoam instalado e os limitadores de fluxo TOPUS, FSFL, SDPUS-C1 e EPUS, prossiga para os próximos passos.

Os comandos devem ser executados dentro da raiz em qualquer pasta 'TOPUS', 'FSFL', 'SDPUS' ou 'EPUS'.

Para rodar os problemas basta dois passos:

### 1. Geração de malha através do comando ```blockMesh```

### 2. Execução do solver ```icoFoam```

A partir dos resultados pode-se gerar os arquivos ".VTK"

Basta rodar o comando ```foamToVTK```

