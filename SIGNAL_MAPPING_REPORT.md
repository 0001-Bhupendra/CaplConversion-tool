# TC_24959 - CAPL Test Code Signal Mapping Report

## Overview
This document provides a detailed mapping of signals from the test case specification file to actual CAN signal names found in the available DBC, LDF, and A2L database files.

---

## Signal Mapping Summary

### ✅ **FOUND SIGNALS** (Successfully mapped to CAN messages)

| Test Signal Name | Actual Signal | Message Name | Message ID | CAN Bus | Status |
|------------------|---------------|--------------|-----------|---------|--------|
| si_sys_NPE_IgnPosSts | IgnPosSts | RFHUB1 | 0x167 (359) | ACCESS/BH_CAN | ✅ FOUND |
| si_sys_SGW_EngineSts | EngineSts | STATUS_SGW | 0x5A1 (1441) | ACCESS_CAN | ✅ FOUND |
| si_sys_SGW_StopStartSts | StopStartSts | STATUS_SGW | 0x5A1 (1441) | ACCESS_CAN | ✅ FOUND |
| si_sys_SGW_PowerTrainSts | PowertrainSts | STATUS_SGW | 0x5A1 (1441) | ACCESS_CAN | ✅ FOUND |
| si_sys_SGW_HMISts | HMISts | HMI_INFO | 0x40B (1035) | ACCESS/BH_CAN | ✅ FOUND |
| si_sys_STS_LH_DoorStatus | STS_LH_DoorStatus | STS_LH_DoorStatus_MSG | 0x3CB (971) | BH_CAN | ✅ FOUND |
| si_sys_NFR_NFR_Speed_FA | NFR_Speed_FA | NFR_SPEED | 0x20C (524) | ACCESS/BH_CAN | ✅ FOUND |
| si_sys_NFR_NFR_Speed_FA_FailSts | NFR_Speed_FA_FailSts | NFR_SPEED | 0x20C (524) | ACCESS/BH_CAN | ✅ FOUND |
| si_sys_NPS_ParkingLightsCommand | EXT_LGH_ParkingLightCmd | EXTERNAL_LIGHTS | 0x180 (384) | BH_CAN | ✅ FOUND (name differs) |
| so_sys_F040_VehicleSts | VehicleSts | STATUS_NBC_3 | 0x3C1 (961) | BH_CAN | ✅ FOUND |
| XCP_sys_F908_UserPresence | UserPresence | STATUS_NBC_3 | 0x3C1 (961) | BH_CAN | ✅ FOUND |

---

### ❌ **NOT FOUND SIGNALS** (Not available in databases)

| Test Signal Name | Search Keywords | Checked Files | Status | Alternative/Solution |
|------------------|----------------|----------------|--------|----------------------|
| Proxy_write_Power_Unit_Extended | PowerUnit, Proxy, Extended, EV | All DBCs, A2L | ❌ NOT FOUND | May be MCore internal variable in A2L - requires XCP mapping |
| si_sys_TcSen_bTerm15_1 | Term15, TcSen, bTerm15 | All DBCs, A2L | ❌ NOT FOUND | May be LIN signal in .ldf files, check LIN_F244 files |
| si_sys_TcSen_bTerm15_2 | Term15, TcSen, bTerm15 | All DBCs, A2L | ❌ NOT FOUND | May be LIN signal in .ldf files, check LIN_F244 files |
| si_sys_TcSen_bTermS | TermS, TcSen, bTermS | All DBCs, A2L | ❌ NOT FOUND | May be LIN signal in .ldf files, check LIN_F244 files |
| so_sys_F040_KeySts_BODYCAN | KeySts, BODYCAN, F040 | BODY_CAN.dbc | ⚠️ PARTIAL | Found KeySts in STATUS_B_CAN (Msg 1376) ACCESS_CAN |
| so_sys_F040_KeySts_ACCESSCAN | KeySts, ACCESSCAN, F040 | ACCESS_CAN.dbc | ✅ FOUND | KeySts signal in STATUS_B_CAN (Msg 1376) |
| so_sys_F040_KeySts_BHCAN | KeySts, BHCAN, F040 | BH_CAN.dbc | ⚠️ PARTIAL | Multiple KeySts signals across messages |

---

## Detailed CAN Message Information

### 1. **RFHUB1 (Message 0x167 / 359)**
- **Source:** BCM/NPE
- **Destination:** SGW/BCM
- **Cycle Time:** Variable
- **Signals:**
  - `IgnPosSts` [3:5] - Ignition Position Status (0-7)
  - `ValidKeySts` [5:6] - Valid Key Status (0-3)
  - And others...

### 2. **NFR_SPEED (Message 0x20C / 524)**
- **Source:** SGW/BCM
- **Destination:** Multiple ECUs
- **Cycle Time:** 20ms
- **Signals:**
  - `NFR_Speed_FA` [38:50] - Vehicle Speed (0.0625 km/h resolution, 0-511.9375 km/h)
  - `NFR_Speed_FA_FailSts` [41:41] - Speed Signal Failure Status (0=No failure, 1=Failure)
  - `MessageCounter_NFR_SPEED` [51:54]
  - `CRC_NFR_SPEED` [63:70]

