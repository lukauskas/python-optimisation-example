MATCH_SCORE = 1
MISMATCH_SCORE = 0
DELETION_SCORE = 0
INSERTION_SCORE = 0

def align(left, right):

    matrix = {}

    # Initialise
    matrix[-1, -1] = 0
    traceback = {}
    for i in xrange(len(left)):
        matrix[i, -1] = (i+1) * DELETION_SCORE
        traceback[i, -1] = i-1, -1

    for i in xrange(len(right)):
        matrix[-1, i] = (i+1) * INSERTION_SCORE
        traceback[-1, i] = -1, i-1



    for i, symbol_left in enumerate(left):
        for j, symbol_right in enumerate(right):
            match_score = matrix[i-1, j-1] + MATCH_SCORE if symbol_left == symbol_right else MISMATCH_SCORE
            deletion = matrix[i-1, j] + DELETION_SCORE
            insertion = matrix[i, j-1] + INSERTION_SCORE
            matrix[i, j], traceback[i, j] = max((match_score, (i-1, j-1)),
                                                (deletion, (i-1, j)),
                                                (insertion, (i, j-1)),
                                                key=lambda x: x[0])

    return matrix[len(left)-1, len(right)-1], traceback

def construct_alignment(left, right, traceback):
    sequence_l = []
    sequence_r = []

    # Initialise at last column
    l, r = len(left)-1, len(right)-1

    # While we're not at the border
    while l > -1 or r > -1:
        new_l, new_r = traceback[l, r]

        if new_l == l:  # insertion
            sequence_l.append('-')
            sequence_r.append(right[r])
        elif new_r == r:  # deletion
            sequence_l.append(left[l])
            sequence_r.append('-')
        else:   # match
            sequence_l.append(left[l])
            sequence_r.append(right[r])

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



