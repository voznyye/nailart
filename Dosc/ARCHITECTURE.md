# Technical Architecture of String Art Generator

## Algorithm Overview

String Art Generator uses a **greedy algorithm** for generating optimal thread routing.

### Basic Principle

1. **Initialization**: Starts from nail 0 (top point of circle)
2. **Iteration**: At each step:
   - Evaluates all possible lines from current nail to others
   - Selects line with maximum "score" (covers darkest areas)
   - "Draws" this line, reducing pixel brightness
   - Moves to selected nail
3. **Stop**: Algorithm stops when:
   - Step limit reached (`NUM_STEPS`)
   - Residual image becomes sufficiently light (`RESIDUAL_THRESHOLD`)
   - No improvements for `MAX_NO_IMPROVE` steps

## Code Structure

```
string_art.py
│
├─ CONFIGURATION (lines 20-68)
│  └─ All configurable parameters
│
├─ NAIL GENERATION (lines 70-95)
│  └─ generate_nails(): Nail position generation
│
├─ IMAGE PREPROCESSING (lines 97-151)
│  ├─ preprocess_image(): Loading and processing
│  └─ enhance_contrast(): Contrast enhancement
│
├─ LINE DRAWING AND SCORING (lines 153-261)
│  ├─ get_line_pixels(): Bresenham's algorithm
│  ├─ score_line(): Line quality evaluation
│  └─ draw_line(): Line drawing
│
├─ STRING ART ALGORITHM (lines 263-350)
│  └─ simulate_string_art(): Main algorithm
│
├─ OUTPUT GENERATION (lines 352-640)
│  ├─ export_scheme_as_png(): Scheme to PNG
│  ├─ export_scheme_as_pdf(): Scheme to PDF
│  ├─ export_instructions_csv(): CSV instructions
│  ├─ export_instructions_txt(): TXT instructions
│  └─ render_drawing_simulation(): Result simulation
│
└─ MAIN PROGRAM (lines 642-733)
   └─ main(): Entry point
```

## Key Components

### 1. Nail Position Generation

```python
def generate_nails(num_nails, radius, center_x, center_y)
```

- Distributes nails evenly on circle
- Starts from top point (90°) for intuitive nail 0
- Returns array of coordinates (x, y)

**Mathematics:**
```
angle = π/2 + (2π × i / num_nails)
x = center_x + radius × cos(angle)
y = center_y + radius × sin(angle)
```

### 2. Image Preprocessing

```python
def preprocess_image(image_path, target_size, invert)
```

**Steps:**
1. Load image
2. Convert to grayscale
3. Crop to square (centered)
4. Resize to `TARGET_SIZE`
5. Normalize to range [0.0, 1.0]
6. Invert (optional): dark areas → high values
7. Enhance contrast

**Inversion:**
- `invert=True`: dark areas get more threads
- Formula: `img_array = 1.0 - img_array`

### 3. Bresenham's Algorithm

```python
def get_line_pixels(x0, y0, x1, y1)
```

Classic algorithm for getting all pixels along a line:
- Efficient (no floating-point operations)
- Used for scoring and drawing lines

### 4. Line Scoring

```python
def score_line(img_array, x0, y0, x1, y1, line_weight)
```

**Principle:**
- Sums brightness of all pixels along line
- High score = line covers many dark areas
- Formula: `score = Σ pixel_values`

### 5. Line Drawing

```python
def draw_line(img_array, x0, y0, x1, y1, strength, line_weight)
```

**Principle:**
- Reduces brightness of pixels along line
- Simulates thread overlay
- Formula: `pixel = max(0, pixel - strength)`
- Clamp to [0.0, 1.0] to prevent negative values

### 6. Main Simulation Algorithm

```python
def simulate_string_art(img_array, nails, num_steps, thread_strength, line_weight)
```

**Pseudocode:**
```
current_nail = 0
instructions = []
working_image = copy(target_image)

for step in 1..NUM_STEPS:
    best_score = -1
    best_nail = -1
    
    for each nail:
        if nail == current_nail: continue
        
        score = score_line(working_image, current_nail, nail)
        
        if score > best_score:
            best_score = score
            best_nail = nail
    
    if no improvement:
        break
    
    draw_line(working_image, current_nail, best_nail)
    instructions.append((current_nail, best_nail))
    current_nail = best_nail
    
    if working_image is mostly blank:
        break

return instructions
```

**Optimizations:**
- **AUTO_STOP**: Automatic stop when reaching optimum
- **RESIDUAL_THRESHOLD**: Threshold for determining "empty" image
- **MAX_NO_IMPROVE**: Stop when no improvements

### 7. Nail Scheme Export

```python
def export_scheme_as_pdf/png(...)
```

