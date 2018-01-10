#!/bin/bash

#Frequencies to scan
freq=( 5180e6 5200e6 5220e6 5240e6 5260e6 5280e6 5300e6 5320e6 5500e6 5520e6 5540e6 5560e6 5580e6 5600e6 5620e6 5640e6 5660e6 5680e6 5700e6 5745e6 5765e6 5785e6 5805e6 5825e6 )

#freq=( 2412e6 2462e6 )

#RF Amp enable/disable
rf_enable=1

#LNA Gain
lna_db=32

#Screw BB AMP; that never helped me.

#Sampling rate
samp_rate=20e6

#number of samples
num_samp=300000000

#For each freequency, store data into a file.
for i in "${freq[@]}"
do
	hackrf_transfer -r $i.IQ -f $i -a $rf_enable -l $lna_db -s $samp_rate -n $num_samp -b $samp_rate
done

#aggregate the files.
touch out.IQ
for i in "${freq[@]}"
do
	if [ ! -f $i.IQ ]; then
		echo "$i.IQ missing!"
	fi
	cat $i.IQ >> out.IQ
	rm $i.IQ
done

echo "done."

#todo: Add SigMF metadata generator (Python?)