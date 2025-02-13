#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import opengate as gate
import opengate.tests.utility as tu
from test013_phys_lists_helpers import create_pl_sim

paths = tu.get_default_test_paths(__file__, "")

# create simulation
sim = gate.Simulation()
ui = sim.user_info
ui.g4_verbose = True

# units
m = gate.g4_units.m
cm = gate.g4_units.cm
mm = gate.g4_units.mm
eV = gate.g4_units.eV
MeV = gate.g4_units.MeV
Bq = gate.g4_units.Bq

# add a material database
print(f"Inside the test file - {paths.data}")
sim.add_material_database(paths.data / "GateMaterials.db")

# set the world size like in the Gate macro
world = sim.world
world.size = [3 * m, 3 * m, 3 * m]

# add a simple crystal volume
crystal = sim.add_volume("Box", "crystal")
crystal.size = [3 * mm, 3 * mm, 20 * mm]
crystal.translation = [0 * cm, 0 * cm, 0 * cm]
crystal.material = "BGO"

# change physics
# For the generation of Cerenkov, physics_list_name must
# be set to G4EmStandardPhysics_option4 and production cuts
# of electron must be set to 0.1 mm (Reason unknown)
# Reference - https://opengate.readthedocs.io/en/latest/generating_and_tracking_optical_photons.html
sim.physics_manager.physics_list_name = "G4EmStandardPhysics_option4"
sim.physics_manager.set_production_cut("crystal", "electron", 0.1 * mm)
sim.physics_manager.energy_range_min = 10 * eV
sim.physics_manager.energy_range_max = 1 * MeV
sim.physics_manager.special_physics_constructors.G4OpticalPhysics = True
# Users can specify their own path optical properties file by
# sim.physics_manager.optical_properties_file = PATH_TO_FILE
# By default, Gate uses the file opengate/data/OpticalProperties.xml


# Change source
source = sim.add_source("GenericSource", "gamma1")
source.particle = "gamma"
source.energy.mono = 0.511 * MeV
source.activity = 10 * Bq
source.direction.type = "momentum"
source.direction.momentum = [0, 0, -1]
source.position.translation = [0 * cm, 0 * cm, 2.2 * cm]

# add phase actor
phase = sim.add_actor("PhaseSpaceActor", "Phase")
phase.mother = crystal.name
phase.attributes = [
    "Position",
    "PostPosition",
    "PrePosition",
    "ParticleName",
    "TrackCreatorProcess",
    "EventKineticEnergy",
    "KineticEnergy",
    "PDGCode",
]
phase.output = paths.output / "test013_phys_lists_6.root"

sim.user_hook_after_run = gate.userhooks.user_hook_dump_material_properties
sim.run()

is_ok = all(t is True for t in sim.output.hook_log)
tu.test_ok(is_ok)
