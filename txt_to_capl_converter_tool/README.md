╔════════════════════════════════════════════════════════════════════════════╗
║                     TXT TO CAPL CONVERTER TOOL v1.0                         ║
║                                                                            ║
║          Convert test case .txt files to CAPL test modules (.can)          ║
║                                                                            ║
║  Author: BCM Test Automation                                               ║
║  Date: November 2026                                                       ║
║  License: Internal Use Only                                                ║
╚════════════════════════════════════════════════════════════════════════════╝


OVERVIEW
════════════════════════════════════════════════════════════════════════════

The TXT to CAPL Converter Tool is a web-based application that automates the
conversion of test case specifications (in .txt format) into CAPL test modules
(.can files) ready for use in Vector CANoe Test Setup.

This tool streamlines test automation workflow by:
  ✓ Parsing structured test case text files
  ✓ Automatically mapping signal names to CAN signals
  ✓ Generating compilable CAPL test modules
  ✓ Supporting batch processing of multiple files
  ✓ Providing easy download and sharing capabilities


KEY FEATURES
════════════════════════════════════════════════════════════════════════════

📤 Multi-File Upload
  - Upload one or more .txt test case files at once
  - Automatic parsing and processing
  - Real-time progress tracking

🔄 Intelligent Signal Mapping
  - Maps test file signal names to actual CAN signals
  - Cross-references 3 DBC databases (ACCESS_CAN, BODY_CAN, BH_CAN)
  - Marks unmapped signals for manual review

📝 CAPL Code Generation
  - Generates complete, compilable CAPL modules
  - Includes 6-phase test framework:
    1. PRE-CONDITION - Initial state setup
    2. STIMULATION-1 - Apply first test conditions
    3. CHECK RESULTS-1 - Verify transitions
    4. STIMULATION-2 - Apply additional conditions
    5. CHECK RESULTS-2 - Final verification
    6. POST-CONDITION - Cleanup and reset
  - Automatic pass/fail tracking and reporting

📥 Multiple Download Options
  - Download individual CAPL files
  - Batch download as ZIP package
  - Includes README and setup instructions
  - Ready to share with teammates

⚙️ Customizable Output
  - Choose detail level (comments on/off)
  - Include/exclude timing measurements
  - Select report format (Console, CSV, or Both)


QUICK START (5 MINUTES)
════════════════════════════════════════════════════════════════════════════

1. INSTALL PYTHON ENVIRONMENT
   
   Windows:
   • Make sure Python 3.8+ is installed (from python.org)
   • OR use system Python if available

