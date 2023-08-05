# -*- coding: utf-8 -*-

from .process import Process
from .win32.enum import ProcessOperations
from .win32.functions import CloseProcessHandle, GetProcessHandle, ReadProcessMemory, WriteProcessMemory

from typing import Optional, Type, TypeVar, Union


T = TypeVar("T")


class OpenProcess(object):
    """
    Class to open a process for reading or writing memory.
    """
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()

    def __init__(
        self,
        *,
        window_title: Optional[str] = None,
        process_name: Optional[str] = None,
        pid: Optional[int] = None,
        permission: ProcessOperations = ProcessOperations.PROCESS_ALL_ACCESS
    ):
        """
        :param window_title: window title of the target program.
        :param process_name: name of the target process.
        :param pid: process ID.
        :param permission: access mode to the process.
        """
        # Instantiate the permission argument.
        self.__permission = permission

        # Create a Process instance.
        self.__process = Process()

        # Set the attributes to the process.
        if pid:
            self.__process.pid = pid

        elif window_title:
            self.__process.window_title = window_title

        elif process_name:
            self.__process.process_name = process_name

        else:
            raise TypeError("You must pass an argument to one of these parameters (window_title, process_name, pid).")

        # Get the process handle.
        self.__process_handle = GetProcessHandle(self.__permission.value, False, self.__process.pid)

    def close(self):
        """
        Close the process handle.
        """
        return CloseProcessHandle(self.__process_handle)

    def read_process_memory(
        self,
        address: int,
        pytype: Type[T],
        bufflength: int
    ) -> T:
        """
        Return a value from a memory address.

        :param address: target memory address (ex: 0x006A9EC0).
        :param pytype: type of the value to be received (str, int or float).
        :param bufflength: value size in bytes (1, 2, 4, 8).
        """
        valid_permissions = [
            ProcessOperations.PROCESS_ALL_ACCESS.value,
            ProcessOperations.PROCESS_VM_READ.value
        ]
        if self.__permission.value not in valid_permissions:
            raise PermissionError("The handle does not have permission to read the process memory.")

        return ReadProcessMemory(self.__process_handle, address, pytype, bufflength)

    def write_process_memory(
        self,
        address: int,
        pytype: Type[T],
        bufflength: int,
        value: Union[str, int, float]
    ) -> T:
        """
        Write a value to a memory address.

        :param address: target memory address (ex: 0x006A9EC0).
        :param pytype: type of value to be written into memory (str, int or float).
        :param bufflength: value size in bytes (1, 2, 4, 8).
        :param value: value to be written (str, int or float).
        """
        valid_permissions = [
            ProcessOperations.PROCESS_ALL_ACCESS.value,
            ProcessOperations.PROCESS_VM_OPERATION.value | ProcessOperations.PROCESS_VM_WRITE.value
        ]
        if self.__permission.value not in valid_permissions:
            raise PermissionError("The handle does not have permission to write to the process memory.")

        return WriteProcessMemory(self.__process_handle, address, pytype, bufflength, value)
