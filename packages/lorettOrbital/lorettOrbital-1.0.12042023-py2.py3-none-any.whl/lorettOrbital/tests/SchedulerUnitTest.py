import unittest
import tempfile

from lorettOrbital.scheduler import Scheduler, SchedulerConfig

class UnitScheduler(unittest.TestCase):
    def setUp(self):
        self.path = tempfile.TemporaryDirectory()
        self.config = SchedulerConfig(lat=55, lon=37, alt=0.1, path=self.path)
        self.scheduler = Scheduler(config=self.config)
    
    
if __name__ == "__main__":
    unittest.main()