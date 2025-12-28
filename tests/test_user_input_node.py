import unittest
from nodes.user_input_node import UserInputNode


class TestUserInputNode(unittest.TestCase):
    
    def setUp(self):
        self.node = UserInputNode()
    
    def test_sanitize_input(self):
        result = self.node.sanitize_input("Test <script>alert('xss')</script>")
        self.assertNotIn('<', result)
        self.assertNotIn('>', result)
        
        result = self.node.sanitize_input("Test   multiple    spaces")
        self.assertEqual(result, "Test multiple spaces")
    
    def test_validate_topic_too_short(self):
        is_valid, error = self.node.validate_topic("short")
        self.assertFalse(is_valid)
        self.assertIn("too short", error.lower())
    
    def test_validate_topic_too_long(self):
        long_topic = "a" * 501
        is_valid, error = self.node.validate_topic(long_topic)
        self.assertFalse(is_valid)
        self.assertIn("too long", error.lower())
    
    def test_validate_topic_valid(self):
        is_valid, error = self.node.validate_topic("This is a valid debate topic")
        self.assertTrue(is_valid)
        self.assertEqual(error, "")
    
    def test_validate_topic_empty(self):
        is_valid, error = self.node.validate_topic("   ")
        self.assertFalse(is_valid)
        self.assertIn("empty", error.lower())


if __name__ == '__main__':
    unittest.main()
