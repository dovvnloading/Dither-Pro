# Dither-Pro

<div align="center">

  ![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
  ![PySide6](https://img.shields.io/badge/PySide6-Qt-41CD52?style=for-the-badge&logo=qt&logoColor=white)
  ![Numba](https://img.shields.io/badge/Numba-Accelerated-00A3E0?style=for-the-badge&logo=numba&logoColor=white)
  ![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

  <br>
  **Transform your images into stunning retro-aesthetic masterpieces with unparalleled speed and precision.**
  <br><br>
  [Features](#features) • [Installation](#installation) • [Usage](#usage) • [Algorithms](#algorithms) • [Contributing](#contributing)

</div>

---

## ✨ Why Dither-Pro?

**Dither-Pro** is more than just an image converter; it's a powerful, high-performance toolkit designed for digital artists and developers seeking to explore the captivating world of retro aesthetics. Leveraging **Numba JIT compilation**, Dither-Pro delivers **near real-time processing** of complex error-diffusion and ordered dithering algorithms, even for high-resolution images.

Built with a sleek **PySide6** interface, it combines the flexibility of command-line tools with the intuitive control of professional graphic design software. Experience granular control over custom palettes, dithering strength, and advanced post-processing — all within a fluid and responsive workflow.

## 🚀 Get Started

Quickly dive into the world of dithering.

### Interface

<p align="center">
  <img width="100%" alt="Dither-Pro Application Screenshot" src="https://github.com/user-attachments/assets/46e8da82-4646-4fde-aa57-4eb1acdb8bd3">
</p>

<!-- Optional: Add a GIF/Video Demo here to showcase real-time features -->
<!-- <p align="center">
  <img width="80%" alt="Dither-Pro Live Demo" src="link-to-your-gif-or-video-thumbnail.gif">
  <br>
  <em>Experience real-time dithering and palette shifts in action!</em>
</p> -->

## Key Features

### Advanced Dithering Engine
*   **Error Diffusion**: Implements classic and cutting-edge diffusion kernels for nuanced results:
    *   **Floyd-Steinberg**: Balances contrast and detail with smooth gradients.
    *   **Atkinson**: Creates a distinctive, high-contrast speckled look.
    *   **Jarvis-Judice-Ninke (JJN)**: Offers a smoother, more distributed error for less patterned output.
    *   **Stucki**: Provides sharper detail and cleaner edges than JJN.
*   **Ordered Dithering**: Achieve authentic retro printing and display effects:
    *   **Bayer Matrix (8x8)**: Ideal for creating structured patterns and halftone approximations.
    *   **Clustered Dot Halftone**: Mimics traditional print processes with varying dot sizes.
*   **Stochastic Dithering**: Introduces controlled randomness for organic textures and noise reduction.
*   **Variable Strength Control**: Precisely blend the original image with the dithered output, from subtle texturing to full pixel art conversion.

### Dynamic Palette Management
*   **Automatic Smart Quantization**: Intelligently generates optimized color palettes directly from your source image.
*   **Iconic Retro Presets**: Instantly transform your images with built-in support for legendary systems:
    *   **Game Boy**: Embrace the classic 4-color greenscale aesthetic.
    *   **PICO-8**: Tap into the vibrant 16-color fantasy console palette.
    *   **CGA**: Recreate the nostalgic look of classic DOS graphics.
*   **Grayscale Precision**: Fine-tune custom bit-depth grayscale conversions.
*   **Flexible Color Count**: Condense images to as few as 2 colors or expand up to 256 for diverse artistic expression.

### Real-Time Post-Processing & Grading
*   **Non-Destructive HSV Tuning**: Effortlessly adjust Hue, Saturation, and Value of your *final dithered result* without re-processing the underlying image data.
*   **Integrated LUT Support**: Apply professional Look-Up Tables (color grading filters) to instantly alter the mood and style of your output.
*   **Instant Feedback**: Switch algorithms, palettes, and post-processing effects on-the-fly with zero lag, thanks to a highly optimized backend.

## Installation

### Prerequisites
*   Python 3.8+
*   `pip` (Python package installer)

### Quick Start Guide

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/dovvnloading/Dither-Pro.git
    cd Dither-Pro
    ```

2.  **Set up Virtual Environment (Highly Recommended)**
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Core Dependencies**
    ```bash
    pip install -r requirements.txt
    ```
    *Key dependencies include: `PySide6` (for UI), `numpy` (for array operations), `numba` (for JIT compilation), `Pillow` (for image loading/saving).*

4.  **Launch the Application**
    ```bash
    # From the Dither-Pro root directory:
    python Dither_app/Dither_app/Dither_app.py
    ```

## Usage Guide

The Dither-Pro interface is intuitively structured across three powerful workflow tabs:

### 1. Dithering Tab
Your primary workspace for fundamental transformations.
*   **Algorithm Selection**: Choose the mathematical method for pixel distribution (e.g., *Atkinson* for high-contrast, *Floyd-Steinberg* for smooth gradients).
*   **Palette Control**: Opt for "Auto" to derive a palette from your source, or select an iconic preset like "Game Boy" for a stylized vintage look.
*   **Colors & Strength**:
    *   **Colors**: Define the maximum number of unique colors in your final output (from 2 to 256).
    *   **Strength**: At 100%, pixels strictly adhere to the selected palette. Lower values intelligently blend the original image back in for subtle texturing.

### 2. Color Adjust Tab
Refine your dithered masterpiece with real-time color modifications.
*   **Hue Rotation**: Effortlessly shift the entire color spectrum of your image.
*   **Saturation Control**: Desaturate for a faded, aged aesthetic or boost for vibrant, punchy colors.
*   **Value Adjustment**: Precisely control the overall brightness and darkness.
*   *Note: All color adjustments are performed using highly optimized NumPy vectorized operations, ensuring instant visual feedback.*

### 3. Grading / LUT Tab
Apply final stylistic filters and professional color grades.
*   **Look-Up Table (LUT) Application**: Select from a range of available LUTs to instantly tint, wash, or stylize your dithered image, achieving complex color grading with a single click.

## Technical Deep Dive

### Performance Optimization with Numba
Dithering algorithms, especially error diffusion, are inherently sequential, meaning each pixel's processing depends on its neighbors' errors. This characteristic typically makes them slow in pure Python. Dither-Pro overcomes this by employing **Numba**, a high-performance Python compiler that Just-In-Time (JIT) compiles critical algorithm functions into optimized machine code. This results in processing speeds comparable to compiled languages like C++.

### Modular Architecture
*   `Dither_app/Dither_app.py`: Contains the main application entry point and orchestrates the user interface (PySide6).
*   `Dither_app/worker.py`: Implements a dedicated `QThread` worker to offload heavy image processing tasks from the main UI thread, ensuring a consistently responsive user experience.
*   `Dither_app/algorithms.py`: Houses the pure, optimized mathematical implementations of all dithering kernels, maintaining a clean separation between computation and presentation.

## Contributing

We welcome contributions from the community! If you're interested in improving Dither-Pro, please check out our [contribution guidelines](CONTRIBUTING.md) (coming soon) or open an issue to discuss new features or bug fixes.

## License

This project is proudly licensed under the MIT License - see the [LICENSE](LICENSE) file for full details.

---

<p align="center">
  Built with passion by <a href="https://github.com/dovvnloading">dovvnloading</a>
</p>
