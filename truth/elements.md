# Ground truth elements

Fill this in BY HAND from design.md, before loading any prompt variant and before
running any model. This file is the yardstick. If a model builds it, and models from
the same family are scored against it, their omissions correlate and the experiment
measures nothing.

Read design.md once, slowly. List every element you can defend as being present in the
document. Where an element is only implied or mentioned in passing, say so in the notes
column: those are the ones the experiment is really about.

## External entities

| ID | Element | Where it appears in design.md | Stated plainly or buried? |
|----|---------|-------------------------------|---------------------------|
| E1 |         |                               |                           |

## Processes

| ID | Element | Where it appears in design.md | Stated plainly or buried? |
|----|---------|-------------------------------|---------------------------|
| P1 |         |                               |                           |

## Data stores

| ID | Element | Where it appears in design.md | Stated plainly or buried? |
|----|---------|-------------------------------|---------------------------|
| D1 |         |                               |                           |

## Data flows

| ID | From | To | Crosses a trust boundary? | Stated plainly or buried? |
|----|------|----|---------------------------|---------------------------|
| F1 |      |    |                           |                           |

## Trust boundaries

| ID | Boundary | Where it appears in design.md |
|----|----------|-------------------------------|
| B1 |          |                               |

## Notes

Anything ambiguous. If you cannot decide whether something is an element, record the
ambiguity here rather than resolving it silently. A contested element is not a fair
thing to score a model against.
