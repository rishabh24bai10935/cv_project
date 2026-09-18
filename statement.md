# Project Statement

**Project:** Computer Vision Application — Spatial-Domain Image Enhancement & Geometric Transformations

---

## 1. Problem Statement

Classical image processing is taught as a set of mathematical mappings — a brightness offset, a log curve, a gamma exponent, a 2×3 affine matrix — but a formula on a slide gives no intuition for what it actually does to a photograph. Learners are told that gamma < 1 "expands dark tones" and that a shear matrix "slants the image", yet they rarely see the two side by side, and almost never see how the result changes as the parameter changes.

The usual alternatives all fall short in different ways:

- **Consumer photo editors** (Photoshop, GIMP, phone apps) apply these operations behind friendly sliders labelled "Exposure" or "Straighten". The underlying transform is hidden, the parameter shown bears no relation to the textbook symbol, and several operations are silently composed at once.
- **Scattered tutorial snippets** demonstrate one technique per script, with no shared input image, no common display format, and no way to compare techniques against each other.
- **Writing it yourself from scratch** hits avoidable obstacles early: OpenCV loads images as BGR while matplotlib expects RGB, `uint8` arithmetic wraps around instead of clipping (so adding 60 to a bright pixel produces a *dark* one), and naive shear or rotation silently crops content off the canvas.

There is also no convenient way to answer the comparative question that matters most in practice — *which enhancement suits this particular image?* — because that requires seeing log, gamma, contrast stretching and thresholding applied to the same source, at the same time.

**The problem this project solves:** provide a single, self-contained, zero-configuration tool that applies each classical spatial-domain enhancement and geometric transformation to a user-supplied image, exposes the textbook parameter directly, displays the original and the result side by side, and can render every technique at once in a comparison grid — so the relationship between formula, parameter and visual outcome becomes immediately observable.

---

## 2. Scope of the Project

### 2.1 In Scope

**Operation coverage**

- Seven spatial-domain point operations: brightness adjustment, contrast adjustment, image negative, log transformation, power-law (gamma) transformation, global thresholding, and piecewise-linear contrast stretching.
- Nine geometric transformations: translation, scaling, rotation, horizontal reflection, vertical reflection, reflection about the origin, shearing along x, shearing along y, and general affine transformation defined by three point correspondences.

**Interaction model**

- Command-line entry point accepting an image path via `--image` / `-i`.
- Numbered, looping text menu; the application returns to the menu after each operation and exits cleanly on `0`.
- Parameter prompts for every operation that takes one, each with a printed default that is accepted by pressing Enter.

**Output and visualisation**

- Side-by-side "Original vs. Processed" figure for every individual operation, using matplotlib.
- Two aggregate comparison modes rendering all spatial techniques, or all geometric techniques, as a labelled grid.
- Automatic saving of the two comparison grids to PNG (`output_spatial_all.png`, `output_geom_all.png`) at 150 dpi.

**Robustness within scope**

- Graceful input fallback chain: explicit `--image` → `input.jpg` in the working directory → auto-generated synthetic test image.
- Correct BGR→RGB conversion on load so displayed colours are accurate.
- Overflow-safe arithmetic: all intermediate results computed in a wider dtype and clipped to `[0, 255]` before casting back to `uint8`.
- Canvas expansion for shear operations so transformed content is not clipped.
- Clear errors for a missing file or an unreadable/unsupported image format, and a re-prompt on an invalid menu selection.

### 2.2 Out of Scope

Deliberately excluded to keep the project focused, dependency-light and readable:

- **Neighbourhood and frequency-domain processing** — convolution filters, blurring, sharpening, edge detection, morphological operations, Fourier-domain filtering, histogram equalisation.
- **Higher-level computer vision** — object detection, segmentation, feature matching, classification, any machine-learning component.
- **Graphical user interface** — no windowed app, no live parameter sliders, no drag-and-drop. Interaction is terminal-based; matplotlib is used for display only.
- **Batch and pipeline processing** — operations apply to one image at a time, and each is applied to the *original*, not chained onto the previous result.
- **Video, animated, and multi-frame input.**
- **Persistence of individual results** — only the two comparison grids are written to disk automatically; single side-by-side figures are displayed and can be saved manually from the matplotlib window.
- **Undo/redo history, presets, or session state.**
- **Non-affine warping** — perspective/homography transforms, lens distortion correction, elastic warps.
- **Packaging and distribution** — no installer, no PyPI package, no containerisation; the project is a single `.py` file run directly.

### 2.3 Assumptions and Constraints

- Python 3.8 or newer is available, with `opencv-python`, `numpy` and `matplotlib` installable via `pip`.
- A desktop environment capable of opening matplotlib windows is present; the application is not designed for headless execution.
- Input images are standard 8-bit still images in a format OpenCV can decode (JPEG, PNG, BMP, TIFF and similar).
- Images are assumed to be of a size a single machine can hold in memory comfortably; no tiling or streaming is performed.
- The user is comfortable running a command in a terminal and typing numeric input.

