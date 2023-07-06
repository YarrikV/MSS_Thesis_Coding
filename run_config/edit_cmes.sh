'''
for folder in mass1[0-9][0-9]; do
	echo $folder
	cp cmes.dat $folder/
done
'''

for folder in mass[0-9][0-9]3; do
        echo $folder
        vim -c '%s/RADIUS/18.6195/' -c 'wq' "$folder/cmes.dat"
done

