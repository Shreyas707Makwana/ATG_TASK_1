# Multi-Agent Debate DAG using LangGraph

A Sophisticated debate system of 8 rounds between two agents (scientist and philosopher). The DAG svg file of whole workflow is in repo along with the debate JSON log of debate in Demo Video.

## 🎥 Demo Video

A 3-4 minute walkthrough demonstrating:
- CLI execution of the debate
- 8-round strict turn-taking
- Judge evaluation and winner determination
- Generated logs and DAG visualization

👉 **Demo Video Link:**  
https://drive.google.com/file/d/1429nVr-22OwaT20yEhmtI-42kAqFbIfq/view?usp=drive_link

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Node Documentation](#node-documentation)
- [DAG Structure](#dag-structure)
- [Testing](#testing)
- [Configuration](#configuration)
- [Reproducibility](#reproducibility)
- [Logs and Outputs](#logs-and-outputs)

## 🎯 Overview

This project implements a **Multi-Agent Debate system** where two AI agents with distinct personas engage in a structured 8-round debate. The system enforces strict turn-taking, validates arguments, maintains comprehensive memory, and uses a judge to evaluate the debate and determine a winner.

**Key Highlights:**
- Exactly 8 rounds with strict turn enforcement
- Two agents with configurable personas (Scientist & Philosopher by default)
- Comprehensive memory management with agent-specific slices
- Duplicate argument detection
- Logical coherence checking
- Detailed logging in JSON Lines format
- Judge evaluation with justified winner selection
- Reproducible debates with seed support

## ✨ Features

### Core Functionality
- ✅ **8-Round Structure**: Exactly 8 rounds, each agent speaks 4 times
- ✅ **Strict Turn Control**: Out-of-order execution is rejected
- ✅ **Memory Management**: Structured storage with agent-specific views
- ✅ **Argument Validation**: Detects and prevents duplicate/similar arguments
- ✅ **Coherence Checking**: Monitors logical consistency and topic drift
- ✅ **Judge Evaluation**: Comprehensive analysis with justified winner determination
- ✅ **Comprehensive Logging**: All node executions, state transitions, and memory snapshots
- ✅ **Deterministic Runs**: Reproducible debates with seed support

### Technical Features
- Modular node-based architecture
- LangGraph DAG implementation
- CLI interface with validation
- Automated test suite
- DAG visualization generation
- JSON Lines logging format

## 🏗️ Architecture

The system uses a **Directed Acyclic Graph (DAG)** architecture implemented with LangGraph:

```
UserInput → Coordinator → AgentA/B → Memory → Logger → [loop back or Judge]
                   ↓
                 Judge → Logger → END
```

Each component is a self-contained node with well-defined inputs and outputs.

## 📦 Installation

### Prerequisites
- Python 3.9+
- pip (Python package manager)
- Graphviz (for DAG visualization)

### Steps

1. **Clone or navigate to the project directory:**
```bash
cd e:\ATG
```

2. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

3. **Install Graphviz (for DAG visualization):**
   - **Windows**: Download from https://graphviz.org/download/
   - **Linux**: `sudo apt-get install graphviz`
   - **Mac**: `brew install graphviz`

4. **Verify installation:**
```bash
python run_debate.py --help
```

## 🚀 Usage

### Basic Usage

Run a debate with default settings:
```bash
python run_debate.py
```

You'll be prompted to enter a debate topic:
```
Enter topic for debate:
(Between 10-500 characters)
> The impact of artificial intelligence on society
```

The system will then execute the 8-round debate and display results.

### Advanced Usage

**With deterministic seed:**
```bash
python run_debate.py --seed 42
```

**Custom log path:**
```bash
python run_debate.py --log-path logs/my_debate.jsonl
```

**Custom personas:**
```bash
python run_debate.py --persona-config scientist,philosopher
```

**Combined options:**
```bash
python run_debate.py --seed 123 --log-path logs/debate_123.jsonl --persona-config scientist,philosopher
```

### Generate DAG Visualization

```bash
python generate_dag.py
```

This creates:
- `debate_dag.png` - Main DAG structure
- `debate_dag.svg` - SVG version
- `debate_dag_detailed.png` - Detailed 8-round flow

## 📁 Project Structure

```
e:\ATG\
├── run_debate.py              # Main entry point
├── generate_dag.py            # DAG visualization generator
├── requirements.txt           # Python dependencies
├── README.md                  # This file
│
├── nodes/                     # Node implementations
│   ├── __init__.py
│   ├── user_input_node.py    # User input with validation
│   ├── agent_node.py          # AI debate agents
│   ├── memory_node.py         # Memory management
│   ├── coordinator_node.py    # Turn control & validation
│   ├── judge_node.py          # Debate evaluation
│   └── logger_node.py         # Comprehensive logging
│
├── persona_templates/         # Agent persona definitions
│   ├── scientist.txt
│   └── philosopher.txt
│
└── tests/                     # Comprehensive test suite
    ├── __init__.py
    ├── test_user_input_node.py
    ├── test_agent_node.py
    ├── test_memory_node.py
    ├── test_coordinator_node.py
    ├── test_judge_node.py
    ├── test_logger_node.py
    └── test_integration.py
```

## 📚 Node Documentation

### 1. UserInputNode

**Purpose**: Handles CLI input for debate topic with validation and sanitization.

**Responsibilities:**
- Accept topic input from user
- Validate length (10-500 characters)
- Sanitize dangerous characters
- Ensure non-empty input

**Key Methods:**
- `get_topic_from_cli()`: Interactive topic collection
- `validate_topic(topic)`: Length and content validation
- `sanitize_input(text)`: Remove dangerous characters

### 2. AgentNode

**Purpose**: Represents a debate agent with specific persona and argument generation.

**Configuration:**
- `agent_id`: Unique identifier (e.g., "AgentA")
- `persona_name`: Persona type (e.g., "scientist", "philosopher")
- `seed`: Optional seed for deterministic behavior

**Responsibilities:**
- Load persona from template files
- Generate arguments based on topic and memory
- Detect and prevent duplicate arguments
- Maintain argument history

**Key Methods:**
- `generate_argument(topic, memory_slice, round_num)`: Generate debate argument
- `_is_duplicate_argument(argument)`: Duplicate detection
- `_similarity_score(text1, text2)`: Calculate text similarity

### 3. MemoryNode

**Purpose**: Maintains structured debate memory with agent-specific slices.

**Memory Entry Structure:**
```json
{
  "round": 1,
  "agent": "AgentA",
  "text": "Argument text...",
  "timestamp": "2025-12-26T10:30:00",
  "meta": {"argument_length": 150}
}
```

**Responsibilities:**
- Store all debate arguments
- Provide agent-specific memory slices
- Maintain chronological order
- Support full memory retrieval

**Key Methods:**
- `add_entry(round, agent, text, metadata)`: Add new memory entry
- `get_memory_slice(agent_id, max_entries)`: Get relevant memory for agent
- `get_full_memory()`: Retrieve complete debate history

### 4. CoordinatorNode

**Purpose**: Enforces debate rules, turn order, and round limits.

**Rules Enforced:**
- Exactly 8 rounds total
- Strict alternating turn order
- 4 turns per agent
- No out-of-order execution

**Responsibilities:**
- Generate and enforce turn order
- Validate each turn attempt
- Detect repeated arguments
- Check logical coherence
- Track debate status

**Key Methods:**
- `validate_turn(agent_id, round_num)`: Validate turn attempt
- `get_next_agent()`: Determine next speaker
- `advance_turn()`: Progress to next round
- `detect_repeated_arguments(memory)`: Find duplicates
- `check_logical_coherence(memory)`: Detect topic drift

### 5. JudgeNode

**Purpose**: Evaluates complete debate and determines winner with justification.

**Evaluation Criteria:**
- Vocabulary richness
- Argument consistency
- Logical progression
- Argument quality and length

**Responsibilities:**
- Analyze argument quality for each agent
- Evaluate logical progression
- Determine winner with confidence score
- Generate comprehensive justification
- Create debate summary

**Key Methods:**
- `determine_winner(memory)`: Evaluate and select winner
- `analyze_argument_quality(arguments)`: Quality metrics
- `evaluate_logical_progression(memory)`: Progression analysis
- `generate_summary(memory, topic)`: Create debate transcript

**Output Format:**
```python
{
  "winner": "AgentA",
  "confidence": 0.75,
  "justification": "Detailed reasoning...",
  "final_scores": {"AgentA": 0.75, "AgentB": 0.68},
  "quality_analysis": {...},
  "progression_scores": {...}
}
```

### 6. LoggerNode

**Purpose**: Comprehensive logging of all debate activity.

**Logged Events:**
- Node inputs and outputs
- State transitions
- Memory snapshots
- Warnings (repetition, coherence)
- Final verdict
- Errors

**Log Format:** JSON Lines (.jsonl)

**Key Methods:**
- `log(entry_type, data)`: Generic log entry
- `log_node_execution(node_execution)`: Log node activity
- `log_memory_snapshot(memory)`: Snapshot debate state
- `log_final_verdict(verdict)`: Log judge decision
- `log_warning(type, message, details)`: Log warnings

## 🔄 DAG Structure

### Node Flow

```
┌─────────────┐
│ UserInput   │ ← Entry point
│ (Get Topic) │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Coordinator │ ← Turn control
│   (Round    │
│   Manager)  │
└──────┬──────┘
       │
       ├─────────────┐
       ▼             ▼
┌──────────┐   ┌──────────┐
│ AgentA   │   │ AgentB   │ ← Debate agents
│(Scientist│   │(Philosoph│
└────┬─────┘   └────┬─────┘
     │              │
     └──────┬───────┘
            ▼
     ┌──────────┐
     │  Memory  │ ← Store arguments
     │  Node    │
     └────┬─────┘
          ▼
     ┌──────────┐
     │  Logger  │ ← Log everything
     │  Node    │
     └────┬─────┘
          │
          ├─→ Loop back to Coordinator (rounds 1-7)
          │
          └─→ (After round 8) ▼
              ┌──────────┐
              │  Judge   │ ← Evaluate
              │  Node    │
              └────┬─────┘
                   ▼
              ┌──────────┐
              │  Logger  │
              └────┬─────┘
                   ▼
                [ END ]
```

### Conditional Routing

The Coordinator uses conditional edges to route execution:
- **Rounds 1-8**: Route to appropriate agent (AgentA or AgentB)
- **After Round 8**: Route to Judge for final evaluation

## 🧪 Testing

### Run All Tests

```bash
python -m pytest tests/ -v
```

### Run Specific Test Suites

```bash
# Test individual nodes
python -m pytest tests/test_user_input_node.py -v
python -m pytest tests/test_agent_node.py -v
python -m pytest tests/test_memory_node.py -v
python -m pytest tests/test_coordinator_node.py -v
python -m pytest tests/test_judge_node.py -v
python -m pytest tests/test_logger_node.py -v

# Integration tests
python -m pytest tests/test_integration.py -v
```

### Test Coverage

The test suite covers:
- ✅ Turn enforcement (out-of-order detection)
- ✅ Duplicate argument detection
- ✅ Memory updates after each round
- ✅ Judge output format and justification
- ✅ Reproducible runs with fixed seed
- ✅ Input validation and sanitization
- ✅ Logging functionality
- ✅ Complete debate flow integration

### Key Test Cases

**Turn Enforcement:**
```python
# AgentB attempting to speak in AgentA's turn fails
is_valid, error = coordinator.validate_turn("AgentB", 1)
assert not is_valid
assert "Out of turn" in error
```

**Duplicate Detection:**
```python
# Same argument detected as duplicate
agent.previous_arguments.append("Test argument")
assert agent._is_duplicate_argument("Test argument") == True
```

**Reproducibility:**
```python
# Same seed produces same arguments
agent1 = AgentNode("AgentA", "scientist", seed=42)
agent2 = AgentNode("AgentA", "scientist", seed=42)
arg1 = agent1.generate_argument(topic, [], 1)
arg2 = agent2.generate_argument(topic, [], 1)
assert arg1 == arg2
```

## ⚙️ Configuration

### Persona Configuration

Personas are defined in `persona_templates/`:

**scientist.txt**: Empirical, data-driven reasoning
**philosopher.txt**: Abstract, ethical reasoning

To add custom personas:
1. Create a new `.txt` file in `persona_templates/`
2. Define the persona characteristics
3. Use `--persona-config` to reference it

### CLI Options

| Option | Description | Default |
|--------|-------------|---------|
| `--seed` | Random seed for deterministic behavior | None (non-deterministic) |
| `--log-path` | Path to log file | `debate_log_<timestamp>.jsonl` |
| `--persona-config` | Comma-separated personas | `scientist,philosopher` |

## 🔁 Reproducibility

### Running Reproducible Debates

Use the `--seed` option to ensure debates are reproducible:

```bash
python run_debate.py --seed 42
```

With the same seed and topic, the debate will produce identical arguments in the same order.

### Sample Reproducible Run

```bash
# Run 1
python run_debate.py --seed 42 --log-path logs/run1.jsonl

# Run 2 (identical to Run 1)
python run_debate.py --seed 42 --log-path logs/run2.jsonl
```

When prompted, enter the same topic for both runs. The generated arguments and final verdict will be identical.

### Verification

Compare log files:
```bash
# On Windows (PowerShell)
Compare-Object (Get-Content logs/run1.jsonl) (Get-Content logs/run2.jsonl)

# On Linux/Mac
diff logs/run1.jsonl logs/run2.jsonl
```

No differences should be reported (except timestamps).

## 📊 Logs and Outputs

### Log File Location

Default: `debate_log_<timestamp>.jsonl`
Custom: Specified via `--log-path`

### Log Format

JSON Lines format (one JSON object per line):

```json
{"timestamp": "2025-12-26T10:30:15.123456", "type": "node_execution", "data": {...}}
{"timestamp": "2025-12-26T10:30:16.234567", "type": "memory_snapshot", "data": {...}}
{"timestamp": "2025-12-26T10:30:45.345678", "type": "final_verdict", "data": {...}}
```

### Log Entry Types

| Type | Description |
|------|-------------|
| `node_execution` | Node input/output data |
| `state_transition` | State changes in the graph |
| `memory_snapshot` | Current memory state |
| `warning` | Repetition or coherence warnings |
| `error` | Error conditions |
| `final_verdict` | Judge's final evaluation |

### DAG Visualizations

Generated by `generate_dag.py`:
- `debate_dag.png` - Main graph structure
- `debate_dag.svg` - Scalable vector version
- `debate_dag_detailed.png` - 8-round flow diagram

## 🎯 Example Session

```bash
$ python run_debate.py --seed 42

================================================================================
MULTI-AGENT DEBATE SYSTEM
================================================================================
AgentA Persona: scientist
AgentB Persona: philosopher
Seed: 42
================================================================================

============================================================
Enter topic for debate:
(Between 10-500 characters)
============================================================
> The ethical implications of artificial intelligence

✓ Topic accepted: 'The ethical implications of artificial intelligence'

================================================================================
Round 1 - AgentA (scientist):
--------------------------------------------------------------------------------
From a scientific perspective on 'The ethical implications of artificial 
intelligence', empirical evidence suggests that we must consider measurable 
outcomes and reproducible results. Round 1 analysis.
================================================================================

================================================================================
Round 2 - AgentB (philosopher):
--------------------------------------------------------------------------------
Philosophically examining 'The ethical implications of artificial intelligence',
we must question the fundamental assumptions underlying our positions and explore
the deeper implications. Round 2 reflection.
================================================================================

[... rounds 3-8 ...]

================================================================================
DEBATE COMPLETE - JUDGE'S VERDICT
================================================================================
[Full debate summary with all 8 rounds...]

================================================================================
WINNER: AgentA

JUSTIFICATION:
AgentA Performance:
  - Vocabulary Richness: 0.645
  - Consistency: 0.823
  - Average Argument Length: 187.3 characters
  - Logical Progression: 0.712
  - Final Score: 0.751

AgentB Performance:
  - Vocabulary Richness: 0.598
  - Consistency: 0.791
  - Average Argument Length: 174.8 characters
  - Logical Progression: 0.689
  - Final Score: 0.698

AgentA emerged victorious with a final score of 0.751.
Key strengths: rich and varied vocabulary, consistent argumentation style,
strong logical progression.
================================================================================

Debate log saved to: debate_log_20251226_103045.jsonl

Debate completed successfully!
```

## 🔍 Technical Details

### Dependencies

- **langgraph**: Graph orchestration framework
- **graphviz**: DAG visualization
- **python-dotenv**: Environment configuration (optional)

### Python Version

Minimum: Python 3.9
Recommended: Python 3.10+

### Performance

- Average debate duration: 10-30 seconds
- Log file size: ~10-50 KB per debate
- Memory usage: < 100 MB

## 🤝 Contributing

This is a technical assignment submission. For questions or issues:

1. Review the code documentation
2. Check test cases for usage examples
3. Examine log files for debugging

## 📝 License

This project is submitted as part of an ATG technical assignment.

## 🎓 Author

Shreyas Makwana - ATG Technical Assignment Submission  
Multi-Agent Debate DAG using LangGraph