---

## 3. Target Users

### 3.1 Primary — Students of image processing and computer vision

Undergraduates and postgraduates taking a digital image processing, computer vision or multimedia course. They have met these transforms as equations and need to connect each formula to its visual effect, verify their own implementations against a working reference, and produce comparison figures for lab reports and assignments.

*What they need from the tool:* textbook parameter names exposed directly, formulas documented next to the code, side-by-side output, and grid figures that can be dropped straight into a report.

### 3.2 Primary — Instructors and teaching assistants

Lecturers preparing course material and TAs running lab sessions, who need to demonstrate a concept live, generate figures for slides, or hand students a reference implementation.

*What they need from the tool:* zero setup friction, the ability to demonstrate on any image (including the built-in synthetic one when no suitable image is at hand), one-key generation of a full comparison grid, and readable source code that can be walked through in class.

### 3.3 Secondary — Self-taught learners and developers new to OpenCV

Developers picking up image processing outside a formal course who want a working, commented starting point covering the fundamentals, and who benefit from having the common traps (BGR vs. RGB, `uint8` overflow, shear cropping) already solved and visible in the code.

*What they need from the tool:* a single readable file, no framework to learn, and functions clean enough to copy into their own project.

### 3.4 Secondary — Practitioners doing quick exploratory work

Photographers, researchers and analysts who occasionally need to preview how a gamma correction, a contrast stretch or a threshold would affect a specific image before committing to a processing decision elsewhere.

*What they need from the tool:* fast turnaround, all candidate enhancements visible at once, and no project setup.

### 3.5 Non-users

The project is not intended for end-users seeking a production photo editor, for teams needing automated batch pipelines, or for anyone requiring a graphical interface with live preview.

---

## 4. High-Level Features

### F1 — Flexible image input with graceful fallback

Accepts an image path on the command line; falls back to `input.jpg` in the working directory; and, failing that, generates a synthetic test image (vertical colour gradient, filled circle, outlined rectangle, overlaid text) so the application can always be demonstrated even with no assets available.

### F2 — Spatial-domain enhancement suite

Seven point operations, each implemented from its defining formula with the mathematically meaningful parameter exposed to the user:

| Operation | Parameter exposed |
|---|---|
| Brightness adjustment | offset β |
| Contrast adjustment | gain α |
| Image negative | — |
| Log transformation | scaling constant c (auto-computed to fill the output range) |
| Power-law / gamma | exponent γ, constant c |
| Global thresholding | threshold T, maximum value |
| Contrast stretching | control points (r₁, s₁) and (r₂, s₂) |

### F3 — Geometric transformation suite

Nine transformations covering the full set of affine operations — translation, anisotropic scaling, rotation about an arbitrary centre, the three reflections, shear along each axis, and a general affine transform specified by three point correspondences — each documented with its transformation matrix.

### F4 — Side-by-side visual comparison

Every individual operation opens a two-panel matplotlib figure showing the original alongside the processed result, titled with the operation and the parameter values used, with grayscale results rendered using an appropriate colormap.

### F5 — Compare-all grid modes

Two dedicated menu options render every technique in a category — spatial or geometric — applied to the same source image, in a single labelled grid. This turns the tool from a demonstrator into a decision aid: the user can see all candidate enhancements at once and pick the one that suits the image.

### F6 — Automatic figure export

Both comparison grids are written to disk as 150 dpi PNGs with a confirmation message, ready for inclusion in reports, slides or documentation without any further steps.

### F7 — Interactive menu loop with sensible defaults

A numbered menu covering all eighteen operations plus exit, redisplayed after each action. Every parameter prompt shows a working default in brackets; pressing Enter accepts it, so a user unfamiliar with a technique can see a good result immediately and then experiment.

### F8 — Numerically correct, artefact-free implementations

Arithmetic is performed in a wider dtype and clipped to the valid 8-bit range before being cast back, preventing the wraparound artefacts that make naive brightness and contrast implementations produce inverted regions. Shear operations enlarge the output canvas in proportion to the shear factor so no content is lost off the edge.

### F9 — Accurate colour handling

Images are converted from OpenCV's BGR ordering to RGB on load and written back as BGR on save, so displayed and exported colours match the source.

### F10 — Self-documenting source

Every operation carries a docstring stating its formula or transformation matrix, the meaning and typical range of each parameter, and the direction of the visual effect — making the file usable as a study reference as well as a running application.

### F11 — Predictable error handling

A missing file raises a clear `FileNotFoundError` naming the path; an undecodable file raises a `ValueError` indicating a possible format problem; an invalid menu selection prints a short message and re-displays the menu rather than crashing or exiting.

### F12 — Single-file, minimal-dependency deployment

The entire application is one Python file depending only on OpenCV, NumPy and matplotlib. There is nothing to build, configure or install beyond three `pip` packages, which keeps it viable in constrained lab environments and easy to share as a single attachment.
