import numpy as np # Import python numpy bindings
cimport numpy as np # Import cpython numpy bindings

MATCH_SCORE = 1
MISMATCH_SCORE = 0
DELETION_SCORE = 0
INSERTION_SCORE = 0

def align(left, right):

    # Precompute lengths as ints
    cdef unsigned int len_left, len_right
    len_left = len(left)
    len_right = len(right)

    # Define matrix to be appropriate 2-dimensional array
    cdef np.ndarray[np.float_t, ndim=2] matrix
    matrix = np.empty((len_left+1, len_right+1))
    # Initialise
    matrix[0, 0] = 0
    traceback = {}

    # Define iterators as ints so loops run in native C
    cdef unsigned int i, j


    for i in xrange(len_left):
        # This should be using optimised lookups for numpy matrix as all indices ints
        matrix[i+1, 0] = (i+1) * DELETION_SCORE
        traceback[i+1, 0] = i, 0

    for i in xrange(len_right):
        matrix[0, i+1] = (i+1) * INSERTION_SCORE
        traceback[0, i+1] = 0, i

    # Define the variables as doubles
    cdef double max_score, match_score, deletion, insertion

    for i, symbol_left in enumerate(left):
        for j, symbol_right in enumerate(right):
            # Matrix lookups below should be optimised
            match_score = matrix[i, j] + MATCH_SCORE if symbol_left == symbol_right else MISMATCH_SCORE
            deletion = matrix[i, j+1] + DELETION_SCORE
            insertion = matrix[i+1, j] + INSERTION_SCORE

            if match_score >= deletion and match_score >= insertion:
                max_score = match_score
                traceback_pos = i, j
            elif deletion > match_score and deletion >= insertion:
                max_score = deletion
                traceback_pos = i, j+1
            else:
                max_score = insertion
                traceback_pos = i+1, j

            matrix[i+1, j+1] = max_score
            traceback[i+1, j+1] = traceback_pos

    return matrix[len(left), len(right)], traceback
