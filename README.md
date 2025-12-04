# Dither-Pro

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=flat&logo=python&logoColor=white)
![PySide6](https://img.shields.io/badge/PySide6-Qt-41CD52?style=flat&logo=qt&logoColor=white)
![Numba](https://img.shields.io/badge/Numba-Accelerated-00A3E0?style=flat&logo=numba&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat)
![GitHub Stars](https://img.shields.io/github/stars/dovvnloading/Dither-Pro?style=flat&label=Stars&color=FCC624)
![GitHub Forks](https://img.shields.io/github/forks/dovvnloading/Dither-Pro?style=flat&label=Forks&color=2193FF)
![GitHub Issues](https://img.shields.io/github/issues/dovvnloading/Dither-Pro?style=flat&label=Issues&color=EB3B5A)
![GitHub Last Commit](https://img.shields.io/github/last-commit/dovvnloading/Dither-Pro?style=flat&label=Last%20Commit&color=5BBCDC)

## Advanced Dithering for Modern Digital Artistry

Dither-Pro is a cutting-edge, high-performance image dithering toolkit meticulously engineered for digital artists, game developers, and retro enthusiasts. Harnessing the power of Numba's JIT compilation, it delivers unparalleled real-time processing of advanced error-diffusion and ordered dithering algorithms, enabling precise visual transformations with a distinctive vintage flair.

Go beyond conventional image converters and gain granular control over your pixel art. Dither-Pro empowers you to craft stunning visual effects, manage intricate color palettes, and optimize your workflow with a fluid, responsive interface built with PySide6.

## Key Features

Dither-Pro provides a comprehensive set of features designed for both artistic control and technical excellence:

### Advanced Dithering Engine
Experience a robust suite of algorithms for nuanced pixel distribution and unique visual textures.
*   **Error Diffusion**: Implement classic algorithms like Floyd-Steinberg, Atkinson, Jarvis-Judice-Ninke (JJN), and Stucki for subtle, high-fidelity dithering.
*   **Ordered Dithering**: Utilize structured patterns such as Bayer Matrix (8x8) and Clustered Dot Halftone for distinct, geometric effects.
*   **Stochastic Dithering**: Introduce controlled randomness to generate organic textures and effectively minimize banding artifacts.
*   **Variable Strength**: Seamlessly blend between the original and dithered images to fine-tune the visual impact and intensity.

### Dynamic Palette Management
Take full command of your color choices with intelligent and flexible palette tools.
*   **Smart Quantization**: Automatically generate optimized color palettes directly from your source images, preserving visual fidelity.
*   **Integrated Presets**: Access a curated collection of iconic retro palettes, including Game Boy, PICO-8, and CGA, ready to apply.
*   **Extensive Customization**: Fine-tune output with grayscale precision and adjustable color counts, supporting a spectrum from 2 to 256 colors.

### 🖼️ Post-Processing Capabilities
Refine your dithered masterpieces with powerful, real-time adjustments.
*   **HSV Tuning**: Perform immediate, non-destructive adjustments to Hue, Saturation, and Value on the dithered output for instant visual feedback.
*   **LUT Support**: Apply professional Look-Up Tables (LUTs) to achieve sophisticated color grading, stylistic effects, and atmospheric moods.
*   **Optimized Performance**: Benefit from an instant feedback loop, powered by vectorized NumPy operations and Numba acceleration for blazing-fast processing.

## 📸 Screenshots

*(To be added: Include screenshots or GIFs showcasing the application's interface and various dithering effects here.)*

## 🚀 Installation

Getting Dither-Pro up and running is straightforward.

### Prerequisites
*   Python 3.8 or a newer version
*   `pip` (Python package installer)

### Setup Steps

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

## 💡 Usage

The Dither-Pro application is intuitively structured around three primary workflows for efficient image manipulation:

### 🌟 Dithering Workspace
This is your central hub for transforming images with pixel precision.
*   **Algorithm Selection**: Choose from a diverse range of advanced algorithms to control how pixels are distributed.
*   **Palette Management**: Efficiently manage color palettes using integrated presets or intelligent auto-generation.
*   **Output Refinement**: Precisely adjust the final dithered output with configurable color counts and dithering strength.

### ⚙️ Color Adjustment Panel
Refine your dithered images with real-time, non-destructive modifications.
*   **Hue**: Globally shift the color spectrum to achieve different moods.
*   **Saturation**: Intensify or desaturate colors for desired vibrancy or muted tones.
*   **Value**: Control the overall brightness and contrast characteristics of your image.

### 🎨 Grading Suite
Apply sophisticated stylistic filters to dramatically alter the mood and visual style of your final image.
*   **LUT Application**: Utilize Look-Up Tables (LUTs) to apply complex color grading and artistic effects, instantly transforming your image's aesthetic.

## 🏛️ Technical Architecture

Dither-Pro is engineered for optimal performance, responsiveness, and maintainability, ensuring a seamless user experience.

*   **UI Layer**: Constructed with `PySide6`, providing a robust, native cross-platform graphical user interface that feels fluid and responsive.
*   **Concurrency Management**: Utilizes `QThread` workers to efficiently offload computationally intensive processing tasks from the main UI thread, ensuring a consistently fluid and non-freezing interface.
*   **High-Performance Computation**: Critical dithering and image processing algorithms are meticulously implemented in `algorithms.py` and are highly optimized with `numba`. This achieves C-like performance speeds essential for real-time pixel manipulation of high-resolution assets.

## 📜 License

This project is licensed under the MIT License. Refer to the [LICENSE](LICENSE) file for comprehensive details.

## 👋 Contributing & Support

We welcome contributions from the community! If you have suggestions, bug reports, or want to contribute code, please feel free to:
*   Open an issue on the [GitHub Issue Tracker](https://github.com/dovvnloading/Dither-Pro/issues).
*   Fork the repository and submit a pull request.

Your feedback and contributions are greatly appreciated!
