import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from nodes import (
    AgentNode,
    MemoryNode,
    CoordinatorNode,
    JudgeNode,
    LoggerNode
)


class TestIntegration(unittest.TestCase):
    
    def setUp(self):
        self.seed = 42
        self.test_log_path = "test_integration_log.jsonl"
        
        self.agent_a = AgentNode("AgentA", "scientist", seed=self.seed)
        self.agent_b = AgentNode("AgentB", "philosopher", seed=self.seed)
        self.memory = MemoryNode()
        self.coordinator = CoordinatorNode("AgentA", "AgentB")
        self.judge = JudgeNode(seed=self.seed)
        self.logger = LoggerNode(log_path=self.test_log_path)
    
    def tearDown(self):
        if os.path.exists(self.test_log_path):
            os.remove(self.test_log_path)
    
    def test_complete_debate_flow(self):
        topic = "The role of artificial intelligence in society"
        
        for round_num in range(1, 9):
            next_turn = self.coordinator.get_next_agent()
            self.assertIsNotNone(next_turn)
            
            expected_round, expected_agent = next_turn
            self.assertEqual(expected_round, round_num)
            
            is_valid, error = self.coordinator.validate_turn(expected_agent, round_num)
            self.assertTrue(is_valid, f"Turn validation failed: {error}")
            
            if expected_agent == "AgentA":
                agent = self.agent_a
            else:
                agent = self.agent_b
            
            memory_slice = self.memory.get_memory_slice(expected_agent)
            argument = agent.generate_argument(topic, memory_slice, round_num)
            
            self.memory.add_entry(round_num, expected_agent, argument)
            
            self.logger.log_node_execution({
                "node": f"{expected_agent}Node",
                "round": round_num,
                "argument_length": len(argument)
            })
            
            self.coordinator.advance_turn()
        
        self.assertTrue(self.coordinator.is_debate_complete())
        
        full_memory = self.memory.get_full_memory()
        self.assertEqual(len(full_memory), 8)
        
        verdict = self.judge.determine_winner(full_memory)
        
        self.assertIn("winner", verdict)
        self.assertIn("confidence", verdict)
        self.assertIn("justification", verdict)
        self.assertIn(verdict["winner"], ["AgentA", "AgentB"])
        
        self.logger.log_final_verdict(verdict)
        
        self.assertTrue(os.path.exists(self.test_log_path))
    
    def test_reproducible_with_fixed_seed(self):
        topic = "Climate change and technology"
        
        arguments_run1 = []
        for round_num in range(1, 9):
            next_turn = self.coordinator.get_next_agent()
            _, expected_agent = next_turn
            
            if expected_agent == "AgentA":
                agent = self.agent_a
            else:
                agent = self.agent_b
            
            memory_slice = self.memory.get_memory_slice(expected_agent)
            argument = agent.generate_argument(topic, memory_slice, round_num)
            arguments_run1.append(argument)
            
            self.memory.add_entry(round_num, expected_agent, argument)
            self.coordinator.advance_turn()
        
        agent_a2 = AgentNode("AgentA", "scientist", seed=self.seed)
        agent_b2 = AgentNode("AgentB", "philosopher", seed=self.seed)
        memory2 = MemoryNode()
        coordinator2 = CoordinatorNode("AgentA", "AgentB")
        
        arguments_run2 = []
        for round_num in range(1, 9):
            next_turn = coordinator2.get_next_agent()
            _, expected_agent = next_turn
            
            if expected_agent == "AgentA":
                agent = agent_a2
            else:
                agent = agent_b2
            
            memory_slice = memory2.get_memory_slice(expected_agent)
            argument = agent.generate_argument(topic, memory_slice, round_num)
            arguments_run2.append(argument)
            
            memory2.add_entry(round_num, expected_agent, argument)
            coordinator2.advance_turn()
        
        self.assertEqual(arguments_run1, arguments_run2)
    
    def test_turn_enforcement_failure(self):
        next_turn = self.coordinator.get_next_agent()
        self.assertEqual(next_turn, (1, "AgentA"))
        
        is_valid, error = self.coordinator.validate_turn("AgentB", 1)
        self.assertFalse(is_valid)
        self.assertIn("Out of turn", error)
        
        is_valid, error = self.coordinator.validate_turn("AgentA", 2)
        self.assertFalse(is_valid)
        self.assertIn("Wrong round", error)
    
    def test_no_duplicate_arguments(self):
        topic = "Test topic for duplicates"
        
        arg1 = self.agent_a.generate_argument(topic, [], 1)
        
        self.assertIn(arg1, self.agent_a.previous_arguments)
        
        is_duplicate = self.agent_a._is_duplicate_argument(arg1)
        self.assertTrue(is_duplicate)
        
        different_arg = "This is a completely different argument with unique content"
        is_duplicate = self.agent_a._is_duplicate_argument(different_arg)
        self.assertFalse(is_duplicate)


if __name__ == '__main__':
    unittest.main()
