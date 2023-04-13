"""
Simple access to the g-force linear acceleration, gauss magnetic and dps angular rate sensors of the
LSM9DS0 through I2C for micropython.

Values are normalized to g-force, gauss and degrees per second according to selected sensitivities.

Based on SparkFun 9 Degrees of Freedom IMU Breakout: LSM9DS0.
https://www.sparkfun.com/products/12636

Code by xix xeaon @ XIXIT.

Thanks to Jim Lindblom @ SparkFun Electronics and his SFE_LSM9DS0.cpp letting me know where to start

See usage at the bottom.
"""


G = 0 # Angular rate sensor
WHO_AM_I_G = 0x0F
CTRL_REG1_G = 0x20
CTRL_REG2_G = 0x21
CTRL_REG3_G = 0x22
CTRL_REG4_G = 0x23
CTRL_REG5_G = 0x24
REFERENCE_G = 0x25
STATUS_REG_G = 0x27
OUT_X_L_G = 0x28
OUT_X_H_G = 0x29
OUT_Y_L_G = 0x2A
OUT_Y_H_G = 0x2B
OUT_Z_L_G = 0x2C
OUT_Z_H_G = 0x2D
FIFO_CTRL_REG_G = 0x2E
FIFO_SRC_REG_G = 0x2F
INT1_CFG_G = 0x30
INT1_SRC_G = 0x31
INT1_TSH_XH_G = 0x32
INT1_TSH_XL_G = 0x33
INT1_TSH_YH_G = 0x34
INT1_TSH_YL_G = 0x35
INT1_TSH_ZH_G = 0x36
INT1_TSH_ZL_G = 0x37
INT1_DURATION_G = 0x38


XM = 1 # Linear acceleration and magnetic sensor
OUT_TEMP_L_XM = 0x05
OUT_TEMP_H_XM = 0x06
STATUS_REG_M = 0x07
OUT_X_L_M = 0x08
OUT_X_H_M = 0x09
OUT_Y_L_M = 0x0A
OUT_Y_H_M = 0x0B
OUT_Z_L_M = 0x0C
OUT_Z_H_M = 0x0D
WHO_AM_I_XM = 0x0F
INT_CTRL_REG_M = 0x12
INT_SRC_REG_M = 0x13
INT_THS_L_M = 0x14
INT_THS_H_M = 0x15
OFFSET_X_L_M = 0x16
OFFSET_X_H_M = 0x17
OFFSET_Y_L_M = 0x18
OFFSET_Y_H_M = 0x19
OFFSET_Z_L_M = 0x1A
OFFSET_Z_H_M = 0x1B
REFERENCE_X = 0x1C
REFERENCE_Y = 0x1D
REFERENCE_Z = 0x1E
CTRL_REG0_XM = 0x1F
CTRL_REG1_XM = 0x20
CTRL_REG2_XM = 0x21
CTRL_REG3_XM = 0x22
CTRL_REG4_XM = 0x23
CTRL_REG5_XM = 0x24
CTRL_REG6_XM = 0x25
CTRL_REG7_XM = 0x26
STATUS_REG_A = 0x27
OUT_X_L_A = 0x28
OUT_X_H_A = 0x29
OUT_Y_L_A = 0x2A
OUT_Y_H_A = 0x2B
OUT_Z_L_A = 0x2C
OUT_Z_H_A = 0x2D
FIFO_CTRL_REG = 0x2E
FIFO_SRC_REG = 0x2F
INT_GEN_1_REG = 0x30
INT_GEN_1_SRC = 0x31
INT_GEN_1_THS = 0x32
INT_GEN_1_DURATION = 0x33
INT_GEN_2_REG = 0x34
INT_GEN_2_SRC = 0x35
INT_GEN_2_THS = 0x36
INT_GEN_2_DURATION = 0x37
CLICK_CFG = 0x38
CLICK_SRC = 0x39
CLICK_THS = 0x3A
TIME_LIMIT = 0x3B
TIME_LATENCY = 0x3C
TIME_WINDOW = 0x3D
Act_THS = 0x3E
Act_DUR = 0x3F


# thanks travc @ stackoverflow
def twos_comp(val, bits=8):
	if (val & (1 << (bits - 1))) != 0:
		val = val - (1 << bits)
	return val


