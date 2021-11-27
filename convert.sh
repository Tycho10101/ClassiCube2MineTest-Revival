if [ $# -eq 0 ]
then
      echo "convert.sh packname cw_file"
      exit
fi

rm -rf extracted_custom/*
rm -rf extracted/*
scripts/extractmetadata.sh ${@:2}
scripts/customblocks_1_extractblockdefs.sh ${@:2}
scripts/customblocks_2_blockseperatejson.sh
scripts/customtexture_1_download.sh
scripts/customtexture_2_rip.sh
scripts/converttomtmod_1.sh $1
