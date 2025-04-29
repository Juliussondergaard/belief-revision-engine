# Belief Revision Engine

This project implements a belief revision engine based on the AGM postulates for belief revision in propositional logic.

## Features

- Belief Base implementation with priority-based beliefs
- Propositional Logic Resolution for entailment checking
- AGM-compliant belief operations:
  - Expansion
  - Contraction
  - Revision
- Implementation of core AGM postulates:
  - Success
  - Inclusion
  - Vacuity
  - Consistency
  - Extensionality

## Project Structure

- `belief_base.py`: Core belief revision implementation
- `logic_utils.py`: Propositional logic utilities
- `tests.py`: AGM postulates testing
- `main.py`: Example usage

## Usage

To run the tests:
```bash
python tests.py
```

To run the example:
```bash
python main.py
```

## Example

```python
from belief_base import BeliefBase

# Create a belief base
bb = BeliefBase(['p', 'p -> q'])

# Check entailment
print(bb.entails('q'))  # True

# Revise beliefs
bb.revise('~p')
print(bb.beliefs)  # Shows updated beliefs
```


