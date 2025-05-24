from pymodbus.server.sync import StartTcpServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.datastore import ModbusSequentialDataBlock
import threading
import time
import random

def run_modbus_server():
    store = ModbusSlaveContext(
        hr=ModbusSequentialDataBlock(0, [250])  # 25.0 degrees C *10 scaling
    )
    context = ModbusServerContext(slaves=store, single=True)

    def update_temp():
        while True:
            new_temp = random.randint(240, 280)  # Random temp 24.0 to 28.0 C
            store.setValues(3, 0, [new_temp])
            time.sleep(2)

    threading.Thread(target=update_temp, daemon=True).start()
    StartTcpServer(context, address=("localhost", 5020))

if __name__ == "__main__":
    run_modbus_server()
