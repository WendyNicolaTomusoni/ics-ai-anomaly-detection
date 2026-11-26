
# Asset Inventory

## 1. Introduction

This document identifies the important assets in the simulated water treatment plant.

The inventory supports cybersecurity analysis, threat modelling and reliability assessment.

## 2. Identified Assets

| ID | Asset | Function | Criticality |
|---|---|---|---|
| A01 | PLC | Processes sensor readings and controls equipment | Critical |
| A02 | SCADA/HMI | Allows operators to monitor and supervise the process | High |
| A03 | Water-level sensor | Measures water level in the tank | High |
| A04 | Pressure sensor | Measures water pressure | High |
| A05 | Flow sensor | Measures water flow | High |
| A06 | Pump and valve | Move water and control its flow | Critical |
| A07 | Industrial network | Enables communication between industrial devices | Critical |
| A08 | AI monitoring system | Detects unusual network behaviour | Medium |

## 3. Asset Dependencies

- The PLC depends on sensor measurements to make control decisions.
- The pump and valve depend on the PLC's control commands.
- The SCADA/HMI depends on network communication to receive process information.
- The PLC and SCADA/HMI depend on the industrial network for Modbus/TCP communication.
- The AI monitoring system depends on access to network traffic for analysis.

## 4. Potential Threats and Failures

| Asset | Threat or Failure | Possible Impact |
|---|---|---|
| PLC | Unauthorised commands | Incorrect equipment operation |
| SCADA/HMI | System compromise or failure | Loss of operator visibility |
| Water-level sensor | Manipulated readings | Incorrect water-level information |
| Pressure sensor | Sensor malfunction | Incorrect pressure measurements |
| Flow sensor | Incorrect readings | Poor process monitoring |
| Pump and valve | Mechanical failure | Disruption of water movement |
| Industrial network | Excessive or malicious traffic | Communication disruption |
| AI monitoring system | Detector failure | Suspicious activity may go undetected |

## 5. Asset Criticality

Criticality is a preliminary assessment based on the potential impact of asset failure.

- Critical: Failure could directly affect essential operations or safety.
- High: Failure could significantly affect monitoring or operational decisions.
- Medium: Failure could reduce supporting capabilities without directly stopping the industrial process.

These classifications will be reviewed during the detailed risk assessment.

## 6. Conclusion

The PLC, industrial network, pumps and valves are important assets because they directly support the industrial process.

Sensors provide information needed for control decisions, while SCADA/HMI allows operators to supervise the plant.

The AI monitoring system provides additional cybersecurity visibility but must remain separate from industrial control operations.