**Features:**
- Scaling from pixel space to physical (mm)
- Adaptive font size based on nail count
- Highlighting every Nth nail (red color)
- Guide lines every 30° for precise placement
- White borders around numbers for readability
- Red star on nail 0 (starting point)
- Physical dimensions on scheme

**Scaling:**
```
scale = drawable_size_px / TARGET_SIZE
x_plot = x * scale + offset_x
y_plot = y * scale + offset_y
```

### 8. CSV Instructions Export

```python
def export_instructions_csv(instructions, nails, filename)
```

**Calculations:**
- **Segment length**: Euclidean distance in mm
  ```
  length_px = √((x1-x0)² + (y1-y0)²)
  length_mm = length_px × px_to_mm_scale
  ```
- **Angle**: atan2 for determining direction (0-360°)
- **Progress**: (step / total_steps) × 100
- **Section**: Division into 10 parts for convenience
- **Total length**: Sum of all segments + 20% safety margin

### 9. Final Result Simulation

```python
def render_drawing_simulation(instructions, nails, canvas_size, filename, dpi)
```

**Technique:**
- RGBA canvas with paper color
- Alpha-blending for realistic thread overlay
- Low alpha (15/255) × many layers = realistic darkening
- Periodic compositing (every 500 lines)
- Nails drawn on top of threads
- Red start marker (nail 0)

**Alpha Compositing:**
```
result = (fg × alpha) + (bg × (1 - alpha))
```

## Parameters and Their Impact

### NUM_NAILS (number of nails)
- **Impact on detail**: More nails → more possible directions → higher detail
- **Impact on complexity**: O(n²) at each iteration (n = NUM_NAILS)
- **Recommendations**: 150-250 for balance

### NUM_STEPS (number of steps)
- **Impact on completeness**: More steps → more complete coverage
- **Impact on time**: Linear increase in execution time
- **Recommendations**: 2000-5000 depending on image

### TARGET_SIZE (processing size)
- **Impact on quality**: Larger → higher accuracy of line evaluation
- **Impact on memory**: Quadratic (TARGET_SIZE²)
- **Impact on speed**: Quadratic increase
- **Recommendations**: 600-1200

### THREAD_STRENGTH (thread strength)
- **Impact on contrast**: Higher → darker result
- **Range**: 0.15-0.30 optimal
- **Adjustment**: Depends on input image contrast

### LINE_WEIGHT (line thickness)
- **Impact on coverage**: Affects score evaluation
- **Adjustment**: 10-15 for most cases

## Algorithm Complexity

### Time Complexity
- **Preprocessing**: O(TARGET_SIZE²)
- **Nail generation**: O(NUM_NAILS)
- **Main loop**: O(NUM_STEPS × NUM_NAILS × line_length)
  - NUM_STEPS iterations
  - NUM_NAILS evaluations at each iteration
  - line_length pixels in each line
- **Total**: O(NUM_STEPS × NUM_NAILS × TARGET_SIZE)

### Space Complexity
- **Working image**: O(TARGET_SIZE²)
- **Nail array**: O(NUM_NAILS)
- **Instructions**: O(NUM_STEPS)
- **Total**: O(TARGET_SIZE²)

## Limitations and Trade-offs

### Greedy Algorithm
- **Advantages**: Fast, simple, gives good results
- **Disadvantages**: Doesn't guarantee global optimum
- **Alternatives**: Genetic algorithms, simulated annealing (slower)

### Single-color Thread
- Current version optimized for single thread color
- Multi-color string art requires separate layers for each color

### Circular Shape
- Nails placed only on circle circumference
- Other shapes (square, heart) require modification

## Possible Improvements

### Algorithmic
1. **Local optimization**: Review last N steps
2. **Beam search**: Consider several best options
3. **Adaptive parameters**: Dynamic THREAD_STRENGTH changes

### Functional
1. **Multi-color string art**: Separate layers for each color
2. **Other shapes**: Square, rectangle, heart
3. **Variable nail density**: More nails in detailed areas

### Performance
1. **Parallelization**: Parallel line evaluation
2. **Caching**: Cache line coordinates
3. **GPU acceleration**: Use CUDA for line evaluation

## Dependencies

### NumPy
- Vector operations on images
- Mathematical functions (cos, sin, arctan2)
- Coordinate arrays

### Pillow (PIL)
- Image loading
- Format conversion
- Canvas drawing (alpha-blending)

### Matplotlib
- PDF/PNG scheme generation
- Plots and visualization
- High-resolution export

## Testing

### Recommended Test Images
1. **High contrast**: Logos, silhouettes
2. **Medium contrast**: Portraits
3. **Low contrast**: Landscapes

### Control Parameters
- Input data validation check
- Edge case tests (NUM_NAILS=10, NUM_STEPS=100)
- Performance test (TARGET_SIZE=2000)

## License

MIT License - free to use for personal and commercial projects.

## Contact

For technical implementation questions, refer to source code and comments.
