"""
Text Parser Module
==================
Parses test case .txt files and extracts test specifications.

Format:
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
"""

import re
from pathlib import Path

class TestCaseParser:
    """Parse test case .txt files into structured data"""
    
    def __init__(self):
        self.sections = {
            'pre_condition': [],
            'stimulation_1': [],
            'expected_results_1': [],
            'stimulation_2': [],
            'expected_results_2': [],
            'post_condition': []
        }
        self.test_case_id = ""
        self.description = ""
        self.wait_time = 500  # default 500ms
        
    def extract_test_case_id(self, filename):
        """Extract test case ID from filename
        
        Examples:
          TC_24959 - TC_F040_NBC_VehicleSts_Comfort_KeyOff.txt
          → TC_24959_KeyOff_Comfort_Test
        """
        # Remove .txt extension
        name_no_ext = Path(filename).stem
        
        # Extract TC number
        tc_match = re.search(r'TC_(\d+)', name_no_ext)
        if not tc_match:
            return "TC_Unknown_Test"
        
        tc_num = tc_match.group(1)
        
        # Extract meaningful part of name
        parts = name_no_ext.split(' - ')
        if len(parts) > 1:
            desc = parts[1].replace('TC_F040_NBC_VehicleSts_', '')
            desc = desc.replace('TC_F040_NBC_', '')
            # Capitalize appropriately
            desc = desc.replace('_', ' ').title().replace(' ', '')
            return f"TC_{tc_num}_{desc}_Test"
        
        return f"TC_{tc_num}_Test"
    
    def parse_line(self, line):
        """Parse a single line and extract signal assignment
        
        Returns: (signal_name, value_or_transition) or None if not parseable
        """
        # Remove comments
        line = line.split('//')[0].strip()
        if not line:
            return None
        
        # Match: signal_name = value
        match = re.match(r'(\w+)\s*=\s*(.+)', line)
        if match:
            signal_name = match.group(1).strip()
            value = match.group(2).strip()
            return (signal_name, value)
        
        return None
    
    def parse_content(self, content, filename):
        """Parse complete test file content"""
        self.test_case_id = self.extract_test_case_id(filename)
        
        lines = content.split('\n')
        current_section = None
        
        for line in lines:
            line_stripped = line.strip()
            
            # Detect section headers
            if '// PRE-CONDITION' in line:
                current_section = 'pre_condition'
                continue
            elif '// STIMULATION-1' in line:
                current_section = 'stimulation_1'
                self.description = line.replace('// STIMULATION-1:', '').strip()
                continue
            elif '// EXPECTED RESULTS-1' in line:
                current_section = 'expected_results_1'
                continue
            elif '// STIMULATION-2' in line:
                current_section = 'stimulation_2'
                self.description = line.replace('// STIMULATION-2:', '').strip()
                continue
            elif '// EXPECTED RESULTS-2' in line:
                current_section = 'expected_results_2'
                continue
            elif '// POST-CONDITION' in line:
                current_section = 'post_condition'
                continue
            
            # Parse line
            if current_section:
                parsed = self.parse_line(line)
                if parsed:
                    signal_name, value = parsed
                    
                    # Handle wait time
                    if signal_name.lower() == 'wait':
                        try:
                            wait_seconds = float(value)
                            self.wait_time = int(wait_seconds * 1000)
                        except:
                            pass
                    else:
                        self.sections[current_section].append({
                            'signal': signal_name,
                            'value': value
                        })
    
    def to_dict(self):
        """Convert parser state to dictionary"""
        return {
            'test_case_id': self.test_case_id,
            'description': self.description,
            'wait_time': self.wait_time,
            'pre_condition': self.sections['pre_condition'],
            'stimulation_1': self.sections['stimulation_1'],
            'expected_results_1': self.sections['expected_results_1'],
            'stimulation_2': self.sections['stimulation_2'],
            'expected_results_2': self.sections['expected_results_2'],
            'post_condition': self.sections['post_condition']
        }


def parse_test_case(content, filename):
    """
    Parse a test case .txt file
    
    Args:
        content (str): File content
        filename (str): Original filename
        
    Returns:
        dict: Parsed test case data
        
    Raises:
        ValueError: If parsing fails
    """
    try:
        parser = TestCaseParser()
        parser.parse_content(content, filename)
        return parser.to_dict()
    except Exception as e:
        raise ValueError(f"Failed to parse test case: {str(e)}")
