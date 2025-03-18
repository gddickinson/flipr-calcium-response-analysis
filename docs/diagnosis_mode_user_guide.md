# FLIPR Analysis Tool: Diagnostic Mode User Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Diagnostic Principle](#diagnostic-principle)
3. [Setting Up the Plate Layout](#setting-up-the-plate-layout)
4. [Configuring Diagnostic Options](#configuring-diagnostic-options)
5. [Quality Control Tests](#quality-control-tests)
6. [Running a Diagnosis](#running-a-diagnosis)
7. [Interpreting Results](#interpreting-results)
8. [Export and Documentation](#export-and-documentation)
9. [Troubleshooting](#troubleshooting)
10. [Best Practices](#best-practices)

## Introduction

The FLIPR Analysis Tool includes a diagnostic module specifically designed for clinical applications, particularly for assessing autism risk based on calcium response patterns. This guide provides detailed instructions for using the diagnostic features and interpreting the results.

The diagnostic functionality evaluates calcium signaling responses to ATP stimulation, normalized against ionomycin response. Research has shown that certain patterns of ATP-induced calcium signals may be associated with autism spectrum disorders. This tool provides a standardized framework for performing these assessments with appropriate quality controls.

## Diagnostic Principle

### Scientific Basis

The diagnostic principle is based on research showing that cells from individuals with autism often display altered purinergic receptor signaling, particularly in response to ATP. When properly normalized to a maximum calcium response (induced by ionomycin), these differences can be quantified.

### Diagnostic Threshold

The diagnosis is based on a configurable threshold for the normalized ATP response:
- **Normalized ATP Response** = (ATP Peak Response / Ionomycin Peak Response) × 100%
- If this value falls below the **Autism Risk Threshold** (default: 20%), a positive result for autism risk is indicated
- If this value is above the threshold, a negative result is indicated

### Quality Control Framework

Before a diagnosis can be made, the data must pass multiple quality control tests to ensure:
1. Technical validity of the calcium measurements
2. Proper baseline stability
3. Expected responses to control compounds
4. Acceptable replicate consistency

Only if all quality control criteria are met will the system provide a diagnostic result.

## Setting Up the Plate Layout

### Required Controls

A diagnostic plate layout requires specific controls placed in designated columns:

1. **Positive Controls**: Samples known to give a response below the threshold
2. **Negative Controls**: Samples known to give a response above the threshold
3. **Buffer Controls** (optional): HBSS buffer alone to establish baseline response
4. **Test Samples**: Patient samples being diagnosed

### Sample Identification

Each sample must have a unique Sample ID assigned in the plate layout:

1. Select wells containing a specific sample
2. Enter the Sample ID in the "Sample ID" field
3. Apply the label to selected wells
4. Repeat for each sample and control

### Example Plate Layout

A typical layout might include:
- Columns 1-2: Positive controls (e.g., cells from confirmed autism cases)
- Columns 3-4: Negative controls (e.g., cells from neurotypical individuals)
- Columns 5-6: Buffer controls (HBSS alone)
- Columns 7-12: Test samples (patient cells)

![Plate Layout Example](plate_layout_example.png)

## Configuring Diagnostic Options

### Accessing Diagnostic Options

1. Open the FLIPR Analysis Tool
2. Navigate to the **Diagnosis Options** tab

### Control Column Configuration

1. Define which columns contain each type of control:
   - **Positive Control**: Specify columns (e.g., 1 to 2)
   - **Negative Control**: Specify columns (e.g., 3 to 4)
   - **Buffer Control**: Specify columns (e.g., 5 to 6) or uncheck "Include buffer control" if not used
   - **Test Samples**: Specify columns (e.g., 7 to 12)

2. The system will automatically check for overlapping column definitions and warn you if found

### Setting the Diagnostic Threshold

1. Set the **Autism Risk Threshold** (default: 20%)
   - This is the value below which a positive autism risk result is indicated
   - This threshold should be established based on validated clinical data

### Configuring Quality Control Tests

Each quality control test has configurable parameters:

1. **Injection Artifact Tests**:
   - **Max signal change during injection**: Maximum allowable signal deviation during compound addition
   - **Time to return to baseline**: Number of frames after injection to return to baseline

2. **Raw Data Tests**:
   - **Minimum baseline value**: Lowest acceptable raw intensity
   - **Maximum baseline value**: Highest acceptable raw intensity
   - **Minimum/Maximum baseline mean**: Range for acceptable baseline average
   - **Maximum baseline SD**: Maximum allowable standard deviation in baseline

3. **ΔF/F₀ Tests**:
   - **Maximum baseline deviation**: How close to zero the normalized baseline should be
   - **Maximum end deviation**: Maximum deviation from zero at end of measurement
   - **Minimum/Maximum peak height**: Range for acceptable peak responses
   - **Minimum/Maximum peak width**: Range for acceptable FWHM values
   - **Minimum/Maximum AUC**: Range for acceptable area under curve

4. **Control Tests**:
   - **Minimum/Maximum positive control response**: Range for positive control normalized response
   - **Minimum/Maximum negative control response**: Range for negative control normalized response
   - **Minimum ionomycin response**: Minimum acceptable ionomycin peak
   - **Maximum CV for responses**: Maximum acceptable coefficient of variation

### Saving and Loading Configurations

To ensure consistent testing across experiments:

1. Configure all parameters for your diagnostic protocol
2. Click "Save Configuration" and provide a filename
3. To reuse this configuration, click "Load Configuration"
4. For standard settings, click "Reset to Defaults"

## Quality Control Tests

### Injection Artifact Control

This test evaluates whether the mechanical disturbance from compound addition is within acceptable limits:

- **Purpose**: Ensure injection artifacts don't interfere with calcium measurements
- **Method**: Measures signal change during compound addition and recovery time
- **Pass Criteria**: Signal changes are within specified limits and recover quickly
- **Failure Impact**: Can indicate pipetting issues or cell monolayer disruption

### Raw Data Quality Control

These tests evaluate the quality of the raw signal:

- **Purpose**: Ensure cells are viable and detector is functioning properly
- **Method**: Checks baseline intensity ranges and stability
- **Pass Criteria**: Signal within defined min/max range with acceptable stability
- **Failure Impact**: Can indicate cell health issues, dye loading problems, or instrument malfunction

### ΔF/F₀ Quality Control

These tests evaluate the normalized signal quality:

- **Purpose**: Ensure proper baseline normalization and signal characteristics
- **Method**: Checks baseline accuracy, peak parameters, and signal return
- **Pass Criteria**: Baseline near zero, peak and response profiles within ranges
- **Failure Impact**: Can indicate normalization issues or abnormal cellular responses

### Control Sample Validation

These tests validate that control samples respond as expected:

- **Purpose**: Ensure the assay is properly discriminating between positive and negative cases
- **Method**: Checks responses from positive and negative controls
- **Pass Criteria**: Controls give responses in expected ranges with acceptable variability
- **Failure Impact**: Can indicate assay drift, reagent issues, or cell preparation problems

### Replicate Consistency

These tests ensure that replicate measurements are sufficiently consistent:

- **Purpose**: Ensure technical reproducibility of measurements
- **Method**: Calculates coefficient of variation (CV) for replicate wells
- **Pass Criteria**: CV below specified threshold
- **Failure Impact**: Can indicate pipetting inconsistency or heterogeneous cell populations

## Running a Diagnosis

### Step-by-Step Procedure

1. **Prepare Plate Layout**:
   - Load FLIPR data file
   - Configure well labels with proper Sample IDs
   - Alternatively, import layout directly from FLIPR CSV

2. **Configure Diagnosis Options**:
   - Navigate to Diagnosis Options tab
   - Set control columns and test parameters
   - Set autism risk threshold

3. **Run Analysis**:
   - Navigate to Analysis tab
   - Check "Remove Injection Artifact" if needed
   - Check "Normalize to Ionomycin" (required)
   - Check "Generate Diagnosis"
   - Data processing and diagnosis will run automatically

4. **View Results**:
   - Diagnosis results will appear in the Results text area
   - The Summary Plots window will display a Diagnosis tab with visual results

### Data Requirements

For accurate diagnosis, ensure:

1. Data includes both ATP and ionomycin responses for each sample
2. Samples are properly labeled with unique Sample IDs
3. Control wells are included in designated columns
4. All samples have replicates (preferably triplicates)

## Interpreting Results

### Diagnostic Outcomes

The system provides three possible diagnostic outcomes:

1. **POSITIVE**:
   - The normalized ATP response is below the autism risk threshold
   - Indicates elevated autism risk based on calcium signaling pattern
   - Reported with actual normalized value for reference

2. **NEGATIVE**:
   - The normalized ATP response is above the autism risk threshold
   - Indicates typical calcium signaling pattern
   - Reported with actual normalized value for reference

3. **INVALID**:
   - One or more quality control tests failed
   - No diagnostic conclusion can be drawn
   - Specific failed tests are listed to guide troubleshooting

### Visualization

The Diagnosis tab in the Summary Plots window provides visual interpretation:

- Bar chart showing normalized ATP response for each sample
- Red threshold line indicating the autism risk threshold
- Color-coded bars (red for positive, green for negative)
- Text summary of all test results

### Quality Control Review

Always review all quality control test results:

1. Check how many tests passed vs. failed
2. Review specific failures and their implications
3. Consider re-running the analysis if critical tests failed
4. Document all QC results along with final diagnosis

## Export and Documentation

### Generating Reports

To document diagnostic results:

1. Click "Export Results" in the Analysis tab
2. Save the Excel workbook to your desired location

### Report Contents

The exported Excel file includes:

1. **Summary** sheet with all group statistics
2. **Experiment Summary** sheet with metadata and results by Sample ID
3. **Individual_Traces** sheet with raw trace data
4. **Mean_Traces** sheet with averaged responses
5. **Peak_Responses** sheet with maximum responses
6. **Analysis_Metrics** sheet with detailed statistics
7. **Diagnosis Results** sheet with:
   - Diagnostic configuration details
   - Sample-specific diagnostic results
   - Quality control test results with pass/fail indicators
   - Color-coded results for easy interpretation

### Documentation Requirements

For clinical applications, always document:

1. Sample information and metadata
2. Complete diagnostic configuration
3. All quality control test results
4. Final diagnostic outcome with normalized values
5. Names of operators and date of analysis

## Troubleshooting

### QC Test Failures

| Test Type | Common Causes | Solutions |
|-----------|---------------|-----------|
| Injection Artifact | Pipetting issues, Cell disturbance | Adjust pipetting speed, Check cell attachment |
| Raw Baseline | Cell health issues, Dye loading problems | Check cell viability, Optimize dye loading |
| Raw Max/Min | Detector issues, Focus problems | Verify instrument settings, Check focus |
| ΔF/F₀ Baseline | Poor normalization, Signal drift | Extend baseline collection, Check for photobleaching |
| Peak Height | Receptor desensitization, Compound degradation | Fresh compounds, Check receptor expression |
| Control Response | Reagent issues, Cell line drift | Validate reagents, Check passage number |
| Replicate CV | Pipetting inconsistency, Cell heterogeneity | Improve pipetting technique, Ensure uniform seeding |

### Common Diagnostic Issues

1. **High Variability in Results**:
   - Ensure consistent cell density across wells
   - Check for edge effects on the plate
   - Verify uniform temperature across the plate

2. **Consistently Failed Controls**:
   - Verify control sample identity
   - Check compound concentrations
   - Validate cell health and receptor expression

3. **All Samples Show Similar Responses**:
   - Check compound addition sequence
   - Verify correct columns were used for analysis
   - Check for cross-contamination

4. **Inconsistent Ionomycin Responses**:
   - Verify ionomycin concentration
   - Check for calcium depletion in media
   - Ensure ionomycin was added at correct time point

## Best Practices

### Experimental Design

1. **Replicate Structure**:
   - Use at least triplicates for all samples and controls
   - Consider multiple plates for critical samples
   - Include technical and biological replicates when possible

2. **Control Selection**:
   - Use well-characterized positive and negative controls
   - Include historical controls for assay validation
   - Consider including borderline cases as reference points

3. **Plate Layout**:
   - Avoid edge wells if possible (use for buffer)
   - Randomize sample positions when feasible
   - Maintain consistent layout for repeated assays

### Data Analysis

1. **Baseline Optimization**:
   - Collect sufficient baseline before compound addition
   - Verify stable baseline across all wells
   - Consider adaptive baseline methods for problematic samples

2. **Signal Processing**:
   - Choose appropriate artifact removal parameters
   - Verify normalization effectiveness visually
   - Consider applying smoothing for noisy data

3. **Threshold Calibration**:
   - Periodically validate the autism risk threshold
   - Consider age and sex-specific thresholds if data supports this
   - Document the validation basis for your threshold

### Clinical Integration

1. **Result Interpretation**:
   - Consider results in context of other clinical indicators
   - Note degree of deviation from threshold
   - Document all quality metrics alongside the diagnosis

2. **Longitudinal Tracking**:
   - Track results over multiple timepoints when possible
   - Note any treatments or interventions between measurements
   - Document passage number and culture conditions

3. **Validation Protocol**:
   - Implement regular validation with known samples
   - Track assay drift over time
   - Maintain a database of historical control responses
