import json
from typing import Dict, Any, List
from datetime import datetime


class MemoryNode:
    
    def __init__(self):
        self.name = "MemoryNode"
        self.memory_store: List[Dict[str, Any]] = []
    
    def add_entry(self, round_num: int, agent_id: str, text: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        entry = {
            "round": round_num,
            "agent": agent_id,
            "text": text,
            "timestamp": datetime.now().isoformat(),
            "meta": metadata or {}
        }
        
        self.memory_store.append(entry)
        return entry
    
    def get_memory_slice(self, agent_id: str, max_entries: int = 5) -> List[Dict[str, Any]]:
        other_agent_entries = [
            entry for entry in self.memory_store 
            if entry["agent"] != agent_id
        ]
        
        return other_agent_entries[-max_entries:]
    
    def get_full_memory(self) -> List[Dict[str, Any]]:
        return self.memory_store.copy()
    
    def get_memory_for_round(self, round_num: int) -> List[Dict[str, Any]]:
        return [entry for entry in self.memory_store if entry["round"] == round_num]
    
    def serialize(self) -> str:
        return json.dumps(self.memory_store, indent=2)
    
    def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]:
        current_round = state.get("current_round", 1)
        current_agent = state.get("current_agent")
        current_argument = state.get("current_argument")
        
        if current_agent and current_argument:
            entry = self.add_entry(
                round_num=current_round,
                agent_id=current_agent,
                text=current_argument,
                metadata={
                    "argument_length": len(current_argument)
                }
            )
            
            return {
                "memory": self.get_full_memory(),
                "node_execution": {
                    "node": self.name,
                    "input": {
                        "round": current_round,
                        "agent": current_agent,
                        "argument_length": len(current_argument)
                    },
                    "output": {
                        "total_entries": len(self.memory_store),
                        "latest_entry": entry
                    }
                }
            }
        
        return {
            "memory": self.get_full_memory(),
            "node_execution": {
                "node": self.name,
                "input": state,
                "output": {"total_entries": len(self.memory_store)}
            }
        }
