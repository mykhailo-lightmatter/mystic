#!/usr/bin/env python
#
# Author: Alta Fang (altafang @caltech and alta @princeton)
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2014 California Institute of Technology.
# License: 3-clause BSD.  The full license text is available at:
#  - http://trac.mystic.cacr.caltech.edu/project/mystic/browser/mystic/LICENSE
"""
chebyshevinputs.py -- cost function container module for NelderMeadSimplexSolver 
and PowellDirectionalSolver for testsolvers_pyre.py
"""

from mystic.models.poly import chebyshev8cost as cost
from mystic.models.poly import chebyshev8coeffs
from mystic.termination import *

ND = 9
maxiter = 999

from numpy import inf
import random
random.seed(123)

x0 = [random.uniform(-5,5) + chebyshev8coeffs[i] for i in range(ND)]

# used with SetStrictRanges
min_bounds = [  0,-1,-300,-1,  0,-1,-100,-inf,-inf]
max_bounds = [200, 1,   0, 1,200, 1,   0, inf, inf]

termination = CandidateRelativeTolerance()
#termination = VTR()
#termination = ChangeOverGeneration()
#termination = NormalizedChangeOverGeneration()

# End of file
