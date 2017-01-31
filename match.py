"""
This file contains a 'match' routine for matching arrays of 
integers, and some functions to test it.
"""
import numpy as np
import sys

############################################################
def match(arr1,arr2,arr2_sorted=False):
    """
    Returns an array of len(arr1) holding the index in arr2
    matching each element of arr1. For elements of arr1 that 
    are not matched in arr2, elments in the returned array -1.
    
    Remember to check for these -1 elements when using the
    result.
    
    Neither arr1 nor arr2 have to be sorted first. Only arr2 
    is sorted in operation.
    
    If arr2 is already sorted, set arr2_sorted=True to speed
    up the routine.

    Example:
        midx    = match(a,b) # Match a in b
        matched = (m >= 0)   # Mask on matched elements 
        w       = np.where(matched)[0] # Select only matched
       
        assert(b[midx[w]] == a[w]) # True
        
    Credit:
        Originally based on Fortran code by John Helly.
    """
    if arr2_sorted:
        # arr2 is already sorted
        sortidx = slice(0,len(arr2))
        tmp2    = arr2
    else:
        # arr2 not sorted, so sort it
        sortidx  = np.argsort(arr2)
        tmp2     = arr2[sortidx]

    # Find where the elements of arr1 can be inserted in arr2
    idx_l = np.searchsorted(tmp2,arr1,side='left')
    idx_r = np.searchsorted(tmp2,arr1,side='right')

    # This handles the case where arr1 is a scalar rather than
    # an array.
    if np.isscalar(idx_l):
        idx_l = array([idx_l])
        idx_r = array([idx_r])

    # Return -1 where no match is found. Note that searchsorted returns
    # len(tmp2) for values beyond the maximum of tmp2. This cannot be 
    # used as an index.
    mask         = idx_r-idx_l == 0
    idx_l[mask]  = -1

    # We matched against the sorted array, but we want to return
    # the index in the unsorted array.
  
    if arr2_sorted:
        matched_index = idx_l
    else:
        # The original list of indices (0,1,2...) in the order of tmp2
        original_index = np.arange(len(arr2))[sortidx]
    
        # Fill in the values where idex_l is positive 
        matched_index = np.where(idx_l >= 0, original_index[idx_l], -1)

    return matched_index

############################################################
# TESTS
############################################################
def test_match_sorted_all_present():
    """
    """
    a = np.array([7,39,18,8,59,0,59,-20,-34,7])
    b = np.sort(a)
    
    right_answer = np.array([np.where(b == x)[0][0] for x in a])
    assert(np.all(b[right_answer] == a))
    
    m = match(a,b,arr2_sorted=True)
    assert(np.all(m >= 0))
    assert(np.all(m == right_answer))
    assert(np.all(b[m] == a))
  
    return True

############################################################
def test_match_unsorted_all_present():
    """
    """
    a = np.array([7,39,18,8,59,0,59,-20,-34,7])
    b = np.unique(a)
    np.random.shuffle(b)
    
    right_answer = np.array([np.where(b == x)[0][0] for x in a])
    assert(np.all(b[right_answer] == a))
    
    m = match(a,b)
    assert(np.all(m >= 0))
    assert(np.all(m == right_answer))
    assert(np.all(b[m] == a))
  
    return True

############################################################
def test_match_unsorted_not_all_present():
    """
    """
    a = np.array([7,39,18,8,59,0,59,-20,-34,7])
    b = np.unique(a)
    np.random.shuffle(b)
    
    a[4]  = 3000
    a[-1] = 2000
    
    right_answer = list()
    for x in a:
        w = np.where(b == x)[0]
        if len(w) > 0:
            right_answer.append(w[0])
        else:
            right_answer.append(-1)
    right_answer = np.array(right_answer)
    
    w = np.where(right_answer >= 0)[0]
    assert(np.all(b[right_answer[w]] == a[w]))
    
    m = match(a,b)
    assert(m[4]  == -1)
    assert(m[-1] == -1)
    assert(np.all(m == right_answer))
    
    w = np.where(m >= 0)[0]
    assert(np.all(b[m[w]] == a[m >=0]))
  
    return True


############################################################
# PERFORMANCE TESTS
############################################################
def test_huge_unsorted(na,nb):
    import time
    import random # python's random, not numpy.random
    
    b    = np.array(random.sample(xrange(0,10*nb),nb))
    c    = random.sample(xrange(0,nb),na)
    a    = b[c]
    
    t0_m = time.time()
    m    = match(a,b)
    t1_m = time.time()
    
    return t1_m-t0_m
    
############################################################
if __name__ == '__main__':
    # Run one of the tests using two integer arguments
    na,nb = int(sys.argv[1]), int(sys.argv[2])
    t = test_huge_unsorted(na,nb)
    print('Matching {} integers against {} integers took {:f}s'.format(na,nb,t))


    
    
   