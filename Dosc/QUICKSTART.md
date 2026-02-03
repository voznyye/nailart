# 🚀 Quick Start - String Art Generator

## Your first result in 5 minutes!

### Step 1: Installation (1 minute)

```bash
# Navigate to project folder
cd art

# Create virtual environment (if not created)
python3 -m venv .venv

# Activate environment
source .venv/bin/activate  # on macOS/Linux
# or
.venv\Scripts\activate  # on Windows

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Prepare an Image (1 minute)

Find or create an image:
- **Format:** JPG or PNG
- **Size:** minimum 500×500 px
- **Content:** portrait, logo, simple object
- **Contrast:** higher is better

💡 **Tip:** Use black and white image with clear contours

### Step 3: Run the Generator (2-5 minutes execution)

```bash
python string_art.py your_image.png
```

### Step 4: Get Results

After completion you will receive:

1. **nails_scheme.pdf** 📋
   - Scheme for placing 180 nails
   - Ready to print on A3
   - With numbers and guides

2. **instructions.csv** 📊
   - 3500 steps of instructions
   - Length of each segment
   - Total thread length: ~30-100 meters

3. **drawing_simulation.png** 🖼️
   - How the result will look
   - Realistic visualization

## What's Next?

### Create Physical Artwork

1. Print `nails_scheme.pdf` on A3
2. Buy materials:
   - Wooden board A3+ size
   - 180 small nails (15-20 mm)
   - Black thread (see length in CSV)
   - Hammer

3. Follow instructions from CSV
4. Enjoy the result! 🎨

### Adjust Parameters

Open `string_art.py` and change:

```python
# Quick variant (2 hours work)
NUM_NAILS = 150
NUM_STEPS = 2000

# Quality variant (5 hours work)
NUM_NAILS = 200
NUM_STEPS = 4000
```

## Need Help?

- 📖 Complete documentation: `README.md`
- 🔧 Configuration examples: `EXAMPLES.md`
- 🏗️ Technical information: `ARCHITECTURE.md`
- ❓ Problems? See FAQ section in README

## Done! 🎉

Now you're ready to create amazing String Art works!
