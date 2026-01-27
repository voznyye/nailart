#!/usr/bin/env python3
"""
STRING ART (NAIL ART) GENERATOR

Professional string art generator optimized for A3 paper format.
Generates string art instructions from an input image.

Creates:
1. A printable scheme (PDF/PNG) with nail positions and numbers (A3, 300 DPI)
2. Step-by-step CSV instructions with length, angle, and progress
3. Realistic simulation of final result

Author: String Art Generator
Version: 2.0
License: MIT
"""

import sys
from typing import List, Tuple
import numpy as np
from numpy.typing import NDArray
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_pdf import PdfPages
import csv


# ============================================================================
# CONFIGURATION - All adjustable parameters optimized for A3 paper
# ============================================================================

# A3 Physical dimensions
A3_WIDTH_MM = 297  # A3 width in millimeters
A3_HEIGHT_MM = 420  # A3 height in millimeters
A3_WIDTH_IN = 11.69  # A3 width in inches
A3_HEIGHT_IN = 16.54  # A3 height in inches

# Working area configuration (with margins)
MARGIN_MM = 35  # Margin from paper edge in millimeters
WORKING_AREA_MM = min(A3_WIDTH_MM, A3_HEIGHT_MM) - 2 * MARGIN_MM  # 227mm square
CIRCLE_RADIUS_MM = WORKING_AREA_MM / 2  # 113.5mm radius

# Image preprocessing
TARGET_SIZE = 800  # Target image will be resized to this dimension (higher = better quality)
INVERT_IMAGE = True  # True: dark areas receive more thread

# Nail configuration (optimized for A3)
NUM_NAILS = 180  # Number of nails evenly distributed on the circle (optimal balance)
CIRCLE_RADIUS = int(TARGET_SIZE * CIRCLE_RADIUS_MM / WORKING_AREA_MM)  # Scaled radius in pixels

# String art algorithm
NUM_STEPS = 3500  # Maximum number of thread segments (optimized for A3)
THREAD_STRENGTH = 0.22  # How much brightness is reduced per line (0.0 to 1.0)
LINE_WEIGHT = 12  # Thickness of the thread line in scoring/drawing

# Auto-stopping behavior
AUTO_STOP = True  # If True, stop early when residual image is sufficiently blank
RESIDUAL_THRESHOLD = 0.02  # When max pixel value in working image falls below this, stop
MAX_NO_IMPROVE = 300  # Stop if best_score is zero for this many consecutive steps

# Output configuration
EXPORT_SCHEME_PDF = True  # Export scheme as PDF
EXPORT_SCHEME_PNG = True  # Export scheme as PNG
SCHEME_DPI = 300  # DPI for printable output
EXPORT_FORMAT = "csv"  # "csv" or "txt" for instructions

# Nail numbering appearance
NAIL_NUMBER_FONT_SIZE_BASE = 8  # Base font size for nail numbers
NAIL_NUMBER_OFFSET_MM = 8  # Distance of numbers from nails in mm
HIGHLIGHT_EVERY_NTH_NAIL = 10  # Highlight every Nth nail with bold marker

# File names
OUTPUT_SCHEME_PDF = "nails_scheme.pdf"
OUTPUT_SCHEME_PNG = "nails_scheme.png"
OUTPUT_INSTRUCTIONS = "instructions.csv"  # or .txt depending on EXPORT_FORMAT


# ============================================================================
# NAIL GENERATION
# ============================================================================

def generate_nails(num_nails: int, radius: float, center_x: float, center_y: float) -> NDArray[np.float64]:
    """
    Generate nail positions evenly distributed on a circle.
    
    Args:
        num_nails: Number of nails to generate
        radius: Circle radius in pixels
        center_x: X coordinate of circle center
        center_y: Y coordinate of circle center
    
    Returns:
        numpy array of shape (num_nails, 2) with (x, y) coordinates
    """
    nails = np.zeros((num_nails, 2))
    
    # Start from top (90 degrees) for intuitive nail 0 position
    for i in range(num_nails):
        angle = (np.pi / 2) + (2 * np.pi * i / num_nails)
        nails[i, 0] = center_x + radius * np.cos(angle)
        nails[i, 1] = center_y + radius * np.sin(angle)
    
    return nails


