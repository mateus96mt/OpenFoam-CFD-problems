declare -a reynolds=("1000" "2500" "3200" "5000" "7500" "10000" "12500" "15000" "17500" "20000" "21000")
declare -a malhas=("32x32" "64x64" "128x128")
declare -a esquemas=("TOPUS" "FSFL" "SDPUS" "EPUS")

for re in ${reynolds[@]};
    do
    for malha in ${malhas[@]};
        do
        for esquema in ${esquemas[@]};
            do

            git add cavity/cavity/Reynolds/$re/malhas/$malha/$esquema/system/*
            git add cavity/cavity/Reynolds/$re/malhas/$malha/$esquema/0/U
            git add cavity/cavity/Reynolds/$re/malhas/$malha/$esquema/0/p
            git add cavity/cavity/Reynolds/$re/malhas/$malha/$esquema/constant/transportProperties

        done;
    done;
done;
