from logic_utils import pl_resolution, negate
import itertools


class BeliefBase:
    def __init__(self, initial_beliefs=None):
        # Initializes the belief base with an optional list of (formula, priority) tuples.
        # Higher priority values indicate stronger beliefs.
        if initial_beliefs is None:
            self.beliefs = []  # List of (formula, priority) tuples
        else:
            self.beliefs = [(belief, 1) for belief in initial_beliefs]  # Default priority 1
    
    def __str__(self):
        return f"BeliefBase({self.beliefs})"

    def expand(self, formula, priority=1):
        if not any(belief[0] == formula for belief in self.beliefs):
            self.beliefs.append((formula, priority))

    def entails(self, formula):
        # Checks if the formula logically follows from the current belief base.
        formulas = [belief[0] for belief in self.beliefs]
        return pl_resolution(formulas, formula)

    def contract(self, formula):
        # Removes formulas from the belief base using partial meet contraction.
        if not self.entails(formula):
            return  # Already not entailed

        # 1. Find minimal subsets that, when removed, make the belief base not entail the formula
        inconsistent_subsets = self._find_inconsistent_subsets(formula)

        if not inconsistent_subsets:
            self.beliefs = []
            return

        # 2. Apply a selection function (here: select the subsets with highest total priority)
        selected_subsets = self._selection_function(inconsistent_subsets)

        # 3. Intersect the selected subsets (formulas that appear in all selected subsets are kept)

        if selected_subsets:
            # Flatten the selected subsets into a single list of beliefs to remove
            beliefs_to_remove = set(itertools.chain.from_iterable(selected_subsets))

            # Remove the beliefs from the belief base
            self.beliefs = [belief for belief in self.beliefs if belief[0] not in beliefs_to_remove]
        else:
            self.beliefs = []

    def _find_inconsistent_subsets(self, formula):
        # Finds all minimal subsets of beliefs that, when removed, make the belief base not entail the formula.
        inconsistent_subsets = []
        for i in range(1 << len(self.beliefs)):  # Iterate through all possible subsets
            subset = [self.beliefs[j] for j in range(len(self.beliefs)) if (i >> j) & 1]
            remaining_beliefs = [belief[0] for belief in self.beliefs if belief not in subset]
            if not pl_resolution(remaining_beliefs, formula):
                inconsistent_subsets.append(set(belief[0] for belief in subset))

        # Ensure minimality (no subset contains another)
        minimal_subsets = []
        for subset in inconsistent_subsets:
            is_minimal = True
            for other_subset in inconsistent_subsets:
                if subset != other_subset and subset.issuperset(other_subset):
                    is_minimal = False
                    break
            if is_minimal:
                minimal_subsets.append(subset)
        return minimal_subsets

    def _selection_function(self, subsets):
        # Selects the subsets with the highest total priority.
        if not subsets:
            return []

        # Calculate the total priority of each subset
        subset_priorities = {}
        for subset in subsets:
            total_priority = sum(belief[1] for belief in self.beliefs if belief[0] in subset)
            subset_priorities[frozenset(subset)] = total_priority

        # Find the maximum priority
        max_priority = max(subset_priorities.values())

        # Select the subsets with the maximum priority
        selected_subsets = [set(subset) for subset, priority in subset_priorities.items() if priority == max_priority]
        return selected_subsets

    def revise(self, formula, priority=1):
        # Revises the belief base with a new formula.
        # Implements: contract(¬φ) followed by expand(φ)
        neg_formula = negate(formula)
        self.contract(neg_formula)
        self.expand(formula, priority)
