LineNum=1
LineNum=$(expr $LineNum)
LineTotal=$(grep -c ^ extracted_custom/BlockNames.json)
LineTotal=$(expr $LineTotal)
mkdir extracted_custom/blocks
while [ $LineNum -le $LineTotal ]; 
do 
	cat extracted_custom/BlockNames.json | head -n $LineNum | tail -n 1
	BlockName=$(cat extracted_custom/BlockNames.json | head -n $LineNum | tail -n 1)
	BlockNameFile=$(echo $BlockName | sed 's/"//g' )
	cat extracted_custom/BlockDefinitions.json | jq 'select(.name=='\"$BlockNameFile\"') | .value ' > extracted_custom/blocks/$BlockNameFile.json
	echo ClassiCube2Minetest: Block: 2: Create Seperate Block JSON: $BlockNameFile
	LineNum=$(($LineNum+1))
done

