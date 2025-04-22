from belief_base import BeliefBase


def test_success_postulate():
    print("🔹 Testing SUCCESS postulate...")
    bb = BeliefBase(['p'])
    bb.revise('q')
    return 'q' in bb.beliefs


def test_inclusion_postulate():
    print("🔹 Testing INCLUSION postulate...")
    bb = BeliefBase(['p', 'p -> q'])
    before = set(bb.beliefs)
    bb.revise('q')
    after = set(bb.beliefs)
    return before.issubset(after)


def test_vacuity_postulate():
    print("🔹 Testing VACUITY postulate...")
    bb = BeliefBase(['p'])
    bb.revise('p')  # revising with something that is already believed
    return 'p' in bb.beliefs and bb.beliefs.count('p') == 1


def run_all_tests():
    print("===== AGM Postulates Tests =====")
    print("Success Postulate:", "✅ Pass" if test_success_postulate() else "❌ Fail")
    print("Inclusion Postulate:",
          "✅ Pass" if test_inclusion_postulate() else "❌ Fail")
    print("Vacuity Postulate:", "✅ Pass" if test_vacuity_postulate() else "❌ Fail")


if __name__ == '__main__':
    run_all_tests()
