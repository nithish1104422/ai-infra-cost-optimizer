
# Unit tests for cost analysis

import unittest
from backend.services import aws_scanner

class TestAWSCostScanner(unittest.TestCase):

    def test_detect_idle_instance(self):
        instance_metrics = {
            "InstanceId": "i-1234567890abcdef0",
            "AverageCPUUtilization": 3.2
        }
        is_idle = aws_scanner.is_instance_idle(instance_metrics)
        self.assertTrue(is_idle)

    def test_detect_active_instance(self):
        instance_metrics = {
            "InstanceId": "i-0987654321fedcba0",
            "AverageCPUUtilization": 45.7
        }
        is_idle = aws_scanner.is_instance_idle(instance_metrics)
        self.assertFalse(is_idle)

if __name__ == '__main__':
    unittest.main()
