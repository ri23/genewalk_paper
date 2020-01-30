#!/bin/bash
#Robert Ietswaart 
#sbatch job to run GeneWalk for REVISIONS
#adjusted from 20200123

revv=REV5ALLG
date=20200127${revv}
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

data_source="pc" #for indra you need more reaction statements
Treatment="QKI JQ1" # 
nthread="8" #for stats 1 #all others: 4 
SEEDS="42" #

for seed in $SEEDS
do
    for ds in $data_source
    do
        for tr in $Treatment
        do
	    if [ ${tr} == 'QKI' ]
	    then
		idt=mgi_id
		fnetwork=${tr}_MGIforINDRA_stmts.pkl
		fgenes=NGF_${tr}_MGIforPANTHER_ref.csv
	    else
		idt=ensembl_id #hgnc_id
		fnetwork=${tr}_HGNCidForINDRA.pkl
		fgenes=${tr}_ensID_ref.csv
            fi
	    stage=all #statistics #null_distribution #node_vectors #all
        
            jobname=GeneWalk_${date}_${tr}_${ds}_seed${seed}_stage${stage}
            sbatch -p priority -n ${nthread} --mem=128G -t 4-00:00:00 --job-name=${jobname} \
                    -o ${baseDir}/LogErr/${jobname}.log -e ${baseDir}/LogErr/${jobname}.err \
                    --mail-user=${notifEm} --mail-type=ALL \
                    --wrap="source genewalkenv/bin/activate; \
            cd ${scDir}/genewalk ; \
            export PYTHONPATH=$PYTHONPATH:. ; \
            $program ${script} --base_folder ${baseDir} --project ${date}_${tr}_${ds}seed${seed} \
            --network_file ${baseDir}/${fnetwork} \
            --network_source ${ds} --genes ${baseDir}/${fgenes} --id_type ${idt} --stage ${stage} \
            --nproc ${nthread} --nreps_graph 10 --nreps_null 10 --random_seed ${seed} ; \
            pip freeze >> ${baseDir}/LogErr/${jobname}py.out"

        done
    done
done

#--mem=32G -t 0-11:59:00 short (all)
#--mem=2G -t 0-00:10:00 short (statistics)
