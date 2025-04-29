# logic_utils.py

import itertools
import re


def to_cnf(expr):
    """
    Converts simple logical expressions into CNF.
    Supports implication (->) and biconditional (<->) transformations.
    Simplified handling.
    """
    expr = expr.replace(' ', '')  # Remove spaces
    expr = expr.replace('<->', '&(~')  # Handle biconditional loosely
    expr = expr.replace('->', '|(~')   # Handle implication loosely
    return expr  # Basic parsing (flat formulas)


def parse_clause(clause):
    """
    Parses a clause like '(~p | q)' into a set of literals: {'~p', 'q'}.
    """
    return set(token.strip() for token in clause.strip('()').split('|'))


def negate(expr):
    """
    Negates a proposition. If already negated, removes the negation.
    """
    if expr.startswith('~'):
        return expr[1:]
    else:
        return '~' + expr


def resolve(ci, cj):
    """
    Applies the resolution rule between two clauses.
    """
    resolvents = set()
    for di in ci:
        for dj in cj:
            if di == negate(dj):
                new_clause = (ci - {di}) | (cj - {dj})
                resolvents.add(frozenset(new_clause))
    return resolvents


def pl_resolution(kb, alpha):
    """
    Propositional Logic Resolution Algorithm.
    Returns True if alpha is entailed by the knowledge base (kb).
    """
    clauses = set()
    for formula in kb:
        cnf = to_cnf(formula)
        clauses.add(frozenset(parse_clause(cnf)))

    neg_alpha = to_cnf(negate(alpha))
    clauses.add(frozenset(parse_clause(neg_alpha)))

    new = set()
    while True:
        pairs = list(itertools.combinations(clauses, 2))
        for (ci, cj) in pairs:
            resolvents = resolve(ci, cj)
            if frozenset() in resolvents:
                return True
            new.update(resolvents)
        if new.issubset(clauses):
            return False
        clauses.update(new)
