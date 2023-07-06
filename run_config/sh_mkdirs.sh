echo "making dirs"

densities=("1e-18", "5e-18", "1e-17")
fluxes=("5e13", "1e14", "5e14")
radii=("10.75", "15.2028", "18.6195")

for i in {1..3}; do
	for j in {1..3}; do
		for k in {1..3}; do
			folder="mass$i$j$k"
			echo $folder
			mkdir $folder
			cp cmes.dat $folder
			vim -c "%s/RADIUS/${radii[$k - 1]}/" -c 'wq' "$folder/cmes.dat"
			vim -c "%s/FLUX/${fluxes[$j - 1]}/" -c 'wq' "$folder/cmes.dat"
			vim -c "%s/DENSITY/${densities[$i - 1]}/" -c 'wq' "$folder/cmes.dat"
			vim -c "%s/,//g" -c 'wq' "$folder/cmes.dat"
		done
	done
done
