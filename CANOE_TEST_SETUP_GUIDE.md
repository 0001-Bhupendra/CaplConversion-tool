# CANoe Test Setup Guide - TC_24959

## Overview
This guide explains how to configure and run the **TC_24959 Test Module** in CANoe's Test Setup for automated pass/fail report generation.

---

## Files Included

1. **TC_24959_KeyOff_Test_Module.can** - Main CAPL test module with:
   - Automatic report file generation
   - Pass/Fail checking
   - Console logging
   - Report summary

2. **SIGNAL_MAPPING_REPORT.md** - Detailed signal mapping documentation

---

## CANoe Test Setup Configuration

### Step 1: Create Test Configuration File (.cfg)

The `F244.cfg` file in your workspace should include reference to DBC files:

```
[Database Files]
{CHANNEL 0}
Databases=MODIFIED_F244_DBC_2024_10_04_ACCESS_CAN.dbc
Databases=MODIFIED_F244_DBC_2025_07_31_BODY_CAN.dbc  
Databases=MODIFIED_F244_DBC_2025_10_31_BH_CAN.dbc

{CHANNEL 1}
Databases=MODIFIED_F244_DBC_2024_10_04_ACCESS_CAN.dbc
Databases=MODIFIED_F244_DBC_2025_07_31_BODY_CAN.dbc
Databases=MODIFIED_F244_DBC_2025_10_31_BH_CAN.dbc
```

### Step 2: Import CAPL Module into CANoe

1. **Open CANoe Test Setup**
   - Open your CANoe project
   - Navigate to **Test Setup** tab

2. **Add CAPL Module**
   - Right-click on "CAPL Test Modules"
   - Select "New..." → "Add..."
   - Browse and select `TC_24959_KeyOff_Test_Module.can`

3. **Configure Measurement Channels**
   - Ensure all three CAN buses are configured:
     - **Channel 0**: ACCESS_CAN (or appropriate channel)
     - **Channel 1**: BODY_CAN (or appropriate channel)
     - **Channel 2**: BH_CAN (or appropriate channel)

### Step 3: Configure Test Environment

In your CANoe configuration, ensure the following:

```
[Channels]
Channel0=ACCESS_CAN
Channel1=BODY_CAN
Channel2=BH_CAN

[SignalDefinition]
UseDBCSignals=1
SignalUpdateInterval=10ms

[TestExecution]
StopTestOnError=0
GenerateHTMLReport=1
ReportDirectory=Reports\
```

---

## Running the Test

### From CANoe Test Setup:

1. **Select Test Case**
   - In Test Setup tab, select "TC_24959_KeyOff_Comfort_Test"

2. **Start Test**
   - Click "Start" button or press F5

3. **Monitor Output**
   - View test execution in Output Console
   - Real-time pass/fail status displayed
   - Signal values shown as they change

4. **Test Completes**
   - Report automatically generated
   - Report file saved as: `TC_24959_Report_<TIMESTAMP>.txt`
   - Overall result shown: **PASS** or **FAIL**

### Via Command Line (Optional):

```batch
CAnoeConsole.exe YourProject.cfg -Test "TC_24959_KeyOff_Comfort_Test" -Run
```

---

## Report Output Format

### Generated Report File Structure:

```
================================================================================
  TEST EXECUTION REPORT
  Test Case: TC_24959 - NBC VehicleSts Comfort KeyOff
  Description: Vehicle Status - Comfort Mode - Key Off Test
================================================================================

Test Start Time: 1234567890 (ms since system start)

[PASS] VehicleSts transition 0->1 successful (Wake_Up -> Comfort)
        Expected: 1
        Actual:   1

[PASS] UserPresence transition 0->2 successful
        Expected: 2
        Actual:   2

[WARNING] so_sys_F040_KeySts_* signals - Requires multi-CAN bus mapping

[PASS] VehicleSts stable at 1 (Comfort)
        Expected: 1 (stable)
        Actual:   1

[PASS] UserPresence stable at 2
        Expected: 2 (stable)
        Actual:   2

================================================================================
  TEST SUMMARY
================================================================================

Total Checks:     4
Passed Checks:    4
Failed Checks:    0
Warning Checks:   1

Test Duration:    1234 ms

OVERALL RESULT:   ✓ PASS

================================================================================
```

---

## Expected Test Results

### Pass Criteria:
✓ VehicleSts transitions from 0 (Wake_Up) to 1 (Comfort) after Stimulation-1  
✓ UserPresence transitions from 0 to 2 after Stimulation-1  
✓ VehicleSts remains stable at 1 after Stimulation-2  
✓ UserPresence remains stable at 2 after Stimulation-2  

### Warning Conditions:
⚠ KeySts_* signals not fully mapped (expected - documented limitation)

### Fail Criteria:
✗ Any expected signal transition does not occur  
✗ Signal values differ from expected ranges  
✗ Timing violations (delays between stimulation and response)

---

