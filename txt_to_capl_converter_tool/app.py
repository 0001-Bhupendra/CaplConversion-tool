"""
TXT to CAPL Converter Tool
==========================
A Streamlit web app to convert test case .txt files to CAPL test modules
for CANoe Test Setup execution.

Features:
  - Upload multiple .txt test case files
  - Automatically parse test specifications
  - Generate CAPL code with 6-phase test framework
  - Download individual CAPL files or batch ZIP package
  - Shareable with teammates

Author: BCM Test Automation
Date: November 2026
"""

import streamlit as st
import os
import io
import zipfile
from pathlib import Path
from datetime import datetime

from text_parser import parse_test_case
from capl_generator import generate_capl_module
from signal_mapping import SIGNAL_MAPPING

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="TXT to CAPL Converter",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM STYLING
# ============================================================================

st.markdown("""
<style>
    .stMainBlockContainer {
        padding: 2rem;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    h1 {
        color: #1f77b4;
        border-bottom: 3px solid #1f77b4;
        padding-bottom: 0.5rem;
    }
    h2 {
        color: #2ca02c;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# HEADER
# ============================================================================

st.title("⚙️ TXT to CAPL Converter Tool")
st.markdown("""
**Convert test case specifications (.txt) → CAPL test modules (.can)**

This tool automatically processes your test case text files and generates 
ready-to-use CAPL test modules for CANoe Test Setup.
""")

# ============================================================================
# SIDEBAR - INFORMATION
# ============================================================================

with st.sidebar:
    st.header("📋 Tool Information")
    st.info("""
    **Features:**
    - 📤 Upload multiple .txt files
    - 🔄 Auto-parse test specifications
    - 📝 Generate CAPL modules
    - 📥 Download individual or batch files
    - 🤝 Share with teammates
    """)
    
    st.markdown("---")
    st.header("📚 Signal Mapping")
    
    if st.checkbox("View Available Signals", False):
        st.markdown("### Mapped Signals")
        for category, signals in SIGNAL_MAPPING["categories"].items():
            with st.expander(f"**{category}** ({len(signals)} signals)"):
                for sig in signals:
                    st.markdown(f"- `{sig['name']}` → `{sig['mapped_name']}`")
    
    st.markdown("---")
    st.header("❓ Help")
    if st.checkbox("Show Expected .txt Format", False):
        st.markdown("""
        ```
        // PRE-CONDITION
        signal_name = value

        // STIMULATION-1: Description
        signal_name = value

        // EXPECTED RESULTS-1: Check conditions
        signal_name = expected_value
        signal_name = initial->final

        // STIMULATION-2: Description
        signal_name = value
        wait = 0.5

        // EXPECTED RESULTS-2: Check conditions
        signal_name = expected_value

        // POST-CONDITION
        signal_name = value
        ```
        """)

# ============================================================================
# MAIN CONTENT - FILE UPLOAD
# ============================================================================

col1, col2 = st.columns([2, 1])

with col1:
    st.header("📤 Upload Test Case Files")
    st.markdown("Select one or more .txt files to convert to CAPL modules:")
    
    uploaded_files = st.file_uploader(
        "Choose .txt files",
        type="txt",
        accept_multiple_files=True,
        key="file_uploader"
    )

with col2:
    st.header("⚙️ Settings")
    
    include_comments = st.checkbox(
        "Include detailed comments",
        value=True,
        help="Adds extensive comments to generated CAPL code"
    )
    
    include_timing = st.checkbox(
        "Include timing details",
        value=True,
        help="Adds timing measurements and wait commands"
    )
    
    report_format = st.radio(
        "Report output format",
        ["Console (Write())", "CSV", "Both"],
        help="How results are reported"
    )

# ============================================================================
# FILE PROCESSING
# ============================================================================

if uploaded_files:
    st.markdown("---")
    st.header("🔄 Processing Files")
    
    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Results storage
    generated_files = {}
    errors = []
    
    with st.spinner("Processing files..."):
        for idx, uploaded_file in enumerate(uploaded_files):
            # Update progress
            progress = (idx + 1) / len(uploaded_files)
            progress_bar.progress(progress)
            status_text.text(f"Processing: {uploaded_file.name} ({idx + 1}/{len(uploaded_files)})")
            
            try:
                # Read file content
                file_content = uploaded_file.getvalue().decode("utf-8")
                
                # Parse test case
                parsed_data = parse_test_case(file_content, uploaded_file.name)
                
                # Generate CAPL code
                capl_code = generate_capl_module(
                    parsed_data,
                    include_comments=include_comments,
                    include_timing=include_timing,
                    report_format=report_format
                )
                
                # Store generated file
                capl_filename = parsed_data['test_case_id'] + ".can"
                generated_files[capl_filename] = capl_code
                
            except Exception as e:
                errors.append({
                    "file": uploaded_file.name,
                    "error": str(e)
                })
    
    status_text.empty()
    progress_bar.empty()
    
    # Display results
    st.markdown("---")
    st.header("✅ Results")
    
    if generated_files:
        st.markdown(f"""
        <div class="success-box">
        <strong>✓ Successfully processed {len(generated_files)} file(s)</strong>
        </div>
        """, unsafe_allow_html=True)
        
        # Display individual file info
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Files Processed", len(generated_files), delta="✓")
        with col2:
            st.metric("Errors", len(errors), delta=f"{len(errors)} ✗" if errors else "0 ✓")
        with col3:
            st.metric("Ready to Download", len(generated_files), delta="✓")
        
        st.markdown("### 📄 Generated CAPL Modules")
        
        # Create tabs for each file
        tabs = st.tabs([f["name"] for f in [{"name": fname} for fname in generated_files.keys()]])
        
        for tab_idx, (capl_filename, capl_code) in enumerate(generated_files.items()):
            with tabs[tab_idx]:
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"**Filename:** `{capl_filename}`")
                    st.markdown(f"**Lines of Code:** `{len(capl_code.splitlines())}`")
                    st.markdown(f"**Generated:** `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`")
                
                with col2:
                    st.download_button(
                        label="📥 Download",
                        data=capl_code,
                        file_name=capl_filename,
                        mime="text/plain",
                        key=f"download_{capl_filename}"
                    )
                
                # Code preview
                with st.expander("👁️ Preview Code", expanded=False):
                    st.code(capl_code[:1000] + "\n... [code truncated for preview] ...", language="cpp")
    
    # Display errors if any
    if errors:
        st.markdown(f"""
        <div class="warning-box">
        <strong>⚠️ Errors encountered during processing:</strong>
        </div>
        """, unsafe_allow_html=True)
        
        for error in errors:
            st.error(f"**{error['file']}**: {error['error']}")
    
    # Batch download
    if generated_files:
        st.markdown("---")
        st.header("📦 Batch Download")
        st.markdown("Download all generated CAPL files as a ZIP package:")
        
        # Create ZIP file
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # Add CAPL files
            for capl_filename, capl_code in generated_files.items():
                zip_file.writestr(capl_filename, capl_code)
            
            # Add README
            readme_content = generate_readme(generated_files)
            zip_file.writestr("README.txt", readme_content)
            
            # Add setup instructions
            setup_content = generate_setup_guide()
            zip_file.writestr("SETUP_INSTRUCTIONS.txt", setup_content)
        
        zip_buffer.seek(0)
        
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="📦 Download All as ZIP",
                data=zip_buffer.getvalue(),
                file_name=f"CAPL_Modules_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
                mime="application/zip",
                key="download_zip"
            )
        
        with col2:
            st.info(f"**ZIP Package Contents:**\n"
                   f"- {len(generated_files)} CAPL module(s)\n"
                   f"- README.txt\n"
                   f"- SETUP_INSTRUCTIONS.txt")

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div class="info-box">
**About This Tool**

TXT to CAPL Converter v1.0 | Created for BCM Test Automation | November 2026

This tool automates conversion of test case specifications to CAPL test modules
for use in Vector CANoe Test Setup environment.

**Questions?** Check the Help section in the sidebar or review the SETUP_INSTRUCTIONS.txt 
in your downloaded ZIP package.
</div>
""", unsafe_allow_html=True)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def generate_readme(generated_files):
    """Generate README for the ZIP package"""
    readme = f"""
╔════════════════════════════════════════════════════════════════════════════╗
║                     TXT to CAPL CONVERTER - OUTPUT PACKAGE                 ║
║                                                                            ║
║  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}                                  ║
║  Total Files: {len(generated_files)}                                                        ║
╚════════════════════════════════════════════════════════════════════════════╝

PACKAGE CONTENTS
════════════════════════════════════════════════════════════════════════════

"""
    
    for idx, capl_filename in enumerate(generated_files.keys(), 1):
        readme += f"\n{idx}. {capl_filename}\n"
        readme += f"   └─ CAPL test module ready for CANoe Test Setup\n"
    
    readme += f"""

SETUP INSTRUCTIONS
════════════════════════════════════════════════════════════════════════════

1. IMPORT INTO CANOE
   - Open CANoe Test Setup
   - Right-click "CAPL Test Modules" in tree view
   - Select "New..." → "Add..."
   - Browse and select the .can files from this package
   - Click OK to load modules

2. VERIFY CONFIGURATION
   - Ensure all required DBC files are loaded in CANoe
   - Check the CANoe project has all 3 CAN channels configured:
     * ACCESS_CAN
     * BODY_CAN
     * BH_CAN

3. RUN TESTS
   - In CANoe Test Setup, select the test case name
   - Click START (or press F5)
   - Monitor Output Console for test execution
   - Results will display in real-time

4. VIEW RESULTS
   - Check Output Console for PASS/FAIL status
   - Each test phase is clearly marked
   - Final summary shows overall test result

TROUBLESHOOTING
════════════════════════════════════════════════════════════════════════════

Issue: "Unknown symbol" errors during compilation
→ Check that all required DBC files are properly loaded in CANoe
→ Verify signal names match the DBC definitions
→ Ensure CAN bus configuration is correct

Issue: Tests don't run
→ Verify testcase name matches the .can file name
→ Check CANoe is not already running this test case
→ Ensure CANoe Test Setup environment is properly configured

Issue: Signals not changing
→ Verify CAN messages are being transmitted
→ Check DBC signal definitions match test expectations
→ Monitor CAN traffic in CANoe while test runs

SIGNAL MAPPING
════════════════════════════════════════════════════════════════════════════

The tool maps test file signal names to actual CAN signals across 3 DBC files:
  • MODIFIED_F244_DBC_2024_10_04_ACCESS_CAN.dbc
  • MODIFIED_F244_DBC_2025_07_31_BODY_CAN.dbc
  • MODIFIED_F244_DBC_2025_10_31_BH_CAN.dbc

If signals are not found during test execution:
  1. Verify DBC files contain the signal definitions
  2. Check signal names in .txt files match DBC names
  3. Ensure DBC files are loaded in CANoe configuration

CUSTOM MODIFICATIONS
════════════════════════════════════════════════════════════════════════════

You can manually edit the .can files to:
  - Add additional signal checks
  - Modify wait times and delays
  - Add custom logic or constraints
  - Change assertion conditions

Note: Edit carefully - CAPL has strict syntax requirements. Refer to Vector
documentation for proper CAPL syntax.

SHARING WITH TEAMMATES
════════════════════════════════════════════════════════════════════════════

To share this package:
  1. Keep all files in this ZIP folder
  2. Send the entire ZIP to teammates
  3. They extract and follow Setup Instructions (step 1-3 above)
  4. CAPL modules are ready to use immediately
  5. No additional setup or configuration needed if DBC files are available

QUESTIONS?
════════════════════════════════════════════════════════════════════════════

For detailed information about:
  - CAPL syntax and features: See Vector CANoe documentation
  - Test setup process: Review SETUP_INSTRUCTIONS.txt
  - Signal mapping details: Check generated .can file comments

════════════════════════════════════════════════════════════════════════════
End of README - Generated by TXT to CAPL Converter Tool
════════════════════════════════════════════════════════════════════════════
"""
    
    return readme