# ============================================================================
# IMAGE PREPROCESSING
# ============================================================================

def preprocess_image(image_path: str, target_size: int, invert: bool) -> NDArray[np.float32]:
    """
    Load and preprocess the input image.
    
    Args:
        image_path: Path to input image file
        target_size: Target size for square output
        invert: Whether to invert the image (dark areas get more thread)
    
    Returns:
        Preprocessed image as numpy float array (0.0 to 1.0)
    """
    # Load image
    img = Image.open(image_path)
    
    # Convert to grayscale
    img = img.convert('L')
    
    # Make it square by cropping to center
    width, height = img.size
    size = min(width, height)
    left = (width - size) // 2
    top = (height - size) // 2
    img = img.crop((left, top, left + size, top + size))
    
    # Resize to target size
    img = img.resize((target_size, target_size), Image.Resampling.LANCZOS)
    
    # Convert to numpy array (0-255)
    img_array = np.array(img, dtype=np.float32)
    
    # Normalize to 0.0 - 1.0
    img_array = img_array / 255.0
    
    # Invert if needed (dark areas should have high values for more thread)
    if invert:
        img_array = 1.0 - img_array
    
    # Enhance contrast using histogram equalization
    img_array = enhance_contrast(img_array)
    
    return img_array


def enhance_contrast(img_array: NDArray[np.float32]) -> NDArray[np.float32]:
    """
    Enhance contrast of the image using simple normalization.
    
    Args:
        img_array: Input image as numpy array (0.0 to 1.0)
    
    Returns:
        Contrast-enhanced image
    """
    # Normalize to full range
    min_val = np.min(img_array)
    max_val = np.max(img_array)
    
    if max_val > min_val:
        img_array = (img_array - min_val) / (max_val - min_val)
    
    return img_array


# ============================================================================
# LINE DRAWING AND SCORING
# ============================================================================

def get_line_pixels(x0: float, y0: float, x1: float, y1: float) -> Tuple[NDArray[np.int32], NDArray[np.int32]]:
    """
    Get pixel coordinates along a line using Bresenham's algorithm.
    
    Args:
        x0, y0: Starting point
        x1, y1: Ending point
    
    Returns:
        Two arrays: x_coords, y_coords of pixels along the line
    """
    x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
    
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    
    x_coords = []
    y_coords = []
    
    x, y = x0, y0
    
    while True:
        x_coords.append(x)
        y_coords.append(y)
        
        if x == x1 and y == y1:
            break
        
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy
    
    return np.array(x_coords, dtype=np.int32), np.array(y_coords, dtype=np.int32)


def score_line(img_array: NDArray[np.float32], x0: float, y0: float, 
               x1: float, y1: float, line_weight: int) -> float:
    """
    Score a potential line by summing pixel intensities along it.
    Higher score means the line covers darker areas (higher values after inversion).
    
    Args:
        img_array: Current image state
        x0, y0: Starting nail coordinates
        x1, y1: Ending nail coordinates
        line_weight: Thickness of line for scoring
    
    Returns:
        Score value (higher is better)
    """
    height, width = img_array.shape
    
    # Get base line pixels
    x_coords, y_coords = get_line_pixels(x0, y0, x1, y1)
    
    # Filter out-of-bounds pixels
    valid = (x_coords >= 0) & (x_coords < width) & (y_coords >= 0) & (y_coords < height)
    x_coords = x_coords[valid]
    y_coords = y_coords[valid]
    
    if len(x_coords) == 0:
        return 0.0
    
    # Sum intensities along the line
    score = np.sum(img_array[y_coords, x_coords])
    
    return float(score)


def draw_line(img_array: NDArray[np.float32], x0: float, y0: float, 
              x1: float, y1: float, strength: float, line_weight: int) -> None:
    """
    Draw a line on the image by reducing pixel intensities.
    
    Args:
        img_array: Image array to modify (in-place)
        x0, y0: Starting nail coordinates
        x1, y1: Ending nail coordinates
        strength: How much to reduce brightness (0.0 to 1.0)
        line_weight: Thickness of line
    """
    height, width = img_array.shape
    
    # Get line pixels
    x_coords, y_coords = get_line_pixels(x0, y0, x1, y1)
    
    # Filter out-of-bounds pixels
    valid = (x_coords >= 0) & (x_coords < width) & (y_coords >= 0) & (y_coords < height)
    x_coords = x_coords[valid]
    y_coords = y_coords[valid]
    
    if len(x_coords) == 0:
        return
    
    # Reduce brightness along the line
    img_array[y_coords, x_coords] -= strength
    
    # Clamp to valid range
    img_array[y_coords, x_coords] = np.maximum(img_array[y_coords, x_coords], 0.0)


