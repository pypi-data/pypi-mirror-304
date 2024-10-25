from enum import Enum
import ftd2xx
import time
import json
from pyorcai2c.utils import find, every

MILLISECOND = 0.001

I2C_CLOCK_DIVISOR = 29
BUFFON_SCLH_SDAH = [0x80, 0xC3, 0xC3]
BUFFON_SCLH_SDAL = [0x80, 0xC1, 0xC3]
BUFFON_SCLL_SDAL = [0x80, 0xC0, 0xC3]
BUFFON_SCLL_SDAH = [0x80, 0xC2, 0xC3]
BUFOFF_SCLL_SDAL = [0x80, 0x00, 0xC0]
BUFOFF_SCLH_SDAH = [0x80, 0x03, 0xC0]
SCLL_SDAHIZ = [0x80, 0x80, 0xC1]
CLOCK_ONLY = [0x8E, 0x00]
CLOCK8 = [0x20, 0x00, 0x00]
START_BIT = BUFFON_SCLH_SDAH+BUFFON_SCLH_SDAL+BUFFON_SCLL_SDAL
STOP_BIT = BUFFON_SCLL_SDAL+BUFFON_SCLH_SDAL+BUFFON_SCLH_SDAH+BUFOFF_SCLH_SDAH

class i2c_response_attribute(Enum):
    ACKS = 'acks'
    DATA = 'data'

class regmap_info:
    def __init__(self, register_names, fields_names):
            self.register_names = register_names
            self.fields_names = fields_names
class i2c_response:
    def __init__(self, acks=None, data=None):
        self.acks = acks if acks else dict()
        self.data = data if data else dict()

    def flatten(self, attribute = None):
        if(attribute):
            if not isinstance(filter, i2c_response_attribute):
                raise TypeError(f'filter must be an instance of i2c_response_filter Enum\npossible alternatives are {list(map(lambda a: a.value, i2c_response_attribute))}')
            else:
                return getattr(self, attribute.value).values()
        else:
            dictionaries = list(filter(lambda a: isinstance(getattr(self, a), dict), dir(self))) 
            return map(lambda d: d.values(), dictionaries)

