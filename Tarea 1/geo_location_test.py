import unittest
from geo_location import Position
from helpers import Distance

class DistanceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.Viña_del_mar = Position(-33.0245, -71.5518, 0)
        cls.Villa_Alemana = Position(-33.0428, -71.3744, 0)
        cls.Treillieres_france = Position(47.333328, -1.63333, 0)  # Alexy
        cls.Moscu = Position(55.755833, 37.617777, 0)
        cls.polo_norte = Position(90.000000, 0.000000, 0)
        cls.polo_sur = Position(-90.000000, 0.000000, 0)
        cls.ecuador = Position(0.000000,0.000000,0)

    @classmethod
    def tearDownClass(cls):
        del cls.Viña_del_mar
        del cls.Villa_Alemana
        del cls.Treillieres_france
        del cls.Moscu
        del cls.polo_norte
        del cls.polo_sur
        del cls.ecuador

    def test_distancia_km(self):
        distance_calculator = Distance(self.Viña_del_mar, self.Villa_Alemana)
        self.assertAlmostEqual(distance_calculator.km(), 16.701 , delta=0.02)

    def test_distancia_nautical(self):
        distance_calculator = Distance(self.Viña_del_mar, self.Moscu)
        self.assertAlmostEqual(distance_calculator.nautical(), 7633.8698704, delta=0.02)

    def test_latitud_invalida(self):
        with self.assertRaises(ValueError) as context:
            Position(90.000001, 0, 0)
        self.assertTrue("Latitude out of range!" in str(context.exception))

    def test_longitud_invalida(self):
        with self.assertRaises(ValueError) as context:
            Position(0, 180.000001, 0)
        self.assertTrue("Longitude out of range!" in str(context.exception))

    def test_latitud_invalida2(self):
        with self.assertRaises(ValueError) as context:
            Position(-90.000001, 0, 0)
        self.assertTrue("Latitude out of range!" in str(context.exception))

    def test_longitud_invalida2(self):
        with self.assertRaises(ValueError) as context:
            Position(0, -180.000001, 0)
        self.assertTrue("Longitude out of range!" in str(context.exception))

    def test_distancia_cero(self):
        distance_calculator = Distance(self.polo_norte, self.polo_norte)
        self.assertAlmostEqual(distance_calculator.km(), 0, delta=0.02)

    def test_valores_frontera(self):
        distance_calculator = Distance(self.polo_norte, self.ecuador)
        self.assertAlmostEqual(distance_calculator.km(),10001.92247, delta=0.02)

    def test_distancia_unidad(self):
        distance_calculator = Distance(self.Viña_del_mar, self.Villa_Alemana)
        self.assertAlmostEqual(distance_calculator.km(), 16.701, delta=0.02)

    def test_unidad_no_valida(self):
        distance_calculator = Distance(self.Treillieres_france, self.Viña_del_mar)
        with self.assertRaises(AttributeError):
            distance_calculator.unit = "millas"
            distance_calculator.km()

if __name__ == '__main__':
    unittest.main()

