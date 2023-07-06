echo "making dirs"

for i in {1..3}; do
	for j in {1..3}; do
		for k in {1..3}; do
			name="mass$i$j$k"
			echo $name
			qsub $name/run.pbs
		done
	done
done
