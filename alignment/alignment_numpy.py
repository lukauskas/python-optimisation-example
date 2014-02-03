import numpy as np

MATCH_SCORE = 1
MISMATCH_SCORE = 0
DELETION_SCORE = 0
INSERTION_SCORE = 0

def align(left, right):

    matrix = np.empty((len(left)+1, len(right)+1), dtype=int)

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

def construct_alignment(left, right, traceback):
    sequence_l = []
    sequence_r = []

    # Initialise at last column
    l, r = len(left), len(right)

    # While we're not at the border
    while l > 0 or r > 0:
        new_l, new_r = traceback[l, r]

        if new_l == l:  # insertion
            sequence_l.append('-')
            sequence_r.append(right[r-1])
        elif new_r == r:  # deletion
            sequence_l.append(left[l-1])
            sequence_r.append('-')
        else:   # match
            sequence_l.append(left[l-1])
            sequence_r.append(right[r-1])

        l, r = new_l, new_r

    return reversed(sequence_l), reversed(sequence_r)


def main(left, right):
    score, traceback = align(left, right)
    print 'Score: {0}'.format(score)

    sequence_l, sequence_r = construct_alignment(left, right, traceback)
    sequence_l = ''.join(sequence_l)
    sequence_r = ''.join(sequence_r)


    print 'Alignment:'

    while len(sequence_l) > 0:
        head_l, head_r = sequence_l[:60], sequence_r[:60]
        sequence_l, sequence_r = sequence_l[60:], sequence_r[60:]

        print head_l
        print head_r
        print

if __name__ == '__main__':
    from sequences import P53_MOUSE, P53_HUMAN
    main(P53_HUMAN, P53_MOUSE)



