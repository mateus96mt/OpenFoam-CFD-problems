declare -a reynolds=( "7500" "10000" "12500")
declare -a malhas=("128x128")
declare -a esquemas=("linear")

for re in ${reynolds[@]};
    do
    for malha in ${malhas[@]};
        do
        for esquema in ${esquemas[@]};
            do

            (cd Reynolds/$re/malhas/$malha/$esquema && blockMesh;icoFoam;)

        done;
    done;
done;
