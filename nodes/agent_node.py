import os
import json
import hashlib
from typing import Dict, Any, List, Optional
from difflib import SequenceMatcher


class AgentNode:
    
    def __init__(self, agent_id: str, persona_name: str, persona_path: Optional[str] = None, seed: Optional[int] = None):
        self.agent_id = agent_id
        self.persona_name = persona_name
        self.seed = seed
        self.name = f"{agent_id}Node"
        self.previous_arguments = []
        
        if persona_path and os.path.exists(persona_path):
            with open(persona_path, 'r', encoding='utf-8') as f:
                self.persona = f.read().strip()
        else:
            self.persona = self._default_persona()
    
    def _default_persona(self) -> str:
        personas = {
            "scientist": """You are a logical scientist who values empirical evidence, 
data-driven reasoning, and the scientific method. You approach debates with 
skepticism and demand proof for claims. You emphasize testable hypotheses 
and reproducible results.""",
            
            "philosopher": """You are a thoughtful philosopher who explores abstract 
concepts, ethical implications, and deeper meanings. You value logical 
consistency, thought experiments, and examining assumptions. You question 
fundamental premises and explore various perspectives."""
        }
        return personas.get(self.persona_name.lower(), "You are a rational debater.")
    
    def _similarity_score(self, text1: str, text2: str) -> float:
        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()
    
    def _is_duplicate_argument(self, new_argument: str, threshold: float = 0.7) -> bool:
        for prev_arg in self.previous_arguments:
            if self._similarity_score(new_argument, prev_arg) > threshold:
                return True
        return False
    
    def generate_argument(self, topic: str, memory_slice: List[Dict], round_num: int) -> str:
        context = self._build_context(memory_slice)
        
        argument = self._template_based_generation(topic, context, round_num)
        
        attempts = 0
        while self._is_duplicate_argument(argument) and attempts < 5:
            argument = self._template_based_generation(topic, context, round_num, variation=attempts+1)
            attempts += 1
        
        if self._is_duplicate_argument(argument):
            argument = f"{argument} (Round {round_num} perspective)"
        
        self.previous_arguments.append(argument)
        return argument
    
    def _build_context(self, memory_slice: List[Dict]) -> str:
        if not memory_slice:
            return "No previous arguments."
        
        context_parts = []
        for entry in memory_slice[-3:]:
            context_parts.append(f"Round {entry['round']} - {entry['agent']}: {entry['text'][:100]}...")
        
        return "\n".join(context_parts)
    
    def _template_based_generation(self, topic: str, context: str, round_num: int, variation: int = 0) -> str:
        if self.seed is not None:
            seed_str = f"{self.seed}{round_num}{variation}{self.agent_id}"
            hash_val = int(hashlib.md5(seed_str.encode()).hexdigest(), 16) % 10
        else:
            hash_val = (round_num + variation) % 10
        
        templates = self._get_persona_templates()
        template_idx = hash_val % len(templates)
        
        template = templates[template_idx]
        argument = template.format(
            topic=topic,
            round=round_num,
            agent=self.agent_id,
            persona=self.persona_name
        )
        
        return argument
    
    def _get_persona_templates(self) -> List[str]:
        if self.persona_name.lower() == "scientist":
            return [
                "From a scientific perspective on '{topic}', empirical evidence suggests that we must consider measurable outcomes and reproducible results. Round {round} analysis.",
                "The data regarding '{topic}' indicates that hypothesis-driven approaches yield the most reliable conclusions. Evidence-based reasoning is paramount.",
                "When examining '{topic}' scientifically, we must apply rigorous methodology and control for confounding variables to reach valid conclusions.",
                "Scientific inquiry into '{topic}' demands skepticism and verification through peer-reviewed processes and experimental validation.",
                "Regarding '{topic}', the quantitative analysis reveals patterns that support data-driven decision making over purely theoretical speculation.",
                "From an empirical standpoint on '{topic}', observational studies and controlled experiments provide the foundation for sound reasoning.",
                "The scientific method applied to '{topic}' requires falsifiable hypotheses and systematic testing to establish credible findings.",
                "Analyzing '{topic}' through the lens of evidence-based science, we must prioritize reproducibility and statistical significance.",
                "When we examine '{topic}' scientifically, the empirical record demonstrates clear correlations that warrant further investigation.",
                "Scientific rigor demands that claims about '{topic}' be supported by peer-reviewed research and verifiable experimental data.",
            ]
        elif self.persona_name.lower() == "philosopher":
            return [
                "Philosophically examining '{topic}', we must question the fundamental assumptions underlying our positions and explore the deeper implications. Round {round} reflection.",
                "The ethical dimensions of '{topic}' require us to consider not just outcomes but the principles and values at stake in this debate.",
                "When contemplating '{topic}' from a philosophical perspective, we encounter profound questions about meaning, purpose, and human nature.",
                "The dialectical approach to '{topic}' reveals tensions between competing values that deserve careful philosophical examination.",
                "Regarding '{topic}', we must engage in critical analysis of the logical structure and conceptual coherence of various arguments.",
                "From an epistemological standpoint on '{topic}', we should examine how we know what we claim to know and the limits of our understanding.",
                "The moral philosophy surrounding '{topic}' compels us to consider universal principles versus contextual considerations in ethical reasoning.",
                "Analyzing '{topic}' philosophically, thought experiments illuminate the logical consequences and hidden assumptions in our thinking.",
                "When we philosophically investigate '{topic}', phenomenological analysis reveals the lived experience and subjective dimensions often overlooked.",
                "The philosophical tradition teaches us that '{topic}' involves complex interrelations between metaphysics, ethics, and practical wisdom.",
            ]
        else:
            return [
                "Considering '{topic}', we must examine multiple perspectives to reach a balanced understanding. Round {round}.",
                "The debate on '{topic}' requires careful analysis of both theoretical and practical implications.",
                "When discussing '{topic}', we should acknowledge the complexity and nuance inherent in this subject.",
                "Regarding '{topic}', historical context and contemporary relevance both inform our understanding.",
            ]
    
    def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]:
        topic = state.get("topic", "")
        memory = state.get("memory", [])
        current_round = state.get("current_round", 1)
        
        memory_slice = [entry for entry in memory if entry.get("agent") != self.agent_id]
        
        argument = self.generate_argument(topic, memory_slice, current_round)
        
        return {
            "current_agent": self.agent_id,
            "current_argument": argument,
            "node_execution": {
                "node": self.name,
                "input": {
                    "topic": topic,
                    "round": current_round,
                    "memory_entries": len(memory_slice)
                },
                "output": {
                    "agent": self.agent_id,
                    "argument": argument
                }
            }
        }
