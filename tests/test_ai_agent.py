
# Unit tests for AI summarizer
import unittest
from backend.ai_agent import summarizer

class TestAISummarizer(unittest.TestCase):

    def test_generate_summary_basic(self):
        input_data = {
            "resource_name": "staging-ec2-01",
            "resource_type": "EC2",
            "usage_data": "Average CPU usage: 5% over 14 days",
            "recommendation": "Downsize to t3.small"
        }
        summary = summarizer.generate_summary(input_data)
        self.assertIn("staging-ec2-01", summary)
        self.assertIn("Downsize to t3.small", summary)

    def test_generate_summary_missing_field(self):
        input_data = {
            "resource_name": "rds-prod-02",
            "usage_data": "Low usage observed",
            "recommendation": "Scale down"
        }
        summary = summarizer.generate_summary(input_data)
        self.assertTrue(isinstance(summary, str))
        self.assertIn("rds-prod-02", summary)

if __name__ == "__main__":
    unittest.main()
