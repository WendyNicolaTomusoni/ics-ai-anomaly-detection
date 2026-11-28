
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import streamlit.components.v1 as components
import time
import random
import html


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AquaGuard | Industrial SCADA",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# DESIGN / CSS
# ============================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #0b1118;
    color: #e6edf3;
}

[data-testid="stSidebar"] {
    background: #111a24;
    border-right: 1px solid #263442;
}

[data-testid="stMetric"] {
    background: #121e2a;
    border: 1px solid #263747;
    padding: 15px;
    border-radius: 10px;
}

[data-testid="stMetricLabel"] {
    color: #8fa4b8;
}

[data-testid="stMetricValue"] {
    color: #e9f2f9;
}

h1, h2, h3 {
    color: #eaf3fa;
}

.section-title {
    font-size: 19px;
    font-weight: 700;
    color: #e8f2fa;
    margin-top: 20px;
    margin-bottom: 4px;
}

.section-subtitle {
    color: #8398aa;
    font-size: 12px;
    margin-bottom: 14px;
}

.panel {
    background: #121e2a;
    border: 1px solid #293b4b;
    border-radius: 10px;
    padding: 16px;
    margin-bottom: 12px;
}

.status-online {
    color: #35d49a;
    font-weight: 700;
}

.status-warning {
    color: #f5b942;
    font-weight: 700;
}

.status-danger {
    color: #ff6577;
    font-weight: 700;
}

.small-muted {
    color: #8297aa;
    font-size: 12px;
}

div[data-testid="stButton"] button {
    border-radius: 7px;
    font-weight: 600;
}

