#!/usr/bin/env python
#
# Author: Patrick Hung (patrickh @caltech)
# Copyright (c) 1997-2014 California Institute of Technology.
# License: 3-clause BSD.  The full license text is available at:
#  - http://trac.mystic.cacr.caltech.edu/project/mystic/browser/mystic/LICENSE
"""
Implements a simple version of the Metropolis-Hastings algorithm
"""


def metropolis_hastings(proposal, target, x):
    """ 
Proposal(x) -> next point. Must be symmetric.
This is because otherwise the PDF of the proposal density is needed
(not just a way to draw from the proposal)
    """
    from numpy import random
    Yt = proposal(x)
    r = min(target(Yt)/(target(x) + 1e-100), 1)
    if random.random() <= r:
        return Yt
    else:
        return x

    
if __name__=='__main__':
    pass

# end of file