# ============================================================================
# STRING ART ALGORITHM
# ============================================================================

def simulate_string_art(img_array: NDArray[np.float32], nails: NDArray[np.float64], 
                       num_steps: int, thread_strength: float, 
                       line_weight: int) -> List[Tuple[int, int]]:
    """
    Simulate the string art generation process with intelligent auto-stopping.
    
    The function supports AUTO_STOP behavior: if AUTO_STOP is True, the
    algorithm will stop early when the residual image becomes sufficiently
    blank (no high-value pixels remain) or when there is no improvement for
    many consecutive steps.
    
    Args:
        img_array: Preprocessed target image
        nails: Array of nail coordinates
        num_steps: Number of thread segments to generate
        thread_strength: Brightness reduction per line
        line_weight: Line thickness
    
    Returns:
        List of tuples (from_nail, to_nail) representing the thread path
    """
    # Create working copy of the image
    working_img = img_array.copy()
    
    # Initialize
    num_nails = len(nails)
    current_nail = 0
    instructions: List[Tuple[int, int]] = []
    
    print(f"Generating up to {num_steps} thread segments (AUTO_STOP={AUTO_STOP})...")
    no_improve = 0
    
    for step in range(num_steps):
        if step % 100 == 0:
            print(f"  Step {step}/{num_steps} - max residual {working_img.max():.4f}")

        # Auto-stop if residual image is mostly blank
        if AUTO_STOP and working_img.max() <= RESIDUAL_THRESHOLD:
            print(f"  Residual below threshold ({working_img.max():.4f} <= {RESIDUAL_THRESHOLD}); stopping at step {step}.")
            break

        best_score = -1.0
        best_nail = -1

        # Try all other nails
        for next_nail in range(num_nails):
            if next_nail == current_nail:
                continue

            # Get coordinates
            x0, y0 = nails[current_nail]
            x1, y1 = nails[next_nail]

            # Score this line
            score = score_line(working_img, x0, y0, x1, y1, line_weight)

            if score > best_score:
                best_score = score
                best_nail = next_nail

        # If best score is non-positive, count as no improvement
        if best_score <= 0 or best_nail == -1:
            no_improve += 1
            if no_improve >= MAX_NO_IMPROVE:
                print(f"  No improvement for {no_improve} consecutive steps; stopping at step {step}.")
                break
            if best_nail == -1:
                print(f"  Warning: No valid nail found at step {step}")
                break
        else:
            no_improve = 0

        # Apply the best line
        x0, y0 = nails[current_nail]
        x1, y1 = nails[best_nail]
        draw_line(working_img, x0, y0, x1, y1, thread_strength, line_weight)

        instructions.append((current_nail, best_nail))
        current_nail = best_nail

    
    print(f"String art generation complete! Generated {len(instructions)} segments.")
    return instructions


# ============================================================================
# OUTPUT GENERATION
# ============================================================================

