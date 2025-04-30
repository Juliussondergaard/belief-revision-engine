# belief_base.py

from logic_utils import pl_resolution, negate
import itertools
import random


class BeliefBase:
    """
    A class representing a belief base with expansion, contraction, revision, and entailment operations.
    Beliefs are stored as (formula, priority) tuples.
    """

    def __init__(self, initial_beliefs=None):
        """
        Initializes the belief base with an optional list of formulas.
        Beliefs are given default priority 1.
        """
        if initial_beliefs is None:
            self.beliefs = []
        else:
            self.beliefs = [(belief, 1) for belief in initial_beliefs]

    def __str__(self):
        return f"BeliefBase({self.beliefs})"

    def expand(self, formula, priority=1):
        """
        Expands the belief base with a new formula and optional priority.
        """
        if not isinstance(formula, str):
            raise ValueError(f"Invalid formula: {formula}")

        formula = formula.strip()  # <--- this line trims spaces at the beginning and end

        if not any(belief[0] == formula for belief in self.beliefs):
            self.beliefs.append((formula, priority))

    def entails(self, formula):
        """
        Checks if the formula logically follows from the current belief base.
        """
        formulas = [belief[0] for belief in self.beliefs]
        return pl_resolution(formulas, formula)

    def contract(self, formula):
        """
        Contracts the belief base using partial meet contraction with priority-based selection.
        Returns the revised belief base.
        """
        if not self.entails(formula):
            return self

        # Find all minimal subsets that need to be removed
        inconsistent_subsets = self._find_inconsistent_subsets(formula)

        if not inconsistent_subsets:
            self.beliefs = []
            return self

        # Select subset based on priorities
        selected_subsets = self._selection_function(inconsistent_subsets)

        if selected_subsets:
            beliefs_to_remove = set(itertools.chain.from_iterable(selected_subsets))
            self.beliefs = [
                belief for belief in self.beliefs if belief[0] not in beliefs_to_remove
            ]
        
        return self

    def revise(self, formula, priority=1):
        """
        Revises the belief base by contracting ¬formula and expanding formula.
        """
        neg_formula = negate(formula)
        self.contract(neg_formula)
        self.expand(formula, priority)

    def is_consistent(self):
        """
        Checks if the belief base is logically consistent (no contradictions).
        """
        formulas = [belief[0] for belief in self.beliefs]
        return not pl_resolution(formulas, 'False')

    def _find_inconsistent_subsets(self, formula):
        """
        Finds minimal subsets of beliefs which, when removed, break entailment of the formula.
        """
        inconsistent_subsets = []
        for i in range(1 << len(self.beliefs)):
            subset = [self.beliefs[j]
                      for j in range(len(self.beliefs)) if (i >> j) & 1]
            remaining_beliefs = [belief[0]
                                 for belief in self.beliefs if belief not in subset]
            if not pl_resolution(remaining_beliefs, formula):
                inconsistent_subsets.append(
                    set(belief[0] for belief in subset))

        # Keep only minimal subsets
        minimal_subsets = []
        for subset in inconsistent_subsets:
            is_minimal = True
            for other in inconsistent_subsets:
                if subset != other and subset.issuperset(other):
                    is_minimal = False
                    break
            if is_minimal:
                minimal_subsets.append(subset)

        return minimal_subsets

    def _selection_function(self, subsets):
        """
        Selects subsets to remove based on minimal priority impact.
        Returns the subset(s) whose removal would result in minimal priority loss.
        """
        if not subsets:
            return []

        # Calculate priority impact for each subset
        subset_priorities = {}
        for subset in subsets:
            # Sum the priorities of beliefs in this subset
            total_priority = sum(
                belief[1] for belief in self.beliefs 
                if belief[0] in subset
            )
            subset_priorities[frozenset(subset)] = total_priority

        # Find subset(s) with minimum total priority
        min_priority = min(subset_priorities.values())
        best_subsets = [
            set(subset) for subset, priority in subset_priorities.items()
            if priority == min_priority
        ]

        # If multiple subsets have the same priority, choose one randomly
        selected_subset = random.choice(best_subsets)
        return [selected_subset]
