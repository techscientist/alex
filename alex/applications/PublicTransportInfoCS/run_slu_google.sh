#!/bin/bash
if [ "$#" != 1 ]; then
    echo "Usage: $0 <train-data-portion>"
    echo "Must be run from within PTICS directory on testing_acl"
    exit 1
fi

ln -s /net/projects/vystadial/data/call-logs/2013-05-30-alex-aotb-prototype/total lm/indomain_data
ln -s /net/projects/vystadial/data/call-logs/2013-05-30-alex-aotb-prototype/total slu/indomain_data

set -e  # exit on any command fail

#cd data
#echo -e `date` '***********************************\nDATABASE DUMP' | tee -a ../training-log-google.txt
#./database.py dump

#cd ../lm
#echo -e `date` '***********************************\nBUILDING LM' | tee -a ../training-log-google.txt
#./build.py --train-limit $1 >> ../training-log-google.txt 2>&1

#cd ../hclg
#echo -e `date` '***********************************\nRUNNING DECODE' | tee -a ../training-log-google.txt
#./run_decode_indomain_google.sh >> ../training-log-google.txt 2>&1


cd slu
cp ~/work/alex-training_exp/alex_1/alex/applications/PublicTransportInfoCS/slu/all*{sem,trn,asr,nbl} .
echo -e `date` '***********************************\nPREPARING SLU DATA' | tee -a ../training-log-google.txt
./prepare_data.py --split-only --train-limit $1 >> ../training-log-google.txt 2>&1


echo -e `date` '***********************************\nTRAINING SLU' | tee -a ../training-log-google.txt
./train.py >> ../training-log-google.txt 2>&1

echo -e `date` '***********************************\nTESTING SLU' | tee -a ../training-log-google.txt
./test.py >> ../training-log-google.txt 2>&1
echo -e `date` '***********************************\nTESTING SLU (BOOTSTRAP)' | tee -a ../training-log-google.txt
./test_bootstrap.py >> ../training-log-google.txt 2>&1

echo -e `date` '***********************************\nDONE' | tee -a ../training-log-google.txt
./print_scores.sh | tee -a ../training-log-google.txt
