# Computer Vision Application — Spatial-Domain Image Enhancement & Geometric Transformations

A single-file, menu-driven Python application for exploring classical image processing techniques. It loads an image of your choice and lets you apply point-processing enhancements and geometric transformations interactively, showing the original and processed result side by side after every operation.

---

## Overview

This project implements two families of classical image processing operations from first principles (using NumPy maths and OpenCV's affine warping primitives):

1. **Spatial-domain enhancement** — point operations that map each pixel's intensity to a new intensity, independent of its neighbours (brightness, contrast, negative, log, gamma, thresholding, contrast stretching).
2. **Geometric transformations** — operations that relocate pixels according to a 2×3 affine matrix (translation, scaling, rotation, reflections, shearing, general affine).

After launching, you pick an operation from a numbered menu, optionally enter parameters (each prompt has a sensible default you can accept by pressing Enter), and a matplotlib window opens with the **Original** and **Processed** images side by side. Two "compare all" options render every technique in a single grid so results can be evaluated against each other at a glance, and these grids are saved to disk as PNGs.

If you don't supply an image, the app falls back to `input.jpg` in the current folder. If that's missing too, it generates a synthetic test image (gradient background, green circle, yellow rectangle, "SAMPLE" text) so the program can always be demonstrated.

---

## Features

### (a) Spatial-Domain Enhancement

| # | Technique | Formula | Parameters |
|---|-----------|---------|------------|
| 1 | Brightness adjustment | `g = f + β` | `beta` ∈ [-255, 255], default 50 |
| 2 | Contrast adjustment | `g = α · f` | `alpha` ∈ [0.0, 3.0], default 1.5 |
| 3 | Image negative | `g = (L-1) - f`, L = 256 | none |
| 4 | Log transformation | `g = c · log(1 + f)` | `c` auto-computed to use the full 0–255 range |
| 5 | Power-law (Gamma) | `g = c · f^γ` on normalised input | `gamma` (< 1 brightens, > 1 darkens), default 0.5 |
| 6 | Thresholding | `g = maxval if f > T else 0` | `T` ∈ [0, 255], default 127 |
| 7 | Contrast stretching | piecewise-linear through (0,0), (r1,s1), (r2,s2), (255,255) | `r1, s1, r2, s2`, defaults 70, 0, 180, 255 |
| 8 | **Compare all** | renders techniques 1–7 in one grid | saved as `output_spatial_all.png` |

### (b) Geometric Transformations

| # | Technique | Matrix | Parameters |
|---|-----------|--------|------------|
| 9 | Translation | `[[1,0,tx],[0,1,ty]]` | `tx, ty` in pixels, defaults 40, 30 |
| 10 | Scaling | bilinear resize | `sx, sy`, defaults 1.5, 1.5 |
| 11 | Rotation | `getRotationMatrix2D` about image centre | `angle` in degrees (CCW positive), default 45 |
| 12 | Horizontal reflection | `[[-1,0,w-1],[0,1,0]]` | none |
| 13 | Vertical reflection | `[[1,0,0],[0,-1,h-1]]` | none |
| 14 | Reflection about origin | `[[-1,0,w-1],[0,-1,h-1]]` | none |
| 15 | Shearing along x | `[[1,shx,0],[0,1,0]]` | `shx` ∈ [-1.0, 1.0], default 0.3 |
| 16 | Shearing along y | `[[1,0,0],[shy,1,0]]` | `shy` ∈ [-1.0, 1.0], default 0.3 |
| 17 | General affine | 3-point correspondence via `getAffineTransform` | `src_pts`, `dst_pts` (sample transform used by default) |
| 18 | **Compare all** | renders techniques 9–17 in one grid | saved as `output_geom_all.png` |

### Quality-of-life features

- Side-by-side original vs. processed display for every single operation.
- Every numeric prompt has a default — press Enter to accept it.
- Shear operations expand the output canvas so no content is clipped.
- Overflow-safe arithmetic: all results are clipped to `[0, 255]` and cast back to `uint8`.
- Automatic synthetic image generation when no input is available.
- Loops back to the menu after each operation; `0` exits cleanly.

---

## Technologies / Tools Used

| Tool | Purpose |
|------|---------|
| **Python 3.8+** | Language runtime |
| **OpenCV** (`opencv-python`) | Image I/O, colour conversion, affine warping, thresholding, flipping, resizing |
| **NumPy** | Array maths for all point-processing operations, masking, clipping |
| **Matplotlib** | Side-by-side and grid visualisation, saving comparison figures |
| **argparse** | Command-line argument parsing (`--image`) |
| **os / sys** | File existence checks and path handling |

---

## Installation & Running

### 1. Prerequisites

- Python 3.8 or newer
- `pip`
- A desktop environment capable of opening matplotlib windows (the app uses `plt.show()`)

### 2. Get the project

```bash
git clone <your-repository-url>
cd <project-folder>
```

Or simply place `cv_app.py` in a folder of your choice.

### 3. (Recommended) Create a virtual environment

```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install opencv-python numpy matplotlib
```

Or, if you create a `requirements.txt` containing:

```
opencv-python
numpy
matplotlib
```

then run:

```bash
pip install -r requirements.txt
```

### 5. Run

```bash
# With your own image
python cv_app.py --image path/to/your_image.jpg

# Short flag
python cv_app.py -i lena.png

# No arguments: uses input.jpg, or generates a synthetic image
python cv_app.py
```

### 6. Use the menu

```
Loaded image: input.jpg  shape=(400, 400, 3)

---- (a) Spatial-Domain Enhancement ----
 1. Brightness adjustment
 2. Contrast adjustment
 ...
 8. Compare ALL spatial techniques in one grid

---- (b) Geometric Transformations ----
 9.  Translation
 ...
 18. Compare ALL geometric techniques in one grid

 0. Exit

Select an option: 5
Gamma value (e.g. 0.4=brighten, 2.5=darken) [default 0.5]: 2.2
```

Close the matplotlib window to return to the menu.

---

## Testing Instructions

### Smoke test — does it run at all?

```bash
python cv_app.py
```

**Expected:** the app reports that no image was supplied, generates `input.jpg`, prints the loaded shape, and displays the menu.

### Test the comparison grids first

These exercise every technique in one shot and are the fastest way to verify the whole application.

```
Select an option: 8    # all spatial techniques
Select an option: 18   # all geometric techniques
```

**Expected:** two grid windows appear, and `output_spatial_all.png` and `output_geom_all.png` are written to the current directory with a confirmation message.

### Functional test checklist

| Option | Input | Expected result |
|--------|-------|-----------------|
| 1 | `beta = 80` | Visibly brighter; bright areas saturate rather than wrapping to black |
| 1 | `beta = -80` | Visibly darker; dark areas clamp at 0, not wrapping to white |
| 2 | `alpha = 2.0` | Higher contrast, highlights clipped |
| 2 | `alpha = 0.4` | Washed-out, low contrast |
| 3 | — | Colours inverted; running it twice returns the original |
| 4 | — | Shadow detail lifted, highlights compressed |
| 5 | `gamma = 0.4` | Brighter, dark tones expanded |
| 5 | `gamma = 2.5` | Darker, bright tones expanded |
| 6 | `T = 127` | Pure black-and-white binary image, grayscale colormap |
| 6 | `T = 0` / `T = 255` | Nearly all white / nearly all black respectively |
| 7 | defaults | Mid-tones stretched, overall punchier |
| 9 | `tx=40, ty=30` | Content shifted right and down, black band on left/top |
| 9 | `tx=-40, ty=-30` | Shifted left and up |
| 10 | `sx=2.0, sy=0.5` | Doubled width, halved height |
| 11 | `angle=90` | Rotated 90° counter-clockwise about the centre |
| 12 / 13 / 14 | — | Mirrored left-right / top-bottom / both; applying twice restores the original |
| 15 / 16 | `0.3` | Slanted image, canvas widened/heightened so nothing is cut off |
| 17 | — | Combined rotation + shear + scale via the default point correspondence |
| 0 | — | Prints `Goodbye!` and exits |

### Edge cases worth verifying

- **Nonexistent path:** `python cv_app.py -i missing.jpg` → raises `FileNotFoundError: Image not found: missing.jpg`.
- **Unsupported/corrupt file:** rename a `.txt` to `.jpg` and pass it → raises `ValueError: Could not read image (unsupported format?)`.
- **Invalid menu choice:** enter `99` or `abc` → prints `Invalid option, please choose again.` and re-displays the menu.
- **Empty input at a parameter prompt:** press Enter → the default value in brackets is used.
- **Grayscale input image:** thresholding should still work without a colour-conversion error.

### Quick automated sanity check

Save as `test_cv_app.py` alongside `cv_app.py` and run `python test_cv_app.py`:

```python
import numpy as np
from cv_app import (
    image_negative, brightness_adjustment, gamma_transform,
    horizontal_reflection, vertical_reflection, thresholding,
    translation, scaling,
)

img = (np.random.rand(64, 64, 3) * 255).astype(np.uint8)

# Negative applied twice is the identity
assert np.array_equal(image_negative(image_negative(img)), img)

# Reflections are their own inverse
assert np.array_equal(horizontal_reflection(horizontal_reflection(img)), img)
assert np.array_equal(vertical_reflection(vertical_reflection(img)), img)

# Output stays inside the valid 8-bit range
for out in (brightness_adjustment(img, 300), brightness_adjustment(img, -300),
            gamma_transform(img, 0.3), gamma_transform(img, 3.0)):
    assert out.dtype == np.uint8 and out.min() >= 0 and out.max() <= 255

# Thresholding produces only two values
assert set(np.unique(thresholding(img, 127, 255))).issubset({0, 255})

# Geometry changes shape as expected
assert translation(img, 10, 10).shape == img.shape
assert scaling(img, 2.0, 0.5).shape[:2] == (32, 128)

print("All checks passed.")
```

---

## Screenshots

Add your own captures here once you've run the app. Suggested set:

| File | What to capture |
|------|-----------------|
| `screenshots/menu.png` | The numbered menu in the terminal after loading an image |
| `screenshots/gamma.png` | A side-by-side original vs. gamma-corrected result |
| `screenshots/output_spatial_all.png` | The spatial-enhancement comparison grid (auto-saved by option 8) |
| `screenshots/output_geom_all.png` | The geometric-transformation comparison grid (auto-saved by option 18) |

Embed them like this:

```markdown
### Spatial-domain comparison grid
![Spatial techniques](screenshots/output_spatial_all.png)

### Geometric transformation grid
![Geometric transforms](screenshots/output_geom_all.png)
```

Options 8 and 18 already write their grids to the project root, so you can move those PNGs straight into a `screenshots/` folder.

---

## Project Structure

```
.
├── cv_app.py                  # The complete application
├── input.jpg                  # Default / auto-generated input image
├── output_spatial_all.png     # Saved by menu option 8
├── output_geom_all.png        # Saved by menu option 18
├── requirements.txt           # Optional
└── README.md
```

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| No window appears when displaying results | You may be on a headless machine. Install a GUI backend (`pip install PyQt5`) or run on a desktop session. |
| `ModuleNotFoundError: No module named 'cv2'` | Run `pip install opencv-python` (note: the import name is `cv2`, the package name is not). |
| Colours look wrong (blue/red swapped) | The app converts BGR→RGB on load for matplotlib; if you add your own display code, remember OpenCV reads images as BGR. |
| Sheared image looks cropped | The output canvas is expanded automatically for shear; for very large factors, reduce `shx`/`shy`. |
