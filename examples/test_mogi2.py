#!/usr/bin/env python

"""
Two mogi sources. Similar to test_mogi.py. (See that one first)

Reference:

[1] Mogi, K. Relations between the eruptions of various
volcanoes and the deformations of the ground surfaces around them, 
Bull. Earthquake. Res. Inst., 36, 99-134, 1958.
"""

from test_mogi import *

# Let the "actual parameters" be :
params0 = [1000.,-100., 10., .2]
params1 = [1500.,-400., 40., 1.5]

forward0 = ForwardMogiFactory(params0)
forward1 = ForwardMogiFactory(params1)

# The data to be "fitted" 
xstations = array([random.uniform(-500,500) for i in range(300)])+1250.
ystations =  0*xstations - 200.
stations  = array((xstations, ystations))

data = forward0(stations) + forward1(stations)
# noisy data, gaussian distribution
noise =  array([[random.normal(0,0.05e-5) for i in range(data.shape[1])] for j in range(data.shape[0])])

# observed data
data_z = -data[2,:] + noise[2,:]

def cost_function(params):
    m0 = ForwardMogiFactory(params[0:4])
    m1 = ForwardMogiFactory(params[4:])
    zdisp = filter_for_zdisp(m0(stations) + m1(stations))
    x = zdisp - data_z
    return 100000. * numpy.sum(real((conjugate(x)*x)))

def plot_noisy_data():
    #import sam
    #sam.putarray('st',stations)
    #sam.putarray('data',data)
    #sam.putarray('noise',noise)
    #sam.eval("plot(st(1,:),-data(3,:)+noise(3,:),'k.')")
    import pylab
    pylab.plot(stations[0,:],-data[2,:]+noise[2,:],'k.')

def plot_sol(params, linestyle = 'b-'):
    import pylab
    #import sam
    s0 = ForwardMogiFactory(params[0:4])
    s1 = ForwardMogiFactory(params[4:])
    xx = arange(-500,500,1)+1250.
    yy = 0*xx - 200.
    ss  = array((xx, yy))
    dd = s0(ss) + s1(ss)
    #sam.putarray('ss',ss)
    #sam.putarray('dd',dd)
    #sam.eval("plot(ss(1,:),-dd(3,:),'%s','LineWidth',2)" % linestyle)
    pylab.plot(ss[0,:],-dd[2,:],'%s'%linestyle,linewidth=2.0)

ND = 8
NP = 80
MAX_GENERATIONS = 5000

def de_solve():
    solver = DifferentialEvolutionSolver(ND, NP)

    solver.enable_signal_handler()

    stepmon = VerboseSow()
    minrange = [-1000., -1000., -100., -1.]*2;
    maxrange = [1000., 1000., 100., 1.]*2;
    solver.SetRandomInitialPoints(min = minrange, max = maxrange)

    solver.Solve(cost_function, Best1Exp, termination = ChangeOverGeneration(generations=300) , \
                 maxiter= MAX_GENERATIONS, CrossProbability=0.5, ScalingFactor=0.5, \
                 StepMonitor = stepmon, sigint_callback = plot_sol)

    solution = solver.Solution()
  
    return solution, stepmon

if __name__ == '__main__':

    #import sam
    pylab.ion()
    plot_noisy_data()
    #sam.eval("hold on")
    desol, dstepmon = de_solve()
    print "desol: ", desol
   #plot_sol(dstepmon.x[-100],'k-')

    plot_sol(desol,'r-')
    pylab.show()

    getch()

# end of file