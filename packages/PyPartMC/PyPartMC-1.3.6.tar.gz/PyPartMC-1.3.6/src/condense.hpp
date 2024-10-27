/*##################################################################################################
# This file is a part of PyPartMC licensed under the GNU General Public License v3 (LICENSE file)  #
# Copyright (C) 2022 University of Illinois Urbana-Champaign                                       #
# Authors: https://github.com/open-atmos/PyPartMC/graphs/contributors                              #
##################################################################################################*/

#pragma once
#include "aero_data.hpp"
#include "aero_state.hpp"
#include "env_state.hpp"
#include "aero_particle.hpp"

extern "C" void f_condense_equilib_particle(
    const void*,
    const void*,
    const void*
) noexcept;

extern "C" void f_condense_equilib_particles(
    const void*,
    const void*,
    const void*
) noexcept;

void condense_equilib_particle(
    const EnvState &env_state,
    const AeroData &aero_data,
    const AeroParticle &aero_particle
);

void condense_equilib_particles(
    const EnvState &env_state,
    const AeroData &aero_data,
    const AeroState &aero_state
);
