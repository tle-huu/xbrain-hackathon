# Copyright (c) 2015-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the BSD+Patents license found in the
# LICENSE file in the root directory of this source tree.

CXX          = g++ -std=c++11
CXXCPP       = g++ -std=c++11 -E
# TODO: Investigate the LAPACKE wrapper for LAPACK, which defines the correct
#   type for FORTRAN integers.
CPPFLAGS     = -DFINTEGER=int 
CXXFLAGS     = -fPIC -fopenmp -m64 -Wno-sign-compare -g -O3 -Wall -Wextra
CPUFLAGS     = -msse4 -mpopcnt
LDFLAGS      = -fopenmp 
LIBS         = -lblas -llapack 
PYTHONCFLAGS = -I/usr/include/python3.6m -I/usr/include/x86_64-linux-gnu/python3.6m -I

NVCC         = 
NVCCLDFLAGS  = 
NVCCLIBS     = 
CUDAROOT     = 
CUDACFLAGS   = 
NVCCFLAGS    = -I $(CUDAROOT)/targets/x86_64-linux/include/ \
-Xcompiler -fPIC \
-Xcudafe --diag_suppress=unrecognized_attribute \
-gencode arch=compute_35,code="compute_35" \
-gencode arch=compute_52,code="compute_52" \
-gencode arch=compute_60,code="compute_60" \
-gencode arch=compute_61,code="compute_61" \
-lineinfo \
-ccbin $(CXX) -DFAISS_USE_FLOAT16

OS = $(shell uname -s)

SHAREDEXT   = so
SHAREDFLAGS = -shared

ifeq ($(OS),Darwin)
	SHAREDEXT   = dylib
	SHAREDFLAGS = -dynamiclib -undefined dynamic_lookup
endif

MKDIR_P      = /bin/mkdir -p
PYTHON       = python3
SWIG         = 

prefix      ?= /usr/local
exec_prefix ?= ${prefix}
libdir       = ${exec_prefix}/lib
includedir   = ${prefix}/include
