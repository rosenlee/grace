

def QuickSort(source):
    if (len(source) > 1):
        partpos = Partion(source)
	parta = source[0:partpos-1]
	partb = source[partpos:]
	print parta
	print partb
	print "source[partpos-1]:", source[partpos-1]
	sortedparta = QuickSort(parta)
	print "sorted:", sortedparta
	sortedpartb = QuickSort(partb)
	print "sortedb:", sortedpartb

	sortedparta.append(source[partpos-1])
	return sortedparta+sortedpartb
    else:
        return  source


def Partion(source):
    i = 0
    j = len(source)-1

    p = source[0]
    while( i <= j):
        while(source[i] <= p):
	     i += 1
	    
	while(source[j] > p ):
	     j -= 1
	#print  i, j
	source[i],source[j] = swap(source[i],source[j])


    print  "outwhile:", i, j
    print source
    #get the position i == j
    source[i],source[j] = swap(source[i],source[j])
    source[0],source[j] = swap(source[0],source[j])

    pos =  min(i,j)
    print j
    return j+1

def swap(a, b):
    tmp = a
    a = b
    b = tmp
    return a,b
 
    
if __name__ == "__main__":
     source=[5,3,1,9,8,2,4,7]
     print QuickSort(source) 



