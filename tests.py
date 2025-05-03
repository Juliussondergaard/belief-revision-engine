from belief_base import BeliefBase


def test_success_postulate():
    # Success Postulate: After revising with φ, φ should be in the belief base.
    print("Testing SUCCESS postulate...")
    bb = BeliefBase(['p'])
    bb.revise('q')
    return 'q' in [belief[0] for belief in bb.beliefs]


def test_inclusion_postulate():
    # Testing INCLUSION postulate...
    print("Testing INCLUSION postulate...")

    # Original belief base
    bb = BeliefBase(['p', 'p -> q'])

    # Expanded base (B + q)
    bb_expanded = BeliefBase(['p', 'p -> q'])  # Clone of original
    bb_expanded.expand('q')
    expanded = set([belief[0] for belief in bb_expanded.beliefs])

    # Revised base (B * q)
    bb.revise('q')
    revised = set([belief[0] for belief in bb.beliefs])

    # Inclusion postulate: B * q ⊆ B + q
    return revised.issubset(expanded)


def test_vacuity_postulate():
    # Testing VACUITY postulate...
    print("Testing VACUITY postulate...")

    # Belief base that does not entail ~q
    bb1 = BeliefBase(['p'])  # Does not contradict q
    bb2 = BeliefBase(['p'])  # Clone for expansion

    bb1.revise('q')  # Revision: B * q
    bb2.expand('q')  # Expansion: B + q

    revised = set([belief[0] for belief in bb1.beliefs])
    expanded = set([belief[0] for belief in bb2.beliefs])

    # Should be equal if ~q was not implied by B
    return revised == expanded


def test_consistency_postulate():
    print("Testing CONSISTENCY postulate...")
    bb = BeliefBase(['p', '~p'])
    bb.revise('q')
    return bb.is_consistent()


def test_extensionality_postulate():
    print("Testing EXTENSIONALITY postulate...")
    bb1 = BeliefBase(['p'])
    bb2 = BeliefBase(['p'])
    bb1.revise('q -> r')
    bb2.revise('~q | r')
    # Check that belief bases have same consequences after logically equivalent revision
    return bb1.entails('r') == bb2.entails('r') and bb2.entails('r') == bb1.entails('r')


def run_all_tests():
    print("\n===== AGM Postulates Tests =====")
    print("Success Postulate:", "✅ Pass" if test_success_postulate() else "❌ Fail")
    print("Inclusion Postulate:",
          "✅ Pass" if test_inclusion_postulate() else "❌ Fail")
    print("Vacuity Postulate:", "✅ Pass" if test_vacuity_postulate() else "❌ Fail")
    print("Consistency Postulate:",
          "✅ Pass" if test_consistency_postulate() else "❌ Fail")
    print("Extensionality Postulate:",
          "✅ Pass" if test_extensionality_postulate() else "❌ Fail")


if __name__ == '__main__':
    run_all_tests()
