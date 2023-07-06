echo "making dirs"

for i in {1..3}; do
	for j in {1..3}; do
		for k in {1..3}; do
			name="mass$i$j$k"
			echo $name
			cp helios_mass.cfg $name/helios.cfg
			vim -c "%s/xxxxx/$name/g" -c 'wq' "$name/helios.cfg"

			cp run.pbs $name/run.pbs
			vim -c "%s/xxxxx/$name/g" -c 'wq' "$name/run.pbs"
		done
	done
done
