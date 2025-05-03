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


def test_priority_handling():
    bb = BeliefBase()
    
    # Add beliefs with different priorities
    bb.expand('p', priority=3)
    bb.expand('q', priority=1)
    bb.expand('p -> q', priority=2)
    
    # Contract 'q' - should remove 'q' (priority 1) instead of 'p' (priority 3)
    bb.contract('q')
    
    # Check that high-priority belief remains
    assert bb.entails('p')
    print("Priority handling test passed")


def main():
    demonstrate_belief_operations()
    test_priority_handling()


if __name__ == '__main__':
    main()
