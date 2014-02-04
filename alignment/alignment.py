from align import align

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



