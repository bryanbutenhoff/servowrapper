#!/usr/bin/env python

from __future__ import print_function
from functools import partial
from dynamixel_sdk import *

class Usb2Dynamixel:

  def __init__(self, device_name, baud_rate, protocol_version):
    self.portHandler = PortHandler(device_name)
    self.portHandler.openPort()
    self.portHandler.setBaudRate(baud_rate)
    self.packetHandler = PacketHandler(protocol_version)

  def check_comm_result(self, dxl_comm_result, dxl_error):
    if dxl_comm_result != COMM_SUCCESS:
      print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
      print("%s" % self.packetHandler.getRxPacketError(dxl_error))

  def write_one_byte(self, dxl_id, address, value):
    dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, dxl_id, address, value)
    self.check_comm_result(dxl_comm_result, dxl_error)

  def write_two_bytes(self, dxl_id, address, value):
    dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(self.portHandler, dxl_id, address, value)
    self.check_comm_result(dxl_comm_result, dxl_error)

  def read_one_bytes(self, dxl_id, address):
    dxl_response, dxl_comm_result, dxl_error = self.packetHandler.read1ByteTxRx(self.portHandler, dxl_id, address)
    self.check_comm_result(dxl_comm_result, dxl_error)
    return dxl_response

  def read_two_bytes(self, dxl_id, address):
    dxl_response, dxl_comm_result, dxl_error = self.packetHandler.read2ByteTxRx(self.portHandler, dxl_id, address)
    self.check_comm_result(dxl_comm_result, dxl_error)
    return dxl_response


class AX12Servo:

  ADDR_TORQUE_ENABLE      = 18
  ADDR_GOAL_POSITION      = 30
  ADDR_PRESENT_POSITION   = 36

  def __init__(self, id):
    self.DXL_ID = id

  def enable_torque(self, usb_dynamixel):
    usb_dynamixel.write_one_byte(self.DXL_ID, self.ADDR_TORQUE_ENABLE, 1)

  def disable_torque(self, usb_dynamixel):
    usb_dynamixel.write_one_byte(self.DXL_ID, self.ADDR_TORQUE_ENABLE, 0)

  def set_goal_position(self, usb_dynamixel, goal_position):
    usb_dynamixel.write_two_bytes(self.DXL_ID, self.ADDR_GOAL_POSITION, goal_position)

  def get_present_position(self, usb_dynamixel):
    return usb_dynamixel.read_two_bytes(self.DXL_ID, self.ADDR_PRESENT_POSITION)
