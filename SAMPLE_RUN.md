# Multi-Agent Debate DAG - Sample Test Run

This document demonstrates a reproducible test run using a fixed seed.

## Test Configuration

- **Seed**: 42
- **Topic**: "The role of scientific evidence in policy making"
- **AgentA Persona**: Scientist
- **AgentB Persona**: Philosopher

## Running the Test

```bash
python -m pytest tests/ -v

python run_debate.py --seed 42
```

When prompted, enter the topic:
```
The role of scientific evidence in policy making
```

## Expected Behavior

1. **Round 1**: AgentA (Scientist) speaks first
2. **Round 2**: AgentB (Philosopher) responds
3. Pattern continues alternating for 8 rounds total
4. Judge evaluates and determines winner
5. Log file created: `debate_log_<timestamp>.jsonl`

## Verification

To verify reproducibility, run the same command twice:

```bash
# First run
python run_debate.py --seed 42 --log-path logs/test_run_1.jsonl

# Second run  
python run_debate.py --seed 42 --log-path logs/test_run_2.jsonl
```

Enter the same topic both times. The arguments should be identical (only timestamps will differ).

## Test Assertions

- ✅ Exactly 8 rounds completed
- ✅ Each agent speaks exactly 4 times
- ✅ Strict alternating pattern maintained
- ✅ No duplicate arguments within each agent
- ✅ Memory updated after each turn
- ✅ Judge provides winner with justification
- ✅ Log file contains all node executions
- ✅ Same seed produces same arguments

## Automated Testing

Run the full test suite:

```bash
python -m pytest tests/ -v
```

Key test: `test_reproducible_with_fixed_seed` in `tests/test_integration.py`
