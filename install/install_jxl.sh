#!/usr/bin/env zsh

if [[ ! -d ${JXL_root_DIR} ]]
then
	echo "please source project"
fi

source_DIR=${JXL_root_DIR}/repo/libjxl
build_DIR=${JXL_root_DIR}/build/libjxl
root_DIR=${JXL_root_DIR}/root

if [[ -d ${build_DIR} ]]
then
	rm -rf ${build_DIR}
fi
mkdir ${build_DIR}

pushd ${build_DIR}
	cmake --install-prefix=${root_DIR} \
		-DCMAKE_CXX_FLAGS="-O3 -march=native -mtune=native" \
		-DCMAKE_BUILD_TYPE=Release -DBUILD_TESTING=OFF \
		-DJPEGXL_ENABLE_DEVTOOLS=ON \
		${source_DIR}
	make -j 4
	make install
popd
