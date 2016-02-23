import unittest
from Metric import Metric


class TestMetric(unittest.TestCase):

    def test_name(self):
        testMetric = Metric("A")
        self.assertEqual("A",testMetric.Name)

    def test_no_data(self):
        testMetric = Metric("No Data")
        self.assertEqual(0, testMetric.N)
        self.assertEqual(0, testMetric.Sum)
        self.assertEqual(None, testMetric.Max)
        self.assertEqual(None, testMetric.Min)
        self.assertEqual(None, testMetric.Avg)

    def test_add_metric(self):
        testMetric = Metric("A")
        testMetric.addDataPoint(0)
        self.assertEqual(1, testMetric.N)
    
    def test_max(self):
        testMetric = Metric("A")
        testMetric.addDataPoint(0)
        testMetric.addDataPoint(5)
        self.assertEqual(5, testMetric.Max)

    def test_min(self):
        testMetric = Metric("A")
        testMetric.addDataPoint(2)
        testMetric.addDataPoint(8)
        self.assertEqual(2, testMetric.Min)

    def test_avg_same(self):
        testMetric = Metric("A")
        testMetric.addDataPoint(4)
        testMetric.addDataPoint(4)
        testMetric.addDataPoint(4)
        testMetric.addDataPoint(4)
        self.assertEqual(4, testMetric.Avg)

    def test_avg_different(self):
        testMetric = Metric("A")
        testMetric.addDataPoint(16)
        testMetric.addDataPoint(8)
        testMetric.addDataPoint(4)
        testMetric.addDataPoint(4)
        self.assertEqual(8, testMetric.Avg)

    def test_sum(self):
        testMetric = Metric("A")
        testMetric.addDataPoint(1)
        testMetric.addDataPoint(2)
        testMetric.addDataPoint(3)
        testMetric.addDataPoint(4)
        self.assertEqual(10, testMetric.Sum)

    def test_n(self):
        testMetric = Metric("A")
        testMetric.addDataPoint(1)
        testMetric.addDataPoint(1)
        testMetric.addDataPoint(1)
        testMetric.addDataPoint(1)
        testMetric.addDataPoint(1)
        testMetric.addDataPoint(1)
        self.assertEqual(6, testMetric.N)

    def test_RoundToSecondDecimal(self):
        testMetric = Metric("Round to two decimal")
        testMetric.addDataPoint(1.851)
        testMetric.addDataPoint(1.85)
        testMetric.addDataPoint(1.85)
        testMetric.addDataPoint(1.85)
        testMetric.addDataPoint(1.85)
        testMetric.addDataPoint(1.85)
        testMetric.addDataPoint(1.85)
        testMetric.addDataPoint(1.849)
        self.assertEqual(1.85, testMetric.Avg)
        self.assertEqual(1.85, testMetric.Max)
        self.assertEqual(1.85, testMetric.Min)





if __name__ == '__main__':
    unittest.main()