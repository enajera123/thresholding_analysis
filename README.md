# Mammography Analysis Tool

![Mammography Analysis Tool](mamografia.png)

## Overview

The Mammography Analysis Tool is a Python application designed for processing mammography images. It provides a user-friendly graphical interface that allows users to load, process, and visualize mammography images. The application utilizes OpenCV for image manipulation and analysis, enabling users to identify and mark areas of concentration in the images.

## Features

- Load various image formats (PNG, JPG, BMP, TIFF, GIF).
- Process images to highlight areas of concentration.
- Display original and processed images side by side.
- User-friendly GUI built with Tkinter.

## Project Structure

```
mammography-analysis
├── src
│   ├── main.py                # Main entry point of the application
│   ├── utils
│   │   ├── __init__.py        # Initialization file for utils package
│   │   ├── image_processing.py  # Functions for image processing tasks
│   │   └── gui_helpers.py      # Helper functions for GUI components
│   └── assets
│       └── __init__.py        # Initialization file for assets package
├── tests
│   ├── __init__.py            # Initialization file for tests package
│   └── test_image_processing.py # Unit tests for image processing functions
├── sample_images
│   └── .gitkeep               # Keeps the sample_images directory in version control
├── requirements.txt            # Lists project dependencies
├── .gitignore                  # Specifies files to ignore in version control
└── README.md                   # Documentation for the project
```

## Installation

1. Clone the repository:
    ```
    git clone <repository-url>
    cd mammography-analysis
    ```

2. Install the required dependencies:
    ```
    pip install -r requirements.txt
    ```

## Usage

1. Run the application:
    ```
    python src/main.py
    ```

2. Use the "Load Image" button to select a mammography image from your file system.

3. Click on "Process Image" to analyze the loaded image and highlight areas of concentration.

4. The original and processed images will be displayed side by side in the application.

## Testing

To run the unit tests for the image processing functionalities, execute the following command:
```
pytest tests/test_image_processing.py
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.