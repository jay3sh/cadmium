// 
// Cadmium - Python library for Solid Modelling
// Copyright (C) 2011 Jayesh Salvi [jayesh <at> 3dtin <dot> com]
//

#include <CGAL/Inverse_index.h>
#include <CGAL/Exact_predicates_exact_constructions_kernel.h>
#include <CGAL/Polyhedron_incremental_builder_3.h>
#include <CGAL/Polyhedron_3.h>
#include <CGAL/Nef_polyhedron_3.h>
#include <CGAL/IO/Polyhedron_iostream.h>

#include <new>
#include <iostream>
#include <sstream>
#include <fstream>


// A modifier creating a triangle with the incremental builder.
template <class HDS>
class Builder : public CGAL::Modifier_base<HDS> {
private:
  double **vertices;
  int numvertices;
  int **faces;
  int numfaces;
  int vtxsize;
  int facesize;
public:

  Builder(double *v[], int numv, int vsize, int *f[], int numf, int fsize) :
  vertices(v),
  numvertices(numv),
  vtxsize(vsize),
  faces(f),
  numfaces(numf),
  facesize(fsize)
  {
  }

  void operator()( HDS& hds) {
    // Postcondition: `hds' is a valid polyhedral surface.
    typedef typename HDS::Vertex Vertex;
    typedef typename Vertex::Point Point;

    CGAL::Polyhedron_incremental_builder_3<HDS> B( hds, true);

    B.begin_surface(numvertices, numfaces, 0);

    int i,j;
    for(i=0; i<numvertices; i++) {
      double *v = vertices[i];
      B.add_vertex(Point(v[0], v[1], v[2]));
    }

    for(i=0; i<numfaces; i++) {
      int *f = faces[i];
      B.begin_facet();
      for(j=0; j<facesize; j++) {
        B.add_vertex_to_facet(f[j]);
      }
      B.end_facet();
    }

    B.end_surface();
  }
};

typedef CGAL::Exact_predicates_exact_constructions_kernel  Kernel;
typedef CGAL::Polyhedron_3<Kernel>         Polyhedron;
typedef CGAL::Nef_polyhedron_3<Kernel> Nef_polyhedron;
typedef CGAL::Point_3<Kernel>              Point_3;
typedef Polyhedron::HalfedgeDS             HalfedgeDS;
typedef Polyhedron::Vertex_iterator        VertexIterator;
typedef Polyhedron::Vertex                 Vertex;
typedef Polyhedron::Facet_iterator         FacetIterator;

