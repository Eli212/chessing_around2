import pd
import sys

def fact(n):
    loc = n * 2
    loc2 = range(0, n)
    if n > 1:
	return n * fact( n - 1 )
    #pd.die('here',24,[1,2,3])	   
    pd.print_stack_ex()
    return 1


# -------------------------

class Node:
	def __init__(self):
		self.a = 42
		self.b = [ 1, 2, 3, 4]
	def kuku(self,depth):
		if depth > 1:
			return 1 + self.kuku(depth - 1)
		pd.print_stack_ex( follow_objects = 1 )
		return 4

	def kuku2(self,depth):
	    if depth > 1:
		self.kuku2( depth - 1 )
	    raise Exception('got it')		

# -------------------------



def main():
	print fact(4)
	sys.stderr.write( "-----------\n" )
	n = Node()
	n.kuku(4)
	sys.stderr.write( "ex-----------\n" )
	try:
	    n.kuku2(6)
	except BaseException: 		
	    pd.print_exception_ex( follow_objects = 1 )
	    #pd.print_stack_ex( follow_objects = 1, frame = sys.exc_info()[2].tb_frame.f_back )
	sys.stderr.write( "-----------\n" )
	m =  [1, 2, 3 ]
	m.append(m);
	pd.print_stack_ex( follow_objects = 1 )


if __name__ == "__main__":
	main()

