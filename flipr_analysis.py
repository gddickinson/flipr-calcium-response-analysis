import sys
import csv
import logging
import pandas as pd
import numpy as np
from typing import Tuple, Dict
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QGridLayout, QWidget, QPushButton,
    QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QColorDialog, QComboBox,
    QMessageBox, QFileDialog, QCheckBox, QTabWidget,
    QMenuBar, QMenu, QAction, QDialog, QSpinBox, QFormLayout, QDialogButtonBox
)
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
import pyqtgraph as pg
import json

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ParametersDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Analysis Parameters")
        self.setModal(True)

        # Create layout
        layout = QFormLayout()

        # Create spinboxes for parameters
        self.artifact_start = QSpinBox()
        self.artifact_start.setRange(0, 1000)
        self.artifact_start.setValue(18)
        self.artifact_start.setToolTip("Start frame of injection artifact")

        self.artifact_end = QSpinBox()
        self.artifact_end.setRange(0, 1000)
        self.artifact_end.setValue(30)
        self.artifact_end.setToolTip("End frame of injection artifact")

        self.baseline_frames = QSpinBox()
        self.baseline_frames.setRange(1, 100)
        self.baseline_frames.setValue(15)
        self.baseline_frames.setToolTip("Number of frames for baseline calculation")

        self.peak_start_frame = QSpinBox()
        self.peak_start_frame.setRange(0, 1000)
        self.peak_start_frame.setValue(20)
        self.peak_start_frame.setToolTip("Start frame for peak detection")

        # Add widgets to layout
        layout.addRow("Artifact Start Frame:", self.artifact_start)
        layout.addRow("Artifact End Frame:", self.artifact_end)
        layout.addRow("Baseline Frames:", self.baseline_frames)
        layout.addRow("Peak Start Frame:", self.peak_start_frame)

        # Add buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addRow(buttons)
        self.setLayout(layout)


class BasePlotWindow(QMainWindow):
    """Base class for all plot windows"""
    def __init__(self, title="Plot Window", parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.resize(800, 600)
        self.was_visible = False

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout(central_widget)

        # Create plot widget with white background
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('w')
        self.plot_widget.setLabel('left', "Signal")
        self.plot_widget.setLabel('bottom', "Time (s)")
        self.plot_widget.addLegend()

        # Create control panel
        control_panel = QWidget()
        control_layout = QHBoxLayout(control_panel)

        # Add clear button
        self.clear_button = QPushButton("Clear Plot")
        self.clear_button.clicked.connect(self.clear_plot)

        # Add show grid checkbox
        self.grid_checkbox = QCheckBox("Show Grid")
        self.grid_checkbox.stateChanged.connect(self.toggle_grid)

        control_layout.addWidget(self.clear_button)
        control_layout.addWidget(self.grid_checkbox)
        control_layout.addStretch()

        # Add widgets to main layout
        self.layout.addWidget(self.plot_widget)
        self.layout.addWidget(control_panel)

        self.plot_items = {}

    def closeEvent(self, event):
        self.was_visible = False
        super().closeEvent(event)

    def clear_plot(self):
        self.plot_widget.clear()
        self.plot_items = {}
        self.plot_widget.addLegend()

    def toggle_grid(self, state):
        self.plot_widget.showGrid(x=state, y=state)

    def plot_trace(self, well: str, times, values, color='b'):
        if well in self.plot_items:
            self.plot_widget.removeItem(self.plot_items[well])
        pen = pg.mkPen(color=color, width=2)
        self.plot_items[well] = self.plot_widget.plot(times, values, pen=pen, name=well)

class RawPlotWindow(BasePlotWindow):
    def __init__(self, parent=None):
        super().__init__(title="Raw Traces", parent=parent)
        self.plot_widget.setLabel('left', "Intensity (A.U.)")

class DFFPlotWindow(BasePlotWindow):
    def __init__(self, parent=None):
        super().__init__(title="ΔF/F₀ Traces", parent=parent)
        self.plot_widget.setLabel('left', "ΔF/F₀ (%)")


class SummaryPlotWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Summary Plots")
        self.resize(800, 600)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Add tab widget for different summary plots
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)

        # Create tabs for different plot types
        self.individual_tab = QWidget()
        self.mean_tab = QWidget()
        self.responses_tab = QWidget()
        self.normalized_tab = QWidget()  # New tab for ionomycin-normalized data

        self.tab_widget.addTab(self.individual_tab, "Individual Traces")
        self.tab_widget.addTab(self.mean_tab, "Mean Traces")
        self.tab_widget.addTab(self.responses_tab, "Peak Responses")
        self.tab_widget.addTab(self.normalized_tab, "Normalized to Ionomycin")

        # Create plot widgets for each tab
        self.individual_plot = pg.PlotWidget()
        self.individual_plot.setBackground('w')
        self.individual_plot.setLabel('left', "ΔF/F₀ (%)")
        self.individual_plot.setLabel('bottom', "Time (s)")

        self.mean_plot = pg.PlotWidget()
        self.mean_plot.setBackground('w')
        self.mean_plot.setLabel('left', "ΔF/F₀ (%)")
        self.mean_plot.setLabel('bottom', "Time (s)")

        self.responses_plot = pg.PlotWidget()
        self.responses_plot.setBackground('w')
        self.responses_plot.setLabel('left', "Peak ΔF/F₀ (%)")
        self.responses_plot.setLabel('bottom', "Group")

        self.normalized_plot = pg.PlotWidget()
        self.normalized_plot.setBackground('w')
        self.normalized_plot.setLabel('left', "Response (% Ionomycin)")
        self.normalized_plot.setLabel('bottom', "Group")

        # Set up layouts for each tab
        individual_layout = QVBoxLayout(self.individual_tab)
        individual_layout.addWidget(self.individual_plot)

        mean_layout = QVBoxLayout(self.mean_tab)
        mean_layout.addWidget(self.mean_plot)

        responses_layout = QVBoxLayout(self.responses_tab)
        responses_layout.addWidget(self.responses_plot)

        normalized_layout = QVBoxLayout(self.normalized_tab)
        normalized_layout.addWidget(self.normalized_plot)

        self.plot_items = {}  # Store plot items for reference

    def clear_plots(self):
        """Clear all plots"""
        self.individual_plot.clear()
        self.mean_plot.clear()
        self.responses_plot.clear()
        self.normalized_plot.clear()
        self.plot_items = {}

