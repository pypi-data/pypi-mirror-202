// This file is part of libigl, a simple c++ geometry processing library.
//
// Copyright (C) 2013 Alec Jacobson <alecjacobson@gmail.com>
//
// This Source Code Form is subject to the terms of the Mozilla Public License
// v. 2.0. If a copy of the MPL was not distributed with this file, You can
// obtain one at http://mozilla.org/MPL/2.0/.
#ifndef IGL_WRITESTL_H
#define IGL_WRITESTL_H
#include "igl_inline.h"
#include <igl/FileEncoding.h>

#ifndef IGL_NO_EIGEN
#  include <Eigen/Core>
#endif
#include <string>
#include <vector>

namespace igl
{
  // Write a mesh to an stl file.
  //
  // Templates:
  //   Scalar  type for positions and vectors (will be read as double and cast
  //     to Scalar)
  // Inputs:
  //   filename path to .obj file
  //   V  double matrix of vertex positions  #F*3 by 3
  //   F  index matrix of triangle indices #F by 3
  //   N  double matrix of vertex positions  #F by 3
  //   encoding enum to set file encoding (ascii by default)
  // Returns true on success, false on errors
  //
  template <typename DerivedV, typename DerivedF, typename DerivedN>
  IGL_INLINE bool writeSTL(
    const std::string & filename,
    const Eigen::MatrixBase<DerivedV> & V,
    const Eigen::MatrixBase<DerivedF> & F,
    const Eigen::MatrixBase<DerivedN> & N,
    FileEncoding encoding=FileEncoding::Ascii);
  template <typename DerivedV, typename DerivedF>
  IGL_INLINE bool writeSTL(
    const std::string & filename,
    const Eigen::MatrixBase<DerivedV> & V,
    const Eigen::MatrixBase<DerivedF> & F,
    FileEncoding encoding=FileEncoding::Ascii);
}

#ifndef IGL_STATIC_LIBRARY
#  include "writeSTL.cpp"
#endif

#endif