#ifdef __cplusplus 
extern "C" {
#endif

int OP_UNION = 1;
int OP_INTERSECTION = 2;
int OP_SUBTRACTION = 3;

int ERR_NOT_SIMPLE = 1;

typedef struct {
  int error;
  int num_vertices;
  int num_faces;
  double **vertices;
  int **faces;
} PolyhedronPack;

void free_ppack( PolyhedronPack *ppack )
{
  //free ppack.
  if ( ppack ) {
    //free ppack->vertices.
    if ( ppack->vertices ) {
      for ( int i = 0; i < ppack->num_vertices; ++i ) {
        free ( ppack->vertices[i] ) ;
        ppack->vertices[i] = NULL;
      }
      free ( ppack->vertices );
      ppack->vertices = NULL;
    }

    //free ppack->faces
    if ( ppack->faces ) {
      for ( int i = 0; i < ppack->num_faces; ++i ) {
        free ( ppack->faces[i] );
        ppack->faces[i] = NULL;
      }
      free ( ppack->faces );
      ppack->faces = NULL;
    }

    free ( ppack );
    ppack = NULL;
  }
}

PolyhedronPack *pack_polyhedron(const Polyhedron& P) {

  typedef Polyhedron::Vertex                                 Vertex;
  typedef Polyhedron::Vertex_const_iterator                  VCI;
  typedef Polyhedron::Facet_const_iterator                   FCI;
  typedef Polyhedron::Halfedge_around_facet_const_circulator HFCC;

  PolyhedronPack *ppack = (PolyhedronPack *) calloc(1, sizeof(PolyhedronPack));
  if(!ppack) { throw std::bad_alloc(); }
  ppack->num_vertices = P.size_of_vertices();
  ppack->num_faces = P.size_of_facets();
  ppack->vertices = (double **) calloc(ppack->num_vertices, sizeof(double *));
  if(!ppack->vertices) {
    free_ppack(ppack);
    throw std::bad_alloc();
  }
  ppack->faces = (int **) calloc(ppack->num_faces, sizeof(int *));
  if(!ppack->faces) {
    free_ppack(ppack);
    throw std::bad_alloc();
  }

  int i=0;
  for(VCI vi = P.vertices_begin(); vi != P.vertices_end(); ++vi, ++i) {
    ppack->vertices[i] = (double *) calloc(3, sizeof(double));
    if(!ppack->vertices[i]) {
      free_ppack(ppack);
      throw std::bad_alloc();
    }
    ppack->vertices[i][0] = CGAL::to_double(vi->point().x());
    ppack->vertices[i][1] = CGAL::to_double(vi->point().y());
    ppack->vertices[i][2] = CGAL::to_double(vi->point().z());
  }

  typedef CGAL::Inverse_index< VCI> Index;
  Index index( P.vertices_begin(), P.vertices_end());

  i=0;
  for(FCI fi = P.facets_begin(); fi != P.facets_end(); ++fi, ++i) {
    HFCC hc = fi->facet_begin();
    HFCC hc_end = hc;
    std::size_t n = circulator_size( hc);
    CGAL_assertion( n == 3);
    ppack->faces[i] = (int *) calloc(3, sizeof(int));
    if(!ppack->faces[i]) {
      free_ppack(ppack);
      throw std::bad_alloc();
    }
    int j=0;
    do {
      ppack->faces[i][j] = index[VCI(hc->vertex())];
      ++hc;
      ++j;
    } while( hc != hc_end);
  }

  return ppack;
}

PolyhedronPack *csgop(
  double *pointsA[], int npointsA, int pointsizeA, 
  int *facesA[], int nfacesA, int facesizeA,
  double *pointsB[], int npointsB, int pointsizeB, 
  int *facesB[], int nfacesB, int facesizeB,
  int op)
{

  Polyhedron pA, pB;
  Builder<HalfedgeDS> builderA(pointsA, npointsA, pointsizeA, facesA, nfacesA, facesizeA);
  Builder<HalfedgeDS> builderB(pointsB, npointsB, pointsizeB, facesB, nfacesB, facesizeB);
  pA.delegate(builderA);
  pB.delegate(builderB);

  Nef_polyhedron nA(pA);
  Nef_polyhedron nB(pB);

  if(op == OP_UNION) {
    nA += nB;
  } else if(op == OP_SUBTRACTION) {
    nA -= nB;
  } else if(op == OP_INTERSECTION) {
    nA *= nB;
  }

  Polyhedron p;

  if(nA.is_simple()) {
    nA.convert_to_polyhedron(p);
    return pack_polyhedron(p);
  } else {
    PolyhedronPack *ppack = (PolyhedronPack *) calloc(1, sizeof(PolyhedronPack));
    if(!ppack) { throw std::bad_alloc(); }
    ppack->error = ERR_NOT_SIMPLE;
    return ppack;
  }

}

int csgop_simple(const char* offA, const char* offB, int op) {
  std::istringstream istreamA(offA);
  std::istringstream istreamB(offB);
  Polyhedron pA, pB;
  istreamA >> pA;
  istreamB >> pB;
  Nef_polyhedron nA(pA);
  Nef_polyhedron nB(pB);

  if(op == OP_UNION) {
    nA += nB;
  } else if(op == OP_SUBTRACTION) {
    nA -= nB;
  } else if(op == OP_INTERSECTION) {
    nA *= nB;
  }

  Polyhedron p;
  nA.convert_to_polyhedron(p);
  std::ofstream out("42.off");
  out << p;
  return 42;
}

#ifdef __cplusplus
}
#endif
