from belief_base import BeliefBase


def demonstrate_belief_operations():
    print("\n=== Belief base ===")

    # Create initial belief base
    print("\n1. Creating initial belief base with 'p' and 'p -> q'")
    bb = BeliefBase(['p', 'p -> q'])
    print("Initial beliefs:", bb.beliefs)

    # Test
    print("\n2. Testing entailment")
    print("Does it entail 'q'?", bb.entails('q'))
    print("Does it entail 'r'?", bb.entails('r'))

    # Demonstrate expansion
    print("\n3. Expanding with 'r'")
    bb.expand('r', priority=2)
    print("After expansion:", bb.beliefs)

    # Demonstrate contraction
    print("\n4. Contracting 'q'")
    bb.contract('q')
    print("After contraction:", bb.beliefs)

    # Demonstrate revision
    print("\n5. Revising with '~p'")
    bb.revise('~p')
    print("After revision:", bb.beliefs)


def main():
    demonstrate_belief_operations()


if __name__ == '__main__':
    main()
