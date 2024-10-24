# from typing import Any, Callable

# class CBoard:
#     def __init__(self, usb_pid: int):
#         pass

#     def can1_receive(self, callable: Callable) -> Callable:
#         print("registered")
#         return callable

# cboard = CBoard(0x2345)

# @cboard.can1_receive
# def foo():
#     print("666")

import librmcspy

librmcspy.add(1, 2)


librmcspy.hello_world()
