max=127

for i in `seq 2 $max`
do
	echo $i
	python handler.py -l "../data/local_data.csv" -p $i -t
done
exit