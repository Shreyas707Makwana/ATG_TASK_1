import argparse
import os
import sys
from typing import TypedDict, Dict, Any
from langgraph.graph import StateGraph, END
from nodes import UserInputNode, AgentNode, MemoryNode, CoordinatorNode, JudgeNode, LoggerNode


class DebateState(TypedDict):
    current_round: int
    next_agent: str
    current_agent: str
    current_argument: str
    memory: list
    debate_complete: bool
    debate_summary: str
    winner: str
    winner_confidence: float
    winner_justification: str
    judge_analysis: dict
    repetition_warnings: list
    coherence_warnings: list
    debate_status: dict
    log_path: str
    node_execution: dict


class DebateOrchestrator:
    def __init__(self, seed: int = None, log_path: str = None, persona_config: dict = None):
        self.seed = seed
        self.log_path = log_path
        self.persona_config = persona_config or {"AgentA": "scientist", "AgentB": "philosopher"}
        self._init_nodes()
        self.graph = self._build_graph()

    def _init_nodes(self):
        persona_a = self.persona_config.get("AgentA", "scientist")
        persona_b = self.persona_config.get("AgentB", "philosopher")
        persona_a_path = f"persona_templates/{persona_a}.txt"
        persona_b_path = f"persona_templates/{persona_b}.txt"
        self.user_input_node = UserInputNode()
        self.agent_a = AgentNode(
            agent_id="AgentA",
            persona_name=persona_a,
            persona_path=persona_a_path if os.path.exists(persona_a_path) else None,
            seed=self.seed,
        )
        self.agent_b = AgentNode(
            agent_id="AgentB",
            persona_name=persona_b,
            persona_path=persona_b_path if os.path.exists(persona_b_path) else None,
            seed=self.seed,
        )
        self.memory_node = MemoryNode()
        self.coordinator_node = CoordinatorNode(agent_a_id="AgentA", agent_b_id="AgentB")
        self.judge_node = JudgeNode(seed=self.seed)
        self.logger_node = LoggerNode(log_path=self.log_path)

    def _build_graph(self):
        workflow = StateGraph(DebateState)
        workflow.add_node("user_input", self._user_input_wrapper)
        workflow.add_node("coordinator", self._coordinator_wrapper)
        workflow.add_node("turn_a", self._turn_a_wrapper)
        workflow.add_node("turn_b", self._turn_b_wrapper)
        workflow.add_node("judge", self._judge_wrapper)
        workflow.add_node("logger", self._logger_wrapper)
        workflow.add_node("logger_final", self._logger_wrapper)
        workflow.set_entry_point("user_input")
        workflow.add_edge("user_input", "coordinator")
        workflow.add_conditional_edges(
            "coordinator",
            self._route_from_coordinator,
            {"turn_a": "turn_a", "turn_b": "turn_b", "judge": "judge"},
        )
        workflow.add_edge("turn_a", "coordinator")
        workflow.add_edge("turn_b", "coordinator")
        workflow.add_edge("judge", "logger_final")
        workflow.add_edge("logger_final", END)
        return workflow.compile()

    def _user_input_wrapper(self, state: Dict[str, Any]) -> Dict[str, Any]:
        return self.user_input_node(state)

    def _coordinator_wrapper(self, state: Dict[str, Any]) -> Dict[str, Any]:
        result = self.coordinator_node(state)
        if not result.get("debate_complete", False):
            self.coordinator_node.advance_turn()
        return result

    def _turn_a_wrapper(self, state: Dict[str, Any]) -> Dict[str, Any]:
        result_agent = self.agent_a(state)
        print("\n" + "=" * 80)
        print(f"Round {state.get('current_round', '?')} - AgentA ({self.agent_a.persona_name}):")
        print("-" * 80)
        print(result_agent.get("current_argument", ""))
        print("=" * 80 + "\n")
        state_after_agent = {**state, **result_agent}
        result_memory = self.memory_node(state_after_agent)
        state_after_memory = {**state_after_agent, **result_memory}
        result_logger = self.logger_node(state_after_memory)
        return {**state_after_memory, "log_path": result_logger.get("log_path", state.get("log_path", ""))}

    def _turn_b_wrapper(self, state: Dict[str, Any]) -> Dict[str, Any]:
        result_agent = self.agent_b(state)
        print("\n" + "=" * 80)
        print(f"Round {state.get('current_round', '?')} - AgentB ({self.agent_b.persona_name}):")
        print("-" * 80)
        print(result_agent.get("current_argument", ""))
        print("=" * 80 + "\n")
        state_after_agent = {**state, **result_agent}
        result_memory = self.memory_node(state_after_agent)
        state_after_memory = {**state_after_agent, **result_memory}
        result_logger = self.logger_node(state_after_memory)
        return {**state_after_memory, "log_path": result_logger.get("log_path", state.get("log_path", ""))}

    def _judge_wrapper(self, state: Dict[str, Any]) -> Dict[str, Any]:
        result = self.judge_node(state)
        print("\n" + "=" * 80)
        print("DEBATE COMPLETE - JUDGE'S VERDICT")
        print("=" * 80)
        print(result.get("debate_summary", ""))
        print("\n" + "=" * 80)
        print(result.get("winner_justification", ""))
        return result

    def _logger_wrapper(self, state: Dict[str, Any]) -> Dict[str, Any]:
        return self.logger_node(state)

    def _route_from_coordinator(self, state: Dict[str, Any]) -> str:
        if state.get("debate_complete", False):
            return "judge"
        next_agent = state.get("next_agent")
        if next_agent == "AgentA":
            return "turn_a"
        if next_agent == "AgentB":
            return "turn_b"
        return "judge"

    def run(self):
        initial_state = {
            "topic": "",
            "current_round": 0,
            "next_agent": "",
            "current_agent": "",
            "current_argument": "",
            "debate_complete": False,
            "debate_summary": "",
            "winner": "",
            "winner_confidence": 0.0,
            "winner_justification": "",
            "judge_analysis": {},
            "repetition_warnings": [],
            "coherence_warnings": [],
            "debate_status": {},
            "log_path": "",
            "node_execution": {},
        }
        print("\n" + "=" * 80)
        print("MULTI-AGENT DEBATE SYSTEM")
        print("=" * 80)
        print(f"AgentA Persona: {self.agent_a.persona_name}")
        print(f"AgentB Persona: {self.agent_b.persona_name}")
        if self.seed is not None:
            print(f"Seed: {self.seed}")
        print("=" * 80)
        final_state = self.graph.invoke(initial_state)
        print(f"\nDebate log saved to: {final_state.get('log_path', 'N/A')}")
        print("\nDebate completed successfully!\n")
        return final_state


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python run_debate.py\n"
            "  python run_debate.py --seed 42\n"
            "  python run_debate.py --log-path logs/debate.jsonl\n"
            "  python run_debate.py --seed 123 --persona-config scientist,philosopher\n"
        ),
    )
    parser.add_argument("--seed", type=int, default=None, help="Random seed for deterministic behavior")
    parser.add_argument(
        "--log-path",
        type=str,
        default=None,
        help="Path to log file (default: debate_log_<timestamp>.jsonl)",
    )
    parser.add_argument(
        "--persona-config",
        type=str,
        default="scientist,philosopher",
        help="Comma-separated personas for AgentA,AgentB (default: scientist,philosopher)",
    )
    args = parser.parse_args()
    personas = args.persona_config.split(",")
    if len(personas) != 2:
        print("Error: --persona-config must specify exactly 2 personas separated by comma")
        sys.exit(1)
    persona_config = {"AgentA": personas[0].strip(), "AgentB": personas[1].strip()}
    orchestrator = DebateOrchestrator(seed=args.seed, log_path=args.log_path, persona_config=persona_config)
    try:
        orchestrator.run()
    except KeyboardInterrupt:
        print("\n\nDebate interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nError during debate: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