2. INSTALL DEPENDENCIES
   
   Navigate to tool directory and run:
   
   Windows (PowerShell):
   > python -m pip install -r requirements.txt
   
   Windows (Command Prompt):
   > python -m pip install -r requirements.txt
   
   Alternative (if above doesn't work):
   > pip install streamlit

3. START THE APPLICATION
   
   Windows (PowerShell):
   > streamlit run app.py
   
   Or use the provided launch script:
   > .\run_tool.bat
   
   The app opens in your default browser at: http://localhost:8501

4. USE THE TOOL
   
   • Click "Choose .txt files" to select test case files
   • Adjust settings in the right panel (optional)
   • Files process automatically
   • Download individual files or entire ZIP package
   • Share generated .can files with teammates

5. IMPORT INTO CANOE
   
   • Open CANoe Test Setup
   • Right-click "CAPL Test Modules" → "New..." → "Add..."
   • Select the generated .can files
   • Click OK
   • Tests are ready to run!


INSTALLATION DETAILS
════════════════════════════════════════════════════════════════════════════

SYSTEM REQUIREMENTS:
  • Windows 10/11 or macOS or Linux
  • Python 3.8 or later
  • 50 MB free disk space
  • Web browser (Chrome, Firefox, Edge, Safari)
  • No internet required (runs locally)

STEP 1: Install Python
─────────────────────────────────────────────────────────────────────────

If not already installed:
  1. Visit https://www.python.org/downloads/
  2. Download Python 3.10+ (recommended)
  3. Run installer with "Add Python to PATH" checked
  4. Verify: Open Command Prompt, type "python --version"

STEP 2: Set Up Virtual Environment (Optional but Recommended)
─────────────────────────────────────────────────────────────────────────

Create isolated environment:

Windows (PowerShell):
  > python -m venv venv
  > .\venv\Scripts\Activate.ps1

Windows (Command Prompt):
  > python -m venv venv
  > venv\Scripts\activate.bat

macOS/Linux:
  $ python3 -m venv venv
  $ source venv/bin/activate

STEP 3: Install Dependencies
─────────────────────────────────────────────────────────────────────────

Install required packages:

  > pip install -r requirements.txt

Verify installation:
  > streamlit --version

STEP 4: Run Application
─────────────────────────────────────────────────────────────────────────

Start the web application:

  > streamlit run app.py

Expected output:
  You can now view your Streamlit app in your browser.
  
  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501

The app automatically opens in your default browser. If not:
  → Manually navigate to http://localhost:8501


TOOL USAGE GUIDE
════════════════════════════════════════════════════════════════════════════

1. UPLOAD FILES
   
   Click "Choose .txt files" button and select one or more test case files.
   
   Supported format:
   • File extension: .txt
   • File size: Up to 10 MB
   • Quantity: Unlimited
   
   Example filenames:
   • TC_24959 - TC_F040_NBC_VehicleSts_Comfort_KeyOff.txt
   • TC_24960 - TC_F040_NBC_VehicleSts_KeyOn_KeyOff.txt

2. CONFIGURE OPTIONS (Sidebar)
   
   Include detailed comments:
   ✓ ON (default) - Extensive comments in generated code
   ✗ OFF - Minimal comments for compact code
   
   Include timing details:
   ✓ ON (default) - Timing measurements, GetTickCount()
   ✗ OFF - No timing (for time-uncritical tests)
   
   Report format:
   • Console (default) - Write() output to CANoe console
   • CSV - File-based reporting (requires CAPL I/O)
   • Both - Both console and CSV outputs

3. PROCESS FILES
   
   Click "Upload" or simply select files - processing is automatic:
   • Progress bar shows processing status
   • Each file is parsed individually
   • CAPL code is generated per file
   • Errors are reported clearly

4. REVIEW RESULTS
   
   Success page shows:
   ✓ Number of files processed
   ✗ Number of errors (if any)
   ✓ Ready to download count
   
   Each generated file shows:
   • Filename: test_case_id.can
   • Lines of Code: automatically calculated
   • Generated timestamp
   • Download button
   • Code preview option

5. DOWNLOAD FILES
   
   Two options:
   
   A) Individual Download
   → Click "📥 Download" button on each file tab
   → Single .can file is downloaded
   → Use for single test import
   
   B) Batch Download
   → Click "📦 Download All as ZIP"
   → All .can files plus documentation
   → Recommended for sharing with teammates
   → ZIP includes:
     - All generated .can modules
     - README.txt (instructions)
     - SETUP_INSTRUCTIONS.txt (detailed guide)

6. IMPORT INTO CANOE
   
   After downloading:
   
   Step 1: Prepare CANoe
   • Open your CANoe project
   • Load all required DBC files
   • Configure CAN channels
   
   Step 2: Import Modules
   • Window → Test Setup
   • Right-click "CAPL Test Modules"
   • Select "New..." → "Add..."
   • Browse and select .can files
   • Click OK
   
   Step 3: Run Tests
   • Select test case
   • Click START (or F5)
   • Monitor Output Console
   • Check [PASS] / [FAIL] results

7. SHARE WITH TEAMMATES
   
   • Use "Download All as ZIP" to create package
   • Share ZIP file via email/file sharing
   • Teammates extract ZIP on their machine
   • They follow SETUP_INSTRUCTIONS.txt
   • Ready to use - no reconfiguration needed!


INPUT FILE FORMAT
════════════════════════════════════════════════════════════════════════════

Test case files should follow this format:

// PRE-CONDITION
signal_name = value
signal_name = value

// STIMULATION-1: Description of what this phase does
signal_name = value
signal_name = value

// EXPECTED RESULTS-1: Check if conditions are met
signal_name = expected_value
signal_name = initial_value->final_value

// STIMULATION-2: Description of additional conditions
signal_name = value
wait = 0.5

// EXPECTED RESULTS-2: Final verification checks
signal_name = expected_value
signal_name = initial_value->final_value

