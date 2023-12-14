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
    
    def _send_command(self, command: str):
        hex_command = self.__commands[command]
        byte_data = bytes.fromhex(hex_command)
        self._send_bytes(byte_data)
    
    def _send_command_and_get_response(self, command: str) -> bytes:
        hex_command = self.__commands[command]
        byte_data = bytes.fromhex(hex_command)
        return self._send_bytes_with_response(byte_data)

    def turn_on(self):
        self._send_command("turn_on")

    def turn_off(self):
        self._send_command("turn_off")

    def ocp_on(self):
        self._send_command('ocp_on')
        
    def ocp_off(self):
        self._send_command('ocp_off')

    def ovp_on(self):
        self._send_command('ovp_on')
    
    def ovp_off(self):
        self._send_command('ovp_off')

    def get_model(self) -> bytes:
        return self._send_command_and_get_response("get_model")

    def get_active_voltage(self) -> bytes:
        return self._send_command_and_get_response("get_active_voltage")

    def get_active_current(self) -> bytes:
        return self._send_command_and_get_response("get_active_current")

    def get_voltage_limit(self) -> bytes:
        return self._send_command_and_get_response("get_voltage_limit")

    def get_current_limit(self) -> bytes:
        return self._send_command_and_get_response("get_current_limit")

    def get_on_off_status(self) -> bytes:
        return self._send_command_and_get_response("get_on_off_status")

    def _send_command_with_value(self, command: str, val: int):
        hex_command = self.__commands[command]
        cmd_bytes = bytes.fromhex(hex_command)
        val_bytes = val.to_bytes(2, byteorder='little')
        self._send_bytes(cmd_bytes + val_bytes)

    def set_output_voltage(self, v: float):
        centivolt = int(v * 100)
        self._send_command_with_value('set_output_voltage', centivolt)

    def set_output_current(self, mA: int):
        self._send_command_with_value('set_output_current', mA)

    def set_ovp_limit(self, v: float):
        centivolt = int(v * 100)
        self._send_command_with_value('set_ovp_limit', centivolt)

    def set_ocp_limit(self, mA: int):
        self._send_command_with_value('set_ocp_limit', mA)
