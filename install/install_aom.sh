#!/usr/bin/env zsh

if [[ ! -d ${JXL_root_DIR} ]]
then
	echo "please source project"
fi

source_DIR=${JXL_root_DIR}/repo/libaom
build_DIR=${JXL_root_DIR}/build/libaom
root_DIR=${JXL_root_DIR}/root

if [[ -d ${build_DIR} ]]
then
	rm -rf ${build_DIR}
fi
mkdir ${build_DIR}

pushd ${build_DIR}
	cmake --install-prefix=${root_DIR} \
		-DCMAKE_CXX_FLAGS="-O3 -march=native -mtune=native" \
		-DBUILD_SHARED_LIBS=1 \
		${source_DIR}
	make
	make install
popd
