
import random


class WaterTreatmentPlant:
    """Simulates the physical behaviour of a water treatment plant."""

    def __init__(self):
        # Tank properties
        self.tank_capacity = 10_000  # Litres
        self.water_volume = 5_000   # Initial volume: 50%

        # Equipment states
        self.pump_on = False
        self.valve_open = True
        self.control_mode = "AUTO"

        # PLC thresholds
        self.low_level_threshold = 30
        self.high_level_threshold = 90

        # Equipment faults
        self.pump_failed = False

        # Sensor faults
        self.sensor_faults = {
            "level": False,
            "pressure": False,
            "flow": False,
        }

        # Process rates (litres per second)
        self.pump_inflow_rate = 120
        self.valve_outflow_rate = 80

        # Latest measurements
        self.level_reading = 50.0
        self.pressure_reading = 0.0
        self.flow_reading = 0.0

    @property
    def actual_water_level(self):
        """Return the actual tank level as a percentage."""
        return (self.water_volume / self.tank_capacity) * 100

    def plc_control(self):
        """Apply automatic PLC control logic."""
        if self.control_mode != "AUTO":
            return

        if self.actual_water_level <= self.low_level_threshold:
            self.pump_on = True

        elif self.actual_water_level >= self.high_level_threshold:
            self.pump_on = False

    def update_process(self, elapsed_seconds=1):
        """Update the physical water process."""
        self.plc_control()

        inflow = 0
        outflow = 0

        if self.pump_on and not self.pump_failed:
            inflow = self.pump_inflow_rate

        if self.valve_open:
            outflow = self.valve_outflow_rate

        change = (inflow - outflow) * elapsed_seconds

        self.water_volume += change

        # Prevent the tank from going below empty or above capacity.
        self.water_volume = max(
            0,
            min(self.tank_capacity, self.water_volume)
        )

        self.read_sensors(inflow, outflow)

    def read_sensors(self, inflow, outflow):
        """Generate simulated sensor measurements."""

        actual_level = self.actual_water_level

        actual_pressure = (
            1.0 + (inflow / 120) * 2.0
        )

        actual_flow = inflow + outflow

        if self.sensor_faults["level"]:
            self.level_reading = 50.0
        else:
            self.level_reading = round(
                actual_level + random.uniform(-0.2, 0.2), 2
            )

        if self.sensor_faults["pressure"]:
            self.pressure_reading = 0.0
        else:
            self.pressure_reading = round(
                actual_pressure + random.uniform(-0.05, 0.05), 2
            )

        if self.sensor_faults["flow"]:
            self.flow_reading = 0.0
        else:
            self.flow_reading = round(
                actual_flow + random.uniform(-1, 1), 2
            )

    def set_manual_controls(self, pump=None, valve=None):
        """Allow an operator to control equipment manually."""
        self.control_mode = "MANUAL"

        if pump is not None:
            self.pump_on = pump

        if valve is not None:
            self.valve_open = valve

    def set_automatic_mode(self):
        """Return control to the PLC."""
        self.control_mode = "AUTO"
        self.plc_control()

    def reset_faults(self):
        """Clear simulated equipment and sensor faults."""
        self.pump_failed = False

        for sensor in self.sensor_faults:
            self.sensor_faults[sensor] = False

    def get_status(self):
        """Return current plant information for the dashboard."""
        return {
            "water_level": self.level_reading,
            "actual_water_level": round(self.actual_water_level, 2),
            "pressure": self.pressure_reading,
            "flow_rate": self.flow_reading,
            "pump_on": self.pump_on,
            "pump_failed": self.pump_failed,
            "valve_open": self.valve_open,
            "control_mode": self.control_mode,
            "sensor_faults": self.sensor_faults.copy(),
        }


if __name__ == "__main__":
    plant = WaterTreatmentPlant()

    print("WATER TREATMENT PLANT SIMULATION")
    print("--------------------------------")

    for second in range(10):
        plant.update_process()

        status = plant.get_status()

        print(f"\nSimulation second: {second + 1}")
        print(f"Water level: {status['water_level']}%")
        print(f"Pressure: {status['pressure']} bar")
        print(f"Flow rate: {status['flow_rate']} L/s")
        print(f"Pump: {'ON' if status['pump_on'] else 'OFF'}")
        print(f"Valve: {'OPEN' if status['valve_open'] else 'CLOSED'}")
        print(f"Mode: {status['control_mode']}")