hr {
    border-color: #293b4b;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# INITIAL PLANT STATE
# ============================================================

def initialise_plant():

    return {
        "running": False,
        "mode": "AUTO",
        "simulation_time": 0,

        "tanks": {
            "T-101": {
                "name": "Raw Water Tank",
                "level": 68.0,
                "capacity": 20000,
                "color": "#3196d6"
            },
            "T-102": {
                "name": "Treatment Tank",
                "level": 52.0,
                "capacity": 15000,
                "color": "#28b8bd"
            },
            "T-103": {
                "name": "Clean Water Tank",
                "level": 76.0,
                "capacity": 20000,
                "color": "#35d49a"
            }
        },

        "pumps": {
            "P-101": {"name": "Raw Intake Pump", "on": True, "speed": 75, "temperature": 42.0},
            "P-102": {"name": "Backup Pump", "on": False, "speed": 0, "temperature": 27.0},
            "P-103": {"name": "Transfer Pump", "on": True, "speed": 65, "temperature": 39.0},
            "P-104": {"name": "Distribution Pump", "on": True, "speed": 70, "temperature": 41.0}
        },

        "valves": {
            "V-101": {"name": "Intake Valve", "open": True, "position": 100},
            "V-102": {"name": "Treatment Valve", "open": True, "position": 100},
            "V-103": {"name": "Transfer Valve", "open": True, "position": 100},
            "V-104": {"name": "Distribution Valve", "open": True, "position": 100}
        },

        "filter": {
            "name": "Sand Filter",
            "status": "ONLINE",
            "pressure": 1.8
        },

        "dosing": {
            "on": True,
            "ph": 7.2
        },

        "sensors": {
            "flow": 65.0,
            "pressure": 2.1,
            "temperature": 24.0,
            "ph": 7.2
        },

        "alarms": [],
        "history": []
    }


if "plant" not in st.session_state:
    st.session_state.plant = initialise_plant()

plant = st.session_state.plant


# ============================================================
# ALARM MANAGEMENT
# ============================================================

def add_alarm(message, severity="WARNING", equipment="SYSTEM"):

    existing = [
        alarm for alarm in plant["alarms"]
        if alarm["message"] == message
        and alarm["equipment"] == equipment
        and not alarm["acknowledged"]
    ]

    if not existing:
        plant["alarms"].insert(0, {
            "time": datetime.now().strftime("%H:%M:%S"),
            "equipment": equipment,
            "message": message,
            "severity": severity,
            "acknowledged": False
        })

    plant["alarms"] = plant["alarms"][:100]


# ============================================================
# PROCESS SIMULATION
# ============================================================

def update_plant():

    if not plant["running"]:
        return

    plant["simulation_time"] += 1

    tanks = plant["tanks"]
    pumps = plant["pumps"]
    valves = plant["valves"]

    # Automatic pump logic
    if plant["mode"] == "AUTO":

        if tanks["T-101"]["level"] < 15:
            pumps["P-101"]["on"] = False
            pumps["P-102"]["on"] = True

        elif tanks["T-101"]["level"] > 30:
            pumps["P-101"]["on"] = True
            pumps["P-102"]["on"] = False

        pumps["P-103"]["on"] = tanks["T-102"]["level"] > 10

        pumps["P-104"]["on"] = (
            tanks["T-103"]["level"] > 15
            and tanks["T-103"]["level"] < 95
        )

    # Valve and pump flow calculations
    intake = (
        0.30 * pumps["P-101"]["speed"]
        if pumps["P-101"]["on"] and valves["V-101"]["open"]
        else 0
    )

    backup = (
        0.30 * pumps["P-102"]["speed"]
        if pumps["P-102"]["on"] and valves["V-101"]["open"]
        else 0
    )

    transfer = (
        0.30 * pumps["P-103"]["speed"]
        if pumps["P-103"]["on"] and valves["V-103"]["open"]
        and valves["V-102"]["open"]
        else 0
    )

    distribution = (
        0.30 * pumps["P-104"]["speed"]
        if pumps["P-104"]["on"] and valves["V-104"]["open"]
        else 0
    )

    # Tank levels
    raw_change = (intake + backup - transfer * 0.35) * 0.035
    treatment_change = (transfer - transfer * 0.85) * 0.035
    clean_change = (transfer * 0.85 - distribution) * 0.035

    tanks["T-101"]["level"] += raw_change
    tanks["T-102"]["level"] += treatment_change
    tanks["T-103"]["level"] += clean_change

    for tank in tanks.values():
        tank["level"] = max(0, min(100, tank["level"]))

    # Pump temperatures
    for pump in pumps.values():

        if pump["on"]:
            pump["temperature"] += random.uniform(-0.15, 0.35)
        else:
            pump["temperature"] -= 0.2

        pump["temperature"] = max(
            24,
            min(100, pump["temperature"])
        )

    # Process measurements
    total_flow = intake + backup + transfer + distribution

    plant["sensors"]["flow"] = max(
        0,
        distribution + random.uniform(-1.5, 1.5)
    )

    plant["sensors"]["pressure"] = max(
        0,
        0.7 + distribution * 0.045 + random.uniform(-0.05, 0.05)
    )

    plant["sensors"]["temperature"] = (
        23 + random.uniform(-0.5, 0.5)
    )

    if plant["dosing"]["on"]:
        plant["dosing"]["ph"] += random.uniform(-0.015, 0.015)
    else:
        plant["dosing"]["ph"] += random.uniform(-0.04, 0.04)

    plant["dosing"]["ph"] = max(
        5.0,
        min(9.5, plant["dosing"]["ph"])
    )

    plant["sensors"]["ph"] = plant["dosing"]["ph"]

    # Filter pressure
    plant["filter"]["pressure"] = max(
        0.5,
        min(4.5, 1.8 + random.uniform(-0.08, 0.08))
    )

    # Alarm conditions
    for tank_id, tank in tanks.items():

        if tank["level"] < 15:
            add_alarm(
                f"{tank['name']} level critically low",
                "CRITICAL",
                tank_id
            )

        if tank["level"] > 95:
            add_alarm(
                f"{tank['name']} level critically high",
                "WARNING",
                tank_id
            )

    for pump_id, pump in pumps.items():

        if pump["temperature"] > 75:
            add_alarm(
                f"{pump['name']} temperature high",
                "CRITICAL",
                pump_id
            )

    if plant["sensors"]["pressure"] < 1:
        add_alarm(
            "Process pressure is below normal",
            "WARNING",
            "PT-101"
        )

    if plant["sensors"]["ph"] < 6.5 or plant["sensors"]["ph"] > 8.5:
        add_alarm(
            "Water pH outside normal operating range",
            "WARNING",
            "AIT-101"
        )

    # Historical data
    plant["history"].append({
        "Time": datetime.now(),
        "Flow (L/s)": round(plant["sensors"]["flow"], 2),
        "Pressure (bar)": round(plant["sensors"]["pressure"], 2),
        "pH": round(plant["sensors"]["ph"], 2),
        "Temperature (°C)": round(plant["sensors"]["temperature"], 2),
        "Raw Tank (%)": round(tanks["T-101"]["level"], 2),
        "Treatment Tank (%)": round(tanks["T-102"]["level"], 2),
        "Clean Tank (%)": round(tanks["T-103"]["level"], 2)
    })

    plant["history"] = plant["history"][-1000:]


# ============================================================
# SVG EQUIPMENT DRAWING
# ============================================================

def make_tank_svg(tank_id, tank, width=190, height=235):

    level = max(0, min(100, tank["level"]))
    water_height = 145 * level / 100
    water_y = 178 - water_height

    safe_name = html.escape(tank["name"])

    return f"""
    <svg width="{width}" height="{height}" viewBox="0 0 190 235"
         xmlns="http://www.w3.org/2000/svg">

        <defs>
            <linearGradient id="water{tank_id}" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="{tank['color']}" stop-opacity="0.85"/>
                <stop offset="100%" stop-color="{tank['color']}" stop-opacity="0.45"/>
            </linearGradient>
            <clipPath id="clip{tank_id}">
                <rect x="36" y="32" width="118" height="146" rx="8"/>
            </clipPath>
        </defs>

        <text x="95" y="17" text-anchor="middle"
              fill="#dce8f1" font-size="12" font-weight="bold">
            {tank_id}
        </text>

        <rect x="36" y="32" width="118" height="146"
              rx="8" fill="#172735" stroke="#7890a3" stroke-width="2"/>

        <g clip-path="url(#clip{tank_id})">
            <rect x="36" y="{water_y:.1f}" width="118"
                  height="{water_height:.1f}"
                  fill="url(#water{tank_id})"/>

            <path d="M36 {water_y:.1f} Q65 {water_y - 5:.1f} 95 {water_y:.1f}
                     T154 {water_y:.1f}"
                  fill="none" stroke="#a5e8ff" stroke-width="2"/>
        </g>

        <path d="M36 50 H25 V42 M154 50 H165 V42"
              fill="none" stroke="#7890a3" stroke-width="3"/>

        <line x1="95" y1="32" x2="95" y2="18"
              stroke="#7890a3" stroke-width="2"/>

        <text x="95" y="104" text-anchor="middle"
              fill="white" font-size="19" font-weight="bold">
            {level:.1f}%
        </text>

        <text x="95" y="197" text-anchor="middle"
              fill="#c6d5e0" font-size="11">
            {safe_name}
        </text>

        <text x="95" y="216" text-anchor="middle"
              fill="#8399aa" font-size="10">
            {tank['capacity']:,} L capacity
        </text>
    </svg>
    """


def pump_svg(pump_id, pump):

    color = "#35d49a" if pump["on"] else "#758493"
    status = "RUNNING" if pump["on"] else "STOPPED"

    return f"""
    <svg width="145" height="110" viewBox="0 0 145 110"
         xmlns="http://www.w3.org/2000/svg">

        <path d="M8 57 H36 M109 57 H137"
              stroke="#6d8496" stroke-width="7" fill="none"/>

        <circle cx="72" cy="57" r="36"
                fill="#1b2b39" stroke="{color}" stroke-width="4"/>

        <path d="M57 39 L91 57 L57 75 Z"
              fill="{color}" stroke="#c9d8e2" stroke-width="1"/>

        <circle cx="72" cy="57" r="6" fill="#dce7ef"/>

        <text x="72" y="12" text-anchor="middle"
              fill="#dce8f1" font-size="12" font-weight="bold">
            {pump_id}
        </text>

        <text x="72" y="103" text-anchor="middle"
              fill="{color}" font-size="10" font-weight="bold">
            {status}
        </text>
    </svg>
    """


def valve_svg(valve_id, valve):

    color = "#35d49a" if valve["open"] else "#ff6577"
    status = "OPEN" if valve["open"] else "CLOSED"

    return f"""
    <svg width="105" height="85" viewBox="0 0 105 85"
         xmlns="http://www.w3.org/2000/svg">

        <path d="M5 43 H100" stroke="#71899a" stroke-width="7"/>

        <path d="M35 27 L52 43 L35 59 Z"
              fill="{color}" stroke="#dce8f1" stroke-width="1"/>

        <path d="M69 27 L52 43 L69 59 Z"
              fill="{color}" stroke="#dce8f1" stroke-width="1"/>

        <line x1="52" y1="27" x2="52" y2="12"
              stroke="#a7bac8" stroke-width="3"/>

        <circle cx="52" cy="10" r="6"
                fill="{color}"/>

        <text x="52" y="76" text-anchor="middle"
              fill="{color}" font-size="10" font-weight="bold">
            {valve_id} {status}
        </text>
    </svg>
    """


# ============================================================
# PROCESS FLOW SVG
# ============================================================

def create_process_diagram():

    tanks = plant["tanks"]
    pumps = plant["pumps"]
    valves = plant["valves"]

    def tank_symbol(x, y, tank_id, tank):
        level = max(0, min(100, tank["level"]))
        fill_height = 95 * level / 100
        fill_y = y + 112 - fill_height
        color = tank["color"]

        return f"""
        <g>
            <rect x="{x}" y="{y}" width="115" height="115"
                  rx="9" fill="#172735" stroke="#8299aa" stroke-width="2"/>
            <rect x="{x+3}" y="{fill_y}" width="109"
                  height="{fill_height}" fill="{color}" opacity="0.75"/>
            <path d="M{x+3} {fill_y} Q{x+30} {fill_y-4} {x+57} {fill_y}
                     T{x+112} {fill_y}"
                  fill="none" stroke="#c5f2ff" stroke-width="2"/>
            <text x="{x+57}" y="{y+53}" text-anchor="middle"
                  fill="white" font-size="19" font-weight="bold">
                {level:.0f}%
            </text>
            <text x="{x+57}" y="{y+137}" text-anchor="middle"
                  fill="#dce8f1" font-size="13" font-weight="bold">
                {tank_id}
            </text>
        </g>
        """

    def pump_symbol(x, y, pump_id, pump):
        color = "#35d49a" if pump["on"] else "#758493"
        status = "ON" if pump["on"] else "OFF"

        return f"""
        <g>
            <circle cx="{x}" cy="{y}" r="23"
                    fill="#172735" stroke="{color}" stroke-width="3"/>
            <path d="M{x-10} {y-12} L{x+12} {y} L{x-10} {y+12} Z"
                  fill="{color}"/>
            <text x="{x}" y="{y+42}" text-anchor="middle"
                  fill="#e1ebf3" font-size="12">{pump_id}</text>
            <text x="{x}" y="{y+56}" text-anchor="middle"
                  fill="{color}" font-size="10">{status}</text>
        </g>
        """

    def valve_symbol(x, y, valve_id, valve):
        color = "#35d49a" if valve["open"] else "#ff6577"

        return f"""
        <g>
            <path d="M{x-15} {y-13} L{x} {y} L{x-15} {y+13} Z"
                  fill="{color}"/>
            <path d="M{x+15} {y-13} L{x} {y} L{x+15} {y+13} Z"
                  fill="{color}"/>
            <text x="{x}" y="{y+32}" text-anchor="middle"
                  fill="#e1ebf3" font-size="11">{valve_id}</text>
        </g>
        """

    svg = f"""
    <svg width="100%" height="490" viewBox="0 0 1100 490"
         xmlns="http://www.w3.org/2000/svg">

        <defs>
            <linearGradient id="plantbg" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0%" stop-color="#142331"/>
                <stop offset="100%" stop-color="#0d1721"/>
            </linearGradient>
        </defs>

        <rect x="1" y="1" width="1098" height="488"
              rx="12" fill="url(#plantbg)"
              stroke="#2b4051" stroke-width="2"/>

        <text x="25" y="32" fill="#e4eef6"
              font-size="17" font-weight="bold">
            WATER TREATMENT FACILITY | PROCESS OVERVIEW
        </text>

        <text x="25" y="53" fill="#8198aa" font-size="11">
            LIVE SIMULATED PROCESS FLOW • EQUIPMENT STATUS • INSTRUMENTATION
        </text>

        <!-- Main process pipes -->
        <g fill="none" stroke="#71899b" stroke-width="8"
           stroke-linecap="round" stroke-linejoin="round">

            <path d="M140 230 H215"/>
            <path d="M260 230 H330"/>
            <path d="M445 230 H515"/>
            <path d="M560 230 H625"/>
            <path d="M740 230 H825"/>
            <path d="M870 230 H965"/>

            <path d="M388 285 V350 H685 V285"/>
            <path d="M685 350 V390 H965 V285"/>

        </g>

        <!-- Water flow highlights -->
        <g fill="none" stroke="#2eadd7" stroke-width="3"
           stroke-linecap="round">
            <path d="M140 230 H215"/>
            <path d="M260 230 H330"/>
            <path d="M445 230 H515"/>
            <path d="M560 230 H625"/>
            <path d="M740 230 H825"/>
            <path d="M870 230 H965"/>
        </g>

        <!-- Tanks -->
        {tank_symbol(25, 165, "T-101", tanks["T-101"])}
        {tank_symbol(330, 165, "T-102", tanks["T-102"])}
        {tank_symbol(825, 165, "T-103", tanks["T-103"])}

        <!-- Pumps -->
        {pump_symbol(238, 230, "P-101", pumps["P-101"])}
        {pump_symbol(538, 230, "P-103", pumps["P-103"])}
        {pump_symbol(848, 230, "P-104", pumps["P-104"])}

        <!-- Valves -->
        {valve_symbol(292, 230, "V-101", valves["V-101"])}
        {valve_symbol(600, 230, "V-102", valves["V-102"])}
        {valve_symbol(790, 230, "V-103", valves["V-103"])}
        {valve_symbol(965, 230, "V-104", valves["V-104"])}

        <!-- Filter equipment -->
        <g>
            <rect x="480" y="335" width="115" height="75"
                  rx="8" fill="#1a3040"
                  stroke="#4da8c8" stroke-width="2"/>
            <path d="M495 353 H580 M495 367 H580 M495 381 H580"
                  stroke="#75c5db" stroke-width="4"/>
            <text x="538" y="430" text-anchor="middle"
                  fill="#dce8f1" font-size="12" font-weight="bold">
                F-101 FILTER
            </text>
        </g>

        <!-- Chemical dosing -->
        <g>
            <rect x="695" y="75" width="90" height="85"
                  rx="8" fill="#243342" stroke="#c49b4d" stroke-width="2"/>
            <path d="M707 125 H773 V151 H707 Z"
                  fill="#d4a84e" opacity="0.75"/>
            <text x="740" y="99" text-anchor="middle"
                  fill="#e9d8a6" font-size="11">CHEMICAL</text>
            <text x="740" y="113" text-anchor="middle"
                  fill="#e9d8a6" font-size="11">DOSING</text>
            <path d="M740 160 V190 H685 V230"
                  fill="none" stroke="#c49b4d" stroke-width="4"
                  stroke-dasharray="6 4"/>
        </g>

        <!-- Instrumentation -->
        <g font-family="Arial" text-anchor="middle">
            <circle cx="165" cy="115" r="23" fill="#142735"
                    stroke="#4da8c8" stroke-width="2"/>
            <text x="165" y="119" fill="#dce8f1" font-size="11">LT</text>
            <text x="165" y="88" fill="#9eb1c0" font-size="10">LIT-101</text>

            <circle cx="440" cy="115" r="23" fill="#142735"
                    stroke="#4da8c8" stroke-width="2"/>
            <text x="440" y="119" fill="#dce8f1" font-size="11">PT</text>
            <text x="440" y="88" fill="#9eb1c0" font-size="10">PIT-101</text>

            <circle cx="920" cy="115" r="23" fill="#142735"
                    stroke="#4da8c8" stroke-width="2"/>
            <text x="920" y="119" fill="#dce8f1" font-size="11">FT</text>
            <text x="920" y="88" fill="#9eb1c0" font-size="10">FIT-101</text>
        </g>

        <!-- Process direction -->
        <g fill="#9fb4c4" font-size="11">
            <text x="25" y="460">RAW WATER INTAKE</text>
            <text x="470" y="460">FILTRATION &amp; TREATMENT</text>
            <text x="850" y="460">CLEAN WATER OUTPUT</text>
        </g>

        <!-- Legend -->
        <circle cx="30" cy="475" r="5" fill="#35d49a"/>
        <text x="42" y="479" fill="#8da3b4" font-size="10">Running</text>
        <circle cx="120" cy="475" r="5" fill="#758493"/>
        <text x="132" y="479" fill="#8da3b4" font-size="10">Stopped</text>
        <circle cx="220" cy="475" r="5" fill="#ff6577"/>
        <text x="232" y="479" fill="#8da3b4" font-size="10">Closed / Alarm</text>

    </svg>
    """

    return svg


# ============================================================
# HEADER
# ============================================================

col_logo, col_title, col_status = st.columns([0.7, 4, 1.5])

with col_logo:
    st.markdown("## 🏭")

with col_title:
    st.markdown("# AQUAGUARD SCADA")
    st.caption("AI-Assisted Industrial Water Treatment Monitoring System")

with col_status:
    if plant["running"]:
        st.markdown('<p class="status-online">● SYSTEM RUNNING</p>', unsafe_allow_html=True)
    else:
        st.markdown('<p class="status-warning">● SYSTEM PAUSED</p>', unsafe_allow_html=True)

st.divider()


# ============================================================
# SIDEBAR CONTROLS
# ============================================================

st.sidebar.title("CONTROL PANEL")
st.sidebar.caption("Industrial Operations")

mode = st.sidebar.radio(
    "Operating mode",
    ["AUTO", "MANUAL"],
    index=0 if plant["mode"] == "AUTO" else 1
)

plant["mode"] = mode

st.sidebar.divider()

if st.sidebar.button("▶ START SIMULATION", use_container_width=True):
    plant["running"] = True
    st.rerun()

if st.sidebar.button("⏸ PAUSE SIMULATION", use_container_width=True):
    plant["running"] = False
    st.rerun()

if st.sidebar.button("↻ RESET PLANT", use_container_width=True):
    st.session_state.plant = initialise_plant()
    st.rerun()

st.sidebar.divider()

st.sidebar.subheader("Equipment Control")

if plant["mode"] == "MANUAL":

    st.sidebar.caption("Manual pump controls")

    for pump_id, pump in plant["pumps"].items():

        pump["on"] = st.sidebar.toggle(
            f"{pump_id} — {pump['name']}",
            value=pump["on"],
            key=f"manual_{pump_id}"
        )

        pump["speed"] = st.sidebar.slider(
            f"{pump_id} speed (%)",
            min_value=0,
            max_value=100,
            value=int(pump["speed"]),
            key=f"speed_{pump_id}"
        )

    st.sidebar.divider()
    st.sidebar.caption("Manual valve controls")

    for valve_id, valve in plant["valves"].items():

        valve["open"] = st.sidebar.toggle(
            f"{valve_id} — {valve['name']}",
            value=valve["open"],
            key=f"valve_{valve_id}"
        )

else:
    st.sidebar.info(
        "AUTO mode controls pumps automatically according to simulated tank levels."
    )

st.sidebar.divider()

plant["dosing"]["on"] = st.sidebar.toggle(
    "Chemical dosing system",
    value=plant["dosing"]["on"],
    key="dosing_control"
)


# ============================================================
# UPDATE SIMULATION
# ============================================================

update_plant()


# ============================================================
# MAIN PROCESS METRICS
# ============================================================

st.markdown('<div class="section-title">Plant Performance Overview</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">Real-time simulated operational measurements</div>', unsafe_allow_html=True)

m1, m2, m3, m4, m5 = st.columns(5)

m1.metric(
    "Water Flow",
    f"{plant['sensors']['flow']:.1f} L/s"
)

m2.metric(
    "System Pressure",
    f"{plant['sensors']['pressure']:.2f} bar"
)

m3.metric(
    "Water pH",
    f"{plant['sensors']['ph']:.2f}"
)

m4.metric(
    "Temperature",
    f"{plant['sensors']['temperature']:.1f} °C"
)

active_pumps = sum(
    1 for pump in plant["pumps"].values() if pump["on"]
)

m5.metric(
    "Active Pumps",
    f"{active_pumps}/4"
)


# ============================================================
# INDUSTRIAL PROCESS DIAGRAM
# ============================================================

st.markdown('<div class="section-title">Industrial Process Flow</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtitle">Live P&ID-inspired process overview | Tanks, pipes, pumps, valves and instrumentation</div>',
    unsafe_allow_html=True
)

process_svg = create_process_diagram()

components.html(
    process_svg,
    height=510,
    scrolling=False
)


# ============================================================
# TANK VISUALISATION
# ============================================================

st.markdown('<div class="section-title">Tank Level Monitoring</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtitle">Visual tank cross-sections showing current water levels and capacity</div>',
    unsafe_allow_html=True
)

tank_columns = st.columns(3)

for column, (tank_id, tank) in zip(tank_columns, plant["tanks"].items()):

    with column:

        st.markdown(
            f'<div class="panel"><b>{tank_id}</b><br>'
            f'<span class="small-muted">{tank["name"]}</span></div>',
            unsafe_allow_html=True
        )

        components.html(
            make_tank_svg(tank_id, tank),
            height=245,
            scrolling=False
        )

        st.progress(
            int(tank["level"]),
            text=f"{tank['level']:.1f}% full"
        )


# ============================================================
# PUMP AND VALVE STATUS
# ============================================================

st.markdown('<div class="section-title">Pump Station</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">Motor status and operating temperature</div>', unsafe_allow_html=True)

pump_columns = st.columns(4)

for column, (pump_id, pump) in zip(pump_columns, plant["pumps"].items()):

    with column:

        components.html(
            pump_svg(pump_id, pump),
            height=120,
            scrolling=False
        )

        st.markdown(f"**{pump['name']}**")

        if pump["on"]:
            st.markdown('<span class="status-online">● RUNNING</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="small-muted">● STOPPED</span>', unsafe_allow_html=True)

        st.caption(f"Speed: {pump['speed']}%")
        st.caption(f"Motor temperature: {pump['temperature']:.1f} °C")


st.markdown('<div class="section-title">Valve Station</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">Valve positions and flow control status</div>', unsafe_allow_html=True)

valve_columns = st.columns(4)

for column, (valve_id, valve) in zip(valve_columns, plant["valves"].items()):

    with column:

        components.html(
            valve_svg(valve_id, valve),
            height=95,
            scrolling=False
        )

        st.markdown(f"**{valve['name']}**")

        st.caption(
            "OPEN" if valve["open"] else "CLOSED"
        )


# ============================================================
# PROCESS INSTRUMENTATION
# ============================================================

st.markdown('<div class="section-title">Instrumentation & Sensors</div>', unsafe_allow_html=True)

sensor_data = pd.DataFrame([
    ["LIT-101", "Raw tank level", f"{plant['tanks']['T-101']['level']:.1f}%", "NORMAL"],
    ["LIT-102", "Treatment tank level", f"{plant['tanks']['T-102']['level']:.1f}%", "NORMAL"],
    ["LIT-103", "Clean tank level", f"{plant['tanks']['T-103']['level']:.1f}%", "NORMAL"],
    ["FIT-101", "Distribution flow", f"{plant['sensors']['flow']:.2f} L/s", "ONLINE"],
    ["PIT-101", "Process pressure", f"{plant['sensors']['pressure']:.2f} bar", "ONLINE"],
    ["AIT-101", "Water pH", f"{plant['sensors']['ph']:.2f}", "ONLINE"],
    ["TIT-101", "Water temperature", f"{plant['sensors']['temperature']:.1f} °C", "ONLINE"]
], columns=["Instrument ID", "Description", "Reading", "Status"])

st.dataframe(
    sensor_data,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# ALARM MANAGEMENT
# ============================================================

st.markdown('<div class="section-title">Alarm & Event Management</div>', unsafe_allow_html=True)

active_alarms = [
    alarm for alarm in plant["alarms"]
    if not alarm["acknowledged"]
]

a1, a2, a3 = st.columns(3)

a1.metric("Active Alarms", len(active_alarms))
a2.metric(
    "Critical Alarms",
    sum(1 for alarm in active_alarms if alarm["severity"] == "CRITICAL")
)
a3.metric(
    "Acknowledged",
    sum(1 for alarm in plant["alarms"] if alarm["acknowledged"])
)

if plant["alarms"]:

    for index, alarm in enumerate(plant["alarms"]):

        severity_color = (
            "#ff6577"
            if alarm["severity"] == "CRITICAL"
            else "#f5b942"
        )

        c1, c2, c3, c4 = st.columns([1, 1.2, 3, 1])

        c1.caption(alarm["time"])
        c2.markdown(
            f"<span style='color:{severity_color};font-weight:bold'>"
            f"{alarm['severity']}</span>",
            unsafe_allow_html=True
        )
        c3.write(f"**{alarm['equipment']}** — {alarm['message']}")

        if not alarm["acknowledged"]:
            if c4.button("ACK", key=f"ack_{index}"):
                alarm["acknowledged"] = True
                st.rerun()
        else:
            c4.caption("Acknowledged")

else:
    st.success("No active alarms. All monitored parameters are within the configured limits.")


# ============================================================
# HISTORICAL PROCESS MONITORING
# ============================================================

st.markdown('<div class="section-title">Historical Process Monitoring</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtitle">Trends from collected simulation measurements</div>',
    unsafe_allow_html=True
)

if plant["history"]:

    history_df = pd.DataFrame(plant["history"])

    tab1, tab2, tab3, tab4 = st.tabs([
        "Flow & Pressure",
        "Tank Levels",
        "Water Quality",
        "Temperature"
    ])

    with tab1:

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=history_df["Time"],
            y=history_df["Flow (L/s)"],
            name="Flow",
            mode="lines",
            line=dict(width=2)
        ))

        fig.update_layout(
            title="Distribution Flow",
            xaxis_title="Time",
            yaxis_title="Flow (L/s)",
            template="plotly_dark",
            height=320
        )

        st.plotly_chart(fig, use_container_width=True)

        fig2 = go.Figure()

        fig2.add_trace(go.Scatter(
            x=history_df["Time"],
            y=history_df["Pressure (bar)"],
            name="Pressure",
            mode="lines",
            line=dict(width=2)
        ))

        fig2.update_layout(
            title="System Pressure",
            xaxis_title="Time",
            yaxis_title="Pressure (bar)",
            template="plotly_dark",
            height=300
        )

        st.plotly_chart(fig2, use_container_width=True)

    with tab2:

        fig = go.Figure()

        for column in [
            "Raw Tank (%)",
            "Treatment Tank (%)",
            "Clean Tank (%)"
        ]:

            fig.add_trace(go.Scatter(
                x=history_df["Time"],
                y=history_df[column],
                mode="lines",
                name=column
            ))

        fig.update_layout(
            title="Tank Level Trends",
            xaxis_title="Time",
            yaxis_title="Level (%)",
            yaxis=dict(range=[0, 100]),
            template="plotly_dark",
            height=380
        )

        st.plotly_chart(fig, use_container_width=True)

    with tab3:

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=history_df["Time"],
            y=history_df["pH"],
            mode="lines",
            name="pH"
        ))

        fig.add_hrect(
            y0=6.5,
            y1=8.5,
            fillcolor="green",
            opacity=0.08,
            line_width=0
        )

        fig.update_layout(
            title="Water pH Trend",
            xaxis_title="Time",
            yaxis_title="pH",
            template="plotly_dark",
            height=330
        )

        st.plotly_chart(fig, use_container_width=True)

    with tab4:

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=history_df["Time"],
            y=history_df["Temperature (°C)"],
            mode="lines",
            name="Water Temperature"
        ))

        fig.update_layout(
            title="Water Temperature Trend",
            xaxis_title="Time",
            yaxis_title="Temperature (°C)",
            template="plotly_dark",
            height=330
        )

        st.plotly_chart(fig, use_container_width=True)

    st.download_button(
        "Download Historical Data (CSV)",
        data=history_df.to_csv(index=False).encode("utf-8"),
        file_name="aquaguard_process_history.csv",
        mime="text/csv"
    )

