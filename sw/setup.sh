#!/bin/env bash
#source /etc/larbys.sh
export LARCV_ANN=0
setupdir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

orig_dir=$PWD
force_rebuild=1;
if [[ ! -d $setupdir/larcv ]]; then
    force_rebuild=1;
fi
if [[ ! -z $1 ]]; then
    force_rebuild=$1;
fi

if [ $force_rebuild -eq 0 ]; then
    source $setupdir/geo2d/config/setup.sh
    source $setupdir/larcv/configure.sh
    source $setupdir/caffe/configure.sh
else

    unset GEO2D_BASEDIR
    if [[ ! -d $setupdir/larcv ]]; then
	git clone https://github.com/LArbys/LArCV $setupdir/larcv;
    fi
    cd $setupdir/larcv;
    source configure.sh;
    make -j6;

    if [[ ! -d $setupdir/caffe ]]; then
	git clone https://github.com/LArbys/caffe $setupdir/caffe;
    fi
    cd $setupdir/caffe;
    git checkout laurel_workspace
    source configure.sh;
    make -j6;
    make pycaffe

    if [[ ! -d $setupdir/geo2d ]]; then
	git clone https://github.com/LArbys/Geo2D $setupdir/geo2d;
    fi
    cd $setupdir/geo2d;
    source config/setup.sh;
    make -j6;

    rm $LARCV_LIBDIR/liblarcv.so

    cd $setupdir/larcv;
    source configure.sh;
    make -j6;

    cd $setupdir/caffe;
    source configure.sh;
    make -j6;
    make pycaffe

    cd $orig_dir;
fi
