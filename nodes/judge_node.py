import hashlib
from typing import Dict, Any, List


class JudgeNode:
    
    def __init__(self, seed: int = None):
        self.name = "JudgeNode"
        self.seed = seed
    
    def analyze_argument_quality(self, arguments: List[str]) -> Dict[str, Any]:
        if not arguments:
            return {
                "avg_length": 0,
                "total_arguments": 0,
                "vocabulary_richness": 0,
                "consistency_score": 0
            }
        
        total_length = sum(len(arg) for arg in arguments)
        avg_length = total_length / len(arguments)
        
        all_words = []
        for arg in arguments:
            all_words.extend(arg.lower().split())
        
        vocab_richness = len(set(all_words)) / len(all_words) if all_words else 0
        
        if len(arguments) > 1:
            lengths = [len(arg) for arg in arguments]
            avg_len = sum(lengths) / len(lengths)
            variance = sum((l - avg_len) ** 2 for l in lengths) / len(lengths)
            consistency_score = 1.0 / (1.0 + variance / 1000.0)
        else:
            consistency_score = 1.0
        
        return {
            "avg_length": avg_length,
            "total_arguments": len(arguments),
            "vocabulary_richness": vocab_richness,
            "consistency_score": consistency_score
        }
    
    def evaluate_logical_progression(self, memory: List[Dict[str, Any]]) -> Dict[str, float]:
        scores = {}
        
        agent_entries = {}
        for entry in memory:
            agent = entry["agent"]
            if agent not in agent_entries:
                agent_entries[agent] = []
            agent_entries[agent].append(entry)
        
        for agent, entries in agent_entries.items():
            if len(entries) < 2:
                scores[agent] = 0.5
                continue
            
            progression_score = 0.0
            
            for i in range(1, len(entries)):
                prev_arg = entries[i-1]["text"].lower()
                curr_arg = entries[i]["text"].lower()
                
                prev_words = set(prev_arg.split())
                curr_words = set(curr_arg.split())
                
                overlap = len(prev_words & curr_words)
                if overlap > 5:
                    progression_score += 0.5
                
                if len(curr_arg) > len(prev_arg):
                    progression_score += 0.3
            
            max_possible = (len(entries) - 1) * 0.8
            scores[agent] = min(1.0, progression_score / max_possible if max_possible > 0 else 0.5)
        
        return scores
    
    def determine_winner(self, memory: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not memory:
            return {
                "winner": "No winner",
                "confidence": 0.0,
                "justification": "No arguments found in memory."
            }
        
        agent_arguments = {}
        for entry in memory:
            agent = entry["agent"]
            if agent not in agent_arguments:
                agent_arguments[agent] = []
            agent_arguments[agent].append(entry["text"])
        
        agent_scores = {}
        agent_analysis = {}
        
        for agent, arguments in agent_arguments.items():
            quality = self.analyze_argument_quality(arguments)
            
            score = (
                quality["vocabulary_richness"] * 0.3 +
                quality["consistency_score"] * 0.2 +
                min(1.0, quality["avg_length"] / 200.0) * 0.2 +
                (quality["total_arguments"] / 4.0) * 0.3
            )
            
            agent_scores[agent] = score
            agent_analysis[agent] = quality
        
        progression_scores = self.evaluate_logical_progression(memory)
        
        final_scores = {}
        for agent in agent_scores:
            final_scores[agent] = (
                agent_scores[agent] * 0.6 +
                progression_scores.get(agent, 0.5) * 0.4
            )
        
        if not final_scores:
            winner = "No winner"
            confidence = 0.0
        else:
            winner = max(final_scores, key=final_scores.get)
            winner_score = final_scores[winner]
            other_scores = [s for a, s in final_scores.items() if a != winner]
            
            if other_scores:
                margin = winner_score - max(other_scores)
                confidence = min(1.0, 0.5 + margin)
            else:
                confidence = 1.0
        
        justification = self._build_justification(
            winner, 
            agent_analysis, 
            progression_scores, 
            final_scores
        )
        
        return {
            "winner": winner,
            "confidence": confidence,
            "final_scores": final_scores,
            "quality_analysis": agent_analysis,
            "progression_scores": progression_scores,
            "justification": justification
        }
    
    def _build_justification(
        self, 
        winner: str, 
        quality_analysis: Dict, 
        progression_scores: Dict, 
        final_scores: Dict
    ) -> str:
        lines = [
            f"WINNER: {winner}",
            "",
            "JUSTIFICATION:",
            ""
        ]
        
        agents = list(final_scores.keys())
        
        for agent in agents:
            quality = quality_analysis.get(agent, {})
            progression = progression_scores.get(agent, 0)
            final = final_scores.get(agent, 0)
            
            lines.append(f"{agent} Performance:")
            lines.append(f"  - Vocabulary Richness: {quality.get('vocabulary_richness', 0):.3f}")
            lines.append(f"  - Consistency: {quality.get('consistency_score', 0):.3f}")
            lines.append(f"  - Average Argument Length: {quality.get('avg_length', 0):.1f} characters")
            lines.append(f"  - Logical Progression: {progression:.3f}")
            lines.append(f"  - Final Score: {final:.3f}")
            lines.append("")
        
        if winner in final_scores:
            winner_score = final_scores[winner]
            lines.append(f"{winner} emerged victorious with a final score of {winner_score:.3f}.")
            
            winner_quality = quality_analysis.get(winner, {})
            
            strengths = []
            if winner_quality.get('vocabulary_richness', 0) > 0.5:
                strengths.append("rich and varied vocabulary")
            if winner_quality.get('consistency_score', 0) > 0.7:
                strengths.append("consistent argumentation style")
            if progression_scores.get(winner, 0) > 0.6:
                strengths.append("strong logical progression")
            
            if strengths:
                lines.append(f"Key strengths: {', '.join(strengths)}.")
        
        return "\n".join(lines)
    
    def generate_summary(self, memory: List[Dict[str, Any]], topic: str) -> str:
        lines = [
            "="*80,
            "DEBATE SUMMARY",
            "="*80,
            f"Topic: {topic}",
            f"Total Rounds: {len(memory)}",
            "",
            "DEBATE TRANSCRIPT:",
            ""
        ]
        
        for entry in memory:
            lines.append(f"Round {entry['round']} - {entry['agent']}:")
            lines.append(f"  {entry['text']}")
            lines.append("")
        
        return "\n".join(lines)
    
    def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]:
        memory = state.get("memory", [])
        topic = state.get("topic", "Unknown topic")
        
        summary = self.generate_summary(memory, topic)
        
        verdict = self.determine_winner(memory)
        
        return {
            "debate_summary": summary,
            "winner": verdict["winner"],
            "winner_confidence": verdict["confidence"],
            "winner_justification": verdict["justification"],
            "judge_analysis": {
                "final_scores": verdict["final_scores"],
                "quality_analysis": verdict["quality_analysis"],
                "progression_scores": verdict["progression_scores"]
            },
            "node_execution": {
                "node": self.name,
                "input": {
                    "topic": topic,
                    "total_rounds": len(memory)
                },
                "output": {
                    "winner": verdict["winner"],
                    "confidence": verdict["confidence"]
                }
            }
        }
