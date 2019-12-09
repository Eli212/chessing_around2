""" utilities for debugging of python scripts. prints stack backtraces that look similar to gdb stacktrace (gdb commands bt and bt full); 
can be used instead of traceback.

Written by Michael Moser (c) 2015
"""

import traceback
import sys
import inspect
import pprint
import linecache


__all__ = [ 'print_stack_ex',  'print_exception_ex', 'die', 'die2' ]

def getrep( value, follow_objects ):
    if follow_objects == 0:
	return value
    try:
	return vars( value ) 	
    except TypeError:
	return value
    return None	


def format_frame( nframe, frame, follow_objects ):
    ret = ''
    if nframe != -1:
	ret += '#' + str(nframe) 
    ret += ' def ' + frame.f_code.co_name + "("
    for i in range(0, frame.f_code.co_argcount):
	if i >0:
	    ret += ", "
	argname = frame.f_code.co_varnames[ i ]  		    
	try:
	    ret += argname  + " = " + pprint.pformat( getrep( frame.f_locals[ argname  ], follow_objects) )
	except Exception as e:
	    ret += '<error while formatting>' + str( e ) # str( frame.f_locals[ argname ]  )
    ret += ") at " + frame.f_code.co_filename + ":" + str( frame.f_lineno ) #str( frame.f_code.co_firstlineno )

    n = frame.f_code.co_argcount
    if n < len(frame.f_code.co_varnames):
	ret += "\nLocal variables:\n"
	while n < len(frame.f_code.co_varnames):
	    varname = frame.f_code.co_varnames[ n ]
	    try:
		varvalue = pprint.pformat( getrep( frame.f_locals[ varname ], follow_objects) ) 
	    except KeyError:
		varname = varvalue = None  # no value assigned to variable, no need to mention this variable ?
	       #line = '<no value assigned to variable>' 
	    except Exception as e:
		varvalue = '<error while formatting>'
	    if varname != None:		    
		ret += varname + ' = ' + varvalue  + "\n"  #   
	    n += 1
    else:
	ret += "\n"
    ret += "Calls next frame at:\n"

    linecache.checkcache(frame.f_code.co_filename)
    ret += "\t" + linecache.getline(frame.f_code.co_filename, frame.f_lineno, frame.f_globals).strip() + ' at: ' + frame.f_code.co_filename + ":" + str( frame.f_lineno )
    ret += '\n\n'
    return ret


def print_stack_ex( skipframes = 0, follow_objects = 0, file = None, frame = None):
    """ print stack trace from an arbitrary point in the program;
	the function is similar to traceback.print_stack , just with more detailed stack trace

	the stack trace includes function names, values of parameters and values of local variables. i find it easier to debug with this stack trace.
	
	parameters:
	skipframes - skip a number of frames if is not 0 (default 0)
	
	follow_objects - if not 0 then representation of object values is printed 
	Please note that follow_objects=1 can generate a lot of output, and can take a lot of time. (default 0)
	
	file -  print to file (default value None - print to standard error stream)
	
	frame - specify a start frame (default None - show from calling function; deepest frame on top marked with #1)

	this function is similar to traceback.print_stack , just with more detailed stack trace.

	works for python 2.7, should work for other versions as well

	example stack trace:

#1 def fact(n = 1) at test_pd.py:10
Local variables:
loc 2
loc2 [0]
Calls next frame at:
	pd.print_stack_ex() at: test_pd.py:10

#2 def fact(n = 2) at test_pd.py:8
Local variables:
loc 4
loc2 [0, 1]
Calls next frame at:
	return n * fact( n - 1 ) at: test_pd.py:8

#3 def fact(n = 3) at test_pd.py:8
Local variables:
loc 6
loc2 [0, 1, 2]
Calls next frame at:
	return n * fact( n - 1 ) at: test_pd.py:8

#4 def fact(n = 4) at test_pd.py:8
Local variables:
loc 8
loc2 [0, 1, 2, 3]
Calls next frame at:
	return n * fact( n - 1 ) at: test_pd.py:8

#5 def main() at test_pd.py:36
Local variables:
Calls next frame at:
	print fact(4) at: test_pd.py:36

#6 def <module>() at test_pd.py:53
Calls next frame at:
	main() at: test_pd.py:53


    """
    if file == None:
	file = sys.stderr
    if frame == None:
	try:
	    raise ZeroDivisionError
	except ZeroDivisionError:
	    frame = sys.exc_info()[2].tb_frame.f_back

    while skipframes != 0:
	frame = frame.f_back
	skipframes -= 1

    nframe = 1 
    while frame is not None:
	ret = format_frame( nframe, frame, follow_objects )
	file.write( ret )

	nframe += 1
        frame = frame.f_back


