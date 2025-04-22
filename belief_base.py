from logic_utils import pl_resolution, negate


class BeliefBase:
    def __init__(self, initial_beliefs=None):
        """
        Initializes the belief base with an optional list of formulas.
        """
        if initial_beliefs is None:
            self.beliefs = []
        else:
            self.beliefs = initial_beliefs.copy()

    def expand(self, formula):
        if formula not in self.beliefs:
            self.beliefs.append(formula)

    def entails(self, formula):
        """
        Checks if the formula logically follows from the current belief base.
        """
        return pl_resolution(self.beliefs, formula)

    def contract(self, formula):
        """
        Removes formulas from the belief base so that the formula no longer follows.
        Tries minimal removal (greedy approach).
        """
        if not self.entails(formula):
            return  # Already not entailed

        # Try removing each belief one by one until formula is no longer entailed
        for i in range(len(self.beliefs)):
            new_base = self.beliefs[:i] + self.beliefs[i+1:]
            if not pl_resolution(new_base, formula):
                self.beliefs = new_base
                return

        # If nothing helped, remove everything (last resort)
        self.beliefs = []

    def __str__(self):
        return f"BeliefBase({self.beliefs})"

    def revise(self, formula):
        """
        Revises the belief base with a new formula.
        Implements: contract(¬φ) followed by expand(φ)
        """
        neg_formula = negate(formula)
        self.contract(neg_formula)
        self.expand(formula)
