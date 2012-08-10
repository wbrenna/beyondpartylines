import numpy as N
import pylab as P
import math


#The following two definitions are helpfully from the Matplotlib Cookbook
#www.scipy.org/Cookbook/Matplotlib/HintonDiagrams. I've modified them here.
def _blob(x,y,area,colour):
	"""
	Draws a square-shaped blob with the given area (< 1) at
	the given coordinates.
	"""
	hs = N.sqrt(area) / 2
	xcorners = N.array([x - hs, x + hs, x + hs, x - hs])
	ycorners = N.array([y - hs, y - hs, y + hs, y + hs])
	P.fill(xcorners, ycorners, colour, edgecolor=colour)

def hinton(W, length, maxWeight=None):
	"""
	Draws a Hinton diagram for visualizing a weight matrix. 
	Temporarily disables matplotlib interactive mode if it is on, 
	otherwise this takes forever.
	"""
	reenable = False
	if P.isinteractive():
		P.ioff()
	P.clf()
	height, width = W.shape
	if not maxWeight:
		#maxWeight = 2**N.ceil(N.log(N.max(N.abs(W)))/N.log(2))
		maxWeight = N.max(N.abs(W))*1.2

	P.fill(N.array([0,width,width,0]),N.array([0,0,height,height]),'gray')
	P.axis('off')
	P.axis('equal')
	correlationcounter = 0
	for x in xrange(width):
		for y in xrange(height):
			_x = x+1
			_y = y+1
			w = W[y,x]
			if w > 0:
				_blob(_x - 0.5, height - _y + 0.5, min(1,w/maxWeight*w/maxWeight),'white')
				correlationcounter += w - 0.5
			elif w < 0:
				_blob(_x - 0.5, height - _y + 0.5, min(1,w/maxWeight*w/maxWeight),'black')
				correlationcounter += w + 0.5

		
	
	correlationindex = abs(correlationcounter/length*100 + 50)
	titlestring = str(correlationindex) + '% agreement' 

	P.title(titlestring)
	if reenable:
		P.ion()
	P.show()


def splitarr(seq, num):
	avg = int(num)
	length = len(seq)
	out = []
	last = 0

	while last <= length-avg:
		out.append(seq[int(last):int(last + avg)])
		last += avg

	tmp = []
	limit = last + avg
	if last < avg*avg:
		while last < limit:
			if last < length:
				tmp.append(seq[int(last)])
			else:
				tmp.append(0)
			last += 1
		out.append(tmp)
		while last < avg*avg:
			out.append([0]*avg)
			last += avg

	return out

def squareandhinton(correlationlist):
	lengthint = math.ceil(math.sqrt(len(correlationlist)))
	
	array = P.array(splitarr(correlationlist,lengthint))
	hinton(array,len(correlationlist))