// POST-CONDITION
signal_name = value
signal_name = value


SECTION EXPLANATIONS:

PRE-CONDITION
  Sets initial state of all signals
  Executed once at beginning
  Example:
    si_sys_NFR_NFR_Speed_FA = 0
    si_sys_SGW_EngineSts = 0

STIMULATION-1
  Applies first set of test conditions
  Triggers state transitions
  Example:
    si_sys_STS_LH_DoorStatus = 3
    si_sys_SGW_HMISts = 1

EXPECTED RESULTS-1
  Verifies signal changes in response to Stimulation-1
  Can check absolute values or transitions
  Example:
    so_sys_F040_VehicleSts = 0->1    (checks transition from 0 to 1)
    XCP_sys_F908_UserPresence = 2    (checks absolute value)

STIMULATION-2
  Applies second set of conditions
  Optional wait time between actions
  Example:
    si_sys_NPS_ParkingLightsCommand = 0
    wait = 0.5                        (500 milliseconds)

EXPECTED RESULTS-2
  Final verification after all stimulations
  Confirms stable state
  Example:
    so_sys_F040_VehicleSts = 1

POST-CONDITION
  Resets all signals to safe/initial state
  Cleans up after test
  Example:
    si_sys_STS_LH_DoorStatus = 1


SIGNAL MAPPING
════════════════════════════════════════════════════════════════════════════

The tool maintains a signal mapping database that translates test file signal
names to actual CAN signal names from the DBC database files.

Currently mapped signals (11 found):
  ✓ NFR_Speed_FA (BODY_CAN)
  ✓ NFR_Speed_FA_FailSts (BODY_CAN)
  ✓ StopStartSts (ACCESS_CAN)
  ✓ EngineSts (ACCESS_CAN)
  ✓ PowertrainSts (ACCESS_CAN)
  ✓ STS_LH_DoorStatus (BH_CAN)
  ✓ IgnPosSts (ACCESS_CAN)
  ✓ HMISts (ACCESS_CAN)
  ✓ EXT_LGH_ParkingLightCmd (ACCESS_CAN)
  ✓ VehicleSts (BODY_CAN)
  ✓ UserPresence (BODY_CAN)

Unmapped signals (not found in DBC files):
  ✗ Proxy_write_Power_Unit_Extended (Requires XCP access)
  ✗ si_sys_TcSen_bTerm15_1 (MCore internal)
  ✗ si_sys_TcSen_bTerm15_2 (MCore internal)
  ✗ si_sys_TcSen_bTermS (MCore internal)
  ✗ so_sys_F040_KeySts_* (Multi-CAN coordination)

For unmapped signals, the tool will:
  1. Comment out the signal assignment in generated code
  2. Mark with [NOT FOUND] in comments
  3. Add warning to output

To add new signal mappings:
  1. Edit signal_mapping.py
  2. Add signal entry to SIGNAL_MAPPING dictionary
  3. Provide: signal name, message name, DBC file
  4. Restart application


TROUBLESHOOTING
════════════════════════════════════════════════════════════════════════════

PROBLEM: "Command not found: streamlit"
SOLUTION:
  • Python may not be in PATH
  • Try: python -m streamlit run app.py
  • Or verify pip install completed successfully

PROBLEM: "ModuleNotFoundError: No module named 'streamlit'"
SOLUTION:
  • Dependencies not installed
  • Run: pip install -r requirements.txt
  • Verify with: pip list

PROBLEM: Port 8501 already in use
SOLUTION:
  • Another Streamlit app is running
  • Close other Streamlit windows
  • Or specify different port: streamlit run app.py --server.port 8502

PROBLEM: Browser won't open automatically
SOLUTION:
  • Manually open http://localhost:8501
  • Check if browser is set as default
  • Try different browser (Chrome, Firefox, Edge)

PROBLEM: "Unknown symbol" error when compiling CAPL in CANoe
SOLUTION:
  • DBC files not loaded in CANoe
  • Verify all 3 DBC files are present and loaded
  • Check signal names match DBC exactly
  • Review signal_mapping.py for correct mappings

PROBLEM: Generated CAPL won't run
SOLUTION:
  • Missing CAPL Test Setup module in CANoe
  • Verify project has CAPL Test Modules enabled
  • Check test name matches file name
  • Ensure CAN channels are properly configured

