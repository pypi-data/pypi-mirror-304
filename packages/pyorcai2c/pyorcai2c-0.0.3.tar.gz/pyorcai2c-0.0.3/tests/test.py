import os, sys
import unittest
import random

cwd = os.getcwd()
sys.path.insert(0, f'{cwd}')
from pyorcai2c.pyorcai2c import ftdi
import pyorcai2c.utils as u

unittest.TestLoader.sortTestMethodsUsing = None

# you need to know the serial number of the FTDI board you are using and provide it to the module
# import ftd2xx
# available_devices = ftd2xx.createDeviceInfoList()
# available_devices = ftd2xx.listDevices()
i2c = ftdi(b'DD290424A')
slave = None
regmap = None

class TestGenericI2cComms(unittest.TestCase):

    def test_00_i2c_bus_scan(self):
        global slave
        scanned = []
        for i in range(0,256,2):
            scanned += [i2c.write(slave=i)]
        acked = u.findIndex(lambda r: r.acks['slave'], scanned)
        self.assertEqual(len(scanned), 256/2)
        self.assertTrue(acked)
        slave = acked*2

    def test_01_i2c_command(self): 
        res = i2c.write(slave=slave, target=random.choice(range(256)))
        self.assertTrue(res.acks['slave'])
        self.assertTrue(res.acks['register'])

    def test_02_i2c_write(self):
        res = i2c.write(slave=slave, target=random.choice(range(256)), data=random.choice(range(256)))
        self.assertTrue(res.acks['slave'])
        self.assertTrue(res.acks['register'])
        self.assertTrue(res.acks['data_0'])

    def test_03_i2c_burst_write(self):
        register = random.choice(range(256))
        data = list(map(lambda x: random.randrange(0, 256), list(range(register, random.randrange(register, 256)))))
        res = i2c.write(slave=slave, target=register, data=data)
        self.assertTrue(res.acks['slave'])
        self.assertTrue(res.acks['register'])
        for i in range(len(data)):
            self.assertTrue(res.acks[f'data_{i}'])
    
    def test_04_i2c_read(self):
        register = random.choice(range(256))
        res = i2c.read(slave=slave, target=register, n=1)
        self.assertTrue(res.acks['slave'])
        self.assertTrue(res.acks['register'])
        self.assertTrue(res.acks['read_slave'])
        self.assertTrue(isinstance(res.data, dict))
        self.assertEqual(len(res.data), 1)
        self.assertEqual(list(res.data.keys())[0], register)
        self.assertTrue(isinstance(list(res.data.values())[0], int))
    
    def test_05_i2c_burst_read(self):
        register = random.choice(range(256))
        n = random.randrange(register, 256) - register
        res = i2c.read(slave=slave, target=register, n=n)
        self.assertTrue(res.acks['slave'])
        self.assertTrue(res.acks['register'])
        self.assertTrue(res.acks['read_slave'])
        self.assertTrue(isinstance(res.data, dict))
        self.assertEqual(len(res.data), n)
        for i in range(n):
            self.assertEqual(list(res.data.keys())[i], register + i)
            self.assertTrue(isinstance(list(res.data.values())[i], int))

    def test_06_load_register_map(self):
        regmap_filepath = os.path.join(cwd, 'regmaps', 'pmic01.json')
        regmap = i2c.load_register_map(regmap_filepath)
        self.assertTrue(regmap)
        self.assertTrue(i2c.regmap)
        self.assertTrue(isinstance(regmap, dict))
        self.assertTrue(isinstance(i2c.regmap, dict))


    def test_07_i2c_regbased_write(self):
        register = random.choice(list(i2c.regmap.keys()))
        res = i2c.write(slave=slave, target=register, data=random.choice(range(256)))
        self.assertTrue(res.acks['slave'])
        self.assertTrue(res.acks['register'])
        self.assertTrue(res.acks['data_0'])

    def test_08_i2c_regbased_burst_write(self):
        register = random.choice(list(i2c.regmap.keys()))
        address = i2c.regmap[register]['address']
        data = list(map(lambda x: random.randrange(0, 256), list(range(address, random.randrange(address, 256)))))
        res = i2c.write(slave=slave, target=register, data=data)
        self.assertTrue(res.acks['slave'])
        self.assertTrue(res.acks['register'])
        for i in range(len(data)):
            self.assertTrue(res.acks[f'data_{i}'])

    def test_09_i2c_fieldbased_write(self):        
        register = random.choice(list(i2c.regmap.keys()))
        field = random.choice(list(i2c.regmap[register]['fields'].keys()))
        res = i2c.write(slave=slave, target=field, data=random.choice(range(256)))
        self.assertTrue(res.acks['slave'])
        self.assertTrue(res.acks['register'])
        self.assertTrue(res.acks['data_0'])
    
if __name__ == '__main__':
    unittest.main()