import json
import os
from typing import Dict, Any
from datetime import datetime


class LoggerNode:
    
    def __init__(self, log_path: str = None):
        self.name = "LoggerNode"
        
        if log_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_path = f"debate_log_{timestamp}.jsonl"
        
        self.log_path = log_path
        self.log_entries = []
        
        log_dir = os.path.dirname(log_path)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
    
    def log(self, entry_type: str, data: Dict[str, Any]):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "type": entry_type,
            "data": data
        }
        
        self.log_entries.append(entry)
        
        with open(self.log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry) + '\n')
    
    def log_node_execution(self, node_execution: Dict[str, Any]):
        self.log(entry_type="node_execution", data=node_execution)
    
    def log_state_transition(self, from_state: Dict[str, Any], to_state: Dict[str, Any]):
        self.log(
            entry_type="state_transition",
            data={
                "from": self._serialize_state(from_state),
                "to": self._serialize_state(to_state)
            }
        )
    
    def log_memory_snapshot(self, memory: list):
        self.log(
            entry_type="memory_snapshot",
            data={
                "total_entries": len(memory),
                "entries": memory
            }
        )
    
    def log_final_verdict(self, verdict: Dict[str, Any]):
        self.log(entry_type="final_verdict", data=verdict)
    
    def log_error(self, error_type: str, message: str, details: Dict[str, Any] = None):
        self.log(
            entry_type="error",
            data={
                "error_type": error_type,
                "message": message,
                "details": details or {}
            }
        )
    
    def log_warning(self, warning_type: str, message: str, details: Dict[str, Any] = None):
        self.log(
            entry_type="warning",
            data={
                "warning_type": warning_type,
                "message": message,
                "details": details or {}
            }
        )
    
    def _serialize_state(self, state: Dict[str, Any]) -> Dict[str, Any]:
        serialized = {}
        
        for key, value in state.items():
            if isinstance(value, (str, int, float, bool, type(None))):
                serialized[key] = value
            elif isinstance(value, (list, dict)):
                try:
                    json.dumps(value)
                    serialized[key] = value
                except (TypeError, ValueError):
                    serialized[key] = str(value)
            else:
                serialized[key] = str(value)
        
        return serialized
    
    def get_log_path(self) -> str:
        return self.log_path
    
    def get_all_logs(self) -> list:
        return self.log_entries.copy()
    
    def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]:
        if "node_execution" in state:
            self.log_node_execution(state["node_execution"])
        
        if "memory" in state:
            self.log_memory_snapshot(state["memory"])
        
        if "repetition_warnings" in state:
            for warning in state["repetition_warnings"]:
                self.log_warning("repetition", warning["message"], warning)
        
        if "coherence_warnings" in state:
            for warning in state["coherence_warnings"]:
                self.log_warning("coherence", warning["message"], warning)
        
        if "winner" in state and "winner_justification" in state:
            self.log_final_verdict({
                "winner": state["winner"],
                "confidence": state.get("winner_confidence", 0),
                "justification": state["winner_justification"],
                "analysis": state.get("judge_analysis", {})
            })
        
        return {
            "log_path": self.log_path,
            "node_execution": {
                "node": self.name,
                "input": {"keys": list(state.keys())},
                "output": {"log_entries": len(self.log_entries)}
            }
        }
