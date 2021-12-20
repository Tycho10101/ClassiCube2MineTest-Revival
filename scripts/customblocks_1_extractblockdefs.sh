mkdir extracted_custom
echo ClassiCube2Minetest: Block: Create BlockDefinitions.json
cat extracted_custom/Metadata.json | jq -r '.CPE | .BlockDefinitions ' > extracted_custom/BlockDefinitions.json

echo ClassiCube2Minetest: Block: Create BlockNames.json
cat extracted_custom/Metadata.json | jq -r '.CPE | .BlockDefinitions | keys[] as $k | "\($k)"' > extracted_custom/BlockNames.json 