class i2c_adapter:
    """This library was written based on an older pyb.I2C interface.
    To make it compatible with the new machine.I2C interface, this
    adapter is provided. -Alden
    """
    def __init__(self, i2c):
        self.i2c = i2c
        
    def mem_write(self, data, addr, memaddr):
        self.i2c.writeto_mem(addr, memaddr, bytes([data]))
        
    def mem_read(self, data, addr, memaddr):
        return self.i2c.readfrom_mem(addr, memaddr, data)
    
    def ensure_compatibility(i2c):
        if i2c is None or hasattr(i2c, 'mem_write'):
            return i2c
        return i2c_adapter(i2c)
        

class LSM9DS0():
	def __init__(self, i2c=None, spi=None, g_sens=None, a_sens=None, m_sens=None, g_addr=0x6B, xm_addr=0x1D):
		if not (i2c or spi):
			raise Exception("must have an i2c or spi object")
		
		self.i2c = i2c_adapter.ensure_compatibility(i2c)
		self.spi = spi
		self.g_addr = g_addr
		self.xm_addr = xm_addr
		if self.spi:
			self.g_addr.high()
			self.xm_addr.high()
		
		# init gyro
		self.write_reg(G, CTRL_REG1_G, 0b00001111)
		self.write_reg(G, CTRL_REG2_G, 0b00000000)
		self.write_reg(G, CTRL_REG3_G, 0b10001000)
		self.write_reg(G, CTRL_REG4_G, 0b00000000)
		self.write_reg(G, CTRL_REG5_G, 0b00000000)
		self.gyro = LSM9DS0.Gyro(self, sens=g_sens)
		
		# init accel
		self.write_reg(XM, CTRL_REG0_XM, 0b00000000)
		self.write_reg(XM, CTRL_REG1_XM, 0b01010111)
		self.write_reg(XM, CTRL_REG2_XM, 0b00000000)
		self.write_reg(XM, CTRL_REG3_XM, 0b00000100)
		self.accel = LSM9DS0.Accel(self, sens=a_sens)
		
		# init mag
		self.write_reg(XM, CTRL_REG4_XM, 0b00000100)
		self.write_reg(XM, CTRL_REG5_XM, 0b10010100)
		self.write_reg(XM, CTRL_REG6_XM, 0b00000000)
		self.write_reg(XM, CTRL_REG7_XM, 0b00000000)
		self.mag = LSM9DS0.Mag(self, sens=m_sens)
	
	def who_am_i(self):
		return (
			self.read_reg(G, WHO_AM_I_G),
			self.read_reg(XM, WHO_AM_I_XM),
		)
	
	def read_reg(self, slave, reg, data=1):
		n_bytes = data if type(data) == int else len(data)
		
		if self.i2c:
			return self.i2c.mem_read(
				data = data,
				addr = self.g_addr if not slave else self.xm_addr,
				memaddr = reg | 0x80 if n_bytes > 1 else reg,
			)
		elif self.spi:
			pin = self.g_addr if not slave else self.xm_addr
			pin.low()
			if n_bytes > 1:
				self.spi.send(0xC0 | reg)
			else:
				self.spi.send(0x80 | reg)
			r = self.spi.recv(data)
			pin.high()
			return r
	
	def write_reg(self, slave, reg, data=0):
		if self.i2c:
			self.i2c.mem_write(
				data = data,
				addr = self.g_addr if not slave else self.xm_addr,
				memaddr = reg,
			)
		elif self.spi:
			pin = self.g_addr if not slave else self.xm_addr
			pin.low()
			self.spi.send(bytes([reg, data]))
			pin.high()
	
	def update_reg(self, slave, reg, value, mask):
		reg_val = self.read_reg(slave, reg)[0]
		reg_new = reg_val & ~mask | value & mask
		self.write_reg(slave, reg, reg_new)
	
	
	class SensorInterface():
		""" these interfaces are intended for simple usage of the device without having to read the device docs """
		sens_bits = {}
		sens_reg = (None, None)
		slave = None
		out_regs = (None, None, None)
		
		def __init__(self, lsm9ds0, sens=None):
			self.lsm9ds0 = lsm9ds0
			self.set_sens(sens)
		
		def x(self):
			b = self.lsm9ds0.read_reg(self.slave, self.out_regs[0], 2)
			return twos_comp(b[1]*256+b[0], 16) * self.sens_bits[self.sens][1]
		
		def y(self):
			b = self.lsm9ds0.read_reg(self.slave, self.out_regs[1], 2)
			return twos_comp(b[1]*256+b[0], 16) * self.sens_bits[self.sens][1]
		
		def z(self):
			b = self.lsm9ds0.read_reg(self.slave, self.out_regs[2], 2)
			return twos_comp(b[1]*256+b[0], 16) * self.sens_bits[self.sens][1]
		
		def all(self):
			b = self.lsm9ds0.read_reg(self.slave, self.out_regs[0], 6)
			return (
				twos_comp(b[1]*256+b[0], 16) * self.sens_bits[self.sens][1],
				twos_comp(b[3]*256+b[2], 16) * self.sens_bits[self.sens][1],
				twos_comp(b[5]*256+b[4], 16) * self.sens_bits[self.sens][1],
			)
		
		def set_sens(self, sens=None):
			if sens is None:
				sens = min(self.sens_bits)
			elif not sens in self.sens_bits:
				raise ValueError('Bad sens: %s for %s; Possible: %s' % (
					sens, self.__class__.__name__, sorted(self.sens_bits.keys())
				))
			self.lsm9ds0.update_reg(self.slave, self.sens_reg[0], self.sens_bits[sens][0] << self.sens_reg[2], self.sens_reg[1])
			self.sens = sens
	
	class Gyro(SensorInterface):
		sens_bits = {
			 245: (0b00,  8.75/1000),
			 500: (0b01, 17.50/1000),
			2000: (0b10, 70.00/1000),
		}
		sens_reg = (CTRL_REG4_G, 0b00110000, 4)
		slave = G
		out_regs = (OUT_X_L_G, OUT_Y_L_G, OUT_Z_L_G)
	
	class Accel(SensorInterface):
		sens_bits = {
			 2: (0b000, 0.061/1000),
			 4: (0b001, 0.122/1000),
			 6: (0b010, 0.183/1000),
			 8: (0b011, 0.244/1000),
			16: (0b100, 0.732/1000),
		}
		sens_reg = (CTRL_REG2_XM, 0b00111000, 3)
		slave = XM
		out_regs = (OUT_X_L_A, OUT_Y_L_A, OUT_Z_L_A)
	
	class Mag(SensorInterface):
		sens_bits = {
			 2: (0b00, 0.08/1000),
			 4: (0b01, 0.16/1000),
			 8: (0b10, 0.32/1000),
			12: (0b11, 0.48/1000),
		}
		sens_reg = (CTRL_REG6_XM, 0b01100000, 5)
		slave = XM
		out_regs = (OUT_X_L_M, OUT_Y_L_M, OUT_Z_L_M)



