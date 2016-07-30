
source = [8,3,2,9,7,1,5,4,6]

def MergeSort(lst):
    if(len(lst) > 1):
    	halfa = lst[0:len(lst)/2]
	halfb = lst[len(lst)/2:]
#	print halfa, halfb
	halfa = MergeSort(halfa)
#	print halfa
	halfb = MergeSort(halfb)
#	print halfb
	return  Merge(halfa, halfb)
    else:
        return  lst




def Merge(srca, srcb):
#    print "srca:", srca
    dest = []
    i, j = 0,0
#    while(i+j < (len(srca)+len(srcb)-1)):
    while(i < len(srca) and j < len(srcb)):
    	if(srca[i] < srcb[j]):
	     dest.append( srca[i])
	     i += 1
	else:
	     dest.append( srcb[j])
	     j += 1

#        print i,j, (len(srca)+len(srcb)-1) 
    while(i < len(srca) ):
	dest.append( srca[i])
	i += 1

    while(j < len(srcb) ):
	dest.append( srcb[j])
	j += 1
    print "merge:", dest
    return  dest

   


if __name__ == "__main__":
    print source
    print MergeSort(source)


