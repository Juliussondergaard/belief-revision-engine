import itertools
import re


def to_cnf(expr):
    # to CNF form
    expr = expr.replace(' ', '')

    if '<->' in expr:
        a, b = expr.split('<->')
        return f"(~{a} | {b}) & (~{b} | {a})"
    elif '->' in expr:
        a, b = expr.split('->')
        return f"(~{a} | {b})"
    else:
        return expr


def parse_clause(clause):
    # Into literals
    return set(token.strip() for token in clause.strip('()').split('|'))


def negate(expr):
    # Negates to proposition
    if expr.startswith('~'):
        return expr[1:]
    else:
        return '~' + expr


def resolve(ci, cj):
    # Apply resolution
    resolvents = set()
    for di in ci:
        for dj in cj:
            if di == negate(dj):
                new_clause = (ci - {di}) | (cj - {dj})
                resolvents.add(frozenset(new_clause))
    return resolvents


def pl_resolution(kb, alpha):
    # Propositional logic resolution algorithm.
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
