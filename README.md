# Workshop Continuo

## Gym membership quote

Run the command-line application with Python:

```text
python gym_quote.py --plan PREMIUM --members 2 --extra SPA --extra GROUP_CLASSES
```

The `--plan` and `--members` arguments are required. Use `--extra` once for
each selected extra; omit it when there are no extras. Plan and extra names
are case-insensitive. Invalid plans, unknown extras, premium-only extras used
with another plan, duplicate extras, and member counts below one are rejected.

### Prices

| Plan or extra | Monthly price per member | Premium plan required |
| --- | ---: | :---: |
| BASIC | 30 | No |
| STANDARD | 45 | No |
| PREMIUM | 70 | No |
| GROUP_CLASSES | 15 | No |
| PERSONAL_TRAINING | 25 | No |
| SPA | 30 | Yes |
| SPECIALIZED_PROGRAM | 40 | Yes |

The quote is calculated as `(plan price + selected extra prices) × members`.

### Assumptions

- The source requirements do not specify a currency; displayed prices and
  totals are therefore currency-neutral amounts.
- Each extra can be selected at most once per quote.
- Plan and extra identifiers use underscores where the source table splits
  their names across lines (for example, `GROUP_CLASSES`).
- Every listed price is a monthly price per member, and the same plan and
  extras apply to every member in the quote.

Run the tests with `pytest` and lint the Python files with
`pylint gym_quote.py test_gym_quote.py`.
