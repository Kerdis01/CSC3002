import unittest
from unittest.mock import patch

class TestResourceMonitor(unittest.TestCase):
    @patch('src.resource_monitor.psutil.cpu_percent')
    def test_get_cpu_usage(self, mock_cpu_percent):
        mock_cpu_percent.return_value = 55.5
        from src.resource_monitor import get_cpu_usage
        cpu_usage = get_cpu_usage()
        self.assertEqual(cpu_usage, "55.50")

    @patch('src.resource_monitor.subprocess.run')
    def test_get_core_voltage(self, mock_run):
        mock_run.return_value.stdout = "volt=1.2000V"
        from src.resource_monitor import get_core_voltage
        core_voltage = get_core_voltage()
        self.assertEqual(core_voltage, "1.20")

    @patch('src.resource_monitor.subprocess.run')
    def test_get_cpu_temperature(self, mock_run):
        mock_run.return_value.stdout = "temp=42.3'C"
        from src.resource_monitor import get_cpu_temperature
        cpu_temp = get_cpu_temperature()
        self.assertEqual(cpu_temp, "42.30")

if __name__ == '__main__':
    unittest.main()