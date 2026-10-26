import unittest
from app import *
class DomainTests(unittest.TestCase):
    def test_constant_field(self):np.testing.assert_allclose(interpolate(np.array([[0.,0.],[1.,1.]]),np.ones((2,3))*4,np.array([[.5,.5]]),.2),4)
    def test_bad_scale(self):
        with self.assertRaises(ValueError):interpolate(np.ones((2,2)),np.ones((2,3)),np.ones((1,2)),0)
    def test_output_shape(self):self.assertEqual(interpolate(np.ones((2,2)),np.ones((2,3)),np.ones((4,2)),.2).shape,(4,3))
