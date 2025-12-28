from typing import Dict, Any, Optional


class CoordinatorNode:
    
    TOTAL_ROUNDS = 8
    TURNS_PER_AGENT = 4
    
    def __init__(self, agent_a_id: str = "AgentA", agent_b_id: str = "AgentB"):
        self.name = "CoordinatorNode"
        self.agent_a_id = agent_a_id
        self.agent_b_id = agent_b_id
        self.turn_order = self._generate_turn_order()
        self.current_turn_index = 0
    
    def _generate_turn_order(self) -> list:
        order = []
        for round_num in range(1, self.TOTAL_ROUNDS + 1):
            if round_num % 2 == 1:
                agent = self.agent_a_id
            else:
                agent = self.agent_b_id
            order.append((round_num, agent))
        return order
    
    def get_next_agent(self) -> Optional[tuple]:
        if self.current_turn_index < len(self.turn_order):
            return self.turn_order[self.current_turn_index]
        return None
    
    def advance_turn(self):
        self.current_turn_index += 1
    
    def validate_turn(self, agent_id: str, round_num: int) -> tuple[bool, str]:
        if self.current_turn_index >= len(self.turn_order):
            return False, "Debate has concluded. No more turns allowed."
        
        expected_round, expected_agent = self.turn_order[self.current_turn_index]
        
        if round_num != expected_round:
            return False, f"Wrong round. Expected round {expected_round}, got round {round_num}."
        
        if agent_id != expected_agent:
            return False, f"Out of turn. Expected {expected_agent}, got {agent_id} in round {round_num}."
        
        return True, ""
    
    def is_debate_complete(self) -> bool:
        return self.current_turn_index >= self.TOTAL_ROUNDS
    
    def get_debate_status(self) -> Dict[str, Any]:
        return {
            "total_rounds": self.TOTAL_ROUNDS,
            "completed_turns": self.current_turn_index,
            "remaining_turns": self.TOTAL_ROUNDS - self.current_turn_index,
            "is_complete": self.is_debate_complete(),
            "next_turn": self.get_next_agent()
        }
    
    def detect_repeated_arguments(self, memory: list) -> list:
        warnings = []
        
        agent_arguments = {}
        for entry in memory:
            agent = entry["agent"]
            if agent not in agent_arguments:
                agent_arguments[agent] = []
            agent_arguments[agent].append(entry["text"])
        
        for agent, arguments in agent_arguments.items():
            for i, arg1 in enumerate(arguments):
                for j, arg2 in enumerate(arguments[i+1:], start=i+1):
                    words1 = set(arg1.lower().split())
                    words2 = set(arg2.lower().split())
                    
                    if len(words1) > 0 and len(words2) > 0:
                        overlap = len(words1 & words2) / min(len(words1), len(words2))
                        if overlap > 0.8:
                            warnings.append({
                                "agent": agent,
                                "turns": [i+1, j+1],
                                "overlap_ratio": overlap,
                                "message": f"{agent} may have repeated similar arguments in turns {i+1} and {j+1}"
                            })
        
        return warnings
    
    def check_logical_coherence(self, memory: list) -> list:
        warnings = []
        
        if len(memory) > 0:
            first_arg = memory[0]["text"].lower()
            first_words = set(first_arg.split())
            
            for i, entry in enumerate(memory[1:], start=2):
                current_words = set(entry["text"].lower().split())
                
                if len(first_words) > 0:
                    overlap = len(first_words & current_words) / len(first_words)
                    if overlap < 0.1:
                        warnings.append({
                            "round": entry["round"],
                            "agent": entry["agent"],
                            "type": "possible_topic_drift",
                            "message": f"Round {entry['round']}: Possible topic drift detected"
                        })
        
        return warnings
    
    def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]:
        memory = state.get("memory", [])
        
        repetition_warnings = self.detect_repeated_arguments(memory)
        
        coherence_warnings = self.check_logical_coherence(memory)
        
        status = self.get_debate_status()
        
        next_turn = self.get_next_agent()
        
        if next_turn:
            next_round, next_agent = next_turn
        else:
            next_round, next_agent = None, None
        
        return {
            "current_round": next_round,
            "next_agent": next_agent,
            "debate_complete": self.is_debate_complete(),
            "repetition_warnings": repetition_warnings,
            "coherence_warnings": coherence_warnings,
            "debate_status": status,
            "node_execution": {
                "node": self.name,
                "input": {"memory_entries": len(memory)},
                "output": {
                    "next_round": next_round,
                    "next_agent": next_agent,
                    "warnings": len(repetition_warnings) + len(coherence_warnings)
                }
            }
        }
