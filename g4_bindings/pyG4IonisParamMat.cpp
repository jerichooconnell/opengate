/* --------------------------------------------------
   Copyright (C): OpenGATE Collaboration
   This software is distributed under the terms
   of the GNU Lesser General  Public Licence (LGPL)
   See LICENSE.md for further details
   -------------------------------------------------- */

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

#include "G4IonisParamMat.hh"

void init_G4IonisParamMat(py::module &m) {

    py::class_<G4IonisParamMat>(m, "G4IonisParamMat")
            //.def(py::init<>())

            // stream output /// FIXME not sure this is the right way to do
            /* .def("__repr__", [](const G4IonisParamMat &IonisParamMat) {
                 std::ostringstream flux;
                 flux << IonisParamMat;
                 return flux.str();
             })*/

            .def("GetMeanExcitationEnergy", &G4IonisParamMat::GetMeanExcitationEnergy);
}