class DataProcessor:
    """Class to handle data processing operations"""
    @staticmethod
    def get_F0(data: pd.DataFrame, baseline_frames: int = 15) -> np.ndarray:
        """Calculate baseline (F0) as mean of first baseline_frames for each row."""
        return data.iloc[:, :baseline_frames].mean(axis=1)

    @staticmethod
    def calculate_dff(data: pd.DataFrame, F0: np.ndarray) -> pd.DataFrame:
        """Calculate ΔF/F₀"""
        return (data.div(F0, axis=0) -1) * 100

    @staticmethod
    def calculate_peak_response(data: pd.DataFrame, start_frame: int = None) -> pd.Series:
        """Calculate peak response"""
        if start_frame is not None:
            data = data.iloc[:, start_frame:]
        return data.max(axis=1)


class WellPlateLabeler(QMainWindow):
    """Main application window"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FLIPR Analysis")

        # Add analysis parameters
        self.analysis_params = {
            'artifact_start': 18,
            'artifact_end': 30,
            'baseline_frames': 15,
            'peak_start_frame': 20
        }

        # Add artifact removal flag
        self.remove_artifact = False

        # Add ionomycin normalization flag
        self.normalize_to_ionomycin = False

        # Initialize plot windows
        self.raw_plot_window = RawPlotWindow()
        self.dff_plot_window = DFFPlotWindow()
        self.summary_plot_window = SummaryPlotWindow()

        # Initialize data processor
        self.processor = DataProcessor()

        # Initialize data storage
        self.raw_data = None
        self.dff_data = None

        # Define a list of default colors that are easily distinguishable
        self.default_colors = [
            '#1f77b4',  # blue
            '#ff7f0e',  # orange
            '#2ca02c',  # green
            '#d62728',  # red
            '#9467bd',  # purple
            '#8c564b',  # brown
            '#e377c2',  # pink
            '#7f7f7f',  # gray
        ]

        # Initialize well_data with default colors cycling through the list
        self.well_data = [
            {
                "well_id": "",
                "label": "",
                "concentration": "",
                "sample_id": "",
                "color": self.default_colors[i % len(self.default_colors)]
            }
            for i in range(96)
        ]

        self.selected_wells = set()
        self.current_color = QColor(self.default_colors[0])
        # Create menus
        self.create_menus()
        self.initUI()

    def initUI(self):
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        self.setCentralWidget(main_widget)

        # Add plot type selection
        plot_group = QWidget()
        plot_layout = QHBoxLayout()
        plot_group.setLayout(plot_layout)

        # Plot toggle buttons
        self.raw_plot_button = QPushButton("Raw Traces")
        self.dff_plot_button = QPushButton("ΔF/F₀ Traces")
        self.summary_plot_button = QPushButton("Summary Plots")

        # Set up toggle behavior
        self.raw_plot_button.setCheckable(True)
        self.dff_plot_button.setCheckable(True)
        self.summary_plot_button.setCheckable(True)

        # Connect signals
        self.raw_plot_button.clicked.connect(lambda: self.toggle_plot_window('raw'))
        self.dff_plot_button.clicked.connect(lambda: self.toggle_plot_window('dff'))
        self.summary_plot_button.clicked.connect(lambda: self.toggle_plot_window('summary'))

        plot_layout.addWidget(self.raw_plot_button)
        plot_layout.addWidget(self.dff_plot_button)
        plot_layout.addWidget(self.summary_plot_button)

        main_layout.addWidget(plot_group)

        # parameters inputs
        params_group = QWidget()
        params_layout = QHBoxLayout()
        params_group.setLayout(params_layout)

        # Add injection artifact removal checkbox
        self.artifact_checkbox = QCheckBox("Remove Injection Artifact")
        self.artifact_checkbox.setChecked(self.remove_artifact)
        self.artifact_checkbox.stateChanged.connect(self.toggle_artifact_removal)
        params_layout.addWidget(self.artifact_checkbox)

        # Add ionomycin normalization checkbox
        self.ionomycin_checkbox = QCheckBox("Normalize to Ionomycin")
        self.ionomycin_checkbox.setChecked(self.normalize_to_ionomycin)
        self.ionomycin_checkbox.stateChanged.connect(self.toggle_ionomycin_normalization)
        params_layout.addWidget(self.ionomycin_checkbox)

        main_layout.addWidget(params_group)

        # Mode selection
        mode_layout = QHBoxLayout()
        self.mode_selector = QComboBox()
        self.mode_selector.addItems(["Simple Label", "Log10 Series", "Clear Wells"])
        mode_layout.addWidget(QLabel("Mode:"))
        mode_layout.addWidget(self.mode_selector)
        main_layout.addLayout(mode_layout)

        # Input fields
        self.label_input = QLineEdit(placeholderText="Enter label for selected wells")
        self.starting_conc_input = QLineEdit(placeholderText="Starting concentration (µM)")
        self.sample_id_input = QLineEdit(placeholderText="Enter sample ID")
        self.color_button = QPushButton("Select Color")
        self.color_button.clicked.connect(self.select_color)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.label_input)
        input_layout.addWidget(self.starting_conc_input)
        input_layout.addWidget(self.sample_id_input)
        input_layout.addWidget(self.color_button)
        main_layout.addLayout(input_layout)

        # Action buttons
        action_layout = QHBoxLayout()
        apply_button = QPushButton("Apply Label")
        apply_button.clicked.connect(self.apply_label)
        clear_button = QPushButton("Clear Selection")
        clear_button.clicked.connect(self.clear_selection)
        save_button = QPushButton("Save Layout")
        save_button.clicked.connect(self.save_layout)
        load_button = QPushButton("Load Layout")
        load_button.clicked.connect(self.load_layout)
        load_data_button = QPushButton("Load Data")
        load_data_button.clicked.connect(self.open_file_dialog)

        action_layout.addWidget(apply_button)
        action_layout.addWidget(clear_button)
        action_layout.addWidget(save_button)
        action_layout.addWidget(load_button)
        action_layout.addWidget(load_data_button)
        main_layout.addLayout(action_layout)

        # 96-Well Plate Layout
        plate_layout = QGridLayout()
        rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        cols = range(1, 13)
        self.wells = []

        # Add top-left corner label for selecting all wells
        top_left_label = QLabel("", alignment=Qt.AlignCenter)
        top_left_label.setStyleSheet("background-color: lightgray;")
        top_left_label.setCursor(Qt.PointingHandCursor)
        # Using a regular function instead of lambda for clarity
        def all_wells_clicked(event):
            self.toggle_all_selection()
        top_left_label.mousePressEvent = all_wells_clicked
        plate_layout.addWidget(top_left_label, 0, 0)

        # Add column headers
        for j, col in enumerate(cols):
            col_label = QLabel(str(col), alignment=Qt.AlignCenter)
            col_label.setCursor(Qt.PointingHandCursor)
            # Create a closure to properly capture the column index
            def make_column_clicked(col_idx):
                return lambda event: self.toggle_column_selection(col_idx)
            col_label.mousePressEvent = make_column_clicked(j)
            plate_layout.addWidget(col_label, 0, j + 1)

        # Add row headers and buttons
        for i, row in enumerate(rows):
            row_label = QLabel(row, alignment=Qt.AlignCenter)
            row_label.setCursor(Qt.PointingHandCursor)
            # Create a closure to properly capture the row index
            def make_row_clicked(row_idx):
                return lambda event: self.toggle_row_selection(row_idx)
            row_label.mousePressEvent = make_row_clicked(i)
            plate_layout.addWidget(row_label, i + 1, 0)

            for j, col in enumerate(cols):
                well_index = i * 12 + j
                well_id = f"{row}{col}"
                button = QPushButton(well_id)
                button.setStyleSheet("background-color: white;")
                # The well button click handler doesn't need modification as it was working correctly
                button.clicked.connect(lambda checked, idx=well_index: self.toggle_well_selection(idx))
                self.wells.append(button)
                # Store the well_id in well_data
                self.well_data[well_index]["well_id"] = well_id
                plate_layout.addWidget(button, i + 1, j + 1)

        main_layout.addLayout(plate_layout)
        main_widget.setLayout(main_layout)

    def create_menus(self):
        """Create menu bar and menus"""
        menubar = self.menuBar()

        # Analysis menu
        analysis_menu = menubar.addMenu('Analysis')

        # Parameters action
        params_action = QAction('Parameters...', self)
        params_action.triggered.connect(self.show_parameters_dialog)
        analysis_menu.addAction(params_action)

        # Help menu
        help_menu = menubar.addMenu('Help')

        # About action
        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

        # Manual action
        manual_action = QAction('User Manual', self)
        manual_action.triggered.connect(self.show_manual)
        help_menu.addAction(manual_action)

    def show_parameters_dialog(self):
        """Show parameters dialog and update values if accepted"""
        dialog = ParametersDialog(self)

        # Set current values
        dialog.artifact_start.setValue(self.analysis_params['artifact_start'])
        dialog.artifact_end.setValue(self.analysis_params['artifact_end'])
        dialog.baseline_frames.setValue(self.analysis_params['baseline_frames'])
        dialog.peak_start_frame.setValue(self.analysis_params['peak_start_frame'])

        if dialog.exec_():
            # Update parameters if dialog is accepted
            self.analysis_params['artifact_start'] = dialog.artifact_start.value()
            self.analysis_params['artifact_end'] = dialog.artifact_end.value()
            self.analysis_params['baseline_frames'] = dialog.baseline_frames.value()
            self.analysis_params['peak_start_frame'] = dialog.peak_start_frame.value()

            # Reprocess data if needed
            if self.raw_data is not None:
                self.process_data()
                self.update_plots()

    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(self, "About FLIPR Analysis",
            "FLIPR Analysis Tool\n\n"
            "A tool for analyzing calcium imaging data from FLIPR experiments.\n\n"
            "Version 1.0")

    def show_manual(self):
        """Show user manual"""
        QMessageBox.information(self, "FLIPR Analysis Tool - Quick Guide",
        """FLIPR Analysis Tool
        Quick Start Guide:

        Loading Data
        • Click 'Load Data' to import your .seq1 file
        • The well plate grid will become active
        Well Selection
        • Click individual wells to select/deselect
        • Click row (A-H) or column (1-12) headers to select entire rows/columns
        • Click top-left corner to select all wells
        Labeling Wells
        • Enter agonist name, concentration, and sample ID
        • Use color selector to assign group colors
        • Select wells and click 'Apply Label'
        • For dilution series, use 'Log10 Series' mode
        Analysis Options
        • Access parameters via Analysis → Parameters menu
        • Toggle 'Remove Injection Artifact' to clean data
        • Enable 'Normalize to Ionomycin' for normalized responses
        Visualization (Summary Plots)
        • Individual Traces: All ΔF/F₀ traces by group
        • Mean Traces: Average responses with SEM
        • Peak Responses: Maximum responses with error bars
        • Normalized Responses: Data as % of ionomycin (when enabled)

        Tips:

        Label wells before analysis for proper grouping
        Set analysis parameters before processing
        Use consistent naming for proper grouping
        Save layouts for repeated analysis

        For more detailed information, please refer to the full user manual.""")


    def show_plot_window(self):
        """Show the plot window and plot selected wells"""
        if not self.raw_data is not None:
            QMessageBox.warning(self, "Warning", "Please load data first")
            return

        self.plot_window.show()
        self.update_plots()

    def toggle_artifact_removal(self, state):
        """Toggle artifact removal and update plots"""
        self.remove_artifact = bool(state)
        if self.raw_data is not None:
            self.process_data()
            self.update_plots()

    def toggle_ionomycin_normalization(self, state):
        """Toggle ionomycin normalization and update plots"""
        self.normalize_to_ionomycin = bool(state)
        if self.raw_data is not None:
            self.update_summary_plots()

    def toggle_plot_window(self, plot_type):
        """Toggle visibility of specified plot window"""
        if self.raw_data is None:
            QMessageBox.warning(self, "Warning", "Please load data first")
            return

        windows = {
            'raw': (self.raw_plot_window, self.raw_plot_button),
            'dff': (self.dff_plot_window, self.dff_plot_button),
            'summary': (self.summary_plot_window, self.summary_plot_button)
        }

        window, button = windows[plot_type]

        if window.isVisible():
            window.hide()
            button.setChecked(False)
        else:
            # Process data if needed
            if plot_type in ['dff', 'summary'] and self.dff_data is None:
                self.process_data()

            window.show()
            button.setChecked(True)

            # Update appropriate plots
            if plot_type == 'summary':
                logger.info("Triggering summary plot update...")
                self.update_summary_plots()
            else:
                self.update_plots()

    def group_data_by_metadata(self):
        """Group data based on available metadata"""
        grouped_data = {}

        # Default group for all wells if no metadata
        all_wells = []

        for idx in range(96):
            well_data = self.well_data[idx]
            well_id = well_data["well_id"]
            all_wells.append(well_id)

            # Create grouping key based on available metadata
            key_parts = []
            if well_data.get("label"):  # Agonist
                key_parts.append(well_data["label"])
            if well_data.get("concentration"):
                key_parts.append(f"{well_data['concentration']}")
            if well_data.get("sample_id"):
                key_parts.append(well_data["sample_id"])

            if key_parts:  # If we have metadata, use it for grouping
                group_key = " | ".join(key_parts)
                if group_key not in grouped_data:
                    grouped_data[group_key] = []
                grouped_data[group_key].append(well_id)

        # If no groups were created, use all wells as a single group
        if not grouped_data:
            grouped_data["All Wells"] = all_wells

        logger.info(f"Created {len(grouped_data)} groups: {list(grouped_data.keys())}")
        return grouped_data

    def get_ionomycin_responses(self):
        """Calculate mean ionomycin responses for each sample ID"""
        ionomycin_responses = {}

        # Group wells by sample ID
        sample_groups = {}
        for idx in range(96):
            well_data = self.well_data[idx]
            if well_data["label"] == "Ionomycin":
                sample_id = well_data.get("sample_id", "default")
                if sample_id not in sample_groups:
                    sample_groups[sample_id] = []
                sample_groups[sample_id].append(well_data["well_id"])

        # Calculate mean ionomycin response for each sample
        for sample_id, wells in sample_groups.items():
            peaks = self.dff_data.loc[wells].max(axis=1)
            ionomycin_responses[sample_id] = peaks.mean()

        return ionomycin_responses


    def update_summary_plots(self):
        """Update summary plots based on grouped data"""
        logger.info("Starting summary plot update...")

        if self.dff_data is None:
            logger.info("Processing data for summary plots...")
            self.process_data()

        # Clear existing plots
        self.summary_plot_window.clear_plots()

        # Get appropriate time values that match the processed data length
        if self.remove_artifact:
            times = self.processed_time_points  # Use already processed time points
        else:
            times = np.array(pd.to_numeric(self.raw_data.columns, errors='coerce'))

        logger.info(f"Time points shape: {times.shape}")
        logger.info(f"Data shape: {self.dff_data.shape}")

        # Get grouped data
        grouped_data = self.group_data_by_metadata()
        logger.info(f"Processing {len(grouped_data)} groups for plotting")

        # Define colors for groups
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f']

        # Plot traces for each group
        for i, (group_name, well_ids) in enumerate(grouped_data.items()):
            logger.info(f"Plotting group '{group_name}' with {len(well_ids)} wells")

            try:
                # Get color for this group
                base_color = colors[i % len(colors)]
                main_color = QColor(base_color)
                transparent_color = QColor(base_color)
                transparent_color.setAlpha(50)
                light_pen = pg.mkPen(color=main_color, width=1, alpha=50)

                # Get group data
                group_data = self.dff_data.loc[well_ids]

                # Plot individual traces with lighter color
                for well_id in well_ids:
                    trace_data = np.array(self.dff_data.loc[well_id])
                    if len(times) == len(trace_data):  # Verify lengths match
                        self.summary_plot_window.individual_plot.plot(
                            times,
                            trace_data,
                            pen=light_pen,
                            name=group_name if well_id == well_ids[0] else None
                        )
                    else:
                        logger.error(f"Data length mismatch for well {well_id}: times={len(times)}, data={len(trace_data)}")

                # Calculate and plot mean trace
                mean_trace = np.array(group_data.mean())
                sem_trace = np.array(group_data.sem())

                if len(times) == len(mean_trace):  # Verify lengths match
                    # Plot mean trace
                    self.summary_plot_window.mean_plot.plot(
                        times,
                        mean_trace,
                        pen=pg.mkPen(main_color, width=2),
                        name=group_name
                    )

                    # Add error bands
                    band_top = mean_trace + sem_trace
                    band_bottom = mean_trace - sem_trace

                    fill = pg.FillBetweenItem(
                        pg.PlotDataItem(times, band_top),
                        pg.PlotDataItem(times, band_bottom),
                        brush=transparent_color
                    )
                    self.summary_plot_window.mean_plot.addItem(fill)
                else:
                    logger.error(f"Data length mismatch for mean trace: times={len(times)}, data={len(mean_trace)}")


                # Calculate peak responses
                peaks = np.array(group_data.max(axis=1))
                peak_mean = np.mean(peaks)
                peak_sem = np.std(peaks) / np.sqrt(len(peaks))

                # Add bar for peak response
                bar = pg.BarGraphItem(
                    x=[i],
                    height=[peak_mean],
                    width=0.8,
                    brush=main_color
                )
                self.summary_plot_window.responses_plot.addItem(bar)

                # Add error bars
                error = pg.ErrorBarItem(
                    x=np.array([i]),
                    y=np.array([peak_mean]),
                    height=np.array([peak_sem * 2]),
                    beam=0.2,
                    pen=pg.mkPen(main_color, width=2)
                )
                self.summary_plot_window.responses_plot.addItem(error)

                logger.info(f"Successfully plotted group {group_name}")

            except Exception as e:
                logger.error(f"Error plotting group {group_name}: {str(e)}")
                import traceback
                logger.error(traceback.format_exc())
                continue

        # Update all plot labels and settings
        for plot in [self.summary_plot_window.individual_plot,
                    self.summary_plot_window.mean_plot]:
            plot.setLabel('left', 'ΔF/F₀ (%)')
            plot.setLabel('bottom', 'Time (s)')

        # Update peak responses plot
        self.summary_plot_window.responses_plot.setLabel('left', 'Peak ΔF/F₀ (%)')
        self.summary_plot_window.responses_plot.setLabel('bottom', 'Groups')

        # Add group labels to response plot
        group_names = list(grouped_data.keys())
        axis = self.summary_plot_window.responses_plot.getAxis('bottom')
        ticks = [(i, name) for i, name in enumerate(group_names)]
        axis.setTicks([ticks])

        # Set axis ranges for responses plot
        n_groups = len(grouped_data)
        self.summary_plot_window.responses_plot.setXRange(-0.5, n_groups - 0.5)

        # Add normalized responses if enabled
        if self.normalize_to_ionomycin:
            try:
                # Get ionomycin responses
                ionomycin_responses = self.get_ionomycin_responses()

                if not ionomycin_responses:
                    logger.warning("No Ionomycin data found for normalization")
                    return

                # Clear normalized plot
                self.summary_plot_window.normalized_plot.clear()

                # Plot normalized responses for each group
                for i, (group_name, well_ids) in enumerate(grouped_data.items()):
                    if group_name == "Ionomycin":  # Skip ionomycin group
                        continue

                    # Get group data
                    group_data = self.dff_data.loc[well_ids]
                    normalized_peaks = []

                    # Calculate normalized responses
                    for well_id in well_ids:
                        # Get sample ID for this well
                        well_idx = next(idx for idx in range(96) if self.well_data[idx]["well_id"] == well_id)
                        sample_id = self.well_data[well_idx].get("sample_id", "default")

                        # Get corresponding ionomycin response
                        ionomycin_response = ionomycin_responses.get(sample_id)
                        if ionomycin_response:
                            peak = group_data.loc[well_id].max()
                            normalized_peaks.append((peak / ionomycin_response) * 100)

                    if normalized_peaks:
                        normalized_peaks = np.array(normalized_peaks)
                        peak_mean = np.mean(normalized_peaks)
                        peak_sem = np.std(normalized_peaks) / np.sqrt(len(normalized_peaks))

                        # Add bar for normalized response
                        bar = pg.BarGraphItem(
                            x=[i],
                            height=[peak_mean],
                            width=0.8,
                            brush=main_color
                        )
                        self.summary_plot_window.normalized_plot.addItem(bar)

                        # Add error bars
                        error = pg.ErrorBarItem(
                            x=np.array([i]),
                            y=np.array([peak_mean]),
                            height=np.array([peak_sem * 2]),
                            beam=0.2,
                            pen=pg.mkPen(main_color, width=2)
                        )
                        self.summary_plot_window.normalized_plot.addItem(error)

                # Update normalized plot labels and axes
                self.summary_plot_window.normalized_plot.setLabel('left', 'Response (% Ionomycin)')
                self.summary_plot_window.normalized_plot.setLabel('bottom', 'Groups')

                # Add group labels
                non_ionomycin_groups = [name for name in group_names if name != "Ionomycin"]
                axis = self.summary_plot_window.normalized_plot.getAxis('bottom')
                ticks = [(i, name) for i, name in enumerate(non_ionomycin_groups)]
                axis.setTicks([ticks])

                # Set axis ranges
                n_groups = len(non_ionomycin_groups)
                self.summary_plot_window.normalized_plot.setXRange(-0.5, n_groups - 0.5)

            except Exception as e:
                logger.error(f"Error calculating normalized responses: {str(e)}")
                import traceback
                logger.error(traceback.format_exc())


        logger.info("Summary plot update completed")


    def open_file_dialog(self):
        """Open file dialog to load FLIPR data"""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Data File", "",
                                                 "Text Files (*.txt *.seq1);;All Files (*)", options=options)
        if file_path:
            try:
                self.raw_data, self.original_filename = self.load_data(file_path)
                QMessageBox.information(self, "Data Loaded", f"Data loaded from {self.original_filename}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load data: {str(e)}")


    def load_data(self, file_path: str) -> Tuple[pd.DataFrame, str]:
        """Load and preprocess FLIPR data from file."""
        try:
            # Read header
            with open(file_path, 'r') as f:
                header = f.readline().strip().split('\t')
            original_filename = header[0]
            header_values = header[5::]  # Time points start from column 5

            # Read data
            with open(file_path, 'r') as file:
                reader = csv.reader(file, delimiter='\t')
                next(reader)  # Skip header
                raw_data = []
                for row in reader:
                    if len(row) > 4:  # Ensure we have enough columns
                        raw_data.append(row[4:])  # Skip first 4 columns

            # Create DataFrame
            data = pd.DataFrame(raw_data)
            data.set_index(0, inplace=True)
            data.index.name = 'Well'

            # Remove any extra columns
            if len(data.columns) > len(header_values):
                data = data.iloc[:, :len(header_values)]

            data.columns = header_values

            # Convert to numeric, replacing any non-numeric values with NaN
            data = data.apply(pd.to_numeric, errors='coerce')

            # Reset processed data
            self.dff_data = None
            self.zeroed_data = None

            # Debug logging
            logger.info(f"Loaded data shape: {data.shape}")
            logger.info(f"Sample of loaded data:\n{data.iloc[:3, :5]}")  # Show first 3 rows, 5 columns

            return data, original_filename

        except Exception as e:
            logger.error(f"Error loading data from {file_path}: {str(e)}")
            raise


    def plot_single_well(self, idx):
        """Plot a single well's trace"""
        well_id = self.well_data[idx]["well_id"]

        if well_id in self.raw_data.index:
            try:
                times = pd.to_numeric(self.raw_data.columns, errors='coerce')
                values = pd.to_numeric(self.raw_data.loc[well_id], errors='coerce')

                if not values.isna().all():
                    color = self.well_data[idx]["color"]
                    self.plot_window.plot_trace(well_id, times, values, color)
            except Exception as e:
                logger.error(f"Error plotting well {well_id}: {str(e)}")

    def toggle_well_selection(self, index):
        """Toggle well selection and update plots immediately"""
        if index in self.selected_wells:
            self.selected_wells.remove(index)
            self.wells[index].setStyleSheet(f"background-color: {self.well_data[index]['color']}; color: black;")

            # Remove trace from all visible plot windows
            well_id = self.well_data[index]["well_id"]
            if self.raw_plot_window.isVisible() and well_id in self.raw_plot_window.plot_items:
                self.raw_plot_window.plot_widget.removeItem(self.raw_plot_window.plot_items[well_id])
                del self.raw_plot_window.plot_items[well_id]

            if self.dff_plot_window.isVisible() and well_id in self.dff_plot_window.plot_items:
                self.dff_plot_window.plot_widget.removeItem(self.dff_plot_window.plot_items[well_id])
                del self.dff_plot_window.plot_items[well_id]
        else:
            self.selected_wells.add(index)
            self.wells[index].setStyleSheet("background-color: lightblue; color: black;")

            # Add trace to all visible plot windows
            if self.raw_data is not None:
                well_id = self.well_data[index]["well_id"]
                times = pd.to_numeric(self.raw_data.columns, errors='coerce')

                # Update raw plot
                if self.raw_plot_window.isVisible() and well_id in self.raw_data.index:
                    values = self.raw_data.loc[well_id]
                    self.raw_plot_window.plot_trace(well_id, times, values, self.well_data[index]["color"])

                # Update ΔF/F₀ plot
                if self.dff_plot_window.isVisible():
                    if self.dff_data is None:
                        self.process_data()
                    if well_id in self.dff_data.index:
                        values = self.dff_data.loc[well_id]
                        self.dff_plot_window.plot_trace(well_id, times, values, self.well_data[index]["color"])

        # Update summary plots if visible
        if self.summary_plot_window.isVisible():
            self.update_summary_plots()

    def toggle_row_selection(self, row_index):
        """Toggle selection of all wells in a row"""
        start_idx = row_index * 12
        end_idx = start_idx + 12
        row_selected = all(idx in self.selected_wells for idx in range(start_idx, end_idx))

        for idx in range(start_idx, end_idx):
            if row_selected and idx in self.selected_wells:
                self.toggle_well_selection(idx)
            elif not row_selected and idx not in self.selected_wells:
                self.toggle_well_selection(idx)

    def toggle_column_selection(self, col_index):
        """Toggle selection of all wells in a column"""
        col_selected = all(idx in self.selected_wells for idx in range(col_index, 96, 12))

        for idx in range(col_index, 96, 12):
            if col_selected and idx in self.selected_wells:
                self.toggle_well_selection(idx)
            elif not col_selected and idx not in self.selected_wells:
                self.toggle_well_selection(idx)

    def toggle_all_selection(self):
        """Toggle selection of all wells"""
        all_selected = len(self.selected_wells) == 96

        for idx in range(96):
            if all_selected and idx in self.selected_wells:
                self.toggle_well_selection(idx)
            elif not all_selected and idx not in self.selected_wells:
                self.toggle_well_selection(idx)

    def select_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.current_color = color

    def apply_label(self):
        """Apply label, concentration, and color to selected wells"""
        mode = self.mode_selector.currentText()
        sample_id = self.sample_id_input.text()

        if mode == "Simple Label":
            label = self.label_input.text()
            concentration = self.starting_conc_input.text()
            for idx in self.selected_wells:
                self.well_data[idx]["label"] = label
                self.well_data[idx]["concentration"] = f"{concentration} µM" if concentration else ""
                self.well_data[idx]["sample_id"] = sample_id
                # Only update color if user has selected a new one (different from default)
                if self.current_color.name() != self.default_colors[idx % len(self.default_colors)]:
                    self.well_data[idx]["color"] = self.current_color.name()
                self.update_button(idx)

        elif mode == "Log10 Series":
            try:
                starting_conc = float(self.starting_conc_input.text())
            except ValueError:
                QMessageBox.warning(self, "Input Error", "Invalid starting concentration")
                return

            if len(self.selected_wells) < 2:
                QMessageBox.warning(self, "Selection Error", "Select at least 2 wells for Log10 Series")
                return

            # Calculate true log10 series concentrations
            sorted_indices = sorted(self.selected_wells)
            num_wells = len(sorted_indices)
            concentrations = [starting_conc / (10 ** i) for i in range(num_wells)]

            for idx, conc in zip(sorted_indices, concentrations):
                self.well_data[idx]["concentration"] = f"{conc:.2f} µM"
                self.well_data[idx]["label"] = self.label_input.text()
                self.well_data[idx]["sample_id"] = sample_id
                if self.current_color.name() != self.default_colors[idx % len(self.default_colors)]:
                    self.well_data[idx]["color"] = self.current_color.name()
                self.update_button(idx)

        elif mode == "Clear Wells":
            for idx in self.selected_wells:
                # Reset to default color when clearing
                default_color = self.default_colors[idx % len(self.default_colors)]
                self.well_data[idx] = {
                    "well_id": self.well_data[idx]["well_id"],
                    "label": "",
                    "concentration": "",
                    "sample_id": "",
                    "color": default_color
                }
                self.update_button(idx)

        # Update all visible plot windows
        if self.raw_plot_window.isVisible():
            self.update_plots()
        if self.dff_plot_window.isVisible():
            if self.dff_data is None:
                self.process_data()
            self.update_plots()
        if self.summary_plot_window.isVisible():
            self.update_summary_plots()

        self.selected_wells.clear()

    def update_button(self, idx):
        """Update button text and color"""
        data = self.well_data[idx]
        text = f"{data['well_id']}"

        if data['label']:
            text += f"\n{data['label']}"
        if data['concentration']:
            text += f"\n{data['concentration']}"
        if data['sample_id']:
            text += f"\n{data['sample_id']}"

        self.wells[idx].setText(text)
        self.wells[idx].setStyleSheet(
            f"background-color: {data['color']}; color: black;"  # Ensure text is always black
        )

    def clear_selection(self):
        """Clear the selection and reset buttons to default state"""
        for idx in self.selected_wells:
            # Get the default color for this index
            default_color = self.default_colors[idx % len(self.default_colors)]

            # Reset the well data but preserve the well_id
            well_id = self.well_data[idx]["well_id"]
            self.well_data[idx] = {
                "well_id": well_id,
                "label": "",
                "concentration": "",
                "sample_id": "",
                "color": default_color
            }

            # Update button appearance
            self.wells[idx].setText(well_id)  # Reset text to just the well ID
            self.wells[idx].setStyleSheet(f"background-color: {default_color}; color: black;")

        # Clear the selection set
        self.selected_wells.clear()

        # Update plots if plot window is visible
        if self.plot_window.isVisible():
            self.update_plots()

    def save_layout(self):
        """Save the current layout to a JSON file"""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Layout", "", "JSON Files (*.json)", options=options)
        if file_path:
            with open(file_path, "w") as f:
                json.dump(self.well_data, f)

    def load_layout(self):
        """Load a layout from a JSON file"""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Load Layout", "", "JSON Files (*.json)", options=options)
        if file_path:
            with open(file_path, "r") as f:
                self.well_data = json.load(f)
            for idx, data in enumerate(self.well_data):
                self.update_button(idx)

    def process_data(self):
        """Process loaded data with artifact removal if enabled"""
        if self.raw_data is None:
            return

        try:
            # Work with a copy of the raw data
            processed_data = self.raw_data.copy()
            self.processed_time_points = pd.to_numeric(processed_data.columns, errors='coerce')

            # Remove artifact if enabled
            if self.remove_artifact:
                n_cols = processed_data.shape[1]
                start_idx = int(n_cols * self.analysis_params['artifact_start']/220)
                end_idx = int(n_cols * self.analysis_params['artifact_end']/220)

                # Store the time points before removing data
                self.processed_time_points = np.concatenate([
                    self.processed_time_points[:start_idx],
                    self.processed_time_points[end_idx:]
                ])

                # Remove artifact points from data
                processed_data = processed_data.drop(processed_data.columns[start_idx:end_idx], axis=1)
                processed_data.columns = self.processed_time_points  # Update column names

            # Calculate F0
            F0 = self.processor.get_F0(processed_data,
                                     baseline_frames=self.analysis_params['baseline_frames'])

            # Calculate ΔF/F₀
            self.dff_data = self.processor.calculate_dff(processed_data, F0)

            logger.info("Data processing completed successfully")
            logger.info(f"Processed data shape: {processed_data.shape}")
            logger.info(f"Time points shape: {self.processed_time_points.shape}")

        except Exception as e:
            logger.error(f"Error processing data: {str(e)}")
            QMessageBox.critical(self, "Error", f"Failed to process data: {str(e)}")


    def update_plots(self):
        """Update all plot windows"""
        if self.raw_data is None:
            return

        # Get appropriate time values
        if self.remove_artifact:
            times = self.processed_time_points
        else:
            times = pd.to_numeric(self.raw_data.columns, errors='coerce')

        # Update plots for each selected well
        for idx in self.selected_wells:
            well_id = self.well_data[idx]["well_id"]
            if well_id in self.raw_data.index:
                # Plot raw data
                if self.raw_plot_window.isVisible():
                    if self.remove_artifact:
                        # Get processed raw data
                        n_cols = self.raw_data.shape[1]
                        start_idx = int(n_cols * self.analysis_params['artifact_start']/220)
                        end_idx = int(n_cols * self.analysis_params['artifact_end']/220)
                        values = pd.concat([
                            self.raw_data.loc[well_id][:start_idx],
                            self.raw_data.loc[well_id][end_idx:]
                        ])
                    else:
                        values = self.raw_data.loc[well_id]
                    self.raw_plot_window.plot_trace(well_id, times, values, self.well_data[idx]["color"])

                # Plot ΔF/F₀ data
                if self.dff_plot_window.isVisible() and self.dff_data is not None:
                    values = self.dff_data.loc[well_id]
                    self.dff_plot_window.plot_trace(well_id, times, values, self.well_data[idx]["color"])


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Set the application style
    app.setStyle('Fusion')

    window = WellPlateLabeler()
    window.show()
    sys.exit(app.exec_())
