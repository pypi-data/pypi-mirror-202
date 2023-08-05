// This file is part of libigl, a simple c++ geometry processing library.
// 
// Copyright (C) 2016 Alec Jacobson <alecjacobson@gmail.com>
// 
// This Source Code Form is subject to the terms of the Mozilla Public License 
// v. 2.0. If a copy of the MPL was not distributed with this file, You can 
// obtain one at http://mozilla.org/MPL/2.0/.
#include "triangulated_grid.h"
#include "grid.h"
#include <cassert>

template <
  typename XType,
  typename YType,
  typename DerivedGV,
  typename DerivedGF>
IGL_INLINE void igl::triangulated_grid(
  const XType & nx,
  const YType & ny,
  Eigen::PlainObjectBase<DerivedGV> & GV,
  Eigen::PlainObjectBase<DerivedGF> & GF)
{
  using namespace Eigen;
  Eigen::Matrix<XType,2,1> res(nx,ny);
  igl::grid(res,GV);
  return igl::triangulated_grid(nx,ny,GF);
};

template <
  typename XType,
  typename YType,
  typename DerivedGF>
IGL_INLINE void igl::triangulated_grid(
  const XType & nx,
  const YType & ny,
  Eigen::PlainObjectBase<DerivedGF> & GF)
{
  GF.resize((nx-1)*(ny-1)*2,3);
  for(int y = 0;y<ny-1;y++)
  {
    for(int x = 0;x<nx-1;x++)
    {
      // index of southwest corner
      const XType sw = (x  +nx*(y+0));
      const XType se = (x+1+nx*(y+0));
      const XType ne = (x+1+nx*(y+1));
      const XType nw = (x  +nx*(y+1));
      // Index of first triangle in this square
      const XType gf = 2*(x+(nx-1)*y);
      GF(gf+0,0) = sw;
      GF(gf+0,1) = se;
      GF(gf+0,2) = nw;
      GF(gf+1,0) = se;
      GF(gf+1,1) = ne;
      GF(gf+1,2) = nw;
    }
  }
}


#ifdef IGL_STATIC_LIBRARY
// Explicit template instantiation
// generated by autoexplicit.sh
template void igl::triangulated_grid<int, int, Eigen::Matrix<double, -1, -1, 0, -1, -1>, Eigen::Matrix<int, -1, -1, 0, -1, -1> >(int const&, int const&, Eigen::PlainObjectBase<Eigen::Matrix<double, -1, -1, 0, -1, -1> >&, Eigen::PlainObjectBase<Eigen::Matrix<int, -1, -1, 0, -1, -1> >&);
#endif