def export_scheme_as_png(nails, radius, center_x, center_y, filename, dpi):
    """
    Export the nail scheme as a PNG image sized for A3 paper with enhanced readability.
    
    Args:
        nails: Array of nail coordinates
        radius: Circle radius
        center_x, center_y: Circle center
        filename: Output filename
        dpi: Resolution for output
    """
    # Create figure for A3 paper
    fig, ax = plt.subplots(figsize=(A3_WIDTH_IN, A3_HEIGHT_IN), dpi=dpi)

    # Determine drawing area (leave margins)
    margin_in = MARGIN_MM / 25.4  # Convert mm to inches
    drawable_w = A3_WIDTH_IN - 2 * margin_in
    drawable_h = A3_HEIGHT_IN - 2 * margin_in
    drawable_size_in = min(drawable_w, drawable_h)
    drawable_size_px = drawable_size_in * dpi
    
    # Compute scale factor from TARGET_SIZE to drawable_size_px
    scale = drawable_size_px / TARGET_SIZE
    
    # Apply scale and translation to nails for plotting
    nails_plot = nails.copy()
    nails_plot[:, 0] = nails[:, 0] * scale + margin_in * dpi + (drawable_w * dpi - drawable_size_px) / 2
    nails_plot[:, 1] = nails[:, 1] * scale + margin_in * dpi + (drawable_h * dpi - drawable_size_px) / 2
    
    # Adjust center and radius for plotting
    center_x_plot = center_x * scale + margin_in * dpi + (drawable_w * dpi - drawable_size_px) / 2
    center_y_plot = center_y * scale + margin_in * dpi + (drawable_h * dpi - drawable_size_px) / 2
    radius_plot = radius * scale

    # Draw reference grid for easier nail placement
    for angle in range(0, 360, 30):
        angle_rad = np.radians(angle)
        x_inner = center_x_plot + radius_plot * 0.95 * np.cos(angle_rad)
        y_inner = center_y_plot + radius_plot * 0.95 * np.sin(angle_rad)
        x_outer = center_x_plot + radius_plot * 1.05 * np.cos(angle_rad)
        y_outer = center_y_plot + radius_plot * 1.05 * np.sin(angle_rad)
        ax.plot([x_inner, x_outer], [y_inner, y_outer], 'gray', linewidth=0.5, alpha=0.3)

    # Draw circle
    circle = patches.Circle((center_x_plot, center_y_plot), radius_plot, fill=False, 
                           edgecolor='black', linewidth=2.5)
    ax.add_patch(circle)

    # Draw start marker (nail 0 at top)
    start_angle = np.radians(90)  # Top position
    marker_size = 15
    x_start = center_x_plot + radius_plot * np.cos(start_angle)
    y_start = center_y_plot + radius_plot * np.sin(start_angle)
    ax.plot(x_start, y_start, 'r*', markersize=marker_size, markeredgecolor='black', markeredgewidth=1.5)

    # Calculate optimal font size and offset
    font_size = max(NAIL_NUMBER_FONT_SIZE_BASE, int(NAIL_NUMBER_FONT_SIZE_BASE * (200 / len(nails))))
    offset_distance_px = (NAIL_NUMBER_OFFSET_MM / 25.4) * dpi

    # Draw nails with improved numbering
    for i, (x, y) in enumerate(nails_plot):
        # Determine if this nail should be highlighted
        is_milestone = (i % HIGHLIGHT_EVERY_NTH_NAIL == 0) and i > 0
        
        # Draw nail point
        nail_size = 8 if is_milestone else 5
        nail_color = 'red' if is_milestone else 'black'
        ax.plot(x, y, 'o', color=nail_color, markersize=nail_size, 
               markeredgecolor='black', markeredgewidth=0.5)
        
        # Calculate offset for number placement
        dx = x - center_x_plot
        dy = y - center_y_plot
        dist = np.sqrt(dx*dx + dy*dy)
        if dist > 0:
            offset_x = x + (dx / dist) * offset_distance_px
            offset_y = y + (dy / dist) * offset_distance_px
        else:
            offset_x, offset_y = x, y
        
        # Draw number with enhanced readability
        bbox_props = dict(boxstyle='round,pad=0.4', fc='white', ec='black', linewidth=1.5 if is_milestone else 0.8)
        text_weight = 'bold' if is_milestone else 'normal'
        ax.text(offset_x, offset_y, str(i), fontsize=font_size,
               ha='center', va='center', bbox=bbox_props, weight=text_weight)

    # Set equal aspect and limits in pixels
    ax.set_aspect('equal')
    ax.set_xlim(0, A3_WIDTH_IN * dpi)
    ax.set_ylim(0, A3_HEIGHT_IN * dpi)
    ax.invert_yaxis()
    ax.axis('off')

    # Add title and dimensions
    title_y = margin_in * dpi * 0.4
    ax.text(A3_WIDTH_IN * dpi / 2, title_y, 
            f'String Art Nail Scheme - {len(nails)} nails (A3 Format)',
            fontsize=18, ha='center', va='center', weight='bold')
    
    # Add physical dimensions
    ax.text(A3_WIDTH_IN * dpi / 2, title_y + 30, 
            f'Circle Diameter: {CIRCLE_RADIUS_MM * 2:.0f}mm | Margin: {MARGIN_MM}mm',
            fontsize=12, ha='center', va='center', style='italic')
    
    # Add legend
    legend_x = margin_in * dpi * 0.7
    legend_y = A3_HEIGHT_IN * dpi - margin_in * dpi * 0.5
    ax.text(legend_x, legend_y, '★ Start (Nail 0)', fontsize=10, color='red', weight='bold')
    ax.text(legend_x, legend_y + 25, f'● Every {HIGHLIGHT_EVERY_NTH_NAIL}th nail', 
           fontsize=10, color='red')

    plt.tight_layout()
    plt.savefig(filename, dpi=dpi, bbox_inches='tight')
    plt.close()

    print(f"Scheme saved as PNG: {filename}")


