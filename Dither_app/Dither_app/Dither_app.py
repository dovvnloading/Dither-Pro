# -*- coding: utf-8 -*-
import sys
import numpy as np
import colorsys
from PIL import Image, ImageQt
from PySide6.QtCore import Qt, QThread, Signal, Slot, QTimer, QPointF
from PySide6.QtGui import QPixmap, QImage, QIcon, QCloseEvent, QPainter, QPen, QColor
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QComboBox, QSlider, QSplitter,
    QMessageBox, QFrame, QStatusBar, QTabWidget
)

from algorithms import DitherAlgorithms
from worker import ImageProcessor
from utils import ImageUtils

class DitheringApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.original_pil_image = None
        self.dithered_pil_image = None
        self.dithered_palette = None
        self.hsv_adjusted_dithered_image = None
        self.final_output_image = None
        self.processing_thread = None
        self.worker = None
        self.hsv_update_timer = QTimer(self)
        self.hsv_update_timer.setSingleShot(True)
        self.hsv_update_timer.setInterval(150)
        self._setup_ui()

    def _create_app_icon(self):
        pixmap = QPixmap(64, 64)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(QColor("#0078d7"))
        pen.setWidth(4)
        painter.setPen(pen)
        v = [QPointF(10,10),QPointF(35,10),QPointF(35,35),QPointF(10,35),QPointF(25,25),QPointF(50,25),QPointF(50,50),QPointF(25,50)]
        edges = [(0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),(0,4),(1,5),(2,6),(3,7)]
        for p1_idx, p2_idx in edges:
            painter.drawLine(v[p1_idx], v[p2_idx])
        painter.end()
        return QIcon(pixmap)

    def _setup_ui(self):
        self.setWindowTitle("Advanced Dithering Tool")
        self.setWindowIcon(self._create_app_icon())
        self.setGeometry(100, 100, 1200, 700)
        self.setStyleSheet(DitheringApp.DARK_STYLESHEET)
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        self.setCentralWidget(main_widget)
        self._create_image_views()
        self._create_controls_panel()
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.original_image_frame)
        splitter.addWidget(self.dithered_image_frame)
        splitter.setSizes([500, 500])
        main_layout.addWidget(splitter, 3)
        main_layout.addWidget(self.controls_frame, 1)
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready. Please open an image file.")
        self._connect_signals()
        self._update_ui_state()

    def _create_image_views(self):
        self.original_image_frame = QFrame()
        original_layout = QVBoxLayout(self.original_image_frame)
        self.original_title = QLabel("Original Image")
        self.original_title.setAlignment(Qt.AlignCenter)
        self.original_title.setStyleSheet("font-weight: bold; font-size: 12pt;")
        self.original_image_label = QLabel("Load an image to begin")
        self.original_image_label.setAlignment(Qt.AlignCenter)
        original_layout.addWidget(self.original_title)
        original_layout.addWidget(self.original_image_label, 1)
        self.dithered_image_frame = QFrame()
        dithered_layout = QVBoxLayout(self.dithered_image_frame)
        dithered_title = QLabel("Final Image")
        dithered_title.setAlignment(Qt.AlignCenter)
        dithered_title.setStyleSheet("font-weight: bold; font-size: 12pt;")
        self.dithered_image_label = QLabel("Processed image will appear here")
        self.dithered_image_label.setAlignment(Qt.AlignCenter)
        dithered_layout.addWidget(dithered_title)
        dithered_layout.addWidget(self.dithered_image_label, 1)

    def _create_controls_panel(self):
        self.controls_frame = QFrame()
        self.controls_frame.setFixedWidth(350)
        controls_layout = QVBoxLayout(self.controls_frame)
        self.open_button = QPushButton("Open Image")
        self.save_button = QPushButton("Save Final Image")
        self.tabs = QTabWidget()
        dither_widget = QWidget()
        dither_layout = QVBoxLayout(dither_widget)
        self.algorithm_combo = QComboBox()
        self.algorithm_combo.addItems(["Floyd-Steinberg", "Atkinson", "Jarvis, Judice, Ninke", "Stucki", "Bayer (Ordered)", "Clustered Dot Halftone", "Random"])
        self.palette_combo = QComboBox()
        palette_options = ["Auto (From Image)", "Grayscale"] + list(DitherAlgorithms.PREDEFINED_PALETTES.keys())
        self.palette_combo.addItems(palette_options)
        self.color_slider = QSlider(Qt.Horizontal)
        self.color_slider.setMinimum(2)
        self.color_slider.setMaximum(256)
        self.color_slider.setValue(8)
        self.color_slider_label = QLabel(f"{self.color_slider.value()} Colors")
        self.color_slider_label.setAlignment(Qt.AlignCenter)
        self.strength_slider = QSlider(Qt.Horizontal)
        self.strength_slider.setMinimum(0)
        self.strength_slider.setMaximum(100)
        self.strength_slider.setValue(100)
        self.strength_slider_label = QLabel(f"{self.strength_slider.value()}%")
        self.strength_slider_label.setAlignment(Qt.AlignCenter)
        self.dither_button = QPushButton("Apply Dithering")
        dither_layout.addWidget(QLabel("Dithering Algorithm:"))
        dither_layout.addWidget(self.algorithm_combo)
        dither_layout.addWidget(QLabel("Color Palette:"))
        dither_layout.addWidget(self.palette_combo)
        dither_layout.addWidget(QLabel("Number of Colors:"))
        dither_layout.addWidget(self.color_slider_label)
        dither_layout.addWidget(self.color_slider)
        dither_layout.addWidget(QLabel("Dithering Strength:"))
        dither_layout.addWidget(self.strength_slider_label)
        dither_layout.addWidget(self.strength_slider)
        dither_layout.addStretch()
        dither_layout.addWidget(self.dither_button)
        adjust_widget = QWidget()
        adjust_layout = QVBoxLayout(adjust_widget)
        self.hue_slider = QSlider(Qt.Horizontal)
        self.hue_slider.setRange(-180, 180)
        self.hue_slider.setValue(0)
        self.hue_label = QLabel("0 deg")
        adjust_layout.addWidget(QLabel("Hue Shift:"))
        adjust_layout.addWidget(self.hue_label)
        adjust_layout.addWidget(self.hue_slider)
        self.sat_slider = QSlider(Qt.Horizontal)
        self.sat_slider.setRange(-100, 100)
        self.sat_slider.setValue(0)
        self.sat_label = QLabel("0%")
        adjust_layout.addWidget(QLabel("Saturation:"))
        adjust_layout.addWidget(self.sat_label)
        adjust_layout.addWidget(self.sat_slider)
        self.val_slider = QSlider(Qt.Horizontal)
        self.val_slider.setRange(-100, 100)
        self.val_slider.setValue(0)
        self.val_label = QLabel("0%")
        adjust_layout.addWidget(QLabel("Value/Brightness:"))
        adjust_layout.addWidget(self.val_label)
        adjust_layout.addWidget(self.val_slider)
        self.reset_hsv_button = QPushButton("Reset Color Adjustments")
        adjust_layout.addStretch()
        adjust_layout.addWidget(self.reset_hsv_button)
        lut_widget = QWidget()
        lut_layout = QVBoxLayout(lut_widget)
        self.lut_combo = QComboBox()
        self.lut_combo.addItems(["None"] + ImageUtils.AVAILABLE_LUTS)
        self.apply_lut_button = QPushButton("Apply Grading")
        lut_layout.addWidget(QLabel("Color Grading LUT:"))
        lut_layout.addWidget(self.lut_combo)
        lut_layout.addStretch()
        lut_layout.addWidget(self.apply_lut_button)
        self.tabs.addTab(dither_widget, "Dithering")
        self.tabs.addTab(adjust_widget, "Color Adjust")
        self.tabs.addTab(lut_widget, "Grading / LUT")
        controls_layout.addWidget(self.open_button)
        controls_layout.addWidget(self.save_button)
        controls_layout.addSpacing(10)
        controls_layout.addWidget(self.tabs)

    def _connect_signals(self):
        self.open_button.clicked.connect(self.open_image)
        self.save_button.clicked.connect(self.save_image)
        self.dither_button.clicked.connect(self.start_dithering)
        self.apply_lut_button.clicked.connect(self.apply_lut)
        self.reset_hsv_button.clicked.connect(self.reset_hsv)
        self.hsv_update_timer.timeout.connect(self._apply_hsv_adjustments_to_dithered)
        self.color_slider.valueChanged.connect(lambda v: self.color_slider_label.setText(f"{v} Colors"))
        self.strength_slider.valueChanged.connect(lambda v: self.strength_slider_label.setText(f"{v}%"))
        self.palette_combo.currentTextChanged.connect(self.on_palette_change)
        self.hue_slider.valueChanged.connect(self._schedule_hsv_update)
        self.sat_slider.valueChanged.connect(self._schedule_hsv_update)
        self.val_slider.valueChanged.connect(self._schedule_hsv_update)

    def _schedule_hsv_update(self):
        self.hue_label.setText(f"{self.hue_slider.value()} deg")
        self.sat_label.setText(f"{self.sat_slider.value()}%")
        self.val_label.setText(f"{self.val_slider.value()}%")
        if self.dithered_pil_image:
            self.hsv_update_timer.start()

    def _apply_hsv_adjustments_to_dithered(self):
        if not self.dithered_palette or not self.dithered_pil_image:
            return
        h_shift = self.hue_slider.value() / 360.0
        s_shift = self.sat_slider.value() / 100.0
        v_shift = self.val_slider.value() / 100.0
        new_palette = []
        for r_orig, g_orig, b_orig in self.dithered_palette:
            h,s,v = colorsys.rgb_to_hsv(r_orig/255.0, g_orig/255.0, b_orig/255.0)
            h = (h + h_shift) % 1.0
            s = max(0.0, min(1.0, s + s_shift))
            v = max(0.0, min(1.0, v + v_shift))
            r_new, g_new, b_new = colorsys.hsv_to_rgb(h, s, v)
            new_palette.append([int(r_new*255), int(g_new*255), int(b_new*255)])
        img_array = np.array(self.dithered_pil_image)
        output_array = img_array.copy()
        for i, original_color in enumerate(self.dithered_palette):
            mask = np.all(img_array == original_color, axis=-1)
            output_array[mask] = new_palette[i]
        self.hsv_adjusted_dithered_image = Image.fromarray(output_array)
        self.final_output_image = self.hsv_adjusted_dithered_image
        self.display_image(self.final_output_image, is_preview=False)
        self.lut_combo.setCurrentIndex(0)
        self.status_bar.showMessage("Adjusting dithered colors...")

    def reset_hsv(self):
        self.hue_slider.setValue(0)
        self.sat_slider.setValue(0)
        self.val_slider.setValue(0)
        if self.dithered_pil_image:
            self.hsv_adjusted_dithered_image = self.dithered_pil_image.copy()
            self.final_output_image = self.hsv_adjusted_dithered_image
            self.display_image(self.final_output_image, is_preview=False)

    def apply_lut(self):
        base_image = self.hsv_adjusted_dithered_image if self.hsv_adjusted_dithered_image else self.dithered_pil_image
        if not base_image:
            return
        lut_name = self.lut_combo.currentText()
        if lut_name == "None":
            self.final_output_image = base_image
        else:
            self.final_output_image = ImageUtils.apply_lut(base_image.copy(), lut_name)
        self.display_image(self.final_output_image, is_preview=False)
        self.status_bar.showMessage(f"Applied '{lut_name}' color grade.")

    def start_dithering(self):
        if not self.original_pil_image:
            return
        self._update_ui_state(is_processing=True)
        dither_params = {'algorithm_name': self.algorithm_combo.currentText(),'palette_name': self.palette_combo.currentText(),'num_colors': self.color_slider.value(),'dither_strength': self.strength_slider.value()}
        self.processing_thread = QThread()
        self.worker = ImageProcessor(self.original_pil_image, dither_params)
        self.worker.moveToThread(self.processing_thread)
        self.processing_thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.on_dithering_complete)
        self.worker.error.connect(self.on_dithering_error)
        self.worker.finished.connect(self.processing_thread.quit)
        self.processing_thread.finished.connect(self._on_thread_finished)
        self.processing_thread.start()

    def display_image(self, pil_img, is_preview):
        target_label = self.original_image_label if is_preview else self.dithered_image_label
        q_image = ImageQt.ImageQt(pil_img)
        pixmap = QPixmap.fromImage(q_image)
        target_label.setPixmap(pixmap.scaled(target_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def on_dithering_complete(self, processed_image, used_palette):
        self.dithered_pil_image = processed_image
        self.dithered_palette = used_palette
        self.hsv_adjusted_dithered_image = None
        self.final_output_image = processed_image
        self.reset_hsv()
        self.lut_combo.setCurrentIndex(0)
        self.display_image(self.final_output_image, is_preview=False)
        self._update_ui_state()
        self.tabs.setCurrentIndex(0)
        self.status_bar.showMessage("Dithering complete. Post-processing enabled.")

    def open_image(self, *args):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")
        if not file_path:
            return
        try:
            self.status_bar.showMessage(f"Loading: {file_path}...")
            self.original_pil_image = Image.open(file_path).convert('RGB')
            self.dithered_pil_image = None
            self.dithered_palette = None
            self.final_output_image = None
            self.display_image(self.original_pil_image, is_preview=True)
            self.original_title.setText("Original Image")
            self.dithered_image_label.setText("Process an image to see results")
            self.dithered_image_label.setPixmap(QPixmap())
            self.reset_hsv()
            self._update_ui_state()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open or read image file:\n{e}")

    def _update_ui_state(self, is_processing=False):
        has_original = self.original_pil_image is not None
        has_dithered = self.dithered_pil_image is not None
        self.tabs.setTabEnabled(0, has_original and not is_processing)
        self.tabs.setTabEnabled(1, has_dithered and not is_processing)
        self.tabs.setTabEnabled(2, has_dithered and not is_processing)
        self.open_button.setEnabled(not is_processing)
        self.save_button.setEnabled(has_dithered and not is_processing)
        if is_processing:
            self.status_bar.showMessage("Processing... Please wait.")
        elif not has_original:
            self.status_bar.showMessage("Ready. Please open an image file.")
        else:
            self.status_bar.showMessage("Image loaded. Ready to dither.")

    def resizeEvent(self, event):
        if self.original_pil_image:
            self.display_image(self.original_pil_image, is_preview=True)
        if self.final_output_image:
            self.display_image(self.final_output_image, is_preview=False)
        super().resizeEvent(event)

    def on_dithering_error(self, traceback_str):
        print("--- PROCESSING ERROR ---")
        print(traceback_str)
        print("------------------------")
        if self.processing_thread and self.processing_thread.isRunning():
            self.processing_thread.quit()
        self._update_ui_state()
        self.status_bar.showMessage("An error occurred. See console for details.")

    def on_palette_change(self, text):
        is_dynamic_palette = text in ["Auto (From Image)", "Grayscale"]
        self.color_slider.setEnabled(is_dynamic_palette)
        self.color_slider_label.setEnabled(is_dynamic_palette)

    def save_image(self):
        image_to_save = self.final_output_image if self.final_output_image else self.dithered_pil_image
        if not image_to_save:
            return
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Final Image", "", "PNG Image (*.png);;JPEG Image (*.jpg)")
        if file_path:
            try:
                image_to_save.save(file_path)
                self.status_bar.showMessage(f"Image successfully saved to {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Save Error", f"Failed to save image:\n{e}")

    def _on_thread_finished(self):
        if self.worker:
            self.worker.deleteLater()
        if self.processing_thread:
            self.processing_thread.deleteLater()
        self.worker, self.processing_thread = None, None

    def closeEvent(self, event: QCloseEvent):
        if self.processing_thread and self.processing_thread.isRunning():
            self.processing_thread.quit()
            self.processing_thread.wait(3000)
        event.accept()

if __name__ == "__main__":
    DitheringApp.DARK_STYLESHEET = """
    QWidget { background-color: #2b2b2b; color: #f0f0f0; font-family: Segoe UI; font-size: 10pt; }
    QMainWindow { background-color: #1e1e1e; }
    QFrame { border: 1px solid #444; border-radius: 4px; }
    QPushButton { background-color: #4a4a4a; border: 1px solid #555; padding: 6px; border-radius: 4px; min-height: 1.5em; }
    QPushButton:hover { background-color: #5a5a5a; } QPushButton:pressed { background-color: #6a6a6a; }
    QPushButton:disabled { background-color: #3a3a3a; color: #777; }
    QComboBox { background-color: #4a4a4a; border: 1px solid #555; border-radius: 4px; padding: 4px; }
    QComboBox::drop-down { border: none; }
    QComboBox QAbstractItemView { background-color: #4a4a4a; border: 1px solid #555; selection-background-color: #0078d7; }
    QSlider::groove:horizontal { border: 1px solid #444; height: 8px; background: #3a3a3a; margin: 2px 0; border-radius: 4px; }
    QSlider::handle:horizontal {
        background: #0078d7;
        border: 1px solid #0078d7;
        width: 16px;
        height: 16px;
        margin: -4px 0;
        border-radius: 8px;
    }
    QLabel { border: none; }
    QStatusBar { background-color: #1e1e1e; color: #aaa; }
    QTabWidget::pane { border: 1px solid #444; top: -1px; } 
    QTabBar::tab { background: #2b2b2b; border: 1px solid #444; padding: 6px; border-bottom: none; } 
    QTabBar::tab:selected { background: #4a4a4a; margin-bottom: -1px; }
    QTabBar::tab:disabled { background: #222; color: #666; }
    """
    app = QApplication(sys.argv)
    window = DitheringApp()
    window.show()
    sys.exit(app.exec())