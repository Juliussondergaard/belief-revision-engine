# test_belief_base.py

from belief_base import BeliefBase


def test_success_postulate():
    """
    Success Postulate: After revising with φ, φ should be in the belief base.
    """
    print("🔹 Testing SUCCESS postulate...")
    bb = BeliefBase(['p'])
    bb.revise('q')
    return 'q' in [belief[0] for belief in bb.beliefs]


def test_inclusion_postulate():
    """
    Inclusion Postulate: After revision, the new belief base should include the original base (except for inconsistencies).
    """
    print("🔹 Testing INCLUSION postulate...")
    bb = BeliefBase(['p', 'p -> q'])
    before = set([belief[0] for belief in bb.beliefs])
    bb.revise('q')
    after = set([belief[0] for belief in bb.beliefs])
    return before.issubset(after)


def test_vacuity_postulate():
    """
    Vacuity Postulate: If the formula is not in conflict, revision acts like expansion.
    """
    print("🔹 Testing VACUITY postulate...")
    bb = BeliefBase(['p'])
    bb.revise('p')
    beliefs = [belief[0] for belief in bb.beliefs if belief[0] == 'p']
    return 'p' in beliefs and beliefs.count('p') == 1


def test_consistency_postulate():
    """
    Consistency Postulate: If the formula is consistent, revision results in a consistent belief base.
    """
    print("🔹 Testing CONSISTENCY postulate...")
    bb = BeliefBase(['p', '~p'])
    bb.revise('q')
    return bb.is_consistent()


def test_extensionality_postulate():
    """
    Extensionality Postulate: If φ and ψ are logically equivalent, then revising with φ or ψ should give the same results.
    """
    print("🔹 Testing EXTENSIONALITY postulate...")
    bb1 = BeliefBase(['p'])
    bb2 = BeliefBase(['p'])
    bb1.revise('q -> r')
    bb2.revise('~q | r')
    # Check that belief bases have same consequences after logically equivalent revision
    return bb1.entails('r') == bb2.entails('r') and bb2.entails('r') == bb1.entails('r')


def run_all_tests():
    """
    Runs all AGM postulate tests and prints results.
    """
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