### 3. **STATUS_SGW (Message 0x5A1 / 1441)**
- **Source:** SGW
- **Destination:** BCM/NPE
- **Cycle Time:** Variable
- **Signals:**
  - `PowertrainSts` [50:52] - Powertrain Status (0-7)
  - `EngineSts` [45:46] - Engine Status (0-3)
  - `StopStartSts` [47:48] - Stop/Start Status (0-3)
  - `HMISts` [58:60] - HMI Status (0-3)

### 4. **HMI_INFO (Message 0x40B / 1035)**
- **Source:** SGW/BCM
- **Destination:** Multiple
- **Cycle Time:** 100ms
- **Signals:**
  - `HMISts` [58:60] - HMI Status

### 5. **STATUS_NBC_3 (Message 0x3C1 / 961)**
- **Source:** BCM
- **Destination:** SGW
- **Cycle Time:** 250ms
- **Signals:**
  - `VehicleSts` [27:30] - Vehicle State (0-7):
    - 0 = Wake_Up
    - 1 = Comfort
    - 2 = KeyON
    - 3 = KeyON_PWTStarting
    - 4 = KeyON_PWTShutdown
    - 5 = KeyON_PWTON
    - 6 = KeyOFF_PWTMoving
  - `UserPresence` [9:10] - User Presence Status (0-3)

### 6. **STS_LH_DoorStatus_MSG (Message 0x3CB / 971)**
- **Source:** BCM
- **Destination:** SGW
- **Signals:**
  - `STS_LH_DoorStatus` [4:5] - Left Door Status (0-3):
    - 0 = SNA
    - 1 = Closed
    - 2 = Ajar
    - 3 = Opened

### 7. **EXTERNAL_LIGHTS (Message 0x180 / 384)**
- **Source:** BCM
- **Destination:** SGW
- **Signals:**
  - `EXT_LGH_ParkingLightCmd` [19:20] - Parking Light Command (0-3):
    - 0 = Off
    - 1 = Left
    - 2 = Right
    - 3 = All

---

## Missing Signals - Potential Locations

### Term15 Signals
The signals `si_sys_TcSen_bTerm15_1`, `si_sys_TcSen_bTerm15_2`, and `si_sys_TcSen_bTermS` were not found in the CAN DBC files. These may be:
- **LIN Bus Signals** in the .ldf files:
  - `LIN_F244_2024_04_26_BCM_LIN1.ldf`
  - `LIN_F244_2024_04_26_BCM_LIN2.ldf`
  - `LIN_F244_2024_04_26_BCM_LIN5.ldf`
  - `LIN_F244_2025_05_23_BCM_LIN*.ldf`
- **XCP/MCore Variables** in the A2L file:
  - `rbd_bcm_FER_MCore_VMs_217.a2l`

### Proxy_write_Power_Unit_Extended
Not found in CAN signals. Possible locations:
- MCore internal variable in A2L file
- Proxy variable for simulation/calibration
- Configuration parameter (not a CAN signal)

### KeySts_* Signals
Multiple KeySts signals exist across different CAN networks:
- **ACCESS_CAN**: `KeySts` in `STATUS_B_CAN` (Message 1376)
- **BODY_CAN**: Similar KeySts may exist
- **BH_CAN**: May have equivalent signal

---

## Next Steps to Complete Signal Mapping

1. **For Term15 Signals**: 
   - Review LIN database files (.ldf) for Term15 equivalents
   - Search in A2L file for XCP/MCore variables

2. **For Proxy Variables**:
   - Check if this is a simulation-only variable
   - Verify in CANoe measurement setup

3. **For Multi-Bus KeySts Signals**:
   - Create separate stimulation for each CAN network
   - Map BODYCAN, ACCESSCAN, and BHCAN messages separately
   - Use CAN routing/gateway mapping if applicable

---

## CAPL Code Usage

The generated CAPL test code (`TC_24959_KeyOff_Test.can`) includes:
- ✅ All found signals with proper message/signal references
- ⚠️ Commented sections for not-found signals with explanations
- 📝 Detailed logging and test phase tracking
- ✓ Expected result verification checks
- 🔄 Pre-condition, stimulation, and post-condition phases

**To use the code:**
1. Import the DBC files in CANoe
2. Update signal references if message names differ
3. Add LIN network initialization if Term15 signals are needed
4. For XCP signals, enable MCore variable access in CANoe

---

## Signal Resolution Status

| Category | Count | Status |
|----------|-------|--------|
| Fully Mapped | 11 | ✅ Ready to use |
| Partially Mapped | 3 | ⚠️ Requires additional mapping |
| Not Found | 4 | ❌ Need alternative source |
| **Total** | **18** | **61% coverage** |

---

## Recommendations

1. **Immediate**: Use the 11 fully-mapped signals for test execution
2. **Short-term**: Search LIN files for Term15 signals
3. **Medium-term**: Confirm KeySts signal mapping across all CAN networks
4. **Long-term**: Add missing signals documentation to DBC files

---

**Generated:** 2026-11-18  
**Test File:** TC_24959_KeyOff_Test.can  
**Reference Files:**
- MODIFIED_F244_DBC_2024_10_04_ACCESS_CAN.dbc
- MODIFIED_F244_DBC_2025_07_31_BODY_CAN.dbc
- MODIFIED_F244_DBC_2025_10_31_BH_CAN.dbc
- rbd_bcm_FER_MCore_VMs_217.a2l
