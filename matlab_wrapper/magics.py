# encoding: utf-8
"""
=============
matlabmagic
=============
Magic command interface for interactive matlab_wrapper.
"""
from __future__ import print_function

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

from IPython.core.magic import (Magics, magics_class, needs_local_scope)
                                
#-----------------------------------------------------------------------------
# Definitions of magic functions for use with IPython
#-----------------------------------------------------------------------------

@magics_class
class MatlabMagics(Magics):
    """A set of magics useful when executing matlab commans.
    """
    matlab = None
    
    def __init__(self,shell,matlab,suffix=''):
        self.matlab = matlab
        self.suffix = suffix
        
        # register magics
        self.magics = dict(cell={},line={})
        line_magics = self.magics['line']
        
        line_magics['matpull' + suffix] = self.pull
        line_magics['matpush' + suffix] = self.push
        line_magics['matlab' + suffix] = self.eval
        
        self.magics['cell']['matlab' + suffix] = self.eval
        
        super(MatlabMagics,self).__init__(shell=shell)
        
    @needs_local_scope
    def pull(self,line,local_ns=None):
        """Pull variables the MATLAB workspace to the python namespace.
        """
        local_ns = local_ns or {}
        for var in line.split(' '):
            local_ns[var] = self.matlab.get(var)
        
    @needs_local_scope
    def push(self,line,local_ns=None):
        """Push variables from the python namespace to the MATLAB workspace.
        """
        local_ns = local_ns or {}
        for var in line.split(' '):
            self.matlab.put(var,local_ns[var])
        
    def eval(self,line,cell=''):
        """Run matlab code from a line or cell.
        """
        if cell:
            self.matlab.eval(cell)
        else:
            self.matlab.eval(line)
            
        if self.matlab.output_buffer:
            tocut = '>> >> >> '
            if self.matlab.output_buffer[:len(tocut)] == tocut:
                print(self.matlab.output_buffer[len(tocut):])
            else:
                print(self.matlab.output_buffer)
        