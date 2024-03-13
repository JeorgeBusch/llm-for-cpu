/*
 * Copyright (c) 2016 Jason Lowe-Power
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are
 * met: redistributions of source code must retain the above copyright
 * notice, this list of conditions and the following disclaimer;
 * redistributions in binary form must reproduce the above copyright
 * notice, this list of conditions and the following disclaimer in the
 * documentation and/or other materials provided with the distribution;
 * neither the name of the copyright holders nor the names of its
 * contributors may be used to endorse or promote products derived from
 * this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 * A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
 * OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 * LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 * DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 * THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

#include "periodic_check/check_object.hh"

#include "base/logging.hh"
#include "base/trace.hh"
//#include "base.hh"
#include <iostream>
#include "sim/stat_control.hh"
#include "cpu/base.hh"

namespace gem5
{

CheckObject::CheckObject(const CheckObjectParams &params) :
    SimObject(params),
	event([this]{ processEvent(); }, name() + ".event"),
	cpu(params.cpu)
{
    std::cout << "Created Check Object!" << std::endl;
}
void
CheckObject::startup()
{
    // Before simulation starts, we need to schedule the event
    schedule(event, 0);
}

void
CheckObject::processEvent()
{
	//Counter num_instr = cpu->numSimulatedInsts(); 
	
	//stats::Scalar &numCycles = cpu->BaseCPUStats.numCycles;
	/*
	if (numCycles == NULL)
		std::cout << "Null" << std::endl;
	else{
		std::cout << "Not Null" << std::endl;
		std::cout << numCycles.unit().getUnitString() << std::endl;
	}
	*/
	//std::cout << numCycles.unit().getUnitString() << std::endl;
    std::cout << "Hello world! Processing the event!" << std::endl;

    schedule(event, curTick() + 1000000000000);
}

} // namespace gem5
