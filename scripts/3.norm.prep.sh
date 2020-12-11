git clone https://bitbucket.org/robvanderg/monoise.git

cd monoise
git reset --hard 082f6913cb5013d54ba1eca9eab7a8d227313c01
cp ../scripts/readgold.cc src/model/
mkdir data
mkdir working
cd data
wget www.robvandergoot.com/data/monoise/da.tar.gz
tar -zxvf da.tar.gz
cd ../src
icmbuild
cd ../../
