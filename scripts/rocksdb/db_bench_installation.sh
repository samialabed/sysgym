#!/bin/bash
pushd $PWD 1>/dev/null


# Install essentials
sudo apt-get install build-essential make

# _install snappy
echo "****************** Installing snappy *******************"
sudo apt-get install libsnappy-dev libzstd-dev liblz4-dev -y

# _install gflag
echo "****************** Installing gflag ********************"
#cd /tmp
# git clone https://github.com/gflags/gflags.git
#cd gflags
#git checkout v2.0
#./configure && make && sudo make _install

sudo apt-get install -y libgflags-dev

# _install rocksdb
echo "****************** Installing rocksdb ******************"
cd /tmp
git clone https://github.com/facebook/rocksdb.git
cd rocksdb
CPATH=/usr/local/include LD_LIBRARY_PATH=/usr/local/lib LIBRARY_PATH=/usr/local/lib DEBUG_LEVEL=0 make db_bench -j7

mkdir -p $HOME/.local/bin 
DIR=$HOME/.local/bin/
if [[ ! -e $DIR ]]; then
    mkdir $DIR
elif [[ ! -d $DIR ]]; then
    echo "$DIR already exists but is not a directory" 1>&2
    exit
fi
mv db_bench $HOME/.local/bin &&
echo "Successfully installed rocksed in "$DIR" !" &&
echo "Adding "$DIR" to your PATH."
echo "export PATH={$DIR}:'$PATH'" >> $HOME/.bashrc

popd 1>/dev/null
