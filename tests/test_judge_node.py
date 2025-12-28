import unittest
from nodes.judge_node import JudgeNode


class TestJudgeNode(unittest.TestCase):
    
    def setUp(self):
        self.judge = JudgeNode(seed=42)
    
    def test_analyze_argument_quality(self):
        arguments = [
            "This is a well-reasoned argument about science",
            "Another thoughtful perspective on the matter",
            "A third argument with substantial content"
        ]
        
        analysis = self.judge.analyze_argument_quality(arguments)
        
        self.assertIn("avg_length", analysis)
        self.assertIn("total_arguments", analysis)
        self.assertIn("vocabulary_richness", analysis)
        self.assertIn("consistency_score", analysis)
        self.assertEqual(analysis["total_arguments"], 3)
    
    def test_determine_winner(self):
        memory = [
            {"round": 1, "agent": "AgentA", "text": "First argument from scientist"},
            {"round": 2, "agent": "AgentB", "text": "First argument from philosopher"},
            {"round": 3, "agent": "AgentA", "text": "Second argument from scientist"},
            {"round": 4, "agent": "AgentB", "text": "Second argument from philosopher"},
        ]
        
        verdict = self.judge.determine_winner(memory)
        
        self.assertIn("winner", verdict)
        self.assertIn("confidence", verdict)
        self.assertIn("justification", verdict)
        self.assertIn("final_scores", verdict)
        
        self.assertIn(verdict["winner"], ["AgentA", "AgentB"])
    
    def test_judge_output_format(self):
        memory = [
            {"round": 1, "agent": "AgentA", "text": "Argument A1"},
            {"round": 2, "agent": "AgentB", "text": "Argument B1"},
            {"round": 3, "agent": "AgentA", "text": "Argument A2"},
            {"round": 4, "agent": "AgentB", "text": "Argument B2"},
            {"round": 5, "agent": "AgentA", "text": "Argument A3"},
            {"round": 6, "agent": "AgentB", "text": "Argument B3"},
            {"round": 7, "agent": "AgentA", "text": "Argument A4"},
            {"round": 8, "agent": "AgentB", "text": "Argument B4"},
        ]
        
        state = {
            "memory": memory,
            "topic": "Test Topic"
        }
        
        result = self.judge(state)
        
        self.assertIn("winner", result)
        self.assertIn("winner_confidence", result)
        self.assertIn("winner_justification", result)
        self.assertIn("debate_summary", result)
        self.assertIn("judge_analysis", result)
        
        self.assertGreater(len(result["winner_justification"]), 0)
    
    def test_generate_summary(self):
        memory = [
            {"round": 1, "agent": "AgentA", "text": "First argument"},
            {"round": 2, "agent": "AgentB", "text": "Second argument"},
        ]
        
        summary = self.judge.generate_summary(memory, "Test Topic")
        
        self.assertIn("Test Topic", summary)
        self.assertIn("AgentA", summary)
        self.assertIn("AgentB", summary)
        self.assertIn("First argument", summary)
        self.assertIn("Second argument", summary)
    
    def test_justification_presence(self):
        memory = [
            {"round": 1, "agent": "AgentA", "text": "Science-based argument"},
            {"round": 2, "agent": "AgentB", "text": "Philosophy-based argument"},
            {"round": 3, "agent": "AgentA", "text": "Another scientific point"},
            {"round": 4, "agent": "AgentB", "text": "Another philosophical point"},
        ]
        
        verdict = self.judge.determine_winner(memory)
        justification = verdict["justification"]
        
        self.assertIn("WINNER:", justification)
        self.assertIn("JUSTIFICATION:", justification)
        self.assertGreater(len(justification), 100)


if __name__ == '__main__':
    unittest.main()
