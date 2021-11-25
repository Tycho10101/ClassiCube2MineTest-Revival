echo ClassiCube2Minetest: Block: 1: Extracting world.json
mkdir extracted
cat $@ | gzip -d | ./nbt2json --big-endian > extracted/world.json
echo ClassiCube2Minetest: Block: 1: Create Metadata.json
mkdir extracted_custom
cat extracted/world.json | jq '.nbt[] | .value[] | select(.name == "Metadata") ' > extracted_custom/Metadata.json
echo ClassiCube2Minetest: Block: 1: Create BlockDefinitions.json
cat extracted_custom/Metadata.json | jq '.value[] | select(.name == "CPE") | .value[] | select(.name == "BlockDefinitions") | .value[] ' > extracted_custom/BlockDefinitions.json
echo ClassiCube2Minetest: Block: 1: Create BlockNames.json
cat extracted_custom/BlockDefinitions.json | jq '.name' > extracted_custom/BlockNames.json 