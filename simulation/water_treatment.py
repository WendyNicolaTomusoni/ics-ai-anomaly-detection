# Water Treatment Plant Simulation

# Initial tank conditions
water_level = 95.0  # Percentage
pump_on = False
valve_open = True

# Sensor readings
pressure = 2.5  # Bar
flow_rate = 10.0  # Litres per second

# PLC control logic
if water_level <= 30:
    pump_on = True
elif water_level >= 90:
    pump_on = False

# Display system information
print("WATER TREATMENT PLANT")
print("---------------------")

print(f"Water Level: {water_level}%")
print(f"Pressure: {pressure} bar")
print(f"Flow Rate: {flow_rate} L/s")

print(f"Pump Status: {'ON' if pump_on else 'OFF'}")
print(f"Valve Status: {'OPEN' if valve_open else 'CLOSED'}")