def export_scheme_as_pdf(nails, radius, center_x, center_y, filename, dpi):
    """
    Export the nail scheme as a PDF sized for A3 paper with enhanced readability.
    
    Args:
        nails: Array of nail coordinates
        radius: Circle radius
        center_x, center_y: Circle center
        filename: Output filename
        dpi: Resolution for output
    """
    # Create figure for A3
    fig, ax = plt.subplots(figsize=(A3_WIDTH_IN, A3_HEIGHT_IN))

    # Compute margins and drawable area
    margin_in = MARGIN_MM / 25.4  # Convert mm to inches
    drawable_w = A3_WIDTH_IN - 2 * margin_in
    drawable_h = A3_HEIGHT_IN - 2 * margin_in
    drawable_size_in = min(drawable_w, drawable_h)
    drawable_size_px = drawable_size_in * dpi

    scale = drawable_size_px / TARGET_SIZE

    nails_plot = nails.copy()
    nails_plot[:, 0] = nails[:, 0] * scale + margin_in * dpi + (drawable_w * dpi - drawable_size_px) / 2
    nails_plot[:, 1] = nails[:, 1] * scale + margin_in * dpi + (drawable_h * dpi - drawable_size_px) / 2

    center_x_plot = center_x * scale + margin_in * dpi + (drawable_w * dpi - drawable_size_px) / 2
    center_y_plot = center_y * scale + margin_in * dpi + (drawable_h * dpi - drawable_size_px) / 2
    radius_plot = radius * scale

    # Draw reference grid
    for angle in range(0, 360, 30):
        angle_rad = np.radians(angle)
        x_inner = center_x_plot + radius_plot * 0.95 * np.cos(angle_rad)
        y_inner = center_y_plot + radius_plot * 0.95 * np.sin(angle_rad)
        x_outer = center_x_plot + radius_plot * 1.05 * np.cos(angle_rad)
        y_outer = center_y_plot + radius_plot * 1.05 * np.sin(angle_rad)
        ax.plot([x_inner, x_outer], [y_inner, y_outer], 'gray', linewidth=0.5, alpha=0.3)

    # Draw circle
    circle = patches.Circle((center_x_plot, center_y_plot), radius_plot, fill=False,
                           edgecolor='black', linewidth=2.5)
    ax.add_patch(circle)

    # Draw start marker
    start_angle = np.radians(90)
    marker_size = 15
    x_start = center_x_plot + radius_plot * np.cos(start_angle)
    y_start = center_y_plot + radius_plot * np.sin(start_angle)
    ax.plot(x_start, y_start, 'r*', markersize=marker_size, markeredgecolor='black', markeredgewidth=1.5)

    # Calculate font size and offset
    font_size = max(NAIL_NUMBER_FONT_SIZE_BASE, int(NAIL_NUMBER_FONT_SIZE_BASE * (200 / len(nails))))
    offset_distance_px = (NAIL_NUMBER_OFFSET_MM / 25.4) * dpi

    # Draw nails with numbers
    for i, (x, y) in enumerate(nails_plot):
        is_milestone = (i % HIGHLIGHT_EVERY_NTH_NAIL == 0) and i > 0
        
        nail_size = 8 if is_milestone else 5
        nail_color = 'red' if is_milestone else 'black'
        ax.plot(x, y, 'o', color=nail_color, markersize=nail_size,
               markeredgecolor='black', markeredgewidth=0.5)
        
        dx = x - center_x_plot
        dy = y - center_y_plot
        dist = np.sqrt(dx*dx + dy*dy)
        if dist > 0:
            offset_x = x + (dx / dist) * offset_distance_px
            offset_y = y + (dy / dist) * offset_distance_px
        else:
            offset_x, offset_y = x, y
        
        bbox_props = dict(boxstyle='round,pad=0.4', fc='white', ec='black', 
                         linewidth=1.5 if is_milestone else 0.8)
        text_weight = 'bold' if is_milestone else 'normal'
        ax.text(offset_x, offset_y, str(i), fontsize=font_size,
               ha='center', va='center', bbox=bbox_props, weight=text_weight)

    ax.set_aspect('equal')
    ax.set_xlim(0, A3_WIDTH_IN * dpi)
    ax.set_ylim(0, A3_HEIGHT_IN * dpi)
    ax.invert_yaxis()
    ax.axis('off')

    # Add title and dimensions
    title_y = margin_in * dpi * 0.4
    ax.text(A3_WIDTH_IN * dpi / 2, title_y,
            f'String Art Nail Scheme - {len(nails)} nails (A3 Format)',
            fontsize=18, ha='center', va='center', weight='bold')
    
    ax.text(A3_WIDTH_IN * dpi / 2, title_y + 30,
            f'Circle Diameter: {CIRCLE_RADIUS_MM * 2:.0f}mm | Margin: {MARGIN_MM}mm',
            fontsize=12, ha='center', va='center', style='italic')
    
    # Add legend
    legend_x = margin_in * dpi * 0.7
    legend_y = A3_HEIGHT_IN * dpi - margin_in * dpi * 0.5
    ax.text(legend_x, legend_y, '★ Start (Nail 0)', fontsize=10, color='red', weight='bold')
    ax.text(legend_x, legend_y + 25, f'● Every {HIGHLIGHT_EVERY_NTH_NAIL}th nail',
           fontsize=10, color='red')

    plt.tight_layout()
    with PdfPages(filename) as pdf:
        pdf.savefig(fig, dpi=dpi, bbox_inches='tight')
    plt.close()

    print(f"Scheme saved as PDF: {filename}")


