import unittest
from nodes.memory_node import MemoryNode


class TestMemoryNode(unittest.TestCase):
    
    def setUp(self):
        self.memory = MemoryNode()
    
    def test_add_entry(self):
        entry = self.memory.add_entry(
            round_num=1,
            agent_id="AgentA",
            text="Test argument",
            metadata={"test": "data"}
        )
        
        self.assertEqual(entry["round"], 1)
        self.assertEqual(entry["agent"], "AgentA")
        self.assertEqual(entry["text"], "Test argument")
        self.assertIn("timestamp", entry)
        self.assertEqual(entry["meta"]["test"], "data")
    
    def test_get_full_memory(self):
        self.memory.add_entry(1, "AgentA", "Arg 1")
        self.memory.add_entry(2, "AgentB", "Arg 2")
        
        full_memory = self.memory.get_full_memory()
        
        self.assertEqual(len(full_memory), 2)
        self.assertEqual(full_memory[0]["agent"], "AgentA")
        self.assertEqual(full_memory[1]["agent"], "AgentB")
    
    def test_get_memory_slice(self):
        self.memory.add_entry(1, "AgentA", "A's first argument")
        self.memory.add_entry(2, "AgentB", "B's first argument")
        self.memory.add_entry(3, "AgentA", "A's second argument")
        
        slice_a = self.memory.get_memory_slice("AgentA")
        self.assertEqual(len(slice_a), 1)
        self.assertEqual(slice_a[0]["agent"], "AgentB")
        
        slice_b = self.memory.get_memory_slice("AgentB")
        self.assertEqual(len(slice_b), 2)
        self.assertTrue(all(e["agent"] == "AgentA" for e in slice_b))
    
    def test_get_memory_for_round(self):
        self.memory.add_entry(1, "AgentA", "Round 1 arg")
        self.memory.add_entry(2, "AgentB", "Round 2 arg")
        self.memory.add_entry(3, "AgentA", "Round 3 arg")
        
        round_2_memory = self.memory.get_memory_for_round(2)
        
        self.assertEqual(len(round_2_memory), 1)
        self.assertEqual(round_2_memory[0]["round"], 2)
    
    def test_serialize(self):
        self.memory.add_entry(1, "AgentA", "Test")
        
        serialized = self.memory.serialize()
        
        self.assertIsInstance(serialized, str)
        self.assertIn("AgentA", serialized)
        self.assertIn("Test", serialized)
    
    def test_memory_updates_after_each_turn(self):
        initial_size = len(self.memory.get_full_memory())
        
        state = {
            "current_round": 1,
            "current_agent": "AgentA",
            "current_argument": "New argument"
        }
        
        result = self.memory(state)
        
        self.assertEqual(len(result["memory"]), initial_size + 1)


if __name__ == '__main__':
    unittest.main()
