# Dither-Pro

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=flat&logo=python&logoColor=white)
![PySide6](https://img.shields.io/badge/PySide6-Qt-41CD52?style=flat&logo=qt&logoColor=white)
![Numba](https://img.shields.io/badge/Numba-Accelerated-00A3E0?style=flat&logo=numba&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat)
![GitHub Stars](https://img.shields.io/github/stars/dovvnloading/Dither-Pro?style=flat&label=Stars&color=FCC624)
![GitHub Forks](https://img.shields.io/github/forks/dovvnloading/Dither-Pro?style=flat&label=Forks&color=2193FF)
![GitHub Issues](https://img.shields.io/github/issues/dovvnloading/Dither-Pro?style=flat&label=Issues&color=EB3B5A)
![GitHub Last Commit](https://img.shields.io/github/last-commit/dovvnloading/Dither-Pro?style=flat&label=Last%20Commit&color=5BBCDC)

Dither-Pro is a high-performance image dithering toolkit engineered for digital artists and developers. Leveraging Numba's JIT compilation, it delivers real-time processing of advanced error-diffusion and ordered dithering algorithms, enabling precise visual transformations.

## Overview

Dither-Pro offers a professional-grade, intuitive interface for transforming images with a distinctive retro aesthetic. Going beyond conventional image converters, it provides unparalleled granular control over color palettes, dithering intensity, and comprehensive post-processing options. Built with PySide6, the application ensures a responsive user experience, while Numba optimizes computationally intensive dithering kernels, guaranteeing a fluid workflow even with high-resolution assets.

## Key Features

### Advanced Dithering Engine
*   **Error Diffusion**: Implement classic algorithms such as Floyd-Steinberg, Atkinson, Jarvis-Judice-Ninke (JJN), and Stucki for nuanced pixel distribution.
*   **Ordered Dithering**: Utilize structured patterns like Bayer Matrix (8x8) and Clustered Dot Halftone for distinctive visual effects.
*   **Stochastic Dithering**: Introduce controlled randomness to generate organic textures and reduce banding artifacts.
*   **Variable Strength**: Seamlessly blend between the original image and the dithered output to fine-tune visual impact.

### Dynamic Palette Management
*   **Smart Quantization**: Automatically generate optimized color palettes directly from source images, ensuring visual fidelity.
*   **Integrated Presets**: Access a curated selection of iconic palettes, including Game Boy, PICO-8, and CGA.
*   **Extensive Customization**: Fine-tune output with grayscale precision and adjustable color counts, supporting 2 to 256 colors.

### Post-Processing Capabilities
*   **HSV Tuning**: Perform real-time adjustments to Hue, Saturation, and Value on the dithered output for immediate visual feedback.
*   **LUT Support**: Apply professional Look-Up Tables (LUTs) to achieve sophisticated color grading and stylistic effects.
*   **Optimized Performance**: Benefit from an instant feedback loop, powered by vectorized NumPy operations and Numba acceleration.

## Installation

### Prerequisites
*   Python 3.8 or a newer version
*   `pip` (Python package installer)

### Setup

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/dovvnloading/Dither-Pro.git
    cd Dither-Pro
    ```

2.  **Create and Activate a Virtual Environment**
    ```bash
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate

    # For macOS/Linux
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

The application is structured around three primary workflows, designed for intuitive image manipulation:

### Dithering
This is the central workspace for transforming images.
*   Select from a variety of advanced algorithms to control pixel distribution.
*   Efficiently manage color palettes through integrated presets or intelligent auto-generation.
*   Precisely adjust the final output with configurable color counts and dithering strength.

### Color Adjustment
Refine your dithered output with real-time, non-destructive modifications.
*   **Hue**: Globally shift the color spectrum of your image.
*   **Saturation**: Intensify or desaturate colors for desired vibrance.
*   **Value**: Control the overall brightness and contrast characteristics.

### Grading
Apply sophisticated stylistic filters using Look-Up Tables (LUTs) to dramatically alter the mood and visual style of your final image.

## Technical Architecture

Dither-Pro is engineered for optimal performance, responsiveness, and maintainability:

*   **UI Layer**: Constructed with `PySide6`, providing a robust, native cross-platform graphical user interface.
*   **Concurrency Management**: Utilizes `QThread` workers to offload computationally intensive processing tasks from the main UI thread, ensuring a consistently fluid and non-freezing interface.
*   **High-Performance Computation**: Critical dithering and image processing algorithms are meticulously implemented in `algorithms.py` and are highly optimized with `numba`. This achieves C-like performance speeds essential for real-time pixel manipulation.

## License

This project is licensed under the MIT License. Refer to the [LICENSE](LICENSE) file for comprehensive details.
