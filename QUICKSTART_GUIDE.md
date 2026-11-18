# TC_24959 Quick Start Guide

## 🚀 Quick Start - 5 Minutes to Test Execution

### Prerequisites
- CANoe 14.0 or higher installed
- 3 DBC files loaded in CANoe
- All 3 CAN buses configured (ACCESS_CAN, BODY_CAN, BH_CAN)

---

## ⚡ Fast Setup

### 1. Load DBC Files
```
File → Open → Select F244.cfg
Verify DBC files in Database view:
  ✓ MODIFIED_F244_DBC_2024_10_04_ACCESS_CAN.dbc
  ✓ MODIFIED_F244_DBC_2025_07_31_BODY_CAN.dbc
  ✓ MODIFIED_F244_DBC_2025_10_31_BH_CAN.dbc
```

### 2. Add CAPL Module
```
Test Setup → CAPL Test Modules → New → Add File
Select: TC_24959_KeyOff_Test_Module.can
Click: OK
```

### 3. Configure Channels
```
Measurement Setup → Channels:
  Channel 0: ACCESS_CAN  (CAN 1)
  Channel 1: BODY_CAN    (CAN 2)
  Channel 2: BH_CAN      (CAN 3)
```

### 4. Run Test
```
Test Setup → Select "TC_24959_KeyOff_Comfort_Test"
Click: Start (or press F5)
Wait for execution (typically 2-3 seconds)
Report generated automatically
```

---

## 📊 Expected Output

### Console Output:
```
═══════════════════════════════════════════════════════════════════
TEST MODULE INITIALIZATION
═══════════════════════════════════════════════════════════════════

Test Case: TC_24959 - NBC VehicleSts Comfort KeyOff
...
✓ PASS: VehicleSts transition 0->1 successful
✓ PASS: UserPresence transition 0->2 successful
✓ PASS: VehicleSts stable at 1 (Comfort)
✓ PASS: UserPresence stable at 2

═══════════════════════════════════════════════════════════════════
TEST EXECUTION SUMMARY
═══════════════════════════════════════════════════════════════════

Total Checks:       4
Passed Checks:      4
Failed Checks:      0
Warning Checks:     1

OVERALL RESULT:     ✓✓✓ PASS ✓✓✓
```

### Report File:
```
TC_24959_Report_<TIMESTAMP>.txt
(Located in CANoe working directory)
```

---

## ✅ Pass/Fail Criteria

| Check | Expected | Requirement |
|-------|----------|-------------|
| VehicleSts transition 0→1 | PASS | Signal reaches value 1 |
| UserPresence transition 0→2 | PASS | Signal reaches value 2 |
| VehicleSts stable at 1 | PASS | Signal stays at 1 |
| UserPresence stable at 2 | PASS | Signal stays at 2 |

**Result**: PASS = All 4 checks pass  
**Result**: FAIL = Any 1 check fails

---

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| "Signal not found" | Load all 3 DBC files, check channels |
| Test times out | Increase Wait() times in CAPL code |
| Report not created | Check file permissions in CANoe folder |
| Wrong signal values | Verify message routing between CAN networks |

---

## 📋 Test Phases (Automatic)

```
Phase 1: PRE-CONDITION
  └─ Set initial vehicle state
     └─ 100ms delay

Phase 2: STIMULATION-1
  └─ Open door, enable HMI
     └─ 200ms propagation delay

Phase 3: CHECK RESULTS-1
  └─ Verify: VehicleSts → 1, UserPresence → 2
     └─ Log pass/fail for each signal

Phase 4: STIMULATION-2
  └─ Set parking light command
     └─ 500ms wait (as per test spec)

Phase 5: CHECK RESULTS-2
  └─ Verify: Signals remain stable
     └─ Log pass/fail for stability

Phase 6: POST-CONDITION
  └─ Reset all signals to initial state
     └─ Cleanup
```

---

## 📁 Project Structure

```
c:\Users\XEB2KOR\Desktop\BCM_text to capl\
│
├── MODIFIED_F244_DBC_2024_10_04_ACCESS_CAN.dbc
├── MODIFIED_F244_DBC_2025_07_31_BODY_CAN.dbc
├── MODIFIED_F244_DBC_2025_10_31_BH_CAN.dbc
│
├── TC_24959_KeyOff_Test_Module.can          ← Run this in CANoe
├── SIGNAL_MAPPING_REPORT.md                 ← Reference
├── CANOE_TEST_SETUP_GUIDE.md                ← Detailed guide
├── QUICKSTART_GUIDE.md                      ← This file
│
└── TC_24959_Report_<TS>.txt                 ← Generated report
```

---

## 🎯 Test Objectives

✓ Verify vehicle state transition from Wake_Up to Comfort  
✓ Verify user presence detection state changes  
✓ Verify stability of signals during comfort mode  
✓ Generate automated pass/fail report  

---

## 📝 Signal Summary

### Input Signals (Stimulation):
- `STS_LH_DoorStatus` - Set to open/closed
- `HMISts` - Set to on/off
- `EXT_LGH_ParkingLightCmd` - Parking light command

### Output Signals (Verification):
- `VehicleSts` - Expected transition: 0→1
- `UserPresence` - Expected transition: 0→2

### Monitor Signals:
- `IgnPosSts`, `EngineSts`, `PowertrainSts`, etc.

---

## ⏱️ Timing Reference

| Phase | Duration | Purpose |
|-------|----------|---------|
| Pre-Condition | 100ms | Initial state setup |
| Stimulation-1 | 0ms | Instant change |
| Propagation-1 | 200ms | Signal settle time |
| Check-1 | 0ms | Verification (non-blocking) |
| Stimulation-2 | 0ms | Command application |
| Wait-2 | 500ms | Test specification requirement |
| Check-2 | 0ms | Verification (non-blocking) |
| Post-Condition | 0ms | Reset |
| **Total** | **~800ms** | Complete test execution |

---

## 🔗 Related Files

- **Source Test Spec**: TC_24959 - TC_F040_NBC_VehicleSts_Comfort_KeyOff.txt
- **Full CAPL Code**: TC_24959_KeyOff_Test_Module.can
- **Signal Details**: SIGNAL_MAPPING_REPORT.md
- **Setup Details**: CANOE_TEST_SETUP_GUIDE.md

---

## 💡 Tips

1. **Monitor in Trace**: Open Trace window to see CAN messages
2. **Watch Window**: Add VehicleSts and UserPresence to watch critical signals
3. **Network Simulation**: Simulate network delays with CANoe settings if needed
4. **Custom Thresholds**: Modify expected values in CAPL code if needed
5. **Loop Testing**: Modify Teardown() to loop back to test for regression

---

## 📞 Support

For detailed information, see:
- `CANOE_TEST_SETUP_GUIDE.md` - Complete setup instructions
- `SIGNAL_MAPPING_REPORT.md` - Signal database reference
- `TC_24959_KeyOff_Test_Module.can` - Full CAPL source code with comments

---

**Version**: 1.0  
**Updated**: 2026-11-18  
**Status**: Ready for use  

✅ All systems go! Start the test from CANoe Test Setup now.
