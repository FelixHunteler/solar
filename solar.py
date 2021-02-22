import subprocess
from time import strftime
import time
from configobj import ConfigObj
from pymodbus.client.sync import ModbusSerialClient as ModbusClient

# read settings from config file
config = ConfigObj("/boot/pvoutput.txt")
NoInvert = int(config['Inverters'])
t_date = format(strftime('%d%m%Y'))
t_time = format(strftime('%H:%M'))

pv_volts=0.0
pv_power=0.0
Wh_today=0

for i in range(NoInvert):
# Read data from inverter
  inverter = ModbusClient(method='rtu', port='/dev/ttyUSB'+str(i), baudrate=9600, stopbits=1, parity='N', bytesize=8, timeout=1)
  inverter.connect()
  rr = inverter.read_input_registers(1,27)
  inverter.close()
  value=rr.registers[2]
  pv_volts=pv_volts+(float(value)/10)
  value=rr.registers[11]
  pv_power=pv_power+(float(value)/10)
  value=rr.registers[26]
  Wh_today=Wh_today+(float(value)*100)

time.sleep(10)
print '%s' %t_date + ' %s' %t_time
print 'pv_volts %s' %pv_volts
print 'pv_power %s' %pv_power
print 'Wh_today %s' %Wh_today
