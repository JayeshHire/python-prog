from abc import ABC, abstractmethod
import types
import inspect
from enum import Enum


class Helper:

    @classmethod
    def get_obj_vars(Obj):
        if inspect.isclass(type(Obj)):
            attrs = [attr for attr in dir(Obj) if not attr.startswith('__')]
            attrs = [attr for attr in attrs if inspect.ismethod(getattr(Obj, attr))]
            return attrs


class Logistic(ABC):
    
    @classmethod
    def retain_trans_detls(logistics: Logistic, transport: Transport):
        # logistics.vehicle_name = vehicle_name
        # logistics.vehicle_no = vehicle_no
        # logistics.loaded = loaded
        var_attrs = Helper.get_obj_vars(transport)
        for attr in var_attrs:
            setattr(logistics, attr, getattr(transport, attr))

    @classmethod
    def clear_trans_detls(logistics: Logistic):
        var_attrs = Helper.get_obj_vars(transport)
        for attr in var_attrs:
            if attr == 'nt_available':
                continue
            try:
                delattr(logistics, attr)
            except AttributeError:
                continue

    def check_attrs_availability(self):
        self_var_attrs = Helper.get_obj_vars(self)
        trans_var_attrs = [attr['attr_name'] for attrs in self.var_attrs if attrs['type'] not AttrTypeEnum.DefaultValAttr]
        nt_available = [] # not available attributes
        for attr in trans_var_attrs:
            if attr == 'var_attrs':
                continue
            if attr not in self_var_attrs:
                nt_available.append(attr)

        self.nt_available = nt_available

        if not nt_available:
            return True # All attributes are available
        return False # Some attributes are missing

    def deliver(self):
        transport = self.create_transport()
        transport.deliver()

    @abstractmethod
    def create_transport(self):
        pass


class AttrTypeEnum(Enum):
    DefaultValAttr = 0
    NormalAttr = 1


class RoadLogistic(Logistic):
    var_attrs = [{
        "attr_name": "vehicle_no",
        "type": AttrTypeEnum.NormalAttr
    },
    {
        "attr_name": "vehicle_name",
        "type": AttrTypeEnum.NormalAttr
    },
    {
        "attr_name": "capacity",
        "type": AttrTypeEnum.NormalAttr
    },
    {
        "attr_name": "loaded",
        "type": AttrTypeEnum.DefaultValAttr,
        "value": 0
    }]
    transport_cls = Truck

    def create_transport(self):
        # first check all the attributes are available
        # if not available raise exception and ask user to run the retain_attr method first
        # if available create a Transport obj and return
        if not check_attrs_availability(self):
            raise AttributeError("Run the retain_trans_detls method to the transport details for this class")

        attrs = [attr["attr_name"] for attr in self.var_attrs]
        attr_vals = {attr: getattr(self, attr, None) for attr in attrs}
        loaded = 0 if attr_vals['loaded'] is None else attr_vals['loaded']

        return Truck(vehicle_no = attr_vals['vehicle_no'], 
        vehicle_name = attr_vals['vehicle_name'],
        capatity = attr_vals['capacity'],
        loaded = loaded
        )
    

class SeaLogistics(Logistic):
    transport_cls = Ship

    def create_transport(self):
        return Ship('Titanic', 2000)


class Transport(ABC):
    
    @abstractmethod
    def load(self, quantity):
        pass
    
    @abstractmethod
    def unload(self, quantity):
        pass


class Overload(Exception):
    def __init__(self, msg: str):
        self.msg = msg
    
class Underload(Exception):
    def __init__(self, msg):
        self.msg = msg

class Truck(Transport):

    def __init__(self, vehicle_no: str, vehicle_name: str, capacity: int, loaded: int = 0):
        self.vehicle_no = vehicle_no
        self.vehicle_name = vehicle_name
        self.capacity = capacity
        self.loaded = loaded
    
    def load(self, quantity: int):
        if (self.capacity - self.loaded) >= quantity:
            self.loaded += quantity
        else:
            raise Overload(f'Truck is being overloaded remove {self.loaded -quantity} quantities of goods')
    
    def unload(self, quantity: int):
        if self.loaded <= quantity:
            self.loaded -= quantity
        else:
            raise Underload(f'Truck is being underload. It has already been unloaded')


class Ship(Transport):

    def __init__(self, Ship_name: str, capacity: int, loaded: int = 0):
        self.ship_name = ship_name
        self.capacity = capacity
        self.loaded = loaded
    
    def load(self, quantity: int):
        if (self.capacity - self.loaded) >= quantity:
            self.loaded += quantity
        else:
            raise Overload(f'Ship is being overloaded remove {ship.loaded -quantity} quantities of goods')
    
    def unload(self, quantity: int):
        if self.loaded <= quantity:
            self.loaded -= quantity
        else:
            raise Underload(f'Ship is being underload. It has already been unloaded')




def main():

    rl = RoadLogistic()