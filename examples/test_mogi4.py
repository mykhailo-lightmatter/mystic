#!/usr/bin/env python

"""
Similar to test_mogi2 (two sources) (See that one first)
"""

from test_mogi2 import params0, params1, stations, data, data_z, ND, NP, plot_sol, plot_noisy_data, MAX_GENERATIONS, ForwardMogiFactory
from mystic.differential_evolution import DifferentialEvolutionSolver
from mystic.termination import ChangeOverGeneration, VTR
from mystic.strategy import Best1Exp, Rand1Exp, Best2Exp, Best2Exp
from mystic import getch, Sow, random_seed

from mystic.forward_model import CostFactory
from mystic.filters import PickComponent

def de_solve(CF):
    solver = DifferentialEvolutionSolver(ND, NP)

    solver.enable_signal_handler()

    stepmon = Sow()
    minrange = [-1000., -1000., -100., -1.]*2;
    maxrange = [1000., 1000., 100., 1.]*2;
    solver.SetRandomInitialPoints(min = minrange, max = maxrange)

    solver.Solve(CF, Best1Exp, termination = ChangeOverGeneration(generations=300) , \
                 maxiter= MAX_GENERATIONS, CrossProbability=0.5, ScalingFactor=0.5, \
                 StepMonitor = stepmon, sigint_callback = plot_sol)

    solution = solver.Solution()
  
    return solution, stepmon

if __name__ == '__main__':

    F = CostFactory()
    F.addModel(ForwardMogiFactory, 'mogi1', 4, outputFilter = PickComponent(2, -1))
    F.addModel(ForwardMogiFactory, 'mogi2', 4, outputFilter = PickComponent(2, -1))
    myCostFunction = F.getCostFunction(evalpts = stations, observations = data_z)
    print F

    def C2(x):
        "This is the new version"
        return 100000 * myCostFunction(x)

    def C3(x):
        "Cost function constructed by hand"
        from test_mogi2 import cost_function
        return cost_function(x)

    def test():
        "call me to see if the functions return the same thing"
        rp = F.getRandomParams()
        print "C2: ", C2(rp)
        print "C3: ", C3(rp)

    test()
    #import sam
    import pylab
    plot_noisy_data()
    #sam.eval("hold on")
    desol, dstepmon = de_solve(C2)
    print "desol: ", desol

   #plot_sol(dstepmon.x[-100],'k-')
    plot_sol(desol,'r-')

    getch()

# end of file