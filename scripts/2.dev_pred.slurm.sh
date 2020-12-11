#!/bin/bash
HPC=1
SUBMIT=1
TIME=00:15:00
PARTITION="red"
mkdir -p slurm
### wrap run into slurm script
while read line;
do
    cmd=`echo "$line" | sed 's/--device 0/--device \$CUDA_VISIBLE_DEVICES/'`
    echo $cmd
    name=`echo "$line"  | awk '{print $8}' | cut -d'/' -f4`
    if [ $HPC -eq 1 ] ;
    then
        echo "#!/bin/bash"  > $$tmp
        echo "#SBATCH --job-name=$name " >> $$tmp
        echo "#SBATCH --time=$TIME" >> $$tmp
        echo "#SBATCH --gres=gpu" >> $$tmp
        echo "#SBATCH --cpus-per-task=2" >> $$tmp
        echo "#SBATCH --nodes=1" >> $$tmp
#        echo "#SBATCH --mem=20G" >> $$tmp
        echo "#SBATCH --ntasks-per-node=1" >> $$tmp
        echo "#SBATCH --partition=$PARTITION" >> $$tmp
        echo "#SBATCH --output=slurm/job.$name.out" >> $$tmp
        echo "#SBATCH -e slurm/job.$name.err" >> $$tmp
        echo "#SBATCH --mail-type=FAIL" >> $$tmp
        echo "module load Anaconda3" >> $$tmp

	echo "echo \"Running on \$(hostname):\" " >> $$tmp
	echo "echo \"CUDA_VISIBLE_DEVICES \$CUDA_VISIBLE_DEVICES\"" >> $$tmp
	echo "sleep 2" >> $$tmp
	echo "nvidia-smi" >> $$tmp
	echo "$cmd" >> $$tmp
	cat $$tmp
	if [ $SUBMIT -eq 1 ] ;
	then
            sbatch $$tmp
	fi
	rm $$tmp
    fi
#done < 1.train.sh | head -1
done < 2.pred.sh
