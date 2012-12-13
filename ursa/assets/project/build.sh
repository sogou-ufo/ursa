
rm -rf output
rm -rf build


ursa build


mkdir output

cd build/
tar cjf ../output/template.bz2 template/
tar cjf ../output/static.bz2 static

cd ../
rm -rf build

