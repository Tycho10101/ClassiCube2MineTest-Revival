mkdir output
mkdir output/worldmods
mkdir output/worldmods/classicubeconverted
rm output/worldmods/classicubeconverted/init.lua
find extracted_custom/blocks/. -name "*.json*" -exec scripts/converttomtmod_1sub_blocks.sh {} \; >> output/worldmods/classicubeconverted/init.lua
mkdir output/worldmods/classicubeconverted/textures
cp extracted_custom/texture_block/* output/worldmods/classicubeconverted/textures/