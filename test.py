import unittest
import utils.datetimeUtil as datetimeutil
from utils.stockUtil import get_stock_depth

class UnitTest(unittest.TestCase):

    def test_getDateRange(self):
        result = datetimeutil.getDateRange(6)
        print(result)
        #self.assertEqual(result, 6)
    
    def test_get_stock_depth(self):
        stockLTPdict = {'MINDTREE' : 4475.40, 'BALAMINES' : 3822.50}
        stockDepthdict = get_stock_depth(stockLTPdict)
        print('stockDepthdict')
        print(stockDepthdict)
        #self.assertEqual(result, 6)

if __name__ == '__main__':
    unittest.main()