def export_instructions_csv(instructions, nails, filename):
    """
    Export enhanced instructions as CSV file with segment length, angle, and progress.
    
    Args:
        instructions: List of (from_nail, to_nail) tuples
        nails: Array of nail coordinates
        filename: Output filename
    """
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Step', 'From_Nail', 'To_Nail', 'Length_mm', 'Angle_deg', 'Progress_%', 'Section'])
        
        total_steps = len(instructions)
        total_length = 0.0
        
        # Calculate physical scale: pixels to mm
        px_to_mm = (CIRCLE_RADIUS_MM * 2) / (CIRCLE_RADIUS * 2)
        
        for i, (from_nail, to_nail) in enumerate(instructions, 1):
            # Calculate segment length in pixels, then convert to mm
            x0, y0 = nails[from_nail]
            x1, y1 = nails[to_nail]
            length_px = np.sqrt((x1 - x0)**2 + (y1 - y0)**2)
            length_mm = length_px * px_to_mm
            total_length += length_mm
            
            # Calculate angle relative to horizontal (0-360 degrees)
            angle_rad = np.arctan2(y1 - y0, x1 - x0)
            angle_deg = (np.degrees(angle_rad) + 360) % 360
            
            # Calculate progress percentage
            progress = (i / total_steps) * 100
            
            # Determine section (divide into 10 sections for easier execution)
            section = (i - 1) // (total_steps // 10 + 1) + 1
            
            writer.writerow([
                i, 
                from_nail, 
                to_nail, 
                f"{length_mm:.1f}",
                f"{angle_deg:.1f}",
                f"{progress:.1f}",
                section
            ])
        
        # Add summary row
        writer.writerow([])
        writer.writerow(['SUMMARY', '', '', '', '', '', ''])
        writer.writerow(['Total Steps', total_steps, '', '', '', '', ''])
        writer.writerow(['Total Thread Length (mm)', f"{total_length:.1f}", '', '', '', '', ''])
        writer.writerow(['Total Thread Length (m)', f"{total_length/1000:.2f}", '', '', '', '', ''])
        writer.writerow(['Recommended Thread', f"{total_length/1000 * 1.2:.2f}m", '(+20% safety margin)', '', '', '', ''])
    
    print(f"Instructions saved as CSV: {filename}")
    print(f"  Total steps: {total_steps}")
    print(f"  Total thread length: {total_length/1000:.2f}m (recommend {total_length/1000 * 1.2:.2f}m with margin)")