else:
    st.info("No historical readings collected yet. Start the simulation to generate process history.")


# ============================================================
# AI ANOMALY MONITORING
# ============================================================

st.markdown('<div class="section-title">AI & Anomaly Monitoring</div>', unsafe_allow_html=True)

st.markdown("""
<div class="panel">
    <h4>Intelligent Process Monitoring</h4>
    <p class="small-muted">
        The current dashboard uses configured operating thresholds to identify
        abnormal process conditions. The machine-learning anomaly detection
        model will be integrated with the collected sensor history in a later
        development stage.
    </p>
</div>
""", unsafe_allow_html=True)

anomalies = []

for pump_id, pump in plant["pumps"].items():

    if pump["temperature"] > 75:
        anomalies.append(
            f"{pump_id}: Abnormally high motor temperature"
        )

for tank_id, tank in plant["tanks"].items():

    if tank["level"] < 15:
        anomalies.append(
            f"{tank_id}: Unusually low water level"
        )

    if tank["level"] > 95:
        anomalies.append(
            f"{tank_id}: Unusually high water level"
        )

if plant["sensors"]["pressure"] < 1:
    anomalies.append("PT-101: Low process pressure")

if plant["sensors"]["ph"] < 6.5 or plant["sensors"]["ph"] > 8.5:
    anomalies.append("AIT-101: Abnormal pH measurement")

if anomalies:

    st.warning("Potential abnormal operating conditions detected.")

    for anomaly in anomalies:
        st.write(f"⚠️ {anomaly}")

else:
    st.success("No configured threshold violations detected.")


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "AquaGuard SCADA | Simulated Industrial Water Treatment System | "
    "Cybersecurity & Reliability Project"
)

st.caption(
    "Demonstration environment only. Equipment, process values and alarms "
    "are simulated and are not connected to physical industrial hardware."
)


# ============================================================
# SIMULATION REFRESH
# ============================================================

if plant["running"]:
    time.sleep(1)
    st.rerun()
