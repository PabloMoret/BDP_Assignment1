max=127

for i in `seq 2 $max`
do
	start handler.py -l "../data/local_data.csv" -p $i -t
done
exit