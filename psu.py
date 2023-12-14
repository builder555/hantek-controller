from serial import Serial

class PSU:
    def __init__(self, port: str = "/dev/ttyUSB0", baudrate: int = 2400):
        self.__port = port
        self.__baudrate = baudrate
        self.__commands = {
            "turn_on": "ff ff 03 06 01",
            "turn_off": "ff ff 03 06 00",
            "get_model": "ff ff 02 20",
            "get_active_voltage": "ff ff 02 09",
            "get_active_current": "ff ff 02 0a",
            "get_voltage_limit": "ff ff 02 12",
            "get_current_limit": "ff ff 02 13",
            "get_on_off_status": "ff ff 02 14",
            "ocp_on": "ff ff 03 1a 01",
            "ocp_off": "ff ff 03 1a 00",
            "ovp_on": "ff ff 03 19 01",
            "ovp_off": "ff ff 03 19 00",
            "set_output_voltage": "ff ff 04 07",
            "set_output_current": "ff ff 04 08",
            "set_ovp_limit": "ff ff 04 17",
            "set_ocp_limit": "ff ff 04 18"
        }

    def _send_bytes(self, byte_data: bytes):
        with Serial(self.__port, self.__baudrate, timeout=1) as ser:
            ser.write(byte_data)

    def _send_bytes_with_response(self, byte_data: bytes) -> bytes:
        with Serial(self.__port, self.__baudrate, timeout=1) as ser:
            ser.write(byte_data)
            resp = ser.readline()
        return resp
    
    def _send_command(self, hex_command: str):
        byte_data = bytes.fromhex(hex_command)
        self._send_bytes(byte_data)
    
    def _send_command_and_get_response(self, hex_command: str) -> bytes:
        byte_data = bytes.fromhex(hex_command)
        return self._send_bytes_with_response(byte_data)

    def turn_on(self):
        self._send_command(self.__commands["turn_on"])

    def turn_off(self):
        self._send_command(self.__commands["turn_off"])

    def get_model(self) -> bytes:
        return self._send_command_and_get_response(self.__commands["get_model"])

    def get_active_voltage(self) -> bytes:
        return self._send_command_and_get_response(self.__commands["get_active_voltage"])

    def get_active_current(self) -> bytes:
        return self._send_command_and_get_response(self.__commands["get_active_current"])

    def get_voltage_limit(self) -> bytes:
        return self._send_command_and_get_response(self.__commands["get_voltage_limit"])

    def get_current_limit(self) -> bytes:
        return self._send_command_and_get_response(self.__commands["get_current_limit"])

    def get_on_off_status(self) -> bytes:
        return self._send_command_and_get_response(self.__commands["get_on_off_status"])

    def ocp_on(self):
        self._send_command(f"ff ff 03 1a 01")
        
    def ocp_off(self):
        self._send_command(f"ff ff 03 1a 00")

    def ovp_on(self):
        self._send_command(f"ff ff 03 19 01")
    
    def ovp_off(self):
        self._send_command(f"ff ff 03 19 00")

    def _send_command_with_value(self, cmd: str, val: int):
        cmd_bytes = bytes.fromhex(cmd)
        val_bytes = val.to_bytes(2, byteorder='little')
        self._send_bytes(cmd_bytes + val_bytes)

    def set_output_voltage(self, v: float):
        command = "ff ff 04 07"
        centivolt = int(v * 100)
        self._send_command_with_value(command, centivolt)

    def set_output_current(self, mA: int):
        command = "ff ff 04 08"
        self._send_command_with_value(command, mA)

    def set_ovp_limit(self, v: float):
        command = "ff ff 04 17"
        centivolt = int(v * 100)
        self._send_command_with_value(command, centivolt)

    def set_ocp_limit(self, mA: int):
        command = "ff ff 04 18"
        self._send_command_with_value(command, mA)
