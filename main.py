from belief_base import BeliefBase


def main():
    # Create initial belief base
    bb = BeliefBase(['p', 'p -> q'])

    print("Initial belief base:", bb)

    # Check if q follows
    print("Does it entail 'q'?", bb.entails('q'))

    # Contract 'q' (remove beliefs so that q no longer follows)
    bb.contract('q')
    print("Belief base after contracting 'q':", bb)

    # Expand with a new belief
    bb.expand('r')
    print("Belief base after expanding with 'r':", bb)


if __name__ == '__main__':
    main()
