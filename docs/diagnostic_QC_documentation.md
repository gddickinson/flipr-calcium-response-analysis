# FLIPR Analysis Tool: Diagnostic System Documentation

## Table of Contents
1. [Introduction](#introduction)
2. [Diagnostic Architecture](#diagnostic-architecture)
3. [Data Organization](#data-organization)
4. [Control Configuration](#control-configuration)
5. [Quality Control Tests](#quality-control-tests)
   - [Injection Artifact Tests](#injection-artifact-tests)
   - [Raw Baseline Tests](#raw-baseline-tests)
   - [ΔF/F₀ Tests](#δff₀-tests)
   - [Control Tests](#control-tests)
   - [Sample Response Tests](#sample-response-tests)
6. [Normalization Methods](#normalization-methods)
7. [Diagnostic Thresholds](#diagnostic-thresholds)
8. [Diagnosis Decision Process](#diagnosis-decision-process)
9. [Visualization and Reporting](#visualization-and-reporting)
10. [Parameter Customization](#parameter-customization)
11. [Troubleshooting](#troubleshooting)

## Introduction

The diagnostic system in the FLIPR Analysis Tool is designed to analyze calcium responses in a standardized, reproducible manner with built-in quality control. The system was initially developed for autism risk assessment through purinergic signaling analysis but can be adapted for other clinical and research applications.

The diagnostic pipeline consists of:
1. Data acquisition and organization by well type
2. Quality control tests to validate data integrity
3. Normalization of ATP responses to reference signals
4. Application of diagnostic thresholds
5. Result determination and visualization

## Diagnostic Architecture

### Core Components

The diagnostic system is implemented through several interlinked classes:

- **DiagnosisOptionsTab**: UI component for configuring diagnostic parameters
- **DiagnosticTests**: Core class that performs the diagnostic analysis
- **WellPlateLabeler**: Parent class that manages the overall application workflow

### Workflow

1. User configures control columns and test parameters in the DiagnosisOptionsTab
2. User enables "Generate Diagnosis" in the Analysis tab
3. The DiagnosticTests class analyzes the data when process_data() is called
4. Test results are logged and stored in the diagnosis_results object
5. Results are displayed in the UI and can be exported to Excel

## Data Organization

The diagnostic system organizes plate data into specific categories:

### Well Types
- **ATP wells**: Contain cells stimulated with ATP
- **Ionomycin wells**: Maximum calcium response reference
- **Buffer wells**: Background response control

### Control Groups
- **Test Samples**: Patient/experimental samples
- **NTC Control**: No cells control
- **Positive Control**: Known response reference

### Sample Organization

Data is organized by sample ID, allowing for matching ATP responses to corresponding ionomycin responses from the same sample. This is critical for proper normalization and diagnosis.

## Control Configuration

### Column Configuration

The diagnostic system uses column-based organization:

- **Test Sample Columns**: Columns containing experimental samples
- **NTC Control Columns**: Columns containing wells with no cells
- **Positive Control Columns**: Columns containing reference samples

### Well Layout

Within each column, wells are organized by type:
- ATP wells (typically 3 per column)
- Ionomycin wells (typically 3 per column)
- Buffer wells (typically 2 per column)

### Implementation

The DiagnosticTests class identifies wells based on their column position and label. Each well is categorized by:
- Column type (sample, NTC, positive control)
- Well type (ATP, ionomycin, buffer)
- Sample ID (from well metadata)

```python
# Example of well grouping
for idx in range(96):
    well_data = self.parent.well_data[idx]
    well_id = well_data['well_id']
    
    # Skip wells without data
    if not well_id or well_id not in self.parent.dff_data.index:
        continue
        
    # Get well location
    row, col = self.get_row_col(well_id)
    
    # Determine well type based on label
    label = well_data.get("label", "").lower()
    sample_id = well_data.get("sample_id", "default")
    
    # Group wells based on column and label
    if col in sample_cols:
        if "atp" in label:
            sample_wells[sample_id]['atp'].append(well_id)
        elif "ionom" in label:
            sample_wells[sample_id]['iono'].append(well_id)
        elif "buffer" in label or "hbss" in label:
            sample_wells[sample_id]['buffer'].append(well_id)
```

## Quality Control Tests

Each diagnostic test validates a specific aspect of data quality. All tests must pass for a diagnosis to be considered valid.

### Injection Artifact Tests

#### check_artifact
- **Purpose**: Ensures the injection artifact is within acceptable limits
- **Parameters**: 
  - `max_change`: Maximum allowable signal change during injection (default: 0.2)
  - `max_frames`: Maximum time to return to baseline (frames) (default: 5)
- **Implementation**: Examines signal change during the injection window and ensures recovery afterward
- **Failure Conditions**: Large artifacts can indicate poor injection technique or excessive signal perturbation

### Raw Baseline Tests

These tests validate the raw signal quality before normalization.

#### check_raw_baseline_min
- **Purpose**: Ensures raw baseline is above minimum detection threshold
- **Parameters**: 
  - `min_value`: Minimum acceptable baseline value (default: 100)
- **Implementation**: 
  ```python
  def check_raw_min(self, results, min_value):
      """Check raw baseline minimum is above threshold"""
      all_passed = True
      failed_groups = []
      
      # Check controls and samples (ATP wells)
      for control_type, control_data in results['controls'].items():
          if control_data['status'] == 'ok':
              for type_name, type_data in control_data['types'].items():
                  if type_data['status'] == 'ok' and 'raw_baseline' in type_data:
                      if type_data['raw_baseline']['min'] < min_value:
                          all_passed = False
                          failed_groups.append(f"{control_type} {type_name}")
                          
      # Similar check for sample ATP wells
      
      # Return result
      return {
          'passed': all_passed,
          'message': message
      }
  ```
- **Failure Conditions**: Low signal indicates poor dye loading or cell health

#### check_raw_baseline_max
- **Purpose**: Ensures baseline is below saturation
- **Parameters**: 
  - `max_value`: Maximum acceptable baseline value (default: 5000)
- **Implementation**: Compares raw baseline against upper limit
- **Failure Conditions**: High baselines indicate potential saturation or excessive dye loading

#### check_raw_baseline_mean
- **Purpose**: Ensures baseline is within optimal detection range
- **Parameters**: 
  - `min_value`: Minimum acceptable mean (default: 500)
  - `max_value`: Maximum acceptable mean (default: 3000)
- **Implementation**: Analyzes mean baseline value across all wells
- **Failure Conditions**: Outlier means indicate inconsistent dye loading or cell distribution

#### check_raw_baseline_sd
- **Purpose**: Validates baseline stability
- **Parameters**: 
  - `max_sd`: Maximum acceptable standard deviation (default: 200)
- **Implementation**: Calculates SD of the baseline period
- **Failure Conditions**: High SD indicates unstable baseline or poor signal quality

### ΔF/F₀ Tests

These tests validate the normalized calcium response signal quality.

#### check_dff_baseline
- **Purpose**: Ensures ΔF/F₀ baseline is approximately zero
- **Parameters**: 
  - `max_deviation`: Maximum acceptable deviation from zero (default: 0.05)
- **Implementation**: 
  ```python
  def check_dff_baseline(self, results, max_deviation):
      """Check ΔF/F₀ baseline is close to zero"""
      all_passed = True
      failed_groups = []
      
      # Check controls (excluding NTC)
      for control_type, control_data in results['controls'].items():
          if control_type != 'ntc' and control_data['status'] == 'ok':
              for type_name, type_data in control_data['types'].items():
                  if type_name != 'buffer' and type_data['status'] == 'ok' and 'dff_baseline' in type_data:
                      mean = abs(type_data['dff_baseline']['mean'])
                      if mean > max_deviation:
                          all_passed = False
                          failed_groups.append(f"{control_type} {type_name}")
                          
      # Return result
      return {
          'passed': all_passed,
          'message': message
      }
  ```
- **Failure Conditions**: Non-zero baseline indicates improper F₀ calculation

#### check_dff_return
- **Purpose**: Validates signal return to baseline after response
- **Parameters**: 
  - `max_deviation`: Maximum deviation at end (default: 0.05)
  - `time_point`: Time to check (s) (default: 60)
- **Implementation**: Checks end-of-trace signal level
- **Failure Conditions**: Persistent elevation indicates incomplete recovery or signal drift

#### check_peak_height
- **Purpose**: Ensures response magnitude is within physiological range
- **Parameters**: 
  - `min_height`: Minimum peak height (default: 0.1)
  - `max_height`: Maximum peak height (default: 3.0)
- **Implementation**: Analyzes peak ΔF/F₀ values
- **Failure Conditions**: Very low or high responses indicate poor cell health or abnormal responses

#### check_peak_width
- **Purpose**: Validates response duration
- **Parameters**: 
  - `min_width`: Minimum width (s) (default: 5)
  - `max_width`: Maximum width (s) (default: 30)
- **Implementation**: Calculates full-width at half-maximum (FWHM)
- **Failure Conditions**: Abnormal kinetics can indicate cell health issues

#### check_auc
- **Purpose**: Ensures total calcium response is within expected range
- **Parameters**: 
  - `min_auc`: Minimum area under curve (default: 1.0)
  - `max_auc`: Maximum area under curve (default: 100.0)
- **Implementation**: Calculates area under ΔF/F₀ curve
- **Failure Conditions**: Abnormal AUC indicates unusual response dynamics

### Control Tests

These tests validate the quality of control wells and ensure proper normalization references.

#### check_pos_control
- **Purpose**: Ensures positive control response is within expected range
- **Parameters**: 
  - `min_resp`: Minimum normalized response (%) (default: 15)
  - `max_resp`: Maximum normalized response (%) (default: 50)
- **Implementation**: 
  ```python
  def check_pos_control(self, results, min_resp, max_resp):
      """Check positive control normalized response is within range"""
      control_data = results['controls'].get('positive')
      if not control_data or control_data['status'] != 'ok':
          return {
              'passed': False,
              'message': "No positive control data available"
          }
      
      atp_data = control_data['types'].get('atp')
      if not atp_data or atp_data['status'] != 'ok' or atp_data['normalized'] is None:
          return {
              'passed': False,
              'message': "Positive control normalization data not available"
          }
      
      norm_resp = atp_data['normalized']['mean']
      passed = min_resp <= norm_resp <= max_resp
      
      return {
          'passed': passed,
          'message': message
      }
  ```
- **Failure Conditions**: Abnormal positive control indicates system-wide issues

#### check_ntc_baseline
- **Purpose**: Ensures no-cell control has low background
- **Parameters**: 
  - `max_value`: Maximum baseline value (default: 50)
- **Implementation**: Examines raw signal from NTC wells
- **Failure Conditions**: High NTC signal suggests contamination or non-specific signal

#### check_ntc_response
- **Purpose**: Confirms no-cell control shows no response
- **Parameters**: 
  - `max_response`: Maximum allowable response (default: 0.05)
- **Implementation**: Checks peak ΔF/F₀ in NTC wells
- **Failure Conditions**: NTC response indicates contamination or artifacts

#### check_ionomycin
- **Purpose**: Validates maximum calcium response reference
- **Parameters**: 
  - `min_peak`: Minimum peak ΔF/F₀ (default: 1.0)
  - `max_cv`: Maximum coefficient of variation (%) (default: 20)
- **Implementation**: Analyzes ionomycin response magnitude and consistency
- **Failure Conditions**: Poor ionomycin response compromises normalization

#### check_atp
- **Purpose**: Ensures ATP response is detectable and consistent
- **Parameters**: 
  - `min_peak`: Minimum peak ΔF/F₀ (default: 0.1)
  - `max_cv`: Maximum coefficient of variation (%) (default: 25)
- **Implementation**: Analyzes ATP response magnitude and consistency
- **Failure Conditions**: Weak or inconsistent ATP response affects diagnosis

#### check_buffer
- **Purpose**: Confirms buffer response is minimal
- **Parameters**: 
  - `max_response`: Maximum ΔF/F₀ (default: 0.1)
  - `max_pct_atp`: Maximum % of ATP response (default: 15)
- **Implementation**: 
  ```python
  def check_buffer(self, results, max_response, max_pct_atp):
      """Check buffer responses are minimal"""
      all_passed = True
      failed_groups = []
      
      # Check each sample's buffer wells against its ATP wells
      for sample_id, sample_data in results['samples'].items():
          if sample_data['status'] == 'ok':
              buffer_data = sample_data['types'].get('buffer')
              atp_data = sample_data['types'].get('atp')
              
              if buffer_data and buffer_data['status'] == 'ok' and atp_data and atp_data['status'] == 'ok':
                  buffer_peak = buffer_data['peak']['mean']
                  atp_peak = atp_data['peak']['mean']
                  
                  # Check absolute buffer response
                  if buffer_peak > max_response:
                      all_passed = False
                      failed_groups.append(f"{sample_id} (buffer peak: {buffer_peak:.3f})")
                  
                  # Check buffer as % of ATP
                  if atp_peak > 0:
                      buffer_pct = (buffer_peak / atp_peak) * 100
                      if buffer_pct > max_pct_atp:
                          all_passed = False
                          failed_groups.append(f"{sample_id} (buffer/ATP: {buffer_pct:.1f}%)")
      
      # Return result
      return {
          'passed': all_passed,
          'message': message
      }
  ```
- **Failure Conditions**: High buffer response suggests non-specific activation

#### check_replicates
- **Purpose**: Validates replicate consistency
- **Parameters**: 
  - `max_cv`: Maximum CV for triplicates (%) (default: 20)
- **Implementation**: Calculates coefficient of variation between replicates
- **Failure Conditions**: High variability between replicates reduces reliability

## Normalization Methods

The system offers two normalization approaches:

### Ionomycin Normalization
- **Purpose**: Normalize ATP responses to maximum calcium signal
- **Implementation**: 
  ```python
  # For each well
  peak = dff_data.loc[well_id].max()
  normalized = (peak / ionomycin_response) * 100
  ```
- **Benefits**: Accounts for cell count and dye loading differences
- **Reference**: Each sample's own ionomycin response is used as reference

### Positive Control Normalization
- **Purpose**: Normalize to a known reference sample
- **Implementation**: 
  ```python
  # First normalize to ionomycin
  iono_normalized = (peak / ionomycin_response) * 100
  
  # Then normalize to positive control
  pc_normalized = (iono_normalized / positive_control_value) * 100
  ```
- **Benefits**: Allows comparison across different plates or experiments
- **Reference**: The positive control's ionomycin-normalized response

## Diagnostic Thresholds

The diagnostic decision is based on configurable thresholds:

### Threshold Types
- **Ionomycin-Normalized ATP Response**: Percentage of maximum calcium signal
- **Positive Control-Normalized ATP Response**: Percentage of reference response

### Default Threshold
- 20% for autism risk assessment (values below indicate risk)

### Implementation
```python
def determine_diagnosis(self, results):
    """Determine diagnosis for each sample based on test results and chosen threshold type"""
    # Check if all tests passed
    all_tests_passed = all(test['passed'] for test in results['tests'].values())
    
    # If any test failed, we can't make a diagnosis
    if not all_tests_passed:
        for sample_id in results['samples'].keys():
            results['diagnosis'][sample_id] = {
                'status': 'INVALID',
                'message': "Cannot diagnose due to failed quality control tests"
            }
        return
    
    # Get threshold settings
    threshold_type = results['threshold_type']
    threshold_value = results['threshold_value']
    
    # For each sample, check the response based on chosen threshold type
    for sample_id, sample_data in results['samples'].items():
        # Get appropriate normalized value
        if "Positive Control-Normalized" in threshold_type:
            # Use double normalization
            norm_resp = atp_data['pc_normalized']['mean']
        else:
            # Use standard ionomycin normalization
            norm_resp = atp_data['normalized']['mean']
        
        # Make diagnosis based on threshold
        if norm_resp <= threshold_value:
            results['diagnosis'][sample_id] = {
                'status': 'POSITIVE',
                'message': f"Autism risk POSITIVE: Response ({norm_resp:.2f}%) is below threshold ({threshold_value}%)",
                'value': norm_resp
            }
        else:
            results['diagnosis'][sample_id] = {
                'status': 'NEGATIVE',
                'message': f"Autism risk NEGATIVE: Response ({norm_resp:.2f}%) is above threshold ({threshold_value}%)",
                'value': norm_resp
            }
```

## Diagnosis Decision Process

1. **Quality Control**: All tests must pass for a valid diagnosis
2. **Normalization**: ATP response is normalized using the selected method
3. **Threshold Application**: Normalized response is compared to threshold
4. **Status Assignment**: 
   - POSITIVE: Below threshold
   - NEGATIVE: Above threshold
   - INVALID: QC tests failed or data missing

## Visualization and Reporting

### Diagnosis Plot
- Bar chart showing normalized responses for each sample
- Color-coded by diagnosis status
- Threshold line displayed for reference
- Sample IDs on x-axis, response values on y-axis

### Diagnosis Summary
- Text summary of QC test results
- List of sample diagnoses with status and values
- Detailed explanation of any failed tests

### Excel Report
The diagnosis results are included in the Excel export in a dedicated "Diagnosis Results" sheet that contains:
- Diagnosis configuration including threshold settings
- Sample-specific diagnostic results
- QC test results with pass/fail indicators
- Control data analysis

## Parameter Customization

All diagnostic parameters can be customized in the Diagnosis Options tab:

### Control Configuration
- Column assignments for samples, NTC, and positive controls
- Well layout specification (ATP, ionomycin, buffer wells per column)

### Test Parameters
- Individual parameters for each QC test
- Threshold type and value for diagnosis

### Important: Applying Changes
After modifying parameters, users must click the "Apply Parameter Changes" button to store the new values. Changes are not automatically applied to ensure intentional modifications.

## Troubleshooting

### Common Issues

#### All Tests Using Default Values
- **Problem**: Parameter changes are not being applied
- **Solution**: Click "Apply Parameter Changes" button after modifications
- **Verification**: Use "Test Raw Baseline Min Parameter" to confirm update

#### Diagnosis Status "INVALID"
- **Problem**: QC tests failed or required data missing
- **Solution**: Check test results to identify failing tests
- **Diagnostic Steps**: Debug each failed test individually

#### NTC or Buffer Test Failures
- **Problem**: Control wells showing unexpected signals
- **Solution**: Check plate layout and well assignments
- **Verification**: Confirm NTC and buffer wells are correctly labeled

#### Inconsistent Normalization
- **Problem**: Ionomycin responses are variable
- **Solution**: Check ionomycin well assignments, ensure proper concentration
- **Analysis**: Look for signs of well cross-contamination

#### All Samples Show Similar Values
- **Problem**: Poor discriminatory power
- **Solution**: Adjust ATP concentration, check positive control
- **Verification**: Ensure ATP and ionomycin concentrations are optimal