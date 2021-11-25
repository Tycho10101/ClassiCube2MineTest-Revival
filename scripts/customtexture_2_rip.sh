
mkdir extracted_custom/textures
cd extracted_custom/textures
echo ClassiCube2Minetest: Texture: 1: Extract Texture ZIP
7za x ../texturezip/*.zip 
cd ../../

mkdir extracted_custom/texture_block

size=$(identify -format '%w %h' extracted_custom/textures/terrain.png)
TerrainSizeX=$(echo $size | cut -d ' ' -f 1)
TerrainSizeY=$(echo $size | cut -d ' ' -f 2)
BlockSizeX=$(expr $TerrainSizeX / 16)
BlockSizeY=$(expr $TerrainSizeY / 16)

CurrentBlockX=1
CurrentBlockY=1

#convert extracted_custom/textures/terrain.png -crop 16x16+0+0 cropped.jpg
BlockNumber=0
while [ $CurrentBlockY -le $BlockSizeY ]; 
do 
	PixelCropX=$(expr $CurrentBlockX \* 16)
	PixelCropX=$(expr $PixelCropX - 16)
	PixelCropY=$(expr $CurrentBlockY \* 16)
	PixelCropY=$(expr $PixelCropY - 16)
	echo ClassiCube2Minetest: Texture: 2: Create Seperate Texture for $BlockNumber: $CurrentBlockX $CurrentBlockY 
	convert extracted_custom/textures/terrain.png -crop 16x16+$PixelCropX+$PixelCropY extracted_custom/texture_block/$BlockNumber.png
	BlockNumber=$(($BlockNumber+1))
	CurrentBlockX=$(($CurrentBlockX+1))
	if (( $CurrentBlockX > $BlockSizeX )); then
	CurrentBlockY=$(($CurrentBlockY+1))
	CurrentBlockX=1
    fi

done
