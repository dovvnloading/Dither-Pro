<img width="1536" height="536" alt="dp_banner" src="https://github.com/user-attachments/assets/824825ec-663b-48d9-9c05-c0a1c7a53594" />


# Dither-Pro

---

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/Framework-PySide6-2492D1.svg" alt="PySide6">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
</p>

Dither-Pro is a high-performance, feature-rich dithering tool designed for artists and developers seeking granular control over image processing. Built with Python and a modern PySide6 interface, it provides a responsive and powerful workflow for transforming images into stylized, limited-color works of art. The backend is heavily optimized with Numba and NumPy for a fluid, real-time user experience.

<p align="center">
  <img width="1202" height="732" alt="Dither-Pro Application Screenshot" src="https://github.com/user-attachments/assets/46e8da82-4646-4fde-aa57-4eb1acdb8bd3">
</p>

## Features

*   **Extensive Algorithm Library**: Go beyond the basics with a wide selection of dithering algorithms, each providing a unique aesthetic:
    *   **Error-Diffusion**: Floyd-Steinberg, Atkinson, Jarvis, Judice, Ninke (JJN), Stucki
    *   **Ordered**: Bayer, Clustered Dot Halftone
    *   **Stochastic**: Random
*   **Complete Palette Control**: Precisely define the color space of your output image.
    *   **Automatic**: Generate an optimal palette directly from the source image.
    *   **Grayscale**: Convert the image to a specified number of grayscale tones.
    *   **Predefined**: Apply classic, retro palettes like Game Boy, PICO-8, and CGA.
*   **Real-Time Post-Processing**: Interactively adjust the dithered output without re-rendering.
    *   **HSV Color Adjustment**: Modify the Hue, Saturation, and Value of the final dithered palette in real-time.
    *   **Color Grading LUTs**: Apply post-process Look-Up Tables (LUTs) for effects like Sepia, Invert, and Cool Tone.
*   **Fine-Grained Adjustments**: Control the number of output colors (2-256) and the overall strength of the dithering effect.
*   **Modern & Responsive UI**: A clean, tabbed dark-theme interface built with PySide6 that is intuitive and scales correctly.
*   **High-Performance Backend**: Core algorithms are JIT-compiled with Numba or vectorized with NumPy to handle large images with minimal delay.

## Getting Started

Follow these instructions to get Dither-Pro running on your local machine.

### Prerequisites

*   Python 3.8 or newer
*   `pip` (Python package installer)

### Installation & Usage

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/dovvnloading/Dither-Pro.git
    cd Dither-Pro
    ```

2.  **Create a virtual environment (Recommended):**
    ```sh
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install the required dependencies:**
    A `requirements.txt` file is provided for easy installation.
    ```sh
    pip install -r requirements.txt
    ```
    The dependencies are: `PySide6`, `numpy`, `numba`, `Pillow`.

4.  **Run the application:**
    ```sh
    python Dither_app.py
    ```

## Development

For developers using Visual Studio, a `.sln` solution file is included in the repository for convenience. This allows you to open the project directly in Visual Studio with the Python workload installed.

The project is structured into four main files for a clean separation of concerns:
*   `Dither_app.py`: The main application entry point, containing all UI code (`QMainWindow`).
*   `worker.py`: Defines the `QObject` worker for multithreaded image processing.
*   `algorithms.py`: Contains all dithering algorithms and performance-critical functions. This module is UI-agnostic.
*   `utils.py`: Contains helper classes and functions, such as the LUT application logic.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.
