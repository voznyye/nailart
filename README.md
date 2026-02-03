# 🎨 String Art Generator (Nail Art)

![String Art](https://img.shields.io/badge/Art-String%20Art-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

Professional string art (nail art) generator - create stunning thread and nail artworks from any image.

## 📋 Table of Contents

- [What is String Art?](#what-is-string-art)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Output Files](#output-files)
- [Step-by-Step Creation Guide](#step-by-step-creation-guide)
- [Code Architecture](#code-architecture)
- [FAQ](#faq)
- [Tips and Recommendations](#tips-and-recommendations)

## 🎯 What is String Art?

**String Art (Nail Art)** is an artistic technique of creating images by wrapping thread between nails fixed on a flat surface. Multiple thread crossings create light and shadow effects, forming a recognizable image.

This project automates the string art planning process:
- Analyzes any image
- Generates optimal thread routing
- Creates print-ready nail placement scheme (A3 format)
- Provides step-by-step creation instructions

## ✨ Features

### 🎨 A3 Format Optimization
- Perfect dimensions for **A3** sheet (297×420 mm)
- Working area: circle with diameter of **227 mm**
- Optimal nail count: **180** (balance of detail and convenience)
- Automatic physical size calculations

### 📍 Clear Nail Placement Scheme
- **Large readable numbering** for each nail
- Contrasting borders around numbers for easy reading
- Every 10th nail highlighted in red
- Red star on nail #0 (starting point)
- Guide lines every 30° for precise placement
- Physical dimensions (mm) on the scheme
- Export to **PDF** and **PNG** (300 DPI)

### 📊 Detailed CSV Instructions
Each step contains:
- Step number
- Start and end nail
- **Segment length** in millimeters
- Direction angle (0-360°)
- Completion progress (%)
- Section number (divided into 10 parts)
- **Total thread length** with safety margin (+20%)

### 🖼️ Realistic Result Simulation
- High-quality visualization of final appearance
- Realistic thread overlay with alpha-blending
- Paper base imitation
- Simulation export to PNG and PDF (A3)
- Red start marker (nail 0)

### 🧮 Smart Algorithm
- Automatic stop when reaching optimum
- Adaptive selection of next thread
- Image quality control at each step

## 🔧 Installation

### Requirements
- **Python 3.8+**
- pip (Python package manager)

### Installing Dependencies

```bash
# Clone or download the project
cd art

# Install dependencies
pip install -r requirements.txt
```

### Dependencies
- `Pillow` >= 9.0.0 - image processing
- `numpy` >= 1.23.0 - mathematical operations
- `matplotlib` >= 3.5.0 - scheme and PDF generation

## 🚀 Quick Start

### 1. Prepare an Image
- Any format: JPG, PNG, BMP, etc.
- Recommended: square image
- High contrast gives better results
- Size: 500×500 px minimum

### 2. Run the Generator

```bash
python string_art.py image.png
```

### 3. Wait for Completion

```
============================================================
STRING ART GENERATOR
============================================================

Configuration:
  Input image: image.png
  Target size: 800x800 pixels
  Number of nails: 180
  Circle radius: 400 pixels
  Number of steps: 3500
  ...

Step 1: Preprocessing image...
Step 2: Generating nail positions...
Step 3: Running string art algorithm...
  Generating up to 3500 thread segments...
  Step 0/3500 - max residual 0.8234
  ...
Step 4: Exporting outputs...

GENERATION COMPLETE!
```

### 4. Get the Files
- `nails_scheme.pdf` / `nails_scheme.png` - nail placement scheme
- `instructions.csv` - step-by-step instructions
- `drawing_simulation.png` / `drawing_simulation.pdf` - result simulation

## ⚙️ Configuration

All parameters can be adjusted at the beginning of `string_art.py`:

### Physical Dimensions (A3)
```python
A3_WIDTH_MM = 297          # A3 sheet width
A3_HEIGHT_MM = 420         # A3 sheet height
MARGIN_MM = 35             # Margin from edge
CIRCLE_RADIUS_MM = 113.5   # Circle radius with nails
```

### Nail Parameters
```python
NUM_NAILS = 180                   # Number of nails
NAIL_NUMBER_FONT_SIZE_BASE = 14   # Numbering font size
NAIL_NUMBER_OFFSET_MM = 8         # Number offset from nails
HIGHLIGHT_EVERY_NTH_NAIL = 10     # Highlight every Nth nail
```

### Algorithm
```python
TARGET_SIZE = 800          # Processing resolution (higher = better quality)
NUM_STEPS = 3500           # Maximum thread segments
THREAD_STRENGTH = 0.22     # Darkening intensity (0.0-1.0)
LINE_WEIGHT = 12           # Thread line thickness
AUTO_STOP = True           # Auto-stop at optimum
```

### Image Processing
```python
INVERT_IMAGE = True        # True: dark areas → more threads
```

### Export
```python
EXPORT_SCHEME_PDF = True   # Scheme to PDF
EXPORT_SCHEME_PNG = True   # Scheme to PNG
SCHEME_DPI = 300           # Print quality
EXPORT_FORMAT = "csv"      # Instructions format: "csv" or "txt"
```

## 📦 Output Files

### 1. `nails_scheme.pdf` / `nails_scheme.png`
**Nail placement scheme** for A3 printing:
- Circle with 180 numbered positions
- Red star on nail 0 (start)
- Every 10th nail highlighted in red
- Guide lines every 30°
- Physical dimensions (227 mm diameter)
- Ready to print on A3 (300 DPI)

**How to use:**
1. Print on A3 sheet
2. Fix the scheme on wooden board/plywood
3. Hammer nails at marked points
4. Remove paper scheme

### 2. `instructions.csv`
**Step-by-step instructions** in CSV format:

| Step | From_Nail | To_Nail | Length_mm | Angle_deg | Progress_% | Section |
|------|-----------|---------|-----------|-----------|------------|---------|
| 1    | 0         | 89      | 218.5     | 178.2     | 0.1        | 1       |
| 2    | 89        | 34      | 167.3     | 45.8      | 0.2        | 1       |
| ...  | ...       | ...     | ...       | ...       | ...        | ...     |

**Additional information:**
- Total number of steps
- Total thread length in meters
- Recommended thread length (with +20% safety margin)

**How to use:**
1. Open CSV in Excel / Google Sheets
2. Start from nail 0 (red star)
3. Follow instructions: from nail → to nail
4. Each section (1-10) is a convenient pause point

### 3. `drawing_simulation.png` / `drawing_simulation.pdf`
**Realistic simulation** of final result:
- Shows how the finished work will look
- All threads drawn with realistic overlay
- Red start marker
- A3 format for comparison

**How to use:**
- Evaluate result before starting work
- Compare with finished work for quality control
- Show expected result to client

## 🛠️ Step-by-Step Creation Guide

### Materials
- **Base:** wooden board/plywood/MDF (minimum A3 size)
- **Nails:** 180 pieces, length 15-25 mm
- **Thread:** black/dark thread (calculate from CSV, usually 30-50 meters)
- **Tools:** hammer, printer, paper glue (temporary)

### Process

#### Stage 1: Base Preparation
1. Take a board at least A3 size (297×420 mm)
2. Sand the surface
3. Optionally paint (white/light background)
4. Let dry

#### Stage 2: Nail Marking
1. Print `nails_scheme.pdf` on A3 sheet
2. Glue the scheme onto the board (temporary glue or tape)
3. **Important:** ensure the circle is exactly centered
4. Hammer nails at each point (180 pieces)
5. Nails should protrude 5-10 mm above surface
6. Carefully remove paper scheme

#### Stage 3: Thread Wrapping
1. Open `instructions.csv`
2. Find nail 0 (red star on board)
3. Tie thread end to nail 0
4. Follow instructions from CSV:
   - **Step 1:** From nail 0 → to nail X
   - **Step 2:** From nail X → to nail Y
   - And so on...
5. **Important:** don't pull thread too tight (medium tension)
6. Don't cut thread between steps - everything is done with one thread
7. Take breaks after each section (10 sections total)

#### Stage 4: Finishing
1. When all steps are completed, tie thread end at last nail
2. Cut excess
3. Optionally: apply clear varnish for protection

### ⏱️ Time Required
- Preparation: 30-60 minutes
- Nail placement: 1-2 hours
- Thread wrapping: 3-6 hours (depends on number of steps)
- **Total:** 5-9 hours of work

## 🏗️ Code Architecture

### Module Structure

```
string_art.py
├── CONFIGURATION          # All configurable parameters
├── NAIL GENERATION        # Nail position generation
├── IMAGE PREPROCESSING    # Image loading and processing
├── LINE DRAWING/SCORING   # Bresenham algorithm, line scoring
├── STRING ART ALGORITHM   # Main simulation algorithm
├── OUTPUT GENERATION      # Scheme, instructions, simulation export
└── MAIN PROGRAM           # Entry point
```

### Key Functions

#### `generate_nails(num_nails, radius, center_x, center_y)`
Generates evenly distributed nail positions on a circle.

#### `preprocess_image(image_path, target_size, invert)`
Loads, scales, and normalizes input image.

#### `simulate_string_art(img_array, nails, num_steps, ...)`
Main algorithm:
1. Starts from nail 0
2. At each step, selects the next nail that best covers dark areas
3. "Draws" the line, reducing brightness in the working image
4. Repeats until reaching optimum or step limit

#### `export_scheme_as_pdf/png(...)`
Creates nail placement scheme:
- Scales coordinates for A3
- Adds numbering with optimal size and offsets
- Draws guides and markers
- Exports in high resolution (300 DPI)

#### `export_instructions_csv(...)`
Creates detailed instructions:
- Calculates physical length of each segment
- Computes angles and progress
- Groups by sections
- Adds summary with total thread length

#### `render_drawing_simulation(...)`
Creates realistic simulation:
- Draws all threads with alpha-blending
- Simulates overlay and darkening
- Adds nails and markers
- Exports to PNG and PDF

## ❓ FAQ

### Can I use a different sheet size?
Yes! Change `A3_WIDTH_MM`, `A3_HEIGHT_MM` and `MARGIN_MM` parameters for other formats (A4, A2, etc.).

### How much thread do I need?
Check `instructions.csv` at the end of the file - it shows recommended thread length with safety margin.

### Can I change the number of nails?
Yes, change `NUM_NAILS`. Recommended range: 150-250.
- **Fewer nails** → easier to create, but less detail
- **More nails** → more detail, but harder to execute

### How to improve image quality?
1. Increase `TARGET_SIZE` (800-1200)
2. Increase `NUM_NAILS` (200-250)
3. Use high-contrast input image

### Program runs too long
1. Decrease `NUM_STEPS` (2500-3000)
2. Decrease `TARGET_SIZE` (600-800)
3. Ensure `AUTO_STOP = True`

### Result is too dark/light
- **Too dark:** decrease `THREAD_STRENGTH` (0.15-0.20)
- **Too light:** increase `THREAD_STRENGTH` (0.25-0.30)

### Can I use colored threads?
Algorithm is optimized for single-color thread. Multi-color string art requires algorithm modification.

## 💡 Tips and Recommendations

### Image Selection
- ✅ **Good:** portraits, faces, simple objects, high contrast
- ❌ **Bad:** complex details, low contrast, many small elements

### Thread Selection
- **Thickness:** 0.5-1 mm (thin sewing or embroidery thread)
- **Color:** black or dark thread on light background
- **Material:** cotton, polyester, acrylic

### Nail Selection
- **Length:** 15-25 mm
- **Thickness:** thin nails or decorative pins
- **Color:** matching base color or silver

### Execution Technique
- Pull thread **evenly** (not too tight, not too loose)
- Check nail numbers for accuracy
- Take breaks every 300-500 steps
- Periodically compare with simulation

### Parameter Optimization
For **quick result** (1-2 hours creation):
```python
NUM_NAILS = 150
NUM_STEPS = 2000
```

For **high quality** (4-6 hours creation):
```python
NUM_NAILS = 200
NUM_STEPS = 4000
TARGET_SIZE = 1000
```

For **very detailed** (6-10 hours creation):
```python
NUM_NAILS = 250
NUM_STEPS = 5000
TARGET_SIZE = 1200
```

## 📄 License

MIT License - free to use for personal and commercial projects.

## 🤝 Contributing

Suggestions and improvements are welcome! 

## 📞 Support

If you encounter problems:
1. Check the FAQ above
2. Ensure all dependencies are installed
3. Check input image format (JPG/PNG)
4. Try reducing parameters for testing

---

**Create amazing artworks!** 🎨✨
