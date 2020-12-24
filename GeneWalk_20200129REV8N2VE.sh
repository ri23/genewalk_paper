#!/bin/bash
#Robert Ietswaart 
#sbatch job to run GeneWalk for REVISIONS
#adjusted from 20200123

revv=REV8N2VE
date=20200129${revv}
script=genewalk/cli_${revv}.py 

program=python
notifEm=robert_ietswaart@hms.harvard.edu
baseDir=/n/groups/churchman/ri23/genewalk
scDir=/n/groups/churchman/ri23/code

module load gcc/6.2.0
module load python/3.6.0
module load java/jdk-1.8u112

cd ${scDir}
mkdir -p ${baseDir}/LogErr

data_source="indra pc"  #
Treatment="QKI JQ1" #
nthread="8" #for stats 1 #all others: 4 
SEEDS="42" #
N2V_P="0.25 1 4.0"
N2V_Q="0.25 1 4.0"

for seed in $SEEDS
do
    for ds in $data_source
    do
        for tr in $Treatment
        do
	    for n2v_p in $N2V_P
	    do
		for n2v_q in $N2V_Q
		do
		    if [ ${tr} == 'QKI' ]
		    then
			idt=mgi_id
			fnetwork=${tr}_MGIforINDRA_stmts.pkl
		    else
			idt=hgnc_id
			fnetwork=${tr}_HGNCidForINDRA.pkl
		    fi
		    stage=all #statistics #null_distribution #node_vectors
		    
		    jobname=GeneWalk_${date}_${tr}_${ds}_seed${seed}_stage${stage}p${n2v_p}q${n2v_q}
		    sbatch -p short -n ${nthread} --mem=128G -t 0-11:59:00 --job-name=${jobname} \
			-o ${baseDir}/LogErr/${jobname}.log -e ${baseDir}/LogErr/${jobname}.err \
			--mail-user=${notifEm} --mail-type=ALL \
			--wrap="source genewalkenv/bin/activate; \
            cd ${scDir}/genewalk ; \
            export PYTHONPATH=$PYTHONPATH:. ; \
            $program ${script} --base_folder ${baseDir} \
            --project ${date}_${tr}_${ds}seed${seed}p${n2v_p}q${n2v_q} \
            --network_file ${baseDir}/${fnetwork} \
            --network_source ${ds} --genes ${baseDir}/${tr}_forGW.csv --id_type ${idt} --stage ${stage} \
            --nproc ${nthread} --nreps_graph 3 --nreps_null 3 --random_seed ${seed} \
            --n2v_p ${n2v_p} --n2v_q ${n2v_q} ; \
            pip freeze >> ${baseDir}/LogErr/${jobname}py.out"
		done
	    done
        done
    done
done

#short -n ${nthread} --mem=32G -t 0-11:59:00 (all indra pc)
