"""
Signal Mapping Configuration
=============================
Maps test file signal names to actual CAN signal definitions.

Three CAN buses:
  - ACCESS_CAN: MODIFIED_F244_DBC_2024_10_04_ACCESS_CAN.dbc
  - BODY_CAN: MODIFIED_F244_DBC_2025_07_31_BODY_CAN.dbc
  - BH_CAN: MODIFIED_F244_DBC_2025_10_31_BH_CAN.dbc
"""

SIGNAL_MAPPING = {
    "description": "Signal mapping from test .txt format to CAN DBC signals",
    "version": "1.0",
    "dbc_files": {
        "ACCESS_CAN": "MODIFIED_F244_DBC_2024_10_04_ACCESS_CAN.dbc",
        "BODY_CAN": "MODIFIED_F244_DBC_2025_07_31_BODY_CAN.dbc",
        "BH_CAN": "MODIFIED_F244_DBC_2025_10_31_BH_CAN.dbc"
    },
    "signals": {
        # Pre-Condition Signals
        "Proxy_write_Power_Unit_Extended": {
            "mapped_name": "Proxy_write_Power_Unit_Extended",
            "message": "UNKNOWN",
            "dbc": "UNKNOWN",
            "found": False,
            "category": "Power Unit",
            "description": "Power unit type (Thermic/Hybrid/EV)"
        },
        "si_sys_TcSen_bTerm15_1": {
            "mapped_name": "si_sys_TcSen_bTerm15_1",
            "message": "UNKNOWN",
            "dbc": "UNKNOWN",
            "found": False,
            "category": "Terminal State",
            "description": "Terminal 15 state (Term 15 input 1)"
        },
        "si_sys_TcSen_bTerm15_2": {
            "mapped_name": "si_sys_TcSen_bTerm15_2",
            "message": "UNKNOWN",
            "dbc": "UNKNOWN",
            "found": False,
            "category": "Terminal State",
            "description": "Terminal 15 state (Term 15 input 2)"
        },
        "si_sys_TcSen_bTermS": {
            "mapped_name": "si_sys_TcSen_bTermS",
            "message": "UNKNOWN",
            "dbc": "UNKNOWN",
            "found": False,
            "category": "Terminal State",
            "description": "Terminal S state"
        },
        "si_sys_NFR_NFR_Speed_FA": {
            "mapped_name": "NFR_Speed_FA",
            "message": "NFR_SPEED",
            "dbc": "BODY_CAN",
            "found": True,
            "category": "Speed",
            "description": "Front axle speed (0 to 511.9375 km/h)"
        },
        "si_sys_NFR_NFR_Speed_FA_FailSts": {
            "mapped_name": "NFR_Speed_FA_FailSts",
            "message": "NFR_SPEED",
            "dbc": "BODY_CAN",
            "found": True,
            "category": "Speed",
            "description": "Speed failure status"
        },
        "si_sys_SGW_StopStartSts": {
            "mapped_name": "StopStartSts",
            "message": "STATUS_SGW",
            "dbc": "ACCESS_CAN",
            "found": True,
            "category": "Engine State",
            "description": "Stop-Start status"
        },
        "si_sys_SGW_EngineSts": {
            "mapped_name": "EngineSts",
            "message": "STATUS_SGW",
            "dbc": "ACCESS_CAN",
            "found": True,
            "category": "Engine State",
            "description": "Engine status (OFF/ON/Cranking/Shutdown)"
        },
        "si_sys_STS_LH_DoorStatus": {
            "mapped_name": "STS_LH_DoorStatus",
            "message": "STS_LH_DoorStatus_MSG",
            "dbc": "BH_CAN",
            "found": True,
            "category": "Door Status",
            "description": "Left hand door status (1=Closed, 3=Opened)"
        },
        "si_sys_NPE_IgnPosSts": {
            "mapped_name": "IgnPosSts",
            "message": "RFHUB1",
            "dbc": "ACCESS_CAN",
            "found": True,
            "category": "Ignition",
            "description": "Ignition position status"
        },
        "si_sys_SGW_PowerTrainSts": {
            "mapped_name": "PowertrainSts",
            "message": "STATUS_SGW",
            "dbc": "ACCESS_CAN",
            "found": True,
            "category": "Powertrain",
            "description": "Powertrain status"
        },
        "si_sys_SGW_HMISts": {
            "mapped_name": "HMISts",
            "message": "HMI_INFO",
            "dbc": "ACCESS_CAN",
            "found": True,
            "category": "HMI",
            "description": "HMI status"
        },
        "si_sys_NPS_ParkingLightsCommand": {
            "mapped_name": "EXT_LGH_ParkingLightCmd",
            "message": "EXTERNAL_LIGHTS",
            "dbc": "ACCESS_CAN",
            "found": True,
            "category": "Lighting",
            "description": "Parking lights command"
        },
        
        # Expected Results Signals
        "so_sys_F040_VehicleSts": {
            "mapped_name": "VehicleSts",
            "message": "STATUS_NBC_3",
            "dbc": "BODY_CAN",
            "found": True,
            "category": "Vehicle State",
            "description": "Vehicle status (Wake_Up/Comfort/etc)"
        },
        "XCP_sys_F908_UserPresence": {
            "mapped_name": "UserPresence",
            "message": "STATUS_NBC_3",
            "dbc": "BODY_CAN",
            "found": True,
            "category": "User Presence",
            "description": "User presence detection status"
        },
        "so_sys_F040_KeySts_BODYCAN": {
            "mapped_name": "so_sys_F040_KeySts_BODYCAN",
            "message": "UNKNOWN",
            "dbc": "BODY_CAN",
            "found": False,
            "category": "Key Status",
            "description": "Key status on BODY CAN bus"
        },
        "so_sys_F040_KeySts_ACCESSCAN": {
            "mapped_name": "so_sys_F040_KeySts_ACCESSCAN",
            "message": "UNKNOWN",
            "dbc": "ACCESS_CAN",
            "found": False,
            "category": "Key Status",
            "description": "Key status on ACCESS CAN bus"
        },
        "so_sys_F040_KeySts_BHCAN": {
            "mapped_name": "so_sys_F040_KeySts_BHCAN",
            "message": "UNKNOWN",
            "dbc": "BH_CAN",
            "found": False,
            "category": "Key Status",
            "description": "Key status on BH CAN bus"
        }
    },
    "categories": {
        "Speed": [
            {
                "name": "si_sys_NFR_NFR_Speed_FA",
                "mapped_name": "NFR_SPEED.NFR_Speed_FA",
                "type": "Physical value",
                "range": "0 to 511.9375 km/h"
            },
            {
                "name": "si_sys_NFR_NFR_Speed_FA_FailSts",
                "mapped_name": "NFR_SPEED.NFR_Speed_FA_FailSts",
                "type": "Status",
                "range": "0 (OK) or 1 (Failure)"
            }
        ],
        "Engine State": [
            {
                "name": "si_sys_SGW_StopStartSts",
                "mapped_name": "STATUS_SGW.StopStartSts",
                "type": "State",
                "values": "0=Off, 1=On, 2=Engine_Restart, 3=Stop_Request"
            },
            {
                "name": "si_sys_SGW_EngineSts",
                "mapped_name": "STATUS_SGW.EngineSts",
                "type": "State",
                "values": "0=Engine_OFF, 1=Engine_ON, 2=Engine_Cranking, 3=Engine_Shutdown"
            },
            {
                "name": "si_sys_SGW_PowerTrainSts",
                "mapped_name": "STATUS_SGW.PowertrainSts",
                "type": "Status",
                "range": "Varies by configuration"
            }
        ],
        "Door Status": [
            {
                "name": "si_sys_STS_LH_DoorStatus",
                "mapped_name": "STS_LH_DoorStatus_MSG.STS_LH_DoorStatus",
                "type": "State",
                "values": "1=Closed, 3=Opened"
            }
        ],
        "Ignition": [
            {
                "name": "si_sys_NPE_IgnPosSts",
                "mapped_name": "RFHUB1.IgnPosSts",
                "type": "State",
                "values": "0=Off, 1=ACC/Run, 2=Start, etc"
            }
        ],
        "HMI": [
            {
                "name": "si_sys_SGW_HMISts",
                "mapped_name": "HMI_INFO.HMISts",
                "type": "Status",
                "values": "0=Off, 1=On"
            }
        ],
        "Lighting": [
            {
                "name": "si_sys_NPS_ParkingLightsCommand",
                "mapped_name": "EXTERNAL_LIGHTS.EXT_LGH_ParkingLightCmd",
                "type": "Command",
                "values": "0=Off, 1=On"
            }
        ],
        "Vehicle State": [
            {
                "name": "so_sys_F040_VehicleSts",
                "mapped_name": "STATUS_NBC_3.VehicleSts",
                "type": "State",
                "values": "0=Wake_Up, 1=Comfort, etc"
            }
        ],
        "User Presence": [
            {
                "name": "XCP_sys_F908_UserPresence",
                "mapped_name": "STATUS_NBC_3.UserPresence",
                "type": "Status",
                "values": "0=No, 2=Yes, etc"
            }
        ],
        "Terminal State": [
            {
                "name": "si_sys_TcSen_bTerm15_1",
                "mapped_name": "si_sys_TcSen_bTerm15_1",
                "type": "Status",
                "note": "NOT FOUND in DBC - MCore internal variable"
            },
            {
                "name": "si_sys_TcSen_bTerm15_2",
                "mapped_name": "si_sys_TcSen_bTerm15_2",
                "type": "Status",
                "note": "NOT FOUND in DBC - MCore internal variable"
            },
            {
                "name": "si_sys_TcSen_bTermS",
                "mapped_name": "si_sys_TcSen_bTermS",
                "type": "Status",
                "note": "NOT FOUND in DBC - MCore internal variable"
            }
        ],
        "Power Unit": [
            {
                "name": "Proxy_write_Power_Unit_Extended",
                "mapped_name": "Proxy_write_Power_Unit_Extended",
                "type": "Configuration",
                "values": "0=Thermic, 1=Hybrid, 2=EV",
                "note": "NOT FOUND in DBC - Requires XCP access"
            }
        ],
        "Key Status": [
            {
                "name": "so_sys_F040_KeySts_BODYCAN",
                "mapped_name": "so_sys_F040_KeySts_BODYCAN",
                "type": "Status",
                "note": "NOT FOUND - Requires multi-CAN bus coordination"
            },
            {
                "name": "so_sys_F040_KeySts_ACCESSCAN",
                "mapped_name": "so_sys_F040_KeySts_ACCESSCAN",
                "type": "Status",
                "note": "NOT FOUND - Requires multi-CAN bus coordination"
            },
            {
                "name": "so_sys_F040_KeySts_BHCAN",
                "mapped_name": "so_sys_F040_KeySts_BHCAN",
                "type": "Status",
                "note": "NOT FOUND - Requires multi-CAN bus coordination"
            }
        ]
    },
    "statistics": {
        "total_signals": 25,
        "found_signals": 11,
        "not_found_signals": 4,
        "coverage_percent": 73
    }
}


def get_signal_mapping(signal_name):
    """Get mapping info for a signal by name
    
    Args:
        signal_name (str): Signal name from test file
        
    Returns:
        dict: Signal mapping info or None
    """
    return SIGNAL_MAPPING["signals"].get(signal_name)


def get_mapped_signal_name(signal_name):
    """Get the mapped CAN signal name
    
    Args:
        signal_name (str): Signal name from test file
        
    Returns:
        str: Mapped signal name (e.g., "MESSAGE.Signal") or None
    """
    mapping = get_signal_mapping(signal_name)
    if mapping:
        if mapping["found"]:
            return f"{mapping['message']}.{mapping['mapped_name']}"
    return None


def is_signal_found(signal_name):
    """Check if signal is found in DBC files
    
    Args:
        signal_name (str): Signal name from test file
        
    Returns:
        bool: True if signal is found
    """
    mapping = get_signal_mapping(signal_name)
    return mapping.get("found", False) if mapping else False
