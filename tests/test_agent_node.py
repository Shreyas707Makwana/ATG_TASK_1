import unittest
from nodes.agent_node import AgentNode


class TestAgentNode(unittest.TestCase):
    
    def setUp(self):
        self.agent_a = AgentNode(
            agent_id="AgentA",
            persona_name="scientist",
            seed=42
        )
        self.agent_b = AgentNode(
            agent_id="AgentB",
            persona_name="philosopher",
            seed=42
        )
    
    def test_agent_initialization(self):
        self.assertEqual(self.agent_a.agent_id, "AgentA")
        self.assertEqual(self.agent_a.persona_name, "scientist")
        self.assertEqual(self.agent_a.seed, 42)
    
    def test_similarity_score(self):
        text1 = "This is a test argument"
        text2 = "This is a test argument"
        score = self.agent_a._similarity_score(text1, text2)
        self.assertEqual(score, 1.0)
        
        text3 = "Completely different text"
        score = self.agent_a._similarity_score(text1, text3)
        self.assertLess(score, 0.5)
    
    def test_duplicate_detection(self):
        arg1 = "This is my first argument about science"
        self.agent_a.previous_arguments.append(arg1)
        
        arg2 = "This is my first argument about science"
        self.assertTrue(self.agent_a._is_duplicate_argument(arg2))
        
        arg3 = "Completely different perspective on the matter"
        self.assertFalse(self.agent_a._is_duplicate_argument(arg3))
    
    def test_generate_argument(self):
        topic = "Artificial Intelligence"
        memory_slice = []
        round_num = 1
        
        argument = self.agent_a.generate_argument(topic, memory_slice, round_num)
        
        self.assertIsInstance(argument, str)
        self.assertGreater(len(argument), 0)
        self.assertIn(topic, argument)
    
    def test_deterministic_with_seed(self):
        topic = "Climate Change"
        memory_slice = []
        
        arg1 = self.agent_a.generate_argument(topic, memory_slice, 1)
        
        agent_a_copy = AgentNode(
            agent_id="AgentA",
            persona_name="scientist",
            seed=42
        )
        arg2 = agent_a_copy.generate_argument(topic, memory_slice, 1)
        
        self.assertEqual(arg1, arg2)
    
    def test_call_method(self):
        state = {
            "topic": "Test Topic",
            "memory": [],
            "current_round": 1
        }
        
        result = self.agent_a(state)
        
        self.assertIn("current_agent", result)
        self.assertIn("current_argument", result)
        self.assertEqual(result["current_agent"], "AgentA")


if __name__ == '__main__':
    unittest.main()
