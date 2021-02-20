#!/bin/bash
HPC=1
SUBMIT=1
TIME=5:00:00
PARTITION="red"
mkdir -p slurm
### wrap run into slurm script
while read line;
do
    cmd=`echo "$line" | sed 's/0/\$CUDA_VISIBLE_DEVICES/'`
    echo $cmd
    name=`echo "$line"  | awk '{print $11}'`
    if [ $HPC -eq 1 ] ;
    then
        echo "#!/bin/bash"  > $$tmp
        echo "#SBATCH --job-name=$name " >> $$tmp
        echo "#SBATCH --time=$TIME" >> $$tmp
        echo "#SBATCH --gres=gpu" >> $$tmp
        echo "#SBATCH --cpus-per-task=2" >> $$tmp
        echo "#SBATCH --nodes=1" >> $$tmp
        echo "#SBATCH --mem=20G" >> $$tmp
        echo "#SBATCH --ntasks-per-node=1" >> $$tmp
        echo "#SBATCH --partition=$PARTITION" >> $$tmp
        echo "#SBATCH --output=slurm/job.$name.out" >> $$tmp
        echo "#SBATCH -e slurm/job.$name.err" >> $$tmp
        echo "#SBATCH --mail-type=FAIL,END" >> $$tmp
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
#done < 1.train.sh | head -5
done < 1.train.sh
