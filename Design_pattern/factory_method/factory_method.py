from abc import ABC, abstractmethod
import types
import inspect
from enum import Enum
from typing import Self


class Helper:

    @classmethod
    def get_obj_vars(cls, Obj):
        if inspect.isclass(type(Obj)):
            attrs = [attr for attr in dir(Obj) if not (attr.startswith('__') or attr.startswith('_'))]
            attrs = [attr for attr in attrs if not inspect.ismethod(getattr(Obj, attr))]
            return attrs


class Transport(ABC):
    
    @abstractmethod
    def load(self, quantity):
        pass
    
    @abstractmethod
    def unload(self, quantity):
        pass
    
    def deliver(self):
        return f"Delivery successfull"


class Logistic(ABC):

    @classmethod
    def retain_trans_detls(cls, logistics: Self, **kwargs):
        var_attrs = [ 
            attr["attr_name"] 
            for attr in logistics.var_attrs 
            if attr["type"].value == 1
            ]
        # for attr in kwargs.keys():
        #     if attr not in var_attrs:
        #         raise Exception(f"Provide a value for {attr}")
        ok_vars = []
        for attr in kwargs.keys():
            if attr in var_attrs:
                ok_vars.append(attr)
        if len(ok_vars) < len(var_attrs):
            raise Exception("some attributes along with their values are missing")

        for attr in var_attrs:
            setattr(logistics, attr, kwargs[attr])

    @classmethod
    def clear_trans_detls(cls, logistics: Self):
        var_attrs = [ attr["attr_name"] for attr in logistics.var_attrs ]
        for attr in var_attrs:
            try:
                delattr(logistics, attr)
            except AttributeError:
                continue

    def check_attrs_availability(self):
        self_var_attrs = Helper.get_obj_vars(self)
        trans_var_attrs = [attrs['attr_name'] for attrs in self.var_attrs if attrs['type'] != AttrTypeEnum.DefaultValAttr]
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



class OverloadErr(Exception):
    def __init__(self, msg: str):
        self.msg = msg
    
class EmptyErr(Exception):
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
            raise OverloadErr(f'Truck is being overloaded remove {quantity} quantities of goods')
    
    def unload(self, quantity: int):
        if self.loaded >= quantity:
            self.loaded -= quantity
        else:
            raise EmptyErr(f'Truck is being EmptyErr. It has already been unloaded')


class Ship(Transport):

    def __init__(self, Ship_name: str, capacity: int, loaded: int = 0):
        self.ship_name = Ship_name
        self.capacity = capacity
        self.loaded = loaded
    
    def load(self, quantity: int):
        if (self.capacity - self.loaded) >= quantity:
            self.loaded += quantity
        else:
            raise OverloadErr(f'Ship is being overloaded remove {quantity} quantities of goods')
    
    def unload(self, quantity: int):
        if self.loaded >= quantity:
            self.loaded -= quantity
        else:
            raise EmptyErr(f'Ship is being EmptyErr. It has already been unloaded')


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
        if not self.check_attrs_availability():
            raise AttributeError("Run the retain_trans_detls method to the transport details for this class")

        attrs = [attr["attr_name"] for attr in self.var_attrs]
        attr_vals = {attr: getattr(self, attr, None) for attr in attrs}
        loaded = 0 if attr_vals.get('loaded', None) is None else attr_vals['loaded']

        return self.transport_cls(vehicle_no = attr_vals['vehicle_no'], 
        vehicle_name = attr_vals['vehicle_name'],
        capacity = attr_vals['capacity'],
        loaded = loaded
        )
    

class SeaLogistics(Logistic):
    var_attrs = [{
        "attr_name": "ship_name",
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
    }
    ]
    transport_cls = Ship

    def create_transport(self):
        if not self.check_attrs_availability():
            raise AttributeError("Run the retain_trans_detls method to the transport details for this class")

        attrs = [attr["attr_name"] for attr in self.var_attrs]
        attr_vals = {attr: getattr(self, attr, None) for attr in attrs}
        loaded = 0 if attr_vals['loaded'] is None else attr_vals['loaded']

        return self.transport_cls(Ship_name = attr_vals['ship_name'],
        capacity = attr_vals['capacity'],
        loaded = loaded
        )


def main():

    rl = Truck(vehicle_name="Malini", vehicle_no="MH.41.AP.8909", capacity=100)
    rl.load(90)
    x = Helper.get_obj_vars(rl)
    print(x)


if __name__ == "__main__":
    main()