def print_exception_ex(follow_objects = 0, file = None):
    '''
	prints an exception with more detailed stack trace, is used as follows:
	the function is similar to traceback.print_exception , just with more detailed stack trace

import pd

try:
   <python code>
except BaseException: 		
    pd.print_exception_ex()
	
    
	parameters:
	
	follow_objects - if not 0 then representation of object values is printed 
	Please note that follow_objects=1 can generate a lot of output, and can take a lot of time. (default 0)
	
	file -  print to file (default value None - print to standard error stream)

	example stack trace:

Exception: got it

#1  def kuku2(self = {'a': 42, 'b': [1, 2, 3, 4]}, depth = 1) at test_pd.py:29
Calls next frame at:
	raise Exception('got it') at: test_pd.py:29

#2  def kuku2(self = {'a': 42, 'b': [1, 2, 3, 4]}, depth = 2) at test_pd.py:28
Calls next frame at:
	self.kuku2( depth - 1 ) at: test_pd.py:28

#3  def kuku2(self = {'a': 42, 'b': [1, 2, 3, 4]}, depth = 3) at test_pd.py:28
Calls next frame at:
	self.kuku2( depth - 1 ) at: test_pd.py:28

#4  def kuku2(self = {'a': 42, 'b': [1, 2, 3, 4]}, depth = 4) at test_pd.py:28
Calls next frame at:
	self.kuku2( depth - 1 ) at: test_pd.py:28

#5  def kuku2(self = {'a': 42, 'b': [1, 2, 3, 4]}, depth = 5) at test_pd.py:28
Calls next frame at:
	self.kuku2( depth - 1 ) at: test_pd.py:28

#6  def kuku2(self = {'a': 42, 'b': [1, 2, 3, 4]}, depth = 6) at test_pd.py:28
Calls next frame at:
	self.kuku2( depth - 1 ) at: test_pd.py:28

#7  def main() at test_pd.py:44
Local variables:
n = {'a': 42, 'b': [1, 2, 3, 4]}
Calls next frame at:
	pd.print_exception_ex( follow_objects = 1 ) at: test_pd.py:44

    '''
    if file == None:
	file = sys.stderr
    
    etype, value, tb = sys.exc_info()
    lines = traceback.format_exception_only(etype, value) 
    for l in lines:
	file.write( l + '\n' )

    frames = []
    while tb != None:
	ret = format_frame( -1,  tb.tb_frame, follow_objects )
	frames.append( ret )
	tb = tb.tb_next

    frames.reverse()
    nframe = 1
    for f in frames:
	file.write( '#' + str(nframe) + ' ' + f )
	nframe += 1

def die(*msg):
    """ receives a variable number of arguments; prints each argument (with pprint) to standard error stream, 
	shows a detailed stack trace (also to standard error, see print_stack_ex, does not follow objects (follow_objects = 0); 
	exit program with error (status 1)
    	this is similar to die built in function in perl
    """    
    for m in msg:
	sys.stderr.write( pprint.pformat( m ) + ' ' )
    sys.stderr.write( '\n\n' )

    print_stack_ex( 1 )
    
    sys.exit(1)

def die2(*msg):
    """ receives a variable number of arguments; prints each argument (with pprint) to standard error stream, 
	shows a detailed stack trace (also to standard error, see print_stack_ex, does follow objects (follow_objects = 1); 
	exit program with error (status 1)
    	this is similar to die built in function in perl
    """    
    for m in msg:
	sys.stderr.write( pprint.pformat( m ) + ' ' )
    sys.stderr.write( '\n\n' )

    print_stack_ex( skipframes = 1, follow_objects = 1 )
    
    sys.exit(1)