def export_instructions_txt(instructions, filename):
    """
    Export instructions as text file.
    
    Args:
        instructions: List of (from_nail, to_nail) tuples
        filename: Output filename
    """
    with open(filename, 'w') as f:
        f.write("STRING ART INSTRUCTIONS\n")
        f.write("=" * 50 + "\n\n")
        
        for i, (from_nail, to_nail) in enumerate(instructions, 1):
            f.write(f"Step {i:4d}: Connect nail {from_nail:3d} to nail {to_nail:3d}\n")
    
    print(f"Instructions saved as TXT: {filename}")


def render_drawing_simulation(instructions, nails, canvas_size, filename, dpi):
    """
    Render a realistic simulation showing how the finished string art will look.
    Uses layered semi-transparent thread lines with alpha compositing for realism.
    
    Args:
        instructions: List of (from_nail, to_nail) tuples
        nails: Array of nail coordinates (in TARGET_SIZE coordinate space)
        canvas_size: Size in pixels of the square canvas (same as TARGET_SIZE)
        filename: Output PNG filename
        dpi: DPI for saving image
    """
    # Create a white RGBA canvas with paper-like tint
    img_px = int(canvas_size)
    canvas = Image.new('RGBA', (img_px, img_px), color=(252, 250, 245, 255))
    
    # Create layer for thread lines
    layer = Image.new('RGBA', (img_px, img_px), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    
    # Thread appearance settings
    thread_color = (25, 25, 25)  # Dark gray/black thread
    base_alpha = 15  # Alpha per line pass (0-255) - adjusted for better visibility
    line_width = max(2, int(LINE_WEIGHT * (img_px / TARGET_SIZE) / 5))
    
    print(f"Rendering {len(instructions)} thread segments...")
    
    for idx, (a, b) in enumerate(instructions):
        x0, y0 = nails[a]
        x1, y1 = nails[b]
        
        # Draw thread line with alpha blending
        ld.line([(x0, y0), (x1, y1)], 
               fill=(thread_color[0], thread_color[1], thread_color[2], base_alpha), 
               width=line_width)
        
        # Periodically composite to simulate accumulation and manage memory
        if (idx + 1) % 500 == 0:
            canvas = Image.alpha_composite(canvas, layer)
            layer = Image.new('RGBA', (img_px, img_px), (0, 0, 0, 0))
            ld = ImageDraw.Draw(layer)
            if (idx + 1) % 1000 == 0:
                print(f"  Rendered {idx + 1}/{len(instructions)} segments...")
    
    # Final composite
    canvas = Image.alpha_composite(canvas, layer)
    
    # Draw nails as small dark circles
    draw_final = ImageDraw.Draw(canvas)
    nail_radius = max(2, int(4 * (img_px / TARGET_SIZE)))
    for x, y in nails:
        draw_final.ellipse(
            [(x - nail_radius, y - nail_radius), (x + nail_radius, y + nail_radius)], 
            fill=(15, 15, 15, 255)
        )
    
    # Add start marker (red dot on nail 0)
    start_x, start_y = nails[0]
    marker_radius = nail_radius + 2
    draw_final.ellipse(
        [(start_x - marker_radius, start_y - marker_radius), 
         (start_x + marker_radius, start_y + marker_radius)],
        fill=(200, 0, 0, 255)
    )
    
    # Convert to RGB for saving
    rgb = canvas.convert('RGB')
    rgb.save(filename, dpi=(dpi, dpi))
    
    # Also save as PDF at A3 size for printing
    pdf_filename = filename.replace('.png', '.pdf')
    fig, ax = plt.subplots(figsize=(A3_WIDTH_IN, A3_HEIGHT_IN))
    ax.imshow(rgb)
    ax.axis('off')
    ax.text(img_px / 2, 30, 'String Art Simulation - Final Result Preview',
            fontsize=16, ha='center', va='top', weight='bold',
            bbox=dict(boxstyle='round,pad=0.5', fc='white', ec='black', alpha=0.8))
    
    plt.tight_layout()
    with PdfPages(pdf_filename) as pdf:
        pdf.savefig(fig, bbox_inches='tight', dpi=dpi)
    plt.close(fig)
    
    print(f"Simulation saved: {filename} and {pdf_filename}")


# ============================================================================
# MAIN PROGRAM
# ============================================================================

def main():
    """Main program entry point."""
    
    # Check command line arguments
    if len(sys.argv) < 2:
        print("Usage: python string_art.py <input_image.jpg|png>")
        print("\nExample: python string_art.py photo.jpg")
        sys.exit(1)
    
    input_image = sys.argv[1]
    
    print("=" * 60)
    print("STRING ART GENERATOR")
    print("=" * 60)
    print()
    
    # Configuration summary
    print("Configuration:")
    print(f"  Input image: {input_image}")
    print(f"  Target size: {TARGET_SIZE}x{TARGET_SIZE} pixels")
    print(f"  Number of nails: {NUM_NAILS}")
    print(f"  Circle radius: {CIRCLE_RADIUS} pixels")
    print(f"  Number of steps: {NUM_STEPS}")
    print(f"  Thread strength: {THREAD_STRENGTH}")
    print(f"  Line weight: {LINE_WEIGHT}")
    print()
    
    # Step 1: Preprocess image
    print("Step 1: Preprocessing image...")
    img_array = preprocess_image(input_image, TARGET_SIZE, INVERT_IMAGE)
    print(f"  Image shape: {img_array.shape}")
    print(f"  Value range: {np.min(img_array):.3f} to {np.max(img_array):.3f}")
    print()
    
    # Step 2: Generate nail positions
    print("Step 2: Generating nail positions...")
    center_x = TARGET_SIZE / 2
    center_y = TARGET_SIZE / 2
    nails = generate_nails(NUM_NAILS, CIRCLE_RADIUS, center_x, center_y)
    print(f"  Generated {len(nails)} nails")
    print()
    
    # Step 3: Run string art algorithm
    print("Step 3: Running string art algorithm...")
    instructions = simulate_string_art(img_array, nails, NUM_STEPS, 
                                      THREAD_STRENGTH, LINE_WEIGHT)
    print(f"  Generated {len(instructions)} thread segments")
    print()
    
    # Step 4: Export outputs
    print("Step 4: Exporting outputs...")
    
    # Export scheme
    if EXPORT_SCHEME_PDF:
        export_scheme_as_pdf(nails, CIRCLE_RADIUS, center_x, center_y,
                           OUTPUT_SCHEME_PDF, SCHEME_DPI)
    
    if EXPORT_SCHEME_PNG:
        export_scheme_as_png(nails, CIRCLE_RADIUS, center_x, center_y,
                           OUTPUT_SCHEME_PNG, SCHEME_DPI)

    # Export a drawing simulation that renders all thread lines onto a white canvas
    simulation_png = 'drawing_simulation.png'
    render_drawing_simulation(instructions, nails, TARGET_SIZE, simulation_png, SCHEME_DPI)
    print(f"Drawing simulation saved: {simulation_png}")
    
    # Export instructions
    if EXPORT_FORMAT == "csv":
        export_instructions_csv(instructions, nails, OUTPUT_INSTRUCTIONS)
    else:
        export_instructions_txt(instructions, OUTPUT_INSTRUCTIONS.replace('.csv', '.txt'))
    
    print()
    print("=" * 60)
    print("GENERATION COMPLETE!")
    print("=" * 60)
    print("\nOutput files:")
    if EXPORT_SCHEME_PDF:
        print(f"  - {OUTPUT_SCHEME_PDF} (nail scheme)")
    if EXPORT_SCHEME_PNG:
        print(f"  - {OUTPUT_SCHEME_PNG} (nail scheme)")
    print(f"  - {OUTPUT_INSTRUCTIONS} (step-by-step instructions)")
    print("\nYou can now use these files to create your string art!")


if __name__ == "__main__":
    main()