def generate_setup_guide():
    """Generate setup instructions guide"""
    return """
╔════════════════════════════════════════════════════════════════════════════╗
║              CAPL TEST MODULES - SETUP & EXECUTION GUIDE                   ║
║                                                                            ║
║  For use with Vector CANoe Test Setup                                      ║
║  Requires: CANoe 11.0+ with CAPL Test Modules feature                     ║
╚════════════════════════════════════════════════════════════════════════════╝

SYSTEM REQUIREMENTS
════════════════════════════════════════════════════════════════════════════

✓ Vector CANoe 11.0 or later
✓ CANoe Test Setup module enabled
✓ CAPL Test Modules feature available
✓ DBC database files for your vehicle
✓ Proper CAN hardware/simulation setup

STEP 1: PREPARE CANOE PROJECT
════════════════════════════════════════════════════════════════════════════

1a. Open your CANoe project configuration
    - File → Open Project
    - Or create a new project

1b. Load all required DBC files:
    - Right-click "Databases" in tree
    - Select "Add Database..."
    - Add these DBC files (adjust paths as needed):
      • MODIFIED_F244_DBC_2024_10_04_ACCESS_CAN.dbc
      • MODIFIED_F244_DBC_2025_07_31_BODY_CAN.dbc
      • MODIFIED_F244_DBC_2025_10_31_BH_CAN.dbc

1c. Configure CAN channels:
    - Ensure your hardware is properly configured
    - Verify channel names match DBC assignments:
      • ACCESS_CAN (channel 1 or as configured)
      • BODY_CAN (channel 2 or as configured)
      • BH_CAN (channel 3 or as configured)

STEP 2: IMPORT CAPL TEST MODULES
════════════════════════════════════════════════════════════════════════════

2a. Open CANoe Test Setup
    - Window → Test Setup
    - Or Tools → Test Setup if not visible

2b. Add CAPL Test Modules
    - Right-click "CAPL Test Modules" in tree
    - Select "New..." → "Add..."
    - Browse to this package folder
    - Select the .can files you want to import
    - Click OK

2c. Verify import
    - Modules should appear under "CAPL Test Modules"
    - Each test case should be listed
    - No compilation errors should appear

STEP 3: CONFIGURE TEST ENVIRONMENT
════════════════════════════════════════════════════════════════════════════

3a. Set up test parameters (optional):
    - Right-click test case in tree
    - Select "Properties..."
    - Configure timeout, logging, etc.

3b. Configure signal sending:
    - Some tests may need MDF or transmit jobs
    - If signals won't change, enable:
      • CANoe simulation mode
      • Or connect to real hardware with transmitter

3c. Verify signal access:
    - Test modules include Write() diagnostics
    - These show if signals are found/not found
    - Check output during test execution

STEP 4: RUN A TEST CASE
════════════════════════════════════════════════════════════════════════════

4a. Select test case:
    - In Test Setup tree, click on test name
    - E.g., "TC_24959_KeyOff_Comfort_Test"

4b. Execute test:
    - Click "START" button
    - Or press F5
    - Or right-click and select "Start"

4c. Monitor execution:
    - Watch Output Console (View → Output)
    - Test proceeds through 6 phases:
      1. PRE-CONDITION - Initial setup
      2. STIMULATION-1 - Apply first conditions
      3. CHECK RESULTS-1 - Verify transitions
      4. STIMULATION-2 - Apply second conditions
      5. CHECK RESULTS-2 - Final verification
      6. POST-CONDITION - Cleanup

4d. Check results:
    - Console shows [PASS] or [FAIL] for each check
    - Final summary shows:
      ✓✓✓ PASS ✓✓✓  → All checks passed
      ✗✗✗ FAIL ✗✗✗  → Some checks failed

STEP 5: INTERPRET RESULTS
════════════════════════════════════════════════════════════════════════════

TEST OUTPUT FORMAT:
───────────────────────────────────────────────────────────────────────────

Test Case:          TC_24959 - Vehicle Status Test
Duration:           1234 ms
Total Checks:       4
Passed Checks:      4
Failed Checks:      0
Warning Checks:     1

OVERALL RESULT:     ✓✓✓ PASS ✓✓✓

WHAT THIS MEANS:
───────────────────────────────────────────────────────────────────────────

✓ PASS     → Check verified successfully
✗ FAIL     → Check failed - signal did not meet expectation
⚠ WARNING  → Check executed but with caveats (e.g., signal not found)
Duration   → Total time test took to execute (ms)
Total      → Number of verification checks

EXAMINING FAILURES:
───────────────────────────────────────────────────────────────────────────

If a check fails, review:
  1. Expected value - what should have happened
  2. Actual value - what actually happened
  3. Test phase - which stage of test it failed in
  4. Timestamp - when failure occurred

Common failure causes:
  • Signal not found in DBC - Add signal to DBC or update test
  • Signal value wrong - Check test stimulation conditions
  • Timing issue - Increase wait times if needed
  • DBC not loaded - Verify DBC is in CANoe configuration

DEBUGGING TIPS
════════════════════════════════════════════════════════════════════════════

1. VERIFY SIGNALS ARE LOADED
   - Insert a test Write() statement to check signal value
   - E.g., Write("Debug: Signal value = %d", MY_MESSAGE.Signal_Name);
   - If signal not found, it will show error in output

2. CHECK SIGNAL DEFINITIONS IN DBC
   - Use CANoe Database Editor to verify:
     • Signal name spelling
     • Message ID
     • Signal length and type
     • Min/max values

3. MONITOR CAN TRAFFIC
   - Window → Trace
   - Run test and monitor messages being sent/received
   - Verify CAN IDs and data values match expectations

4. TEST TIMING
   - Increase Wait() times if signals take longer to propagate
   - Modify "wait = X" in original .txt file
   - Regenerate .can file using converter tool

5. ENABLE CAPL DEBUGGING
   - Write() output shows detailed test execution flow
   - Each phase is clearly marked in output
   - Use this to trace execution step-by-step

COMMON ISSUES & SOLUTIONS
════════════════════════════════════════════════════════════════════════════

ISSUE: "Unknown symbol" compilation error
CAUSE: Signal or message name not in loaded DBC
FIX:   1. Verify DBC contains signal definition
       2. Check spelling matches DBC exactly
       3. Ensure DBC is loaded in CANoe

ISSUE: Tests run but signals don't change
CAUSE: CAN messages not being transmitted
FIX:   1. Enable CANoe simulation mode
       2. Verify CAN channel is active
       3. Check message definitions in DBC

ISSUE: Tests timeout or won't complete
CAUSE: Signal conditions never met
FIX:   1. Increase Wait() times
       2. Verify test stimulation values
       3. Check CAN message transmit setup

ISSUE: Different results each time test runs
CAUSE: Timing-sensitive or state-dependent test
FIX:   1. Ensure clean initial conditions
       2. Run test from same state each time
       3. Increase safety margins in timing

MODIFYING TESTS
════════════════════════════════════════════════════════════════════════════

You can edit the generated .can files to customize tests:

1. EDIT IN ANY TEXT EDITOR
   - Open .can file in Notepad++, VS Code, etc.
   - Or use CANoe CAPL Editor

2. MODIFY WAIT TIMES
   - Find: Wait(500);  // 500 ms
   - Change to: Wait(1000);  // 1000 ms

3. CHANGE SIGNAL VALUES
   - Find: STATUS_NBC_3.VehicleSts = 1;
   - Change to: STATUS_NBC_3.VehicleSts = 2;

4. ADD NEW CHECKS
   - Duplicate existing check block
   - Modify condition and signals
   - Follow CAPL syntax rules

5. RELOAD IN CANOE
   - Save modified .can file
   - Right-click test in Test Setup
   - Select "Reload"
   - Recompile if needed

CAPL SYNTAX QUICK REFERENCE
════════════════════════════════════════════════════════════════════════════

Variable declaration:
  int myVar = 0;
  dword timeVar = GetTickCount();

Send signal:
  MESSAGE_NAME.Signal_Name = value;

Read signal:
  int result = MESSAGE_NAME.Signal_Name;

Conditional:
  if (MESSAGE_NAME.Signal_Name == 1) { ... }

Output to console:
  Write("Debug: value = %d", varName);

Wait/delay:
  Wait(500);  // milliseconds

Comments:
  // Single line comment
  /* Multi-line
     comment */

BEST PRACTICES
════════════════════════════════════════════════════════════════════════════

1. ALWAYS START FROM CLEAN STATE
   - Run PRE-CONDITION phase every time
   - Reset all signals to known values
   - Prevents test cross-contamination

2. USE MEANINGFUL WAIT TIMES
   - 100 ms for fast response signals
   - 200-500 ms for ECU processing
   - 1000+ ms for user interaction signals

3. VERIFY EXPECTATIONS ARE REALISTIC
   - Signal transitions take real time
   - Hardware has processing delays
   - Timing margins prevent flaky tests

4. DOCUMENT CUSTOM MODIFICATIONS
   - Add comments explaining changes
   - Note why certain wait times are needed
   - Help teammates understand your edits

5. TEST IN BOTH SIMULATION AND HARDWARE
   - Simulation mode may not match real behavior
   - Some timing assumptions may be wrong
   - Always validate on real hardware

GETTING HELP
════════════════════════════════════════════════════════════════════════════

For detailed information:
  • CANoe Help: Press F1 in CANoe
  • CAPL Reference: CANoe → Help → CAPL Documentation
  • DBC Format: Vector documentation or DBC specification
  • Test results: Check README.txt in this package

════════════════════════════════════════════════════════════════════════════
End of Setup Guide - Ready to test!
════════════════════════════════════════════════════════════════════════════
"""