PROBLEM: Test runs but signals don't change
SOLUTION:
  • CAN messages not being transmitted
  • Enable CANoe simulation mode
  • Verify message definitions in DBC
  • Check CAN hardware configuration
  • Increase Wait() times if needed


ADVANCED TOPICS
════════════════════════════════════════════════════════════════════════════

CUSTOMIZING SIGNAL MAPPINGS

If you need to map additional signals:

1. Open signal_mapping.py in a text editor
2. Find the SIGNAL_MAPPING dictionary
3. Add your signal in the "signals" section:

   "your_signal_name": {
       "mapped_name": "SIGNAL_NAME",
       "message": "MESSAGE_NAME",
       "dbc": "ACCESS_CAN",  # or BODY_CAN or BH_CAN
       "found": True,
       "category": "Your Category",
       "description": "Signal description"
   }

4. Save the file
5. Restart the application
6. Your signal is now available for processing

MODIFYING GENERATED CAPL CODE

After generating .can files:

1. Open in text editor (Notepad++, VS Code, etc.)
2. Edit CAPL code as needed:
   • Change signal values
   • Modify wait times
   • Add custom logic
   • Fix compilation errors

3. Options:
   • Use in CANoe directly
   • Or regenerate from .txt with updated mapping

4. Remember CAPL syntax rules:
   • Variables must be declared before use
   • Case-sensitive (MESSAGE.Signal vs message.signal)
   • No complex expressions in conditions
   • Use Write() for console output

BATCH PROCESSING MULTIPLE PROJECTS

To process many test files:

1. Place all .txt files in one folder
2. Upload all at once to tool
3. Download ZIP package
4. Extract to your project
5. Import all .can files to CANoe
6. Run test suite


PERFORMANCE NOTES
════════════════════════════════════════════════════════════════════════════

• Processing speed: ~100-500 files per second
• Maximum file size: 10 MB per file
• Recommended batch size: 10-50 files
• Memory usage: ~50-100 MB
• Network: None (runs locally)
• Browser resource usage: Minimal


GETTING SUPPORT
════════════════════════════════════════════════════════════════════════════

For issues or questions:

1. Check TROUBLESHOOTING section above
2. Review SETUP_INSTRUCTIONS.txt (included in ZIP)
3. Examine error messages in browser console (F12)
4. Check CANoe CAPL documentation
5. Verify DBC file definitions
6. Test with simple .txt file first
7. Contact BCM Test Automation team

Documentation:
  • CANoe Help: Press F1 in CANoe
  • CAPL Reference: CANoe → Help → CAPL Documentation
  • DBC Format: Vector documentation
  • Streamlit: https://docs.streamlit.io


CONTRIBUTING IMPROVEMENTS
════════════════════════════════════════════════════════════════════════════

This tool can be extended with:
  • New signal mappings
  • Additional DBC file support
  • Custom CAPL templates
  • Advanced report generation
  • Integration with CI/CD systems
  • Database backends

Contact BCM Test Automation team for custom enhancements.


VERSION HISTORY
════════════════════════════════════════════════════════════════════════════

v1.0 (November 2026)
  ✓ Initial release
  ✓ Multi-file upload and batch processing
  ✓ Automatic signal mapping (11 signals)
  ✓ 6-phase CAPL test generation
  ✓ Pass/fail tracking
  ✓ Individual and batch download
  ✓ ZIP package with documentation
  ✓ Streamlit web interface
  ✓ Cross-platform support (Windows/Mac/Linux)


DISCLAIMER
════════════════════════════════════════════════════════════════════════════

This tool is provided as-is for internal use by BCM Test Automation team.

Generated CAPL code is based on test specifications provided in .txt files.
Users are responsible for:
  • Verifying generated code correctness
  • Ensuring signal mappings match their DBC definitions
  • Testing generated CAPL modules before production use
  • Maintaining test case specifications
  • Backing up critical test cases

The tool authors are not responsible for:
  • Incorrect signal mappings (user must verify)
  • DBC file content or accuracy
  • CANoe configuration or licensing
  • Test execution results or failures


════════════════════════════════════════════════════════════════════════════
End of README

For the latest version and updates, check with BCM Test Automation team.
════════════════════════════════════════════════════════════════════════════
