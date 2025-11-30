# Dither-Pro

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PySide6](https://img.shields.io/badge/PySide6-Qt-41CD52?style=for-the-badge&logo=qt&logoColor=white)
![Numba](https://img.shields.io/badge/Numba-Accelerated-00A3E0?style=for-the-badge&logo=numba&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

A high-performance image dithering toolkit designed for digital artists and developers. Dither-Pro leverages Numba JIT compilation to deliver real-time processing of complex error-diffusion and ordered dithering algorithms.

## Overview

Dither-Pro provides a professional-grade interface for transforming images using retro aesthetic algorithms. Unlike standard converters, it offers granular control over palettes, dithering strength, and post-processing. The application is built with PySide6 for a responsive user experience and utilizes Numba to optimize computationally intensive dithering kernels, ensuring a fluid workflow even with high-resolution assets.

## Key Features

### Advanced Dithering Engine
*   **Error Diffusion**: Includes Floyd-Steinberg, Atkinson, Jarvis-Judice-Ninke (JJN), and Stucki algorithms.
*   **Ordered Dithering**: Supports Bayer Matrix (8x8) and Clustered Dot Halftone patterns.
*   **Stochastic Dithering**: Adds controlled randomness for organic textures.
*   **Variable Strength**: Allows blending between the original image and the dithered output.

### Dynamic Palette Management
*   **Smart Quantization**: Automatically generates optimized color palettes from source images.
*   **Presets**: Includes Game Boy, PICO-8, and CGA palettes.
*   **Customization**: Supports grayscale precision and variable color counts (2 to 256 colors).

### Post-Processing
*   **HSV Tuning**: Real-time Hue, Saturation, and Value adjustments on the dithered output.
*   **LUT Support**: Apply Look-Up Tables for professional color grading.
*   **Performance**: Instant feedback loop enabled by vectorized NumPy operations.

## Installation

### Prerequisites
*   Python 3.8 or higher
*   pip (Python package installer)

### Setup

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/dovvnloading/Dither-Pro.git
    cd Dither-Pro
    ```

2.  **Create a Virtual Environment**
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

4.  **Run the Application**
    ```bash
    python Dither_app/Dither_app/Dither_app.py
    ```

## Usage

The application is organized into three primary workflows:

### Dithering
The core workspace for image transformation.
*   Select algorithms to determine pixel distribution.
*   Manage palettes using presets or auto-generation.
*   Adjust color count and dithering strength.

### Color Adjustment
Refine the output with real-time modifications.
*   **Hue**: Shift the color spectrum.
*   **Saturation**: Adjust color intensity.
*   **Value**: Control brightness and contrast.

### Grading
Apply stylistic filters using Look-Up Tables (LUTs) to alter the mood and visual style of the final image.

## Technical Architecture

Dither-Pro is designed for performance and maintainability:

*   **UI Layer**: Built with `PySide6`, providing a native cross-platform interface.
*   **Concurrency**: Uses `QThread` workers to offload processing from the main UI thread, preventing interface freezing.
*   **Computation**: Critical algorithms are implemented in `algorithms.py` and optimized with `numba` to achieve C-like performance speeds for pixel manipulation.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
