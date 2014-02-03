MATCH_SCORE = 1
MISMATCH_SCORE = 0
DELETION_SCORE = 0
INSERTION_SCORE = 0

def align(left, right):

    matrix = {}

    # Initialise
    matrix[0, 0] = 0
    traceback = {}
    for i in xrange(len(left)):
        matrix[i+1, 0] = (i+1) * DELETION_SCORE
        traceback[i+1, 0] = i, 0

    for i in xrange(len(right)):
        matrix[0, i+1] = (i+1) * INSERTION_SCORE
        traceback[0, i+1] = 0, i



    for i, symbol_left in enumerate(left):
        for j, symbol_right in enumerate(right):
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