class ftdi:
    def __init__(self, serial_number, clock_divisor = I2C_CLOCK_DIVISOR):
        self.com = ftd2xx.openEx(serial_number)
        # MPSSE enable
        self.com.setBitMode(0, 2) #Set bit mode = MPSSE
        time.sleep(10*MILLISECOND)
        # Clock divisor setting
        byte_high = clock_divisor // 256
        byte_low = clock_divisor % 256
        self._write([0x86, byte_low, byte_high])    
        # Init SDA and SCL pins
        # for the SDA, SCL buffered board you need to setup SDA and SCL before turning on the buffers to avoid glitches
        self._write([0x80, 0x03, 0xFB])
        self._write([0x80, 0xC3, 0xFB])
        #Disable Clock Divide by 5
        self._write([0x8A])
        #Enable Three Phase Clock
        self._write([0x8C])

    def close(self):
        self.com.close()

    def _write(self, data):
        s = bytes(data)
        return(self.com.write(s))

    def _read(self, nbytes):
        s = self.com.read(nbytes)
        return [ord(c) for c in s] if type(s) is str else list(s)
    
    def _build_send_byte(self, data):
        prefix = [0x11, 0x00, 0x00]
        read_ack = [0x22, 0x00]
        drive_sda_anaing_with_scl_Low = [0x80, 0xC2, 0xC3]
        byte_array = prefix + [data] + SCLL_SDAHIZ + read_ack + drive_sda_anaing_with_scl_Low
        return(byte_array)   

    def _build_read_byte(self, n):   
        byte_array = []
        for i in range (n):
            if  i + 1 == n:           
                byte_array += SCLL_SDAHIZ + CLOCK8 + CLOCK_ONLY + STOP_BIT
            else:           
                byte_array += SCLL_SDAHIZ + CLOCK8+ BUFFON_SCLL_SDAL + CLOCK_ONLY
        return(byte_array)
    
    def _evaluate_ack(self, a):
        return (a % 2) == 0

    def _i2c_write(self, slave:int, register:int=None, data:int|list=None):
        byte_array = START_BIT + self._build_send_byte(slave) 
        if register:
             byte_array += self._build_send_byte(register)
        if isinstance(data, list):
            n = len(data)
            for i in range(n):
                byte_array += self._build_send_byte(data[i])
        elif isinstance(data, int):
                byte_array += self._build_send_byte(data)
                n = 1
        else:
            n = 0
        byte_array += STOP_BIT
        self._write(byte_array)
        n_acks = 1 + (1 if register else 0) + n
        acks = self._read(n_acks)
        res = i2c_response()
        for i, a in enumerate(acks):
            ack = self._evaluate_ack(a)
            if i == 0:
                res.acks['slave'] = ack
            elif i == 1:
                res.acks['register'] = ack
            else:
                res.acks[f'data_{i-2}'] = ack
        return(res)

    def _i2c_read(self, slave:int, register:int, n:int):
        read_slave = slave + 1 if slave % 2 == 0 else slave
        byte_array = START_BIT + self._build_send_byte(slave) + self._build_send_byte(register) + START_BIT + self._build_send_byte(read_slave)
        byte_array += self._build_read_byte(n)
        self._write(byte_array)
        data = self._read(3 + n)
        res = i2c_response()
        for i, a in enumerate(data):
            ack = self._evaluate_ack(a)
            if i == 0:
                res.acks['slave'] = ack
            elif i == 1:
                res.acks['register'] = ack
            elif i == 2:
                res.acks[f'read_slave'] = ack
            else:
                res.data[register + i - 3] = data[i]
        return res
    
    def _retrieve_regmap_info(self):
        if(self.regmap):
            register_names = [r for r in self.regmap.keys()]
            fields_names = [f for fields in map(lambda r: r[1]['fields'].keys() , self.regmap.items()) for f in fields]
            return regmap_info(register_names=register_names, fields_names=fields_names)
        else:
            raise Exception('Error: register map is not loaded')

    
    def _generate_field_mask(self, offset, size):
        mask =''.join(map(lambda i: '1' if (i < 8 - offset) and (i > 8 - offset - size) else '0', range(8)))
        return int(f'0b{mask}', 2)
    
    def _find_register_from_field(self, field):
        register = find(lambda r: field in r['fields'].keys()  , self.regmap.values())
        return register

    
    def _i2c_write_field(self, slave, field, data):
        if(not isinstance(data, int)):
            raise TypeError("data agument of _i2c_write_field must be an integer NUMBER")
        register = self._find_register_from_field(field)
        address = register['address']
        if(register['fields'][field]['size'] < 8):
            read = self._i2c_read(slave=slave, register=address, n=1)
            if every(lambda a: a, read.acks):
                binaryData = bin(data)
                slicedData = binaryData[0: register['fields'][field]['size']]
                shiftedData = int(slicedData, 2) << register['fields'][field]['offset']
                mask = self._generate_field_mask(register['fields'][field]['offset'], register['fields'][field]['size'])
                fieldData = mask & shiftedData
                sideData = (~mask & list(read.data.values())[0])
                newData = fieldData + sideData
                res = self._i2c_write(slave=slave, register=address, data=newData)
            else:
                raise Exception("Internal Error: NACK on _i2c_read of READ-MODIFY_WRITE operation during an _i2c_write_field")
        else:
            res = self._i2c_write(slave=slave, register=address, data=data)
        return res
    
    def _i2c_read_field(self, slave, field):
        register = self._find_register_from_field(field)
        address = register['address']
        read = self._i2c_read(slave=slave, register=address, n=1)
        mask = self._generate_field_mask(register['fields'][field]['offset'], register['fields'][field]['size'])
        fieldData = mask & list(read.data.values())[0]
        zero_based_data = fieldData >> register['fields'][field]['offset']
        res = i2c_response(acks=read.acks, data=zero_based_data)
        return res
    
    def load_register_map(self, filepath:str):
        regmap = None
        try:            
            with open(filepath, 'r') as file:
                regmap = json.load(file)
        except Exception as error:
            print("An exception occurred:", error)
        finally:
            self.regmap = regmap
            return regmap
        
    def write(self, slave:int, target:str|int=None, data:int|list=None):
        if(target is None or isinstance(target, int)):
            res = self._i2c_write(slave=slave, register=target, data=data)
        else:
            regmap_info = self._retrieve_regmap_info()
            if(target in regmap_info.register_names):
                address = self.regmap[target]['address']
                res = self._i2c_write(slave=slave, register=address, data=data)
            elif(target in regmap_info.fields_names):
                res = self._i2c_write_field(slave=slave, field=target, data=data)
            else:
                raise Exception(f'Error: attempting to read {target} but that is not found in the loaded register map')
        return res
    
    def read(self, slave:int, target:str|int, n:int=1):
        if(isinstance(target, int)):
            res = self._i2c_read(slave=slave, register=target, n=n)
        else:
            regmap_info = self._retrieve_regmap_info()
            if(target in regmap_info.register_names):
                address = self.regmap[target]['address']
                res = self._i2c_read(slave=slave, register=address, n=n)
            elif(target in regmap_info.fields_names):
                res = self._i2c_read_field(slave=slave, field=target)
            else:
                raise Exception(f'Error: attempting to read {target} but that is not found in the loaded register map')
        return res



