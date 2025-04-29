from belief_base import BeliefBase


def test_success_postulate():
    # Testing SUCCESS postulate...
    print("🔹 Testing SUCCESS postulate...")
    bb = BeliefBase(['p'])
    bb.revise('q')
    return 'q' in [belief[0] for belief in bb.beliefs]


def test_inclusion_postulate():
    # Testing INCLUSION postulate...
    print("🔹 Testing INCLUSION postulate...")
    bb = BeliefBase(['p', 'p -> q'])
    before = set([belief[0] for belief in bb.beliefs])
    bb.revise('q')
    after = set([belief[0] for belief in bb.beliefs])
    return before.issubset(after)


def test_vacuity_postulate():
    # Testing VACUITY postulate...
    print("🔹 Testing VACUITY postulate...")
    bb = BeliefBase(['p'])
    bb.revise('p')  # revising with something that is already believed
    beliefs = [belief[0] for belief in bb.beliefs if belief[0] == 'p']
    return 'p' in beliefs and beliefs.count('p') == 1


def test_consistency_postulate():
    # Testing CONSISTENCY postulate...
    print("🔹 Testing CONSISTENCY postulate...")
    bb = BeliefBase(['p', '~p'])
    bb.revise('q')
    # After revision, the belief base should be consistent
    return not bb.entails('False')  # Assuming 'False' represents contradiction


def test_extensionality_postulate():
    # Testing EXTENSIONALITY postulate...
    print("🔹 Testing EXTENSIONALITY postulate...")
    # If two belief bases have the same logical consequences, revising them with logically equivalent formulas
    # should result in belief bases with the same logical consequences.
    bb1 = BeliefBase(['p'])
    bb2 = BeliefBase(['p'])
    bb1.revise('q -> r')
    bb2.revise('~q | r')  # Logically equivalent to q -> r
    # Check if the resulting belief bases have the same logical consequences (simplified check)
    return bb1.entails('r') == bb2.entails('r')


def run_all_tests():
    print("===== AGM Postulates Tests =====")
    print("Success Postulate:", "Pass" if test_success_postulate() else "Fail")
    print("Inclusion Postulate:",
          "Pass" if test_inclusion_postulate() else "Fail")
    print("Vacuity Postulate:", "Pass" if test_vacuity_postulate() else "Fail")
    print("Consistency Postulate:", "Pass" if test_consistency_postulate() else "Fail")
    print("Extensionality Postulate:", "Pass" if test_extensionality_postulate() else "Fail")


if __name__ == '__main__':
    run_all_tests()
