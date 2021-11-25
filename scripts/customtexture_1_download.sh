TextureURLParsed=$(cat extracted_custom/Metadata.json | jq '.value[] | select(.name == "CPE") | .value[] | select(.name == "EnvMapAppearance") | .value[] | select(.name == "TextureURL") | .value ')
TextureURL=$(echo $TextureURLParsed | sed 's/"//g' )
echo ClassiCube2Minetest: Texture: 1: Download Texture ZIP
mkdir extracted_custom/texturezip
wget $TextureURL -P extracted_custom/texturezip
