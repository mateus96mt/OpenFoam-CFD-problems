declare -a reynolds=("1000" "2500" "3200" "5000" "7500" "10000" "12500" "15000" "17500" "20000" "21000")
declare -a malhas=("128x128")
declare -a esquemas=("FSFL")

for re in ${reynolds[@]};
    do
    for malha in ${malhas[@]};
        do
        for esquema in ${esquemas[@]};
            do

            (cd Reynolds/$re/malhas/$malha/$esquema && blockMesh;icoFoam | grep 'Solving for Uy, Initial residual =' | awk -F"," {'tol=1e-3;it=it+1;split($2,a,"=");print "it: " it "   residual: " a[2];if(a[2] > 0 && a[2]<tol){print "Minimal residual " tol " reached! Ending execution...";print "it: " it "   residual: " a[2] >"residual.txt";exit 1;}}';
)

        done;
    done;
done;
