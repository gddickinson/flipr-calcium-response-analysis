# FLIPR Analysis Tool: Comprehensive User Manual

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Getting Started](#getting-started)
4. [Interface Overview](#interface-overview)
5. [Data Management](#data-management)
6. [Plate Layout Configuration](#plate-layout-configuration)
7. [Experiment Metadata](#experiment-metadata)
8. [Data Analysis](#data-analysis)
9. [Visualization](#visualization)
10. [Diagnosis Mode](#diagnosis-mode)
11. [Exporting Results](#exporting-results)
12. [Tips and Shortcuts](#tips-and-shortcuts)
13. [Troubleshooting](#troubleshooting)
14. [Appendix](#appendix)

## Introduction

The FLIPR Analysis Tool is a specialized application designed for analyzing calcium imaging data from FLIPR (Fluorometric Imaging Plate Reader) experiments. This manual provides comprehensive instructions for using all features of the software.

### Purpose and Applications

The FLIPR Analysis Tool helps researchers:
- Process and visualize calcium flux data from 96-well plates
- Calculate normalized responses and key metrics
- Compare responses across different conditions
- Generate standardized reports and visualizations
- Perform diagnostic analyses for clinical applications

### System Requirements

- **Operating System**: Windows 10/11, macOS 10.14+, or Linux
- **Processor**: 2.0 GHz dual-core or better
- **Memory**: 4 GB RAM minimum, 8 GB recommended
- **Disk Space**: 200 MB for application, plus space for data files
- **Python**: Version 3.9 or later
- **Dependencies**: PyQt5, pandas, numpy, pyqtgraph, matplotlib, openpyxl

## Installation

### Standard Installation

1. **Install Python** (version 3.9 or higher)
   - Download from [python.org](https://www.python.org/downloads/)
   - Ensure "Add Python to PATH" is checked during installation

2. **Install Required Packages**
   - Open a terminal or command prompt
   - Run the following command:
   ```
   pip install PyQt5 pandas numpy pyqtgraph matplotlib openpyxl
   ```

3. **Download FLIPR Analysis Tool**
   - Download the latest version from [repository]
   - Extract the files to your preferred location

4. **Launch the Application**
   - Navigate to the installation directory
   - Run the main script:
   ```
   python flipr_analysis.py
   ```

### Troubleshooting Installation

If you encounter issues during installation:

- **Missing Dependencies**: Ensure all required packages are installed with:
  ```
  pip install -r requirements.txt
  ```

- **Version Conflicts**: Create a virtual environment to isolate dependencies:
  ```
  python -m venv flipr_env
  source flipr_env/bin/activate  # On Windows: flipr_env\Scripts\activate
  pip install -r requirements.txt
  ```

- **Permission Issues**: Run pip with administrator privileges or use the `--user` flag:
  ```
  pip install --user -r requirements.txt
  ```

## Getting Started

### Initial Configuration

When you first launch the FLIPR Analysis Tool, follow these steps to configure your workspace:

1. **Set Analysis Parameters**
   - Go to Analysis → Parameters
   - Configure default settings for:
     - Artifact start/end frames
     - Baseline frames
     - Peak detection parameters

2. **Configure Default Colors**
   - Default colors are used for automatic group assignment
   - Custom colors can be selected for each experiment

### Basic Workflow

A typical analysis workflow includes:

1. **Load Data**: Import FLIPR data file (.seq1 or .txt)
2. **Configure Plate Layout**: Define well groups and conditions
3. **Set Metadata**: Document experiment details
4. **Process Data**: Apply normalization and analysis
5. **Visualize Results**: View plots and summary statistics
6. **Export Results**: Generate detailed reports

## Interface Overview

The FLIPR Analysis Tool interface consists of:

### Main Window

- **Title Bar**: Displays current file name
- **Status Bar**: Shows processing status and messages
- **Tab Interface**: Contains primary function areas

### Menu Bar

- **File Menu**
  - Open Data File
  - Import/Export Layout
  - Load CSV Layout
  - Save/Load Templates
  - Exit

- **Analysis Menu**
  - Analysis Parameters
  - Plot Options
  - Data Processing Settings

- **Help Menu**
  - User Manual
  - About
  - Check for Updates

### Main Tabs

1. **Plate Layout Tab**: Configure well assignments
2. **Analysis Tab**: Process data and view results
3. **Experiment Metadata Tab**: Document experiment details
4. **Diagnosis Options Tab**: Configure diagnostic analysis

### Plot Windows

- **Raw Traces Window**: Display raw intensity values
- **ΔF/F₀ Traces Window**: Display normalized responses
- **Summary Plots Window**: Multiple visualization tabs

## Data Management

### Supported File Formats

The FLIPR Analysis Tool works with the following file formats:

- **FLIPR Data Files**
  - .seq1 files (FLIPR native format)
  - Tab-delimited text files (.txt)
  - Both formats must contain a header row and time-series data

- **Layout Files**
  - JSON layout files (.json) for well configurations
  - CSV files from FLIPR for direct layout import

- **Template Files**
  - Metadata templates (.json)
  - Diagnosis configuration templates (.json)

### Loading Data

1. **From Main Interface**
   - Click "Load Data" in the Plate Layout Tab
   - Or use File → Open Data File from menu

2. **File Selection Dialog**
   - Navigate to your data file location
   - Select .seq1 or .txt file
   - Click "Open"

3. **Data Validation**
   - The system will validate file format and structure
   - A confirmation message appears on successful loading
   - Error messages display if issues are detected

### Importing Layouts

#### From JSON Files

1. Click "Load Layout" or use File → Import Layout
2. Select previously saved layout file (.json)
3. Well configurations will be loaded automatically

#### From FLIPR CSV Files

1. Click "Load CSV Layout" or use File → Load CSV Layout
2. Select CSV file exported from FLIPR machine
3. The system will extract well IDs and group assignments
4. Well layout will update automatically

### Saving Layouts and Templates

1. **Saving Plate Layouts**
   - Click "Save Layout" or use File → Export Layout
   - Choose location and filename
   - Layout will be saved in JSON format

2. **Saving Metadata Templates**
   - In Experiment Metadata tab, click "Save Template"
   - Choose location and filename
   - Template will be saved in JSON format

3. **Saving Diagnosis Configurations**
   - In Diagnosis Options tab, click "Save Configuration"
   - Choose location and filename
   - Configuration will be saved in JSON format

## Plate Layout Configuration

### Understanding the Plate Grid

The 96-well plate grid is represented as:
- 8 rows (A-H) × 12 columns (1-12)
- Each well is identified by its coordinates (e.g., A1, B7, H12)
- Wells can be labeled with:
  - Agonist/compound name
  - Concentration
  - Sample ID
  - Custom color

### Selection Methods

The application offers multiple ways to select wells:

1. **Individual Selection**
   - Click on wells to select/deselect
   - Hold Shift and click to select multiple wells
   - Selected wells are highlighted in light blue

2. **Row/Column Selection**
   - Click row headers (A-H) to select entire rows
   - Click column headers (1-12) to select entire columns

3. **Range Selection**
   - Select a well, then hold Shift and select another well
   - All wells in the rectangular range will be selected

4. **Select All**
   - Click the top-left corner button to select all wells
   - Click again to deselect all

### Labeling Wells

After selecting wells, you can apply labels using one of three modes:

1. **Simple Label Mode**
   - Enter agonist name in "Agonist" field
   - Enter concentration in "Conc (µM)" field
   - Enter sample ID in "Sample ID" field
   - Select color by clicking the color button
   - Check which properties to apply
   - Click "Apply Label" to apply to selected wells

2. **Log10 Series Mode**
   - Select this mode from the dropdown
   - Enter starting concentration
   - Select wells in sequence (highest to lowest concentration)
   - Click "Apply Label"
   - System automatically calculates dilution series

3. **Clear Wells Mode**
   - Select this mode from the dropdown
   - Select wells to clear
   - Click "Apply Label"
   - All properties will be removed from selected wells

### Modifying Text Size

To adjust the text size in well buttons:
1. Use the "Button Text Size" spinner control
2. Select a value between 6 and 20 points
3. Well button text will update automatically

### Color Coding

Colors help visualize different conditions:
1. Click the color button to open the color picker
2. Select a color for the current selection
3. Click "Apply Label" to apply the color
4. Colors are preserved in plots and exports

## Experiment Metadata

The Experiment Metadata tab allows you to document details about your experiment for comprehensive record-keeping.

### Available Metadata Fields

The metadata panel includes fields for:

- **Experiment Identification**
  - Accession ID
  - Aliquot
  - Plate per run date

- **Sample Details**
  - Passage #
  - Cell Density
  - Phenotype

- **Experimental Conditions**
  - Objective
  - Experiment Date
  - Media Type
  - FBS Lot No
  - Time Frame
  - Variable A
  - Lab Operator

- **Results Context**
  - Schmunk Ca2+ Signal
  - Result of interest
  - Expected/Optimal Results

### Managing Metadata Templates

For consistent documentation across experiments:

1. **Saving Templates**
   - Enter commonly used metadata
   - Click "Save Template"
   - Choose location and filename
   - Template will be saved as JSON

2. **Loading Templates**
   - Click "Load Template"
   - Select previously saved template file
   - All fields will be populated automatically

3. **Clearing Fields**
   - Click "Clear All" to reset all fields

### Metadata Integration

Metadata is integrated with analysis results:
- Included in the Experiment Summary worksheet in Excel exports
- Combined with sample-specific results
- Provides complete experimental context for analysis

## Data Analysis

### Setting Analysis Parameters

Access analysis parameters via Analysis → Parameters to configure:

1. **Artifact Removal Settings**
   - **Artifact Start Frame**: Beginning of injection artifact
   - **Artifact End Frame**: End of injection artifact
   - These frames will be removed during processing

2. **Baseline Calculation**
   - **Baseline Frames**: Number of frames used to calculate F₀
   - These frames define the denominator in ΔF/F₀ calculation

3. **Peak Detection**
   - **Peak Start Frame**: Frame to begin peak detection
   - Ensures peaks are found after any artifact

### Processing Data

In the Analysis tab, several processing options are available:

1. **Artifact Removal**
   - Toggle "Remove Injection Artifact" checkbox
   - When enabled, specified frames are removed from analysis

2. **Ionomycin Normalization**
   - Toggle "Normalize to Ionomycin" checkbox
   - When enabled, responses are normalized to ionomycin
   - Groups by Sample ID to match samples with their ionomycin controls

3. **Diagnosis Generation**
   - Toggle "Generate Diagnosis" checkbox
   - When enabled, diagnostic analysis is performed
   - Requires Ionomycin normalization

### Viewing Results

Results are displayed in several ways:

1. **Results Text Area**
   - Shows summary statistics for each group
   - Displays peak responses, time to peak, and AUC
   - Shows normalized responses when enabled
   - Includes diagnosis results when enabled

2. **Plot Buttons**
   - "Raw Traces": Opens window with raw intensity plots
   - "ΔF/F₀ Traces": Opens window with normalized plots
   - "Summary Plots": Opens window with multiple plot types

## Visualization

### Opening Plot Windows

Three types of plot windows are available:

1. **Raw Traces**
   - Click "Raw Traces" button in Analysis tab
   - Shows raw intensity values over time
   - Useful for checking baseline stability and signal quality

2. **ΔF/F₀ Traces**
   - Click "ΔF/F₀ Traces" button in Analysis tab
   - Shows normalized responses over time
   - Allows comparison of response magnitudes across conditions

3. **Summary Plots**
   - Click "Summary Plots" button in Analysis tab
   - Contains multiple tabs with different visualization types

### Summary Plot Types

The Summary Plots window includes multiple tabs:

1. **Individual Traces**
   - Shows all individual ΔF/F₀ traces by group
   - Each group is color-coded
   - Individual replicates shown with low opacity
   - Group average shown with higher opacity

2. **Mean Traces**
   - Shows average response for each group
   - Includes SEM error bands
   - Legend identifies each group

3. **Peak Responses**
   - Bar chart showing maximum response for each group
   - Includes error bars for SEM
   - Labels show numerical values

4. **Area Under Curve**
   - Bar chart showing AUC values for each group
   - Includes error bars for SEM
   - Represents integrated calcium response

5. **Time to Peak**
   - Bar chart showing time to maximum response
   - Includes error bars for SEM
   - Useful for comparing response kinetics

6. **Normalized to Ionomycin**
   - Bar chart showing responses as percentage of ionomycin
   - Only available when normalization is enabled
   - Adjusts for differences in loading and expression

7. **Diagnosis**
   - Bar chart showing normalized ATP responses
   - Includes threshold line for autism risk
   - Color-coded by diagnostic outcome
   - Only available when diagnosis is enabled

8. **Plot Settings**
   - Controls for customizing plot appearance
   - Adjust axis labels, scales, and formatting

### Plot Controls

Each plot window includes controls for customization:

1. **Plot Manipulation**
   - Pan: Click and drag
   - Zoom: Scroll wheel or selection box
   - Reset view: Right-click and select "Reset View"

2. **Display Options**
   - Toggle grid: "Show Grid" checkbox
   - Clear plot: "Clear Plot" button
   - Legend visibility: Toggle in context menu

3. **Export Options**
   - Save as image: Use toolbar in summary plots
   - Copy to clipboard: Right-click menu
   - Print: Printer icon in toolbar

## Diagnosis Mode

### Overview

The diagnosis mode provides clinical assessment capabilities based on calcium response patterns. For detailed instructions, refer to the separate [Diagnostic Mode User Guide](#).

### Basic Setup

1. **Configure Control Columns**
   - Navigate to Diagnosis Options tab
   - Specify columns for positive controls, negative controls, buffer controls, and test samples
   - Check for any overlapping column assignments

2. **Set Quality Control Parameters**
   - Configure thresholds for each quality control test
   - Adjust based on your established protocol
   - Save configuration as template for consistency

3. **Run Diagnosis**
   - In Analysis tab, check "Generate Diagnosis"
   - Process data (automatically runs diagnostic tests)
   - Review results in text area and Diagnosis plot tab

### Interpreting Results

Diagnosis results include:
- POSITIVE/NEGATIVE/INVALID status for each sample
- Normalized ATP response values
- Quality control test outcomes
- Color-coded visualization in Diagnosis plot

## Exporting Results

### Excel Export

To export comprehensive results:

1. Click "Export Results" in the Analysis tab
2. Choose location and filename in the dialog
3. The system generates an Excel workbook with multiple sheets

### Excel Workbook Contents

The exported Excel file includes these worksheets:

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

To export plate layout back to FLIPR:

1. Go to File → Export FLIPR Layout
2. Choose location and filename with .fmg extension
3. The layout will be saved in FLIPR-compatible format

## Tips and Shortcuts

### Efficiency Techniques

1. **Plate Layout Shortcuts**
   - Shift+click for range selection
   - Double-click row/column headers to select all wells in that row/column
   - Use Log10 Series for quick dilution series

2. **Template Usage**
   - Create template files for common plate layouts
   - Save metadata templates for similar experiments
   - Save diagnosis configurations for standardized testing

3. **Data Navigation**
   - Use plot navigation tools for detailed inspection
   - Right-click on plots for context menu options
   - Use mouse wheel to zoom in/out

### Time-Saving Features

1. **CSV Layout Import**
   - Use CSV import to quickly reconstruct plate layouts
   - Saves time compared to manual well labeling

2. **Column-based Selection**
   - Define controls and conditions by column for easier group definition
   - Use column-selection option in diagnosis setup

3. **Batch Processing**
   - Use consistent file naming for easier data management
   - Save layouts for reuse across multiple plates

## Troubleshooting

### Common Issues

1. **Data Loading Problems**
   - **Issue**: File won't load or throws error
   - **Solution**: Check file format, encoding, and structure
   - **Prevention**: Use standard FLIPR export settings

2. **Empty or Incorrect Plots**
   - **Issue**: Plots show no data or unexpected patterns
   - **Solution**: Verify well selection and data processing options
   - **Prevention**: Check raw data before normalization

3. **Inconsistent Normalization**
   - **Issue**: Normalized values vary unexpectedly
   - **Solution**: Check baseline stability and ionomycin responses
   - **Prevention**: Use consistent baseline frames

4. **Export Failures**
   - **Issue**: Excel export fails
   - **Solution**: Close any open Excel files, check permissions
   - **Prevention**: Save regularly during analysis

### Error Messages

Common error messages and their resolutions:

| Error Message | Likely Cause | Resolution |
|---------------|--------------|------------|
| "Invalid file format" | File type not supported | Ensure file is .seq1 or .txt format |
| "No data found in file" | Empty or corrupted file | Check file contents and re-export from FLIPR |
| "Well not found in data" | Well reference mismatch | Ensure well IDs match between layout and data |
| "Memory error" | File too large | Reduce file size or increase available memory |
| "Permission denied" | File access issue | Check file permissions and close other programs |

### Getting Support

If you encounter persistent issues:
1. Check log files in the application directory
2. Consult the FAQ section on the website
3. Contact support at [george.dickinson@gmail.com]
4. Provide detailed information about your issue and system

## Appendix

### Glossary

- **Artifact**: Signal disturbance caused by compound injection
- **AUC**: Area Under Curve, integrated calcium response
- **Baseline**: Initial signal before compound addition
- **CV**: Coefficient of Variation, measure of replicate consistency
- **ΔF/F₀**: Normalized calcium response (change in fluorescence/baseline)
- **FWHM**: Full Width at Half Maximum, measure of peak width
- **Ionomycin**: Calcium ionophore used for maximum response calibration
- **SEM**: Standard Error of the Mean, statistical measure of variability
- **Time to Peak**: Time from compound addition to maximum response

### Mathematical Formulas

- **ΔF/F₀ Calculation**:
  ```
  ΔF/F₀ = (F - F₀) / F₀
  ```
  Where F₀ is the average of baseline frames

- **Area Under Curve**:
  ```
  AUC = ∫ᵃᵇ ΔF/F₀(t) dt
  ```
  Calculated using trapezoidal integration

- **Coefficient of Variation**:
  ```
  CV = (Standard Deviation / Mean) × 100%
  ```
  Used to assess replicate consistency

### Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Open File | Ctrl+O |
| Save Layout | Ctrl+S |
| Export Results | Ctrl+E |
| Exit | Alt+F4 |
| Select All Wells | Ctrl+A |
| Clear Selection | Esc |
| Toggle Grid | Ctrl+G |
| Show Raw Traces | Ctrl+1 |
| Show ΔF/F₀ Traces | Ctrl+2 |
| Show Summary Plots | Ctrl+3 |
| Reset View | Ctrl+R |
