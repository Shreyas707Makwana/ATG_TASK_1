import unittest
from nodes.coordinator_node import CoordinatorNode


class TestCoordinatorNode(unittest.TestCase):
    
    def setUp(self):
        self.coordinator = CoordinatorNode(
            agent_a_id="AgentA",
            agent_b_id="AgentB"
        )
    
    def test_turn_order_generation(self):
        turn_order = self.coordinator.turn_order
        
        self.assertEqual(len(turn_order), 8)
        
        for i, (round_num, agent_id) in enumerate(turn_order, start=1):
            self.assertEqual(round_num, i)
            if i % 2 == 1:
                self.assertEqual(agent_id, "AgentA")
            else:
                self.assertEqual(agent_id, "AgentB")
    
    def test_get_next_agent(self):
        next_turn = self.coordinator.get_next_agent()
        
        self.assertIsNotNone(next_turn)
        self.assertEqual(next_turn, (1, "AgentA"))
    
    def test_advance_turn(self):
        self.coordinator.advance_turn()
        
        next_turn = self.coordinator.get_next_agent()
        self.assertEqual(next_turn, (2, "AgentB"))
    
    def test_validate_turn_correct_order(self):
        is_valid, error = self.coordinator.validate_turn("AgentA", 1)
        self.assertTrue(is_valid)
        self.assertEqual(error, "")
    
    def test_validate_turn_wrong_agent(self):
        is_valid, error = self.coordinator.validate_turn("AgentB", 1)
        self.assertFalse(is_valid)
        self.assertIn("Out of turn", error)
    
    def test_validate_turn_wrong_round(self):
        is_valid, error = self.coordinator.validate_turn("AgentA", 2)
        self.assertFalse(is_valid)
        self.assertIn("Wrong round", error)
    
    def test_turn_enforcement(self):
        is_valid, error = self.coordinator.validate_turn("AgentA", 1)
        self.assertTrue(is_valid)
        
        is_valid, error = self.coordinator.validate_turn("AgentB", 1)
        self.assertFalse(is_valid)
        
        self.coordinator.advance_turn()
        
        is_valid, error = self.coordinator.validate_turn("AgentB", 2)
        self.assertTrue(is_valid)
        
        is_valid, error = self.coordinator.validate_turn("AgentA", 2)
        self.assertFalse(is_valid)
    
    def test_is_debate_complete(self):
        self.assertFalse(self.coordinator.is_debate_complete())
        
        for _ in range(8):
            self.coordinator.advance_turn()
        
        self.assertTrue(self.coordinator.is_debate_complete())
    
    def test_get_debate_status(self):
        status = self.coordinator.get_debate_status()
        
        self.assertEqual(status["total_rounds"], 8)
        self.assertEqual(status["completed_turns"], 0)
        self.assertEqual(status["remaining_turns"], 8)
        self.assertFalse(status["is_complete"])
    
    def test_detect_repeated_arguments(self):
        memory = [
            {"round": 1, "agent": "AgentA", "text": "This is my first argument about science"},
            {"round": 2, "agent": "AgentB", "text": "Philosophy is important"},
            {"round": 3, "agent": "AgentA", "text": "This is my first argument about science"}
        ]
        
        warnings = self.coordinator.detect_repeated_arguments(memory)
        
        self.assertGreater(len(warnings), 0)
        self.assertEqual(warnings[0]["agent"], "AgentA")
    
    def test_check_logical_coherence(self):
        memory = [
            {"round": 1, "agent": "AgentA", "text": "Science is based on empirical evidence"},
            {"round": 2, "agent": "AgentB", "text": "Philosophy examines fundamental assumptions"},
        ]
        
        warnings = self.coordinator.check_logical_coherence(memory)
        
        self.assertIsInstance(warnings, list)


if __name__ == '__main__':
    unittest.main()
