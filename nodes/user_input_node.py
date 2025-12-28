import re
from typing import Dict, Any


class UserInputNode:
    
    MIN_TOPIC_LENGTH = 10
    MAX_TOPIC_LENGTH = 500
    
    def __init__(self):
        self.name = "UserInputNode"
    
    def sanitize_input(self, text: str) -> str:
        sanitized = re.sub(r'[<>{}\\]', '', text)
        sanitized = ' '.join(sanitized.split())
        return sanitized.strip()
    
    def validate_topic(self, topic: str) -> tuple[bool, str]:
        if topic is None or not str(topic).strip():
            return False, "Topic cannot be empty or only whitespace."

        stripped = topic.strip()
        if len(stripped) < self.MIN_TOPIC_LENGTH:
            return False, f"Topic too short. Minimum {self.MIN_TOPIC_LENGTH} characters required."
        
        if len(stripped) > self.MAX_TOPIC_LENGTH:
            return False, f"Topic too long. Maximum {self.MAX_TOPIC_LENGTH} characters allowed."
        
        return True, ""
    
    def get_topic_from_cli(self) -> str:
        while True:
            print("\n" + "="*60)
            print("Enter topic for debate:")
            print(f"(Between {self.MIN_TOPIC_LENGTH}-{self.MAX_TOPIC_LENGTH} characters)")
            print("="*60)
            
            topic = input("> ").strip()
            
            sanitized_topic = self.sanitize_input(topic)
            
            is_valid, error_msg = self.validate_topic(sanitized_topic)
            
            if is_valid:
                print(f"\n✓ Topic accepted: '{sanitized_topic}'")
                return sanitized_topic
            else:
                print(f"\n✗ Invalid topic: {error_msg}")
                print("Please try again.\n")
    
    def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]:
        topic = self.get_topic_from_cli()
        
        return {
            "topic": topic,
            "node_execution": {
                "node": self.name,
                "input": state,
                "output": {"topic": topic}
            }
        }
