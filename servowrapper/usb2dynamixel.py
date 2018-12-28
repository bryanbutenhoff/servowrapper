#!/usr/bin/env python

from __future__ import print_function
from functools import partial
from dynamixel_sdk import *

class PortHandlerWrapper():

  def __init__(self, devicename, baudrate):
    self.devicename = devicename
    self.baudrate = baudrate

  def __enter__(self):
    self.portHandler = PortHandler(self.devicename)
    max_timeout = 10
    count = 0
    while (not self.portHandler.openPort()) and (max_timeout >= count):
      print("Failed to open the port.")
      print("Trying again...")
      count += 1
      sleep(1)
    if max_timeout < count:
      print("Timeout on openning the port.")
      raise
    count = 0
    if (not self.portHandler.setBaudRate(self.baudrate)) and (max_timeout >= count):
      print("Failed to change the baudrate")
      print("Trying again...")
      count += 1
      sleep(1)
    if max_timeout < count:
      print("Timeout on setting baudrate.")
      raise
    return self.portHandler

  def __exit__(self, type, value, traceback):
    self.portHandler.closePort()

class Usb2Dynamixel:

  def __init__(self, device_name, baud_rate, protocol_version):
    self.portHandlerWrapper = PortHandlerWrapper(device_name, baud_rate)
    self.packetHandler = PacketHandler(protocol_version)
    self.servo_list = {}

  def add_AX12(self, id):
    self.servo_list[id] = AX12Servo(id, self.portHandlerWrapper, self.packetHandler)

  def execute(self, id, command, data = ''):
    ret_val = self.servo_list[id].execute(command, data)
    print(ret_val)
    return ret_val

class AX12Servo:

  DISABLE_TORQUE = 0
  ENABLE_TORQUE = 1

  ADDR_MX_TORQUE_ENABLE      = 18
  ADDR_MX_GOAL_POSITION      = 30
  ADDR_MX_PRESENT_POSITION   = 36

  DXL_MINIMUM_POSITION_VALUE  = 10
  DXL_MAXIMUM_POSITION_VALUE  = 1000
  DXL_MOVING_STATUS_THRESHOLD = 10

  def __init__(self, id, portHandlerWrapper, packetHandler):
    self.portHandlerWrapper = portHandlerWrapper
    self.packetHandler = packetHandler
    self.DXL_ID = id

  def check_comm_result(self, dxl_comm_result, dxl_error):
    if dxl_comm_result != COMM_SUCCESS:
      print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
      print("%s" % self.packetHandler.getRxPacketError(dxl_error))

  def write_one_byte(self, address, value):
    with self.portHandlerWrapper as portHandler:
      dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(portHandler, self.DXL_ID, address, value)
    self.check_comm_result(dxl_comm_result, dxl_error)

  def write_two_bytes(self, address, value):
    with self.portHandlerWrapper as portHandler:
      dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(portHandler, self.DXL_ID, address, value)
    self.check_comm_result(dxl_comm_result, dxl_error)

  def read_one_bytes(self, address):
    with self.portHandlerWrapper as portHandler:
      dxl_response, dxl_comm_result, dxl_error = self.packetHandler.read1ByteTxRx(portHandler, self.DXL_ID, address)
    self.check_comm_result(dxl_comm_result, dxl_error)
    return dxl_response

  def read_two_bytes(self, address):
    with self.portHandlerWrapper as portHandler:
      dxl_response, dxl_comm_result, dxl_error = self.packetHandler.read2ByteTxRx(portHandler, self.DXL_ID, address)
    self.check_comm_result(dxl_comm_result, dxl_error)
    return dxl_response

  def enable_torque(self):
    self.write_one_byte(self.ADDR_MX_TORQUE_ENABLE, self.ENABLE_TORQUE)

  def disable_torque(self):
    self.write_one_byte(self.ADDR_MX_TORQUE_ENABLE, self.DISABLE_TORQUE)

  def set_goal_position(self, goal_position):
    self.write_two_bytes(self.ADDR_MX_GOAL_POSITION, goal_position)

  def get_present_position(self):
    return self.read_two_bytes(self.ADDR_MX_PRESENT_POSITION)

  def execute(self, command, data):
    if hasattr(data, 'data'):
      command_list = {
        "set_goal_position": self.set_goal_position,
      }
      my_command = command_list.get(command, partial(print, "Unknown method with data: {}".format(data.data)))
      return my_command(data.data)
    else:
      command_list = {
        "enable_torque": self.enable_torque,
        "disable_torque": self.disable_torque,
        "get_present_position": self.get_present_position
      }
      my_command = command_list.get(command, partial(print, "Unknown method"))
      return my_command()
