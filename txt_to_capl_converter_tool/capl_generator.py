"""
CAPL Generator Module
=====================
Generates CAPL test modules from parsed test case specifications.

This generates complete, compilable CAPL code that can run in CANoe Test Setup.
"""

from signal_mapping import get_mapped_signal_name, is_signal_found


def generate_capl_module(parsed_data, include_comments=True, include_timing=True, report_format="Console"):
    """
    Generate CAPL test module from parsed test case data
    
    Args:
        parsed_data (dict): Parsed test case data from text_parser
        include_comments (bool): Include detailed comments in output
        include_timing (bool): Include timing measurements
        report_format (str): "Console", "CSV", or "Both"
        
    Returns:
        str: Complete CAPL module code
    """
    
    tc_id = parsed_data.get('test_case_id', 'Unknown_Test')
    description = parsed_data.get('description', 'Test case specification')
    wait_time = parsed_data.get('wait_time', 500)
    
    pre_cond = parsed_data.get('pre_condition', [])
    stim_1 = parsed_data.get('stimulation_1', [])
    expect_1 = parsed_data.get('expected_results_1', [])
    stim_2 = parsed_data.get('stimulation_2', [])
    expect_2 = parsed_data.get('expected_results_2', [])
    post_cond = parsed_data.get('post_condition', [])
    
    # Initialize template
    template = []
    
    # Header
    if include_comments:
        template.append("/*")
        template.append("=" * 75)
        template.append(f"  TEST MODULE: {tc_id}")
        template.append("=" * 75)
        template.append(f"  Description: {description}")
        template.append("")
        template.append("  Auto-generated CAPL test module for CANoe Test Setup")
        template.append("  Format: 6-phase test with pre-condition, stimulation, results check,")
        template.append("          and post-condition phases")
        template.append("")
        template.append("  PHASES:")
        template.append("    1. PRE-CONDITION - Initial state setup")
        template.append("    2. STIMULATION-1 - Apply first test conditions")
        template.append("    3. CHECK RESULTS-1 - Verify transitions")
        template.append("    4. STIMULATION-2 - Apply second test conditions")
        template.append("    5. CHECK RESULTS-2 - Final verification")
        template.append("    6. POST-CONDITION - Cleanup and reset")
        template.append("")
        template.append("  NOTES:")
        template.append("    - All wait times are in milliseconds")
        template.append("    - Signal syntax: MESSAGE_NAME.Signal_Name")
        template.append("    - Console output via Write() function")
        template.append("    - Test result: PASS if all checks pass, FAIL otherwise")
        template.append("")
        template.append("=" * 75)
        template.append("*/")
        template.append("")
    
    # Global variables for tracking
    template.append("// Test tracking variables")
    template.append("int g_TestPassed = 1;")
    template.append("int g_TotalChecks = 0;")
    template.append("int g_PassedChecks = 0;")
    template.append("int g_FailedChecks = 0;")
    template.append("int g_WarningChecks = 0;")
    template.append("")
    
    # Main testcase
    template.append(f"testcase {tc_id}()")
    template.append("{")
    template.append("  // Local variables")
    template.append("  int passed = 0;")
    template.append("  int failed = 0;")
    template.append("  int warnings = 0;")
    template.append("  int total = 0;")
    if include_timing:
        template.append("  dword startTime = GetTickCount();")
        template.append("  dword endTime;")
    template.append("")
    
    # Phase 1: Pre-condition
    template.append("  // " + "=" * 70)
    template.append("  // PHASE 1: PRE-CONDITION - Initial State Setup")
    template.append("  // " + "=" * 70)
    template.append("")
    
    if include_comments:
        template.append("  Write(\"\");")
        template.append("  Write(\"PHASE 1: PRE-CONDITION - Setting initial state...\");")
        template.append("")
    
    for item in pre_cond:
        signal = item.get('signal', '')
        value = item.get('value', '0')
        mapped = get_mapped_signal_name(signal)
        
        if mapped:
            template.append(f"  {mapped} = {value};")
        else:
            if include_comments:
                template.append(f"  // [NOT FOUND] {signal} = {value};")
    
    template.append("  Wait(100);")
    template.append("")
    
    # Phase 2: Stimulation-1
    template.append("  // " + "=" * 70)
    template.append("  // PHASE 2: STIMULATION-1 - Apply Test Conditions")
    template.append("  // " + "=" * 70)
    template.append("")
    
    if include_comments:
        template.append("  Write(\"\");")
        template.append("  Write(\"PHASE 2: STIMULATION-1 - Applying test conditions...\");")
        template.append("")
    
    for item in stim_1:
        signal = item.get('signal', '')
        value = item.get('value', '0')
        mapped = get_mapped_signal_name(signal)
        
        if mapped:
            template.append(f"  {mapped} = {value};")
        else:
            if include_comments:
                template.append(f"  // [NOT FOUND] {signal} = {value};")
    
    template.append(f"  Wait({wait_time});")
    template.append("")
    
    # Phase 3: Check Results-1
    template.append("  // " + "=" * 70)
    template.append("  // PHASE 3: CHECK EXPECTED RESULTS-1")
    template.append("  // " + "=" * 70)
    template.append("")
    
    if include_comments:
        template.append("  Write(\"\");")
        template.append("  Write(\"PHASE 3: CHECKING EXPECTED RESULTS-1...\");")
        template.append("")
    
    check_num = 1
    for item in expect_1:
        signal = item.get('signal', '')
        value = item.get('value', '')
        mapped = get_mapped_signal_name(signal)
        
        if mapped:
            # Handle transitions (e.g., 0->1)
            if '->' in str(value):
                expected, _ = str(value).split('->')
                expected = expected.strip()
            else:
                expected = value
            
            template.append(f"  total = total + 1;")
            template.append(f"  if ({mapped} == {expected}) {{")
            template.append(f"    passed = passed + 1;")
            template.append(f"    Write(\"  [PASS] Check {check_num}: {signal} == {expected}\");")
            template.append(f"  }} else {{")
            template.append(f"    failed = failed + 1;")
            template.append(f"    g_TestPassed = 0;")
            template.append(f"    Write(\"  [FAIL] Check {check_num}: {signal} - Expected: {expected}, Got: %d\", {mapped});")
            template.append(f"  }}")
            template.append("")
            check_num += 1
        else:
            if include_comments:
                template.append(f"  // [NOT FOUND] Check: {signal} = {value}")
                template.append("")
    
    template.append("  Wait(500);")
    template.append("")
    
    # Phase 4: Stimulation-2
    template.append("  // " + "=" * 70)
    template.append("  // PHASE 4: STIMULATION-2 - Apply Additional Conditions")
    template.append("  // " + "=" * 70)
    template.append("")
    
    if include_comments:
        template.append("  Write(\"\");")
        template.append("  Write(\"PHASE 4: STIMULATION-2 - Applying additional conditions...\");")
        template.append("")
    
    for item in stim_2:
        signal = item.get('signal', '')
        value = item.get('value', '0')
        mapped = get_mapped_signal_name(signal)
        
        if mapped:
            template.append(f"  {mapped} = {value};")
        else:
            if include_comments:
                template.append(f"  // [NOT FOUND] {signal} = {value};")
    
    template.append(f"  Wait({wait_time});")
    template.append("")
    
    # Phase 5: Check Results-2
    template.append("  // " + "=" * 70)
    template.append("  // PHASE 5: CHECK EXPECTED RESULTS-2")
    template.append("  // " + "=" * 70)
    template.append("")
    
    if include_comments:
        template.append("  Write(\"\");")
        template.append("  Write(\"PHASE 5: CHECKING EXPECTED RESULTS-2...\");")
        template.append("")
    
    for item in expect_2:
        signal = item.get('signal', '')
        value = item.get('value', '')
        mapped = get_mapped_signal_name(signal)
        
        if mapped:
            # Handle transitions
            if '->' in str(value):
                expected, _ = str(value).split('->')
                expected = expected.strip()
            else:
                expected = value
            
            template.append(f"  total = total + 1;")
            template.append(f"  if ({mapped} == {expected}) {{")
            template.append(f"    passed = passed + 1;")
            template.append(f"    Write(\"  [PASS] Check {check_num}: {signal} == {expected}\");")
            template.append(f"  }} else {{")
            template.append(f"    failed = failed + 1;")
            template.append(f"    g_TestPassed = 0;")
            template.append(f"    Write(\"  [FAIL] Check {check_num}: {signal} - Expected: {expected}, Got: %d\", {mapped});")
            template.append(f"  }}")
            template.append("")
            check_num += 1
        else:
            if include_comments:
                template.append(f"  // [NOT FOUND] Check: {signal} = {value}")
                template.append("")
    
    # Phase 6: Post-condition
    template.append("  // " + "=" * 70)
    template.append("  // PHASE 6: POST-CONDITION - Cleanup and Reset")
    template.append("  // " + "=" * 70)
    template.append("")
    
    if include_comments:
        template.append("  Write(\"\");")
        template.append("  Write(\"PHASE 6: POST-CONDITION - Resetting to initial state...\");")
        template.append("")
    
    for item in post_cond:
        signal = item.get('signal', '')
        value = item.get('value', '0')
        mapped = get_mapped_signal_name(signal)
        
        if mapped:
            template.append(f"  {mapped} = {value};")
        else:
            if include_comments:
                template.append(f"  // [NOT FOUND] {signal} = {value};")
    
    template.append("")
    
    # Test Summary
    if include_timing:
        template.append("  endTime = GetTickCount();")
    
    template.append("")
    template.append("  // " + "=" * 70)
    template.append("  // TEST SUMMARY")
    template.append("  // " + "=" * 70)
    template.append("")
    
    if include_timing:
        template.append("  Write(\"\");")
        template.append("  Write(\"═══════════════════════════════════════════════════════════════════\");")
        template.append("  Write(\"TEST EXECUTION SUMMARY\");")
        template.append("  Write(\"═══════════════════════════════════════════════════════════════════\");")
        template.append("  Write(\"\");")
        template.append("  Write(\"Test Case:          %s\", \"%s\");" % (tc_id, tc_id))
        template.append("  Write(\"Duration:           %%d ms\", (endTime - startTime));")
    else:
        template.append("  Write(\"\");")
        template.append("  Write(\"═══════════════════════════════════════════════════════════════════\");")
        template.append("  Write(\"TEST EXECUTION SUMMARY\");")
        template.append("  Write(\"═══════════════════════════════════════════════════════════════════\");")
        template.append("  Write(\"\");")
    
    template.append("  Write(\"Total Checks:       %%d\", total);")
    template.append("  Write(\"Passed Checks:      %%d\", passed);")
    template.append("  Write(\"Failed Checks:      %%d\", failed);")
    template.append("  Write(\"Warning Checks:     %%d\", warnings);")
    template.append("  Write(\"\");")
    
    template.append("")
    template.append("  if (g_TestPassed == 1 && failed == 0) {")
    template.append("    Write(\"OVERALL RESULT:     ✓✓✓ PASS ✓✓✓\");")
    template.append("  } else {")
    template.append("    Write(\"OVERALL RESULT:     ✗✗✗ FAIL ✗✗✗\");")
    template.append("  }")
    
    template.append("")
    template.append("  Write(\"\");")
    template.append("  Write(\"═══════════════════════════════════════════════════════════════════\");")
    template.append("  Write(\"TEST EXECUTION COMPLETE\");")
    template.append("  Write(\"═══════════════════════════════════════════════════════════════════\");")
    template.append("")
    template.append("}")
    
    # Footer
    template.append("")
    template.append("/*")
    template.append("=" * 75)
    template.append("  END OF TEST MODULE")
    template.append("=" * 75)
    template.append("*/")
    
    return "\n".join(template)
