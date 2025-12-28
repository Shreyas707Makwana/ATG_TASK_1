
__version__ = "1.0.0"
__author__ = "ML Engineer Candidate"
__assignment__ = "ATG Technical - Multi-Agent Debate DAG"

PACKAGE_NAME = "multi_agent_debate_dag"
DESCRIPTION = "Multi-Agent Debate DAG using LangGraph"
REQUIREMENTS = [
    "langgraph>=0.2.0",
    "graphviz>=0.20.1",
    "typing-extensions>=4.8.0"
]

DEFAULT_ROUNDS = 8
DEFAULT_TURNS_PER_AGENT = 4
DEFAULT_LOG_FORMAT = "jsonl"
MIN_TOPIC_LENGTH = 10
MAX_TOPIC_LENGTH = 500

AVAILABLE_PERSONAS = [
    "scientist",
    "philosopher"
]
