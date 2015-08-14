# If you put this file in the ~/.ipython/profile_default directory on OS X or, apparently,
# the %/.ipython/ directory on Windows then it should be run and the functions defined
# herein set up for use automatically whenever you start iPython.

import sys

# both of these from Python for Data Analysis, page 65.

# add a call to set_trace() in any other code and it'll break into the debugger
# right at that point
def set_trace():
    from IPython.core.debugger import Pdb
    Pdb(color_scheme='Linux').set_trace(sys._getframe().f_back)
    
# to enter a function and break into the debugger, call the function as follows:
# debug(f, 1, 2, z=3)
# where f is the function name, and 1, 2, and z=3 are params
def debug(f, *args, **kwargs):
    from IPython.core.debugger import Pdb
    pdb = Pdb(color_scheme='Linux')
    return pdb.runcall(f, *args, **kwargs)