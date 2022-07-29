declare -a reynolds=("1000" "2500" "3200" "5000" "7500" "10000" "12500" "15000" "17500" "20000" "21000")
declare -a malhas=("128x128")
declare -a esquemas=("CUBICK")

for re in ${reynolds[@]};
    do
    for malha in ${malhas[@]};
        do
        for esquema in ${esquemas[@]};
            do

            (cd Reynolds/$re/malhas/$malha/$esquema && blockMesh;mv constant/transportProperties constant/physicalProperties;gnome-terminal -e "icoFoam")

        done;
    done;
done;