if __name__ == "__main__":
	import pyb
	
	## SPI mode:
	## physical connections (pyb - LSM9DS0):
	## Y12     - CSG
	## Y11     - CSXM
	## MOSI(1) - SDA
	## MISO(1) - SDOG and SDOXM
	## SCK(1)  - SCL
	#spi = pyb.SPI(1, mode=pyb.SPI.MASTER, baudrate=328125)
	#spi_g = pyb.Pin('Y12', pyb.Pin.OUT_PP)
	#spi_xm = pyb.Pin('Y11', pyb.Pin.OUT_PP)
	#lsm9ds0 = LSM9DS0(spi=spi, g_addr=spi_g, xm_addr=spi_xm, g_sens=500, a_sens=4, m_sens=12)
	
	# I2C mode:
	# physical connections (pyb - LSM9DS0):
	# SDA(2) - SDA
	# SCL(2) - SCL
	i2c = pyb.I2C(2, mode=pyb.I2C.MASTER, baudrate=100000)
	lsm9ds0 = LSM9DS0(i2c=i2c, g_sens=500, a_sens=4, m_sens=12)
	
	g_id, xm_id = lsm9ds0.who_am_i()
	print((g_id, xm_id)) # (b'\xd4', b'I')
	
	pyb.delay(1000)
	
	lsm9ds0.accel.set_sens(16)
	
	while True:
		print(lsm9ds0.accel.all())
		mag_x = lsm9ds0.mag.x()
		gyro_z = lsm9ds0.gyro.z()
		pyb.delay(100)


