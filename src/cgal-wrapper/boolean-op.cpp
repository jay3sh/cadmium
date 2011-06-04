
#include <CGAL/Exact_predicates_exact_constructions_kernel.h>
#include <CGAL/Gmpz.h>
#include <CGAL/Homogeneous.h>
#include <CGAL/Polyhedron_3.h>
#include <CGAL/IO/Polyhedron_iostream.h>
#include <CGAL/Nef_polyhedron_3.h>
#include <CGAL/IO/Nef_polyhedron_iostream_3.h>
#include <iostream>
#include <fstream>

typedef CGAL::Exact_predicates_exact_constructions_kernel  Kernel;
typedef CGAL::Polyhedron_3<Kernel>  Polyhedron;
typedef CGAL::Nef_polyhedron_3<Kernel> Nef_polyhedron;
typedef Kernel::Vector_3  Vector_3;
typedef Kernel::Aff_transformation_3  Aff_transformation_3;

int main(int argc, char *argv[]) {
  std::ifstream off1(argv[1]);
  std::ifstream off2(argv[2]);
  Polyhedron p1, p2;
  off1 >> p1;
  off2 >> p2;

  Nef_polyhedron n1(p1);
  Nef_polyhedron n2(p2);

  n1 += n2;

  Polyhedron p;
  n1.convert_to_polyhedron(p);
  std::cout << p << std::endl;
}
