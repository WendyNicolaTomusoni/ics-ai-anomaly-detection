
# Vulnerability Assessment and Risk Analysis

## 1. Introduction

This document identifies potential vulnerabilities and evaluates cybersecurity and reliability risks in the simulated water treatment plant.

The assessment considers the likelihood and potential impact of different incidents.

## 2. Identified Vulnerabilities

| ID | Vulnerability | Affected Asset |
|---|---|---|
| V01 | Insufficient network access controls | PLC |
| V02 | Modbus/TCP communication lacks built-in authentication | Industrial network |
| V03 | Weak SCADA login credentials | SCADA/HMI |
| V04 | Insufficient validation of sensor readings | Sensors |
| V05 | Lack of network traffic monitoring | Industrial network |
| V06 | Inadequate backup and recovery procedures | SCADA/PLC |

These are preliminary assessment assumptions to be verified during implementation and testing.

## 3. Risk Assessment Method

Risk is calculated using:

Risk Score = Likelihood × Impact

Both likelihood and impact use a scale from 1 to 5.

### Likelihood

1. Very unlikely
2. Unlikely
3. Possible
4. Likely
5. Very likely

### Impact

1. Negligible
2. Minor
3. Moderate
4. Major
5. Severe

### Risk Classification

| Score | Risk Level |
|---|---|
| 1–4 | Low |
| 5–9 | Medium |
| 10–16 | High |
| 17–25 | Critical |

## 4. Preliminary Risk Register

| ID | Risk Scenario | Likelihood | Impact | Risk Score | Level |
|---|---|---|---|---|---|
| R01 | Unauthorised PLC commands | 3 | 5 | 15 | High |
| R02 | Manipulated sensor readings | 3 | 4 | 12 | High |
| R03 | Excessive Modbus requests | 4 | 4 | 16 | High |
| R04 | SCADA ransomware | 3 | 5 | 15 | High |
| R05 | Network equipment failure | 3 | 4 | 12 | High |
| R06 | AI monitoring system failure | 2 | 3 | 6 | Medium |

These scores are preliminary estimates and will be reviewed after testing.

## 5. Risk Mitigation Measures

| Risk ID | Proposed Mitigation |
|---|---|
| R01 | Network segmentation and PLC access restrictions |
| R02 | Sensor validation and plausibility checks |
| R03 | Network traffic monitoring and AI anomaly detection |
| R04 | Backups, endpoint protection and recovery procedures |
| R05 | Network redundancy and equipment maintenance |
| R06 | Monitoring health checks and system logging |

## 6. AI Anomaly Detection Relevance

The AI anomaly detection system will primarily focus on unusual network communication patterns, including:

- Unexpected increases in Modbus request frequency.
- Unusual communication between devices.
- Unexpected register write activity.
- Abnormal connection patterns.

The AI system will generate alerts for investigation rather than automatically controlling industrial equipment.

## 7. Conclusion

The preliminary assessment identifies unauthorised PLC commands, manipulated sensor readings, excessive network requests and ransomware as important cybersecurity scenarios.

Network failures and monitoring system failures are also considered because the project addresses operational reliability.

The risk register will guide the selection of scenarios for simulation and the evaluation of the proposed security solution.
