# Dither-Pro

<div align="center">

  ![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
  ![PySide6](https://img.shields.io/badge/PySide6-Qt-41CD52?style=for-the-badge&logo=qt&logoColor=white)
  ![Numba](https://img.shields.io/badge/Numba-Accelerated-00A3E0?style=for-the-badge&logo=numba&logoColor=white)
  ![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

  **A high-performance, algorithmic dithering suite built for digital artists and developers.**
  
  [Features](#features) • [Installation](#installation) • [Usage](#usage) • [Algorithms](#algorithms)

</div>

---

**Dither-Pro** is a specialized image processing tool that transforms standard images into limited-color retro aesthetic masterpieces. Unlike basic converters, Dither-Pro utilizes **Numba JIT compilation** to accelerate complex error-diffusion and ordered dithering algorithms, allowing for high-resolution processing in near real-time.

Built with a modern **PySide6** interface, it bridges the gap between command-line libraries and professional graphic design software, offering granular control over palettes, dithering strength, and post-process color grading.

## Interface

<p align="center">
  <img width="100%" alt="Dither-Pro Application Screenshot" src="https://github.com/user-attachments/assets/46e8da82-4646-4fde-aa57-4eb1acdb8bd3">
</p>

## Features

### Advanced Dithering Engine
*   **Error Diffusion**: Implements classic and modern diffusion kernels including **Floyd-Steinberg**, **Atkinson**, **Jarvis-Judice-Ninke (JJN)**, and **Stucki**.
*   **Ordered Dithering**: Offers **Bayer** matrix (8x8) and **Clustered Dot Halftone** for retro printing effects.
*   **Stochastic**: Random dithering with controllable noise thresholds.
*   **Variable Strength**: Blend the original image with the dithered output using the "Strength" slider for subtle texturing.

### Palette Management
*   **Automatic Quantization**: Dynamically generates the optimal palette from the source image.
*   **Retro Presets**: Built-in support for iconic systems:
    *   **Game Boy** (4-color greenscale)
    *   **PICO-8** (Fantasy console 16-color)
    *   **CGA** (Classic DOS palettes)
*   **Grayscale Control**: Custom bit-depth grayscale conversion.
*   **Color Count**: Reduce images down to as few as 2 colors or up to 256.

### Real-Time Post-Processing
*   **HSV Tuning**: Shift Hue, Saturation, and Value of the *final dithered result* without re-processing the geometry.
*   **LUT Support**: Apply look-up tables (color grading) to the output.
*   **Non-Destructive**: Switch algorithms or palettes instantly; the backend handles the heavy lifting.

## Installation

### Prerequisites
*   Python 3.8+
*   pip

### Quick Start

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/dovvnloading/Dither-Pro.git
    cd Dither-Pro
    ```

2.  **Set up Virtual Environment (Recommended)**
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```
    *Core dependencies: `PySide6`, `numpy`, `numba`, `Pillow`*

4.  **Launch**
    ```bash
    # Windows
    python Dither_app\Dither_app\Dither_app.py
    
    # macOS/Linux (adjust path as needed based on where you run it)
    python Dither_app/Dither_app/Dither_app.py
    ```

## Usage

The interface is divided into three workflow tabs:

### 1. Dithering Tab
This is your main workspace.
*   **Algorithm**: Select the math used to disperse pixels (e.g., *Atkinson* for high-contrast, *Floyd-Steinberg* for smooth gradients).
*   **Palette**: Choose "Auto" to keep the original colors (reduced), or pick a preset like "Game Boy" for a stylized look.
*   **Colors/Strength**: 
    *   *Colors*: Defines how many unique colors are allowed in the output (2-256).
    *   *Strength*: At 100%, pixels are strictly snapped to the palette. Lower values blend the original image back in.

### 2. Color Adjust Tab
Modify the output *after* dithering.
*   **Hue**: Rotate the color spectrum.
*   **Saturation**: Desaturate for a faded look or boost for vibrancy.
*   **Value**: Adjust brightness/darkness.
*   *Note: These operations are vectorized with NumPy for instant feedback.*

### 3. Grading / LUT Tab
Apply final stylistic filters.
*   Select from available Look-Up Tables (LUTs) to tint or wash the image.

## Technical Details

**Performance Optimization**
Dithering—specifically error diffusion—is inherently serial (pixel B depends on the error from pixel A). Python loops are typically too slow for this. Dither-Pro uses **Numba** to JIT-compile these algorithms into machine code, achieving performance comparable to C++.

**Architecture**
*   `Dither_app.py`: Main UI thread (PySide6).
*   `worker.py`: Dedicated `QThread` worker to prevent UI freezing during heavy processing.
*   `algorithms.py`: Pure mathematical implementations of dithering kernels, decoupled from the UI.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Built by <a href="https://github.com/dovvnloading">dovvnloading</a>
</p>
