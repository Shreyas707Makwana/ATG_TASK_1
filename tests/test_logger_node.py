import unittest
import os
import json
from nodes.logger_node import LoggerNode


class TestLoggerNode(unittest.TestCase):
    
    def setUp(self):
        self.test_log_path = "test_debate_log.jsonl"
        self.logger = LoggerNode(log_path=self.test_log_path)
    
    def tearDown(self):
        if os.path.exists(self.test_log_path):
            os.remove(self.test_log_path)
    
    def test_logger_initialization(self):
        self.assertEqual(self.logger.log_path, self.test_log_path)
        self.assertEqual(len(self.logger.log_entries), 0)
    
    def test_log_entry(self):
        data = {"test": "data", "value": 123}
        self.logger.log("test_entry", data)
        
        self.assertEqual(len(self.logger.log_entries), 1)
        entry = self.logger.log_entries[0]
        
        self.assertEqual(entry["type"], "test_entry")
        self.assertEqual(entry["data"], data)
        self.assertIn("timestamp", entry)
    
    def test_log_node_execution(self):
        node_execution = {
            "node": "TestNode",
            "input": {"key": "value"},
            "output": {"result": "success"}
        }
        
        self.logger.log_node_execution(node_execution)
        
        self.assertEqual(len(self.logger.log_entries), 1)
        self.assertEqual(self.logger.log_entries[0]["type"], "node_execution")
    
    def test_log_memory_snapshot(self):
        memory = [
            {"round": 1, "agent": "AgentA", "text": "Test argument"}
        ]
        
        self.logger.log_memory_snapshot(memory)
        
        self.assertEqual(len(self.logger.log_entries), 1)
        entry = self.logger.log_entries[0]
        self.assertEqual(entry["type"], "memory_snapshot")
        self.assertEqual(entry["data"]["total_entries"], 1)
    
    def test_log_final_verdict(self):
        verdict = {
            "winner": "AgentA",
            "confidence": 0.85,
            "justification": "AgentA won because..."
        }
        
        self.logger.log_final_verdict(verdict)
        
        self.assertEqual(len(self.logger.log_entries), 1)
        self.assertEqual(self.logger.log_entries[0]["type"], "final_verdict")
    
    def test_log_error(self):
        self.logger.log_error("TestError", "Something went wrong", {"detail": "info"})
        
        entry = self.logger.log_entries[0]
        self.assertEqual(entry["type"], "error")
        self.assertEqual(entry["data"]["error_type"], "TestError")
    
    def test_log_warning(self):
        self.logger.log_warning("TestWarning", "Warning message", {"detail": "info"})
        
        entry = self.logger.log_entries[0]
        self.assertEqual(entry["type"], "warning")
        self.assertEqual(entry["data"]["warning_type"], "TestWarning")
    
    def test_log_file_creation(self):
        self.logger.log("test1", {"data": "first"})
        self.logger.log("test2", {"data": "second"})
        
        self.assertTrue(os.path.exists(self.test_log_path))
        
        with open(self.test_log_path, 'r') as f:
            lines = f.readlines()
        
        self.assertEqual(len(lines), 2)
        
        for line in lines:
            entry = json.loads(line)
            self.assertIn("timestamp", entry)
            self.assertIn("type", entry)
            self.assertIn("data", entry)
    
    def test_get_all_logs(self):
        self.logger.log("entry1", {"data": 1})
        self.logger.log("entry2", {"data": 2})
        
        all_logs = self.logger.get_all_logs()
        
        self.assertEqual(len(all_logs), 2)
        self.assertEqual(all_logs[0]["data"]["data"], 1)
        self.assertEqual(all_logs[1]["data"]["data"], 2)


if __name__ == '__main__':
    unittest.main()
