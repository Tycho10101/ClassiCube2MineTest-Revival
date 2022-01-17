
mkdir extracted_custom/
mkdir extracted_custom/texture_block
mkdir extracted_custom/blocks
mkdir extracted_custom/textures

cd extracted_custom/textures
echo ClassiCube2Minetest: Texture: Extract Texture ZIP
7za x ../texturezip/texturezip.zip 
if [ ! -f "terrain.png" ]
then
    find . -type f -name 'terrain.png' -exec mv {} . \;
    find . -type f -name 'skybox.png' -exec mv {} . \;
fi
cd ../../

size=$(identify -format '%w %h' extracted_custom/textures/terrain.png)
TerrainSizeX=$(echo $size | cut -d ' ' -f 1)
TerrainSizeY=$(echo $size | cut -d ' ' -f 2)
BlockSize=$(expr $TerrainSizeX / 16)
BlockSizeX=$(expr $TerrainSizeX / $BlockSize)
BlockSizeY=$(expr $TerrainSizeY / $BlockSize)

CurrentBlockX=1
CurrentBlockY=1

#convert extracted_custom/textures/terrain.png -crop 16x16+0+0 cropped.jpg
BlockNumber=0
while [ $CurrentBlockY -le $BlockSizeY ]; 
do 
	PixelCropX=$(expr $CurrentBlockX \* $BlockSize)
	PixelCropX=$(expr $PixelCropX - $BlockSize)
	PixelCropY=$(expr $CurrentBlockY \* $BlockSize)
	PixelCropY=$(expr $PixelCropY - $BlockSize)
	echo ClassiCube2Minetest: Texture: Create Seperate Texture for $BlockNumber: $CurrentBlockX $CurrentBlockY 
	xString="x"
	convert extracted_custom/textures/terrain.png -crop $BlockSize$xString$BlockSize+$PixelCropX+$PixelCropY extracted_custom/texture_block/$BlockNumber.png
	BlockNumber=$(($BlockNumber+1))
	CurrentBlockX=$(($CurrentBlockX+1))
	if (( $CurrentBlockX > $BlockSizeX )); then
	CurrentBlockY=$(($CurrentBlockY+1))
	CurrentBlockX=1
    fi
done
