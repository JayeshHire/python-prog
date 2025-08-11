import unittest
from factory_method import *


class TestHelper(unittest.TestCase):

    def test_truck(self):
        truck_attrs = ["capacity", "loaded", "vehicle_name", "vehicle_no"]
        truck = Truck(vehicle_no = "MH.14.AS.9896", vehicle_name = "tata sumo", capacity = 100)
        attrs = Helper.get_obj_vars(truck)
        self.assertListEqual(truck_attrs, 
        attrs, 
        "attributes are not equal"
        )
    
    def test_ship(self):
        ship_attrs = ["capacity", "loaded", "ship_name"]
        ship = Ship(Ship_name = "titanic", capacity = 1230)
        attrs = Helper.get_obj_vars(ship)
        self.assertListEqual(
            ship_attrs,
            attrs,
            "attributes are not equal"
        ) 


class TestTruckFunc(unittest.TestCase):

    def setUp(self):
        self.truck = Truck(vehicle_no = "MH.14.AE.7564",
        vehicle_name = "tata nano", 
        capacity = 100
        )

    def tearDown(self):
        self.truck = None 

    def test_load(self):
        # load the truck
        self.truck.load(80)
        self.assertEqual(self.truck.loaded,
        80
        )

        # increase the load beyond capacity and test 
        # exception
        self.truck.load(20)
        self.assertEqual(self.truck.loaded,
        100)

        with self.assertRaises(OverloadErr):
            self.truck.load(10)

    def test_unload(self):
        self.truck.load(100)

        self.truck.unload(30)
        self.assertEqual(
            self.truck.loaded,
            70
        )

        self.truck.unload(70)
        self.assertEqual(
            self.truck.loaded,
            0
        )

        # check for empty err exception
        with self.assertRaises(EmptyErr):
            self.truck.unload(80)


class TestShipFunc(unittest.TestCase):

    def setUp(self):
        self.ship = Ship(
            Ship_name = "Crz0F",
            capacity = 1000
        )
    
    def tearDown(self):
        self.ship = None

    def test_load(self):
        # load goods
        self.ship.load(700)

        self.assertEqual(
            self.ship.loaded,
            700
        )

        self.ship.load(300)
        self.assertEqual(
            self.ship.loaded,
            1000
        )

        # check for overload err exception
        with self.assertRaises(OverloadErr):
            self.ship.load(100)
        
    def test_unload(self):
        self.ship.load(1000)

        # check unload
        self.ship.unload(300)
        self.assertEqual(
            self.ship.loaded,
            700
        )

        self.ship.unload(700)
        self.assertEqual(
            self.ship.loaded,
            0
        )

        # check for empty err exception
        with self.assertRaises(EmptyErr):
            self.ship.unload(200)
        

class TestLogisticsClsMthds(unittest.TestCase):

    def setUp(self):
        self.rd_logistics = RoadLogistic()
        self.sea_logistics = SeaLogistics()
        self.truck_inp_dict = {
            "vehicle_no": "MH.14.WS.8769",
            "vehicle_name": "Tata sumo",
            "capacity": 100
        }
        self.ship_inp_dict = {
            "ship_name": "titanic",
            "capacity": 1000
        }

    def test_static_methods(self):
        
        # retain transport details for road logistics
        Logistic.retain_trans_detls(
            self.rd_logistics,
            **self.truck_inp_dict
        )
        truck_vars = vars(self.rd_logistics)
        self.assertDictEqual(
            truck_vars,
            self.truck_inp_dict
        )

        # retain transport details for sea logistics
        Logistic.retain_trans_detls(
            self.sea_logistics,
            **self.ship_inp_dict
        )
        ship_vars = vars(self.sea_logistics)
        self.assertDictEqual(
            ship_vars,
            self.ship_inp_dict
        )


class TestFactoryMethod(unittest.TestCase):

    def setUp(self):
        self.rd_logistics = RoadLogistic()
        self.sea_logistics = SeaLogistics()
        self.truck_inp_dict = {
            "vehicle_no": "MH.14.WS.8769",
            "vehicle_name": "Tata sumo",
            "capacity": 100,
            "loaded": 0
        }
        self.ship_inp_dict = {
            "ship_name": "titanic",
            "capacity": 1000,
            "loaded": 0
        }

        Logistic.retain_trans_detls(
            self.rd_logistics,
            **self.truck_inp_dict
        )

        Logistic.retain_trans_detls(
            self.sea_logistics,
            **self.ship_inp_dict
        )
    
    def tearDown(self):
        self.sea_logistics = None
        self.rd_logistics = None

    def test_truck_creation(self):
        truck = self.rd_logistics.create_transport()

        self.assertIsInstance(
            truck,
            Truck
            )
        truck_vars = vars(truck)
        self.assertDictEqual(
            truck_vars,
            self.truck_inp_dict
        )

        ship = self.sea_logistics.create_transport()
        self.assertIsInstance(
            ship,
            Ship
        )
        ship_vars = vars(ship)
        self.assertDictEqual(
            ship_vars,
            self.ship_inp_dict
        )