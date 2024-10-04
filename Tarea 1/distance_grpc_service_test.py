import unittest
from google.protobuf.json_format import MessageToJson
from distance_grpc_service import *
import json
import grpc


def test_valid_request(sourcelat, sourcelon, destinationlat, destinationlon, unit):

    with grpc.insecure_channel("localhost:50051") as channel:
        stub = pb2_grpc.DistanceServiceStub(channel)

        message = pb2.SourceDest(
            source=pb2.Position(
                latitude=sourcelat, longitude=sourcelon
            ),
            destination=pb2.Position(
                latitude=destinationlat, longitude=destinationlon
            ),
            unit=unit
        )

        print(f"Message sent:\n{MessageToJson(message)}\n")

        response = stub.geodesic_distance(message)

        try:
            return json.loads(MessageToJson(response))
        except KeyError:
            print("One or more keys are missing!")

class DistanceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.Viña_del_mar = Position(-33.0245, -71.5518, 0)
        cls.Villa_Alemana = Position(-33.0428, -71.3744, 0)
        cls.Treillieres_france = Position(47.333328, -1.63333, 0)  # Alexy
        cls.Moscu = Position(55.755833, 37.617777, 0)
        cls.polo_norte = Position(90.000000, 0.000000, 0)
        cls.polo_sur = Position(-90.000000, 0.000000, 0)
        cls.ecuador = Position(0.000000, 0.000000, 0)

    @classmethod
    def tearDownClass(cls):
        del cls.Viña_del_mar
        del cls.Villa_Alemana
        del cls.Treillieres_france
        del cls.Moscu
        del cls.polo_norte
        del cls.polo_sur

    def test_defaultUnit(self):
        result = test_valid_request(self.Viña_del_mar._latitude, self.Viña_del_mar._longitude, self.Moscu._latitude, self.Moscu._longitude,  "")
        self.assertEqual(result["unit"], "km")
        self.assertAlmostEqual(result["distance"], 7633.8698704, delta=0.02)

    def test_invalid_input(self):
        result = test_valid_request(100, 200, -10, -200, "km")
        self.assertEqual(result["distance"], -1.0)
        self.assertEqual(result["unit"], "invalid")
        print(result["distance"])
        print(result["unit"])



if __name__ == '__main__':
    unittest.main()