## Test Execution Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                      TEST INITIALIZATION                            │
│                                                                     │
│  - Load DBC files (ACCESS_CAN, BODY_CAN, BH_CAN)                   │
│  - Initialize report file                                           │
│  - Capture initial signal states                                    │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│                    PHASE 1: PRE-CONDITION                           │
│                                                                     │
│  Set initial vehicle state:                                         │
│  - NFR_Speed_FA = 0 km/h                                            │
│  - StopStartSts = 0, EngineSts = 0                                 │
│  - STS_LH_DoorStatus = 1 (Closed)                                  │
│  - IgnPosSts = 1 (ACC/Run)                                         │
│  - PowertrainSts = 0                                                │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│               PHASE 2: STIMULATION-1 (Apply Conditions)            │
│                                                                     │
│  - Set STS_LH_DoorStatus = 3 (Opened)                              │
│  - Set HMISts = 1 (HMI_ON)                                         │
│  - Wait 200ms for propagation                                       │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│          PHASE 3: CHECK RESULTS-1 (Verify Transitions)            │
│                                                                     │
│  ✓ CHECK: VehicleSts 0→1? (Expected: 1 for Comfort)               │
│  ✓ CHECK: UserPresence 0→2?                                        │
│  ⚠ WARNING: KeySts_* signals need separate mapping                 │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│          PHASE 4: STIMULATION-2 (Parking Light Command)           │
│                                                                     │
│  - Set EXT_LGH_ParkingLightCmd = 0 (Off)                           │
│  - Wait 500ms (0.5 seconds as per test spec)                       │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│        PHASE 5: CHECK RESULTS-2 (Verify Stability)                │
│                                                                     │
│  ✓ CHECK: VehicleSts still = 1? (Comfort - stable)                │
│  ✓ CHECK: UserPresence still = 2? (stable)                         │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│          PHASE 6: POST-CONDITION (Cleanup & Reset)                │
│                                                                     │
│  - Reset all signals to initial state                               │
│  - Clean up test environment                                        │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│                   TEST REPORT GENERATION                            │
│                                                                     │
│  - Generate summary (Passed/Failed/Warnings)                        │
│  - Save report file: TC_24959_Report_<TIMESTAMP>.txt               │
│  - Display: OVERALL RESULT = PASS or FAIL                           │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Troubleshooting

### Issue: "Signal not found" error

**Solution:**
- Verify DBC files are loaded in CANoe
- Check that all 3 CAN channels are configured
- Review SIGNAL_MAPPING_REPORT.md for alternate signal names

### Issue: Report not generated

**Solution:**
- Check file write permissions in CANoe working directory
- Verify g_ReportFileHandle is valid (> 0)
- Check if FOpen/FPrint functions are available in CAPL environment

### Issue: Test hangs or times out

**Solution:**
- Increase Wait() times if signals take longer to propagate
- Check if CAN messages are being sent on correct channels
- Verify message cycle times in DBC files

### Issue: Expected signal values not achieved

**Solution:**
- Check DBC for signal value ranges
- Verify signal receiver configuration
- Confirm gateway/routing between CAN networks
- Review signal value tables (VAL_ definitions)

---

## Advanced Configuration

### Custom Report Location:

Modify `g_ReportFilePath` in the CAPL module:

```capl
snprintf(g_ReportFilePath, 256, "C:\\Reports\\TC_24959_Report_%d.txt", GetTickCount());
```

### HTML Report Generation:

To enable HTML report output, add to CANoe Test Setup configuration:

```
[ReportGeneration]
GenerateHTMLReport=1
HTMLReportDirectory=Reports\HTML\
```

### Custom Logging:

Add additional checks in `PHASE 3` or `PHASE 5`:

```capl
// Check additional signal values
if (STATUS_NBC_3.SomeSignal == ExpectedValue) {
    LogResult("Custom check description", 1, "expected", "actual");
} else {
    LogResult("Custom check description", 0, "expected", "actual");
}
```

---

## Maintenance

### Version Information
- **Test Module**: TC_24959_KeyOff_Test_Module.can v1.0
- **CANoe Version**: 14.0 or higher recommended
- **CAPL Version**: CAPL 2.0 or higher
- **Report Date**: 2026-11-18

### Update Log
- **v1.0** (2026-11-18): Initial release with 11 mapped signals, 4 checks, automated reporting

---

## Support & Documentation

For more information:
- See: `SIGNAL_MAPPING_REPORT.md` - Detailed signal mapping
- See: `TC_24959_KeyOff_Test_Module.can` - Full CAPL source code
- Original Test Spec: `TC_24959 - TC_F040_NBC_VehicleSts_Comfort_KeyOff.txt`

---

## Notes

1. **Signal Availability**: 11 out of 15 signals successfully mapped from DBC files (73% coverage)
2. **Multi-CAN Support**: Test operates across 3 separate CAN buses (ACCESS/BODY/BH)
3. **Automatic Reporting**: Report file generated automatically after test completion
4. **Console Feedback**: Real-time test progress displayed in CANoe Output Console
5. **Customizable**: CAPL source code can be modified for additional checks or parameters

---

**Last Updated**: 2026-11-18  
**Created For**: CANoe Test Environment  
**Test Status**: Ready for Execution
