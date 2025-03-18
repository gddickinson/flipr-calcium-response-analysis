# FLIPR Analysis Tool User Manual

## Table of Contents
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Getting Started](#getting-started)
4. [Main Interface](#main-interface)
5. [Loading Data](#loading-data)
6. [Plate Layout Configuration](#plate-layout-configuration)
7. [Experiment Metadata](#experiment-metadata)
8. [Data Analysis](#data-analysis)
9. [Diagnostic Analysis](#diagnostic-analysis)
10. [Visualization](#visualization)
11. [Exporting Results](#exporting-results)
12. [Troubleshooting](#troubleshooting)

## Introduction

The FLIPR Analysis Tool is a specialized software application designed for analyzing calcium imaging data from FLIPR (Fluorometric Imaging Plate Reader) experiments. It provides a comprehensive suite of tools for data processing, visualization, analysis, and diagnostic evaluation of calcium responses in 96-well plate formats.

### Key Features
- Interactive 96-well plate layout configuration
- Raw and ΔF/F₀ trace visualization
- Automated artifact removal
- Statistical analysis with multiple metrics
- Ionomycin normalization capability
- Comprehensive data export options
- Area Under Curve (AUC) analysis
- Time to peak measurements
- Direct import from FLIPR CSV output
- Experiment metadata tracking
- Diagnostic analysis for clinical applications

## Installation

### System Requirements
- Python 3.9 or later
- Required libraries:
  - PyQt5
  - pandas
  - numpy
  - pyqtgraph
  - openpyxl
  - matplotlib

### Installation Steps
1. Install Python from https://www.python.org/downloads/
2. Install required packages using pip:
```bash
pip install PyQt5 pandas numpy pyqtgraph openpyxl matplotlib
```
3. Download and run the FLIPR Analysis Tool script

## Getting Started

### Initial Setup
1. Launch the application
2. Configure analysis parameters (Analysis → Parameters)
3. Load your FLIPR data file
4. Configure your plate layout before analysis

### File Formats
The tool accepts FLIPR output files in the following formats:
- .seq1 files (FLIPR native format)
- Tab-delimited text files (.txt)
- CSV files for layout import (direct from FLIPR machine)
- File must contain a header row and time-series data

## Main Interface

### Window Layout
The interface consists of four main tabs:
1. **Plate Layout Tab**
   - 96-well plate grid
   - Well labeling controls
   - Mode selection
   - Action buttons

2. **Analysis Tab**
   - Plot controls
   - Analysis parameters
   - Results display
   - Export options

3. **Experiment Metadata Tab**
   - Experiment details
   - Sample information
   - Protocol parameters
   - Experimental conditions

4. **Diagnosis Options Tab**
   - Control column selection
   - Quality control test parameters
   - Diagnostic thresholds
   - Buffer control options

### Menu Bar
- **File**: Layout export options, CSV layout import
- **Analysis**: Parameter settings
- **Help**: Manual and about information

## Loading Data

### Loading a Data File
1. Click "Load Data" or use File → Open
2. Select your .seq1 or .txt file
3. The file will be validated and loaded
4. A confirmation message will appear upon successful loading

### Loading Layout from FLIPR CSV
1. Click "Load CSV Layout" or use File → Load CSV Layout
2. Select the CSV file exported from your FLIPR machine
3. The application will extract well IDs and group names
4. Well layout will be updated with the imported information

### Data Validation
The tool automatically checks for:
- Correct file format
- Complete header information
- Valid numerical data
- Appropriate number of columns

## Plate Layout Configuration

### Well Selection
- Click individual wells to select/deselect
- Click row headers (A-H) to select entire rows
- Click column headers (1-12) to select entire columns
- Click top-left corner to select all wells
- Shift-select for range selection

### Labeling Modes
1. **Simple Label**
   - Enter agonist name
   - Enter concentration
   - Enter sample ID
   - Choose color
   - Apply to selected wells

2. **Log10 Series**
   - Enter starting concentration
   - Select multiple wells in order
   - System calculates dilution series

3. **Clear Wells**
   - Removes all labels from selected wells

### Color Coding
- Click color button to open color picker
- Colors help visualize different conditions
- Colors are preserved in plots and exports

## Experiment Metadata

### Metadata Fields
- Accession ID
- Aliquot
- Plate per run date
- Passage #
- Objective
- Experiment Date
- Media Type
- FBS Lot No
- Cell Density
- Time Frame
- Variable A
- Lab Operator
- Schmunk Ca2+ Signal
- Phenotype
- Result of interest
- Expected/Optimal Results

### Template Management
- Save commonly used metadata as templates
- Load templates for consistent experiment documentation
- Reset to defaults when needed

### Data Integration
- Metadata is combined with analysis results
- Sample IDs from plate layout are used to organize results
- Complete experimental context is preserved in exports

## Data Analysis

### Analysis Parameters
Access via Analysis → Parameters to set:
- Artifact Start Frame: Beginning of injection artifact
- Artifact End Frame: End of injection artifact
- Baseline Frames: Number of frames for F₀ calculation
- Peak Start Frame: Frame to begin peak detection

### Processing Options
1. **Artifact Removal**
   - Toggle "Remove Injection Artifact"
   - Automatically removes specified frames
   - Updates all calculations and plots

2. **Ionomycin Normalization**
   - Toggle "Normalize to Ionomycin"
   - Normalizes responses to ionomycin control
   - Groups by sample ID

3. **Area Under Curve**
   - Automatically calculated for all traces
   - Displayed in summary plots and exports
   - Uses trapezoidal integration

4. **Time to Peak**
   - Calculated from start of response
   - Accounts for artifact removal if enabled
   - Shown in summary plots and exports

## Diagnostic Analysis

### Diagnosis Setup
1. Configure control columns in the Diagnosis Options tab:
   - Positive Control: Define columns containing positive controls
   - Negative Control: Define columns containing negative controls
   - Buffer Control: Define columns containing buffer (optional)
   - Test Samples: Define columns containing test samples

2. Configure quality control tests:
   - Injection Artifact Tests
   - Raw Data Tests
   - ΔF/F₀ Tests
   - Control Tests
   
3. Set diagnostic threshold:
   - Autism Risk Threshold: Define the normalized ATP response threshold

### Running Diagnosis
1. Enable "Generate Diagnosis" in the Analysis tab
2. Process data (diagnosis runs automatically)
3. View results in the Analysis tab and Diagnosis plot

### Quality Control
- Tests validate data quality before diagnosis
- Failed tests invalidate diagnosis
- Test results are documented in exports
- Buffer control can be optional based on experiment design

### Diagnostic Output
- Sample-specific diagnosis with normalized values
- Color-coded status (POSITIVE/NEGATIVE/INVALID)
- Comprehensive test result documentation
- Visualization in dedicated Diagnosis tab

## Visualization

### Available Plot Types
1. **Raw Traces**
   - Shows raw intensity values
   - Individual well traces
   - Color-coded by group

2. **ΔF/F₀ Traces**
   - Normalized calcium responses
   - Baseline-corrected
   - Color-coded by group

3. **Summary Plots**
   - Individual Traces: All responses by group
   - Mean Traces: Average with SEM
   - Peak Responses: Bar graphs with error bars
   - Area Under Curve: AUC comparison
   - Time to Peak: Response timing
   - Normalized (when enabled): % of ionomycin
   - Diagnosis (when enabled): Diagnostic results with threshold

### Plot Controls
- Toggle grid display
- Clear individual plots
- Show/hide legend
- Export plots as images

## Exporting Results

### Excel Export
Creates a workbook with multiple sheets:
1. **Summary**
   - Group statistics
   - Peak responses
   - AUC values
   - Time to peak
   - Normalized responses (if enabled)

2. **Experiment Summary**
   - Comprehensive metadata with analysis results
   - Sample-specific results organized by Sample ID
   - Combines experimental context with quantitative results

3. **Individual_Traces**
   - Complete trace data
   - Well assignments
   - Concentrations

4. **Mean_Traces**
   - Averaged responses
   - SEM calculations
   - Time points

5. **Peak_Responses**
   - Maximum responses
   - Time to peak
   - AUC values

6. **Analysis_Metrics**
   - Detailed statistics
   - Group comparisons
   - Quality metrics

7. **Diagnosis Results** (when diagnosis is enabled)
   - Diagnosis configuration
   - Sample-specific diagnostic results
   - Quality control test results
   - Color-coded pass/fail indicators

### FLIPR Format Export
- Exports plate layout as .fmg file
- Compatible with FLIPR software
- Preserves groups and colors

## Troubleshooting

### Common Issues

1. **Data Loading Problems**
   - Check file format
   - Verify data structure
   - Ensure no missing values

2. **CSV Layout Import Issues**
   - Verify CSV structure matches expected format
   - Check for Well ID and Group columns
   - Make sure encoding is correct (CP-1252)

3. **Plot Display Issues**
   - Verify well selection
   - Check data processing
   - Confirm parameter settings

4. **Diagnosis Issues**
   - Ensure control columns are correctly defined
   - Check for overlapping column definitions
   - Verify ionomycin wells are properly labeled
   - Make sure quality control thresholds are appropriate

5. **Export Errors**
   - Check file permissions
   - Close existing Excel files
   - Verify available disk space

### Error Messages
- Detailed error messages in status bar
- Log file for debugging
- Contact support for assistance

### Support
For additional support or to report issues:
[george.dickinson@gmail.com]

## Tips and Best Practices

1. **Data Organization**
   - Label wells before analysis
   - Use consistent naming
   - Save layouts for repeated experiments
   - Import layouts directly from FLIPR CSV when available

2. **Analysis Workflow**
   - Set parameters first
   - Verify well assignments
   - Review raw data before processing
   - Document experiment metadata

3. **Diagnostic Setup**
   - Validate control columns carefully
   - Check for overlapping column definitions
   - Fine-tune quality control thresholds
   - Save diagnostic configurations as templates

4. **Quality Control**
   - Check baseline stability
   - Verify artifact removal
   - Compare replicates
   - Review all diagnosis test results

5. **Data Export**
   - Save layouts separately
   - Document parameter settings
   - Include all relevant metadata
   - Use clear Sample IDs for consistency
