LineNum=1
LineNum=$(expr $LineNum)
LineTotal=$(grep -c ^ extracted_custom/BlockNames.json)
LineTotal=$(expr $LineTotal)
mkdir extracted_custom/blocks
while [ $LineNum -le $LineTotal ]; 
do 
	BlockName=$(cat extracted_custom/BlockNames.json | head -n $LineNum | tail -n 1)
	cat extracted_custom/BlockDefinitions.json | jq '.'\"$BlockName\"'' > extracted_custom/blocks/$BlockName.json
	echo ClassiCube2Minetest: Block: Create Seperate Block JSON: $BlockName
	LineNum=$(($LineNum+1))
done

