"""
====================================================================
  Computer Vision Application
  Spatial-Domain Image Enhancement + Geometric Transformations
====================================================================

WHAT THIS APPLICATION DOES
---------------------------
Loads an image supplied by the user and lets them:
  (a) Apply spatial-domain (point-processing) enhancement operations
        - Brightness adjustment
        - Contrast adjustment
        - Image negative
        - Log transformation
        - Power-law (Gamma) transformation
        - Thresholding
        - Contrast stretching
  (b) Apply geometric transformations
        - Translation
        - Scaling
        - Rotation
        - Horizontal reflection
        - Vertical reflection
        - Reflection about the origin
        - Shearing along x-axis
        - Shearing along y-axis
        - General affine transformation

Every operation displays the ORIGINAL and the PROCESSED image
side by side (matplotlib). Two extra "compare all" modes render a
grid of every technique at once so results can be compared directly.

HOW TO RUN
----------
    python cv_app.py --image path/to/your_image.jpg

If --image is not given, the script looks for "input.jpg" in the
current folder, and if that is missing too, it auto-generates a
synthetic test image so the program can still be demonstrated.

Then just follow the on-screen numbered menu.

REQUIREMENTS
------------
    pip install opencv-python numpy matplotlib
====================================================================
"""

import argparse
import os
import sys

import cv2
import numpy as np
import matplotlib.pyplot as plt


# ====================================================================
# ------------------------- UTILITIES ---------------------------------
# ====================================================================

def load_image(path, as_gray=False):
    """Load an image from disk. Returns an RGB (or grayscale) numpy array."""
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Image not found: {path}")
    flag = cv2.IMREAD_GRAYSCALE if as_gray else cv2.IMREAD_COLOR
    img = cv2.imread(path, flag)
    if img is None:
        raise ValueError(f"Could not read image (unsupported format?): {path}")
    if not as_gray:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img


def make_synthetic_image(path="input.jpg", size=(400, 400)):
    """Generate a simple synthetic test image if the user has none handy."""
    h, w = size
    img = np.zeros((h, w, 3), dtype=np.uint8)
    # background gradient
    for y in range(h):
        img[y, :, 0] = int(255 * y / h)
        img[y, :, 2] = 255 - int(255 * y / h)
    cv2.circle(img, (w // 2, h // 2), min(h, w) // 4, (0, 255, 0), -1)
    cv2.rectangle(img, (30, 30), (130, 130), (255, 255, 0), 3)
    cv2.putText(img, "SAMPLE", (60, h - 40), cv2.FONT_HERSHEY_SIMPLEX,
                1.1, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.imwrite(path, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
    return path


def show_pair(original, processed, title, cmap=None, save_path=None):
    """Display / save original vs processed image side by side."""
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    axes[0].imshow(original, cmap=cmap)
    axes[0].set_title("Original")
    axes[0].axis("off")

    axes[1].imshow(processed, cmap=cmap if processed.ndim == 2 else None)
    axes[1].set_title(title)
    axes[1].axis("off")

    plt.suptitle(title)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
        print(f"  -> saved comparison to {save_path}")
    plt.show()


def show_grid(images_titles, main_title, cmap=None, save_path=None, ncols=4):
    """Display a grid of (image, title) pairs for multi-technique comparison."""
    n = len(images_titles)
    ncols = min(ncols, n)
    nrows = int(np.ceil(n / ncols))
    fig, axes = plt.subplots(nrows, ncols, figsize=(4 * ncols, 4 * nrows))
    axes = np.array(axes).reshape(-1)
    for ax, (img, title) in zip(axes, images_titles):
        ax.imshow(img, cmap=cmap if img.ndim == 2 else None)
        ax.set_title(title, fontsize=10)
        ax.axis("off")
    for ax in axes[len(images_titles):]:
        ax.axis("off")
    plt.suptitle(main_title, fontsize=14)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
        print(f"  -> saved comparison grid to {save_path}")
    plt.show()


def to_uint8(img):
    return np.clip(img, 0, 255).astype(np.uint8)


# ====================================================================
# ------------------- (a) SPATIAL-DOMAIN ENHANCEMENT -------------------
# ====================================================================

def brightness_adjustment(img, beta):
    """
    Add/subtract a constant to every pixel.
    Parameters:
        beta : int, range typically [-255, 255]. Positive -> brighter.
    Formula: g(x,y) = f(x,y) + beta
    """
    return to_uint8(img.astype(np.int16) + beta)


def contrast_adjustment(img, alpha):
    """
    Multiply every pixel by a gain factor.
    Parameters:
        alpha : float, typically in [0.0, 3.0].
                alpha > 1 increases contrast, alpha < 1 decreases it.
    Formula: g(x,y) = alpha * f(x,y)
    """
    return to_uint8(img.astype(np.float32) * alpha)


def image_negative(img):
    """
    Invert the image (photographic negative).
    Formula: g(x,y) = (L-1) - f(x,y),  L = 256 for 8-bit images.
    No parameters required.
    """
    L = 256
    return to_uint8((L - 1) - img.astype(np.int16))


def log_transform(img, c=None):
    """
    Log transformation - expands dark pixel values, compresses bright ones.
    Parameters:
        c : float, scaling constant. If None, c is auto-computed so the
            output fully uses the 0-255 range: c = 255 / log(1 + max_pixel)
    Formula: g(x,y) = c * log(1 + f(x,y))
    """
    img_f = img.astype(np.float32)
    if c is None:
        c = 255.0 / np.log(1 + np.max(img_f) + 1e-6)
    out = c * np.log(1 + img_f)
    return to_uint8(out)


def gamma_transform(img, gamma, c=1.0):
    """
    Power-law (Gamma) transformation.
    Parameters:
        gamma : float, > 0.
                gamma < 1 brightens (expands dark tones),
                gamma > 1 darkens (expands bright tones).
        c     : float, scaling constant, default 1.0.
    Formula: g(x,y) = c * f(x,y)^gamma   (computed on normalized [0,1] input)
    """
    img_norm = img.astype(np.float32) / 255.0
    out = c * np.power(img_norm, gamma) * 255.0
    return to_uint8(out)


def thresholding(img, thresh=127, maxval=255):
    """
    Simple global thresholding -> binary image.
    Parameters:
        thresh : int [0,255], threshold value T.
        maxval : int [0,255], value assigned to pixels above T.
    Formula: g(x,y) = maxval if f(x,y) > T else 0
    """
    if img.ndim == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    else:
        gray = img
    _, out = cv2.threshold(gray, thresh, maxval, cv2.THRESH_BINARY)
    return out


def contrast_stretching(img, r1=70, s1=0, r2=180, s2=255):
    """
    Piecewise-linear contrast stretching.
    Parameters:
        (r1, s1) : input/output value of the first control point (0<=r1<=255)
        (r2, s2) : input/output value of the second control point (r1<r2<=255)
        Typical defaults stretch mid-tones out to the full [0,255] range.
    Formula (piecewise linear through (0,0),(r1,s1),(r2,s2),(255,255)):
        for r < r1:            s = (s1/r1) * r                     (if r1>0)
        for r1 <= r <= r2:     s = ((s2-s1)/(r2-r1)) * (r-r1) + s1
        for r > r2:            s = ((255-s2)/(255-r2)) * (r-r2) + s2
    """
    img_f = img.astype(np.float32)
    out = np.zeros_like(img_f)

    # region 1: 0 -> r1
    mask1 = img_f < r1
    if r1 > 0:
        out[mask1] = (s1 / r1) * img_f[mask1]

    # region 2: r1 -> r2
    mask2 = (img_f >= r1) & (img_f <= r2)
    if r2 != r1:
        out[mask2] = ((s2 - s1) / (r2 - r1)) * (img_f[mask2] - r1) + s1

    # region 3: r2 -> 255
    mask3 = img_f > r2
    if r2 != 255:
        out[mask3] = ((255 - s2) / (255 - r2)) * (img_f[mask3] - r2) + s2
    else:
        out[mask3] = 255

    return to_uint8(out)


# ====================================================================
# --------------------- (b) GEOMETRIC TRANSFORMATIONS -------------------
# ====================================================================

def translation(img, tx, ty):
    """
    Shift the image by (tx, ty) pixels.
    Parameters:
        tx : int, shift along x-axis (columns). Positive -> right.
        ty : int, shift along y-axis (rows).    Positive -> down.
    Matrix: [[1,0,tx],[0,1,ty]]
    """
    h, w = img.shape[:2]
    M = np.float32([[1, 0, tx], [0, 1, ty]])
    return cv2.warpAffine(img, M, (w, h))


def scaling(img, sx, sy, interpolation=cv2.INTER_LINEAR):
    """
    Resize the image by scale factors.
    Parameters:
        sx : float, scale factor along x-axis (e.g. 1.5 = 150% width)
        sy : float, scale factor along y-axis
        interpolation : cv2 interpolation flag (default: bilinear)
    """
    h, w = img.shape[:2]
    new_w, new_h = max(1, int(w * sx)), max(1, int(h * sy))
    return cv2.resize(img, (new_w, new_h), interpolation=interpolation)


def rotation(img, angle, scale=1.0, center=None):
    """
    Rotate the image about a center point.
    Parameters:
        angle  : float, rotation angle in degrees (counter-clockwise positive).
        scale  : float, isotropic scale factor applied during rotation, default 1.0.
        center : (x, y) tuple, rotation center. Defaults to image center.
    """
    h, w = img.shape[:2]
    if center is None:
        center = (w / 2, h / 2)
    M = cv2.getRotationMatrix2D(center, angle, scale)
    return cv2.warpAffine(img, M, (w, h))


def horizontal_reflection(img):
    """
    Mirror the image left-right (flip about the vertical axis).
    No parameters required.
    Matrix: [[-1,0,w-1],[0,1,0]]
    """
    return cv2.flip(img, 1)


def vertical_reflection(img):
    """
    Mirror the image top-bottom (flip about the horizontal axis).
    No parameters required.
    Matrix: [[1,0,0],[0,-1,h-1]]
    """
    return cv2.flip(img, 0)


def reflection_about_origin(img):
    """
    Reflect the image about the origin (180-degree flip: both axes).
    No parameters required.
    Matrix: [[-1,0,w-1],[0,-1,h-1]]
    """
    return cv2.flip(img, -1)


def shear_x(img, shx):
    """
    Shear the image along the x-axis.
    Parameters:
        shx : float, shear factor (typical range -1.0 to 1.0).
    Matrix: [[1, shx, 0], [0, 1, 0]]
    """
    h, w = img.shape[:2]
    M = np.float32([[1, shx, 0], [0, 1, 0]])
    new_w = int(w + abs(shx) * h)
    return cv2.warpAffine(img, M, (new_w, h))


def shear_y(img, shy):
    """
    Shear the image along the y-axis.
    Parameters:
        shy : float, shear factor (typical range -1.0 to 1.0).
    Matrix: [[1, 0, 0], [shy, 1, 0]]
    """
    h, w = img.shape[:2]
    M = np.float32([[1, 0, 0], [shy, 1, 0]])
    new_h = int(h + abs(shy) * w)
    return cv2.warpAffine(img, M, (w, new_h))


def affine_transform(img, src_pts=None, dst_pts=None):
    """
    General affine transformation defined by 3 point correspondences
    (covers combinations of translation, rotation, scaling and shearing
    in a single 2x3 matrix).
    Parameters:
        src_pts : list of 3 (x,y) points in the input image.
        dst_pts : list of 3 (x,y) points that src_pts should map to.
        If not given, a sample transform is demonstrated using default points.
    """
    h, w = img.shape[:2]
    if src_pts is None:
        src_pts = np.float32([[0, 0], [w - 1, 0], [0, h - 1]])
    if dst_pts is None:
        dst_pts = np.float32([[w * 0.0, h * 0.15],
                               [w * 0.85, h * 0.0],
                               [w * 0.15, h * 0.95]])
    src_pts = np.float32(src_pts)
    dst_pts = np.float32(dst_pts)
    M = cv2.getAffineTransform(src_pts, dst_pts)
    return cv2.warpAffine(img, M, (w, h))


# ====================================================================
# ---------------------------- MENU / DRIVER ---------------------------
# ====================================================================

SPATIAL_MENU = """
---- (a) Spatial-Domain Enhancement ----
 1. Brightness adjustment
 2. Contrast adjustment
 3. Image negative
 4. Log transformation
 5. Gamma (power-law) transformation
 6. Thresholding
 7. Contrast stretching
 8. Compare ALL spatial techniques in one grid
"""

GEOM_MENU = """
---- (b) Geometric Transformations ----
 9.  Translation
 10. Scaling
 11. Rotation
 12. Horizontal reflection
 13. Vertical reflection
 14. Reflection about the origin
 15. Shearing along x-axis
 16. Shearing along y-axis
 17. Affine transformation
 18. Compare ALL geometric techniques in one grid
"""

EXIT_MENU = """
 0. Exit
"""


def run_spatial_all(img):
    results = [
        (img, "Original"),
        (brightness_adjustment(img, 60), "Brightness (+60)"),
        (contrast_adjustment(img, 1.6), "Contrast (x1.6)"),
        (image_negative(img), "Negative"),
        (log_transform(img), "Log transform"),
        (gamma_transform(img, 0.5), "Gamma (0.5)"),
        (thresholding(img, 127, 255), "Threshold (T=127)"),
        (contrast_stretching(img), "Contrast stretch"),
    ]
    show_grid(results, "Spatial-Domain Enhancement - Comparison", ncols=4,
               save_path="output_spatial_all.png")


def run_geom_all(img):
    results = [
        (img, "Original"),
        (translation(img, 40, 30), "Translation (40,30)"),
        (scaling(img, 1.4, 0.8), "Scaling (1.4x, 0.8y)"),
        (rotation(img, 35), "Rotation (35 deg)"),
        (horizontal_reflection(img), "Horizontal reflection"),
        (vertical_reflection(img), "Vertical reflection"),
        (reflection_about_origin(img), "Reflection about origin"),
        (shear_x(img, 0.3), "Shear X (0.3)"),
        (shear_y(img, 0.3), "Shear Y (0.3)"),
        (affine_transform(img), "Affine transform"),
    ]
    show_grid(results, "Geometric Transformations - Comparison", ncols=5,
               save_path="output_geom_all.png")


def ask_float(prompt, default):
    raw = input(f"{prompt} [default {default}]: ").strip()
    return float(raw) if raw else default


def ask_int(prompt, default):
    raw = input(f"{prompt} [default {default}]: ").strip()
    return int(raw) if raw else default


def main():
    parser = argparse.ArgumentParser(description="CV Image Enhancement & Transformation App")
    parser.add_argument("--image", "-i", type=str, default=None,
                         help="Path to the input image")
    args = parser.parse_args()

    img_path = args.image
    if img_path is None:
        if os.path.isfile("input.jpg"):
            img_path = "input.jpg"
        else:
            print("No --image supplied and 'input.jpg' not found.")
            print("Generating a synthetic sample image: input.jpg")
            img_path = make_synthetic_image("input.jpg")

    original = load_image(img_path)
    print(f"Loaded image: {img_path}  shape={original.shape}")

    while True:
        print(SPATIAL_MENU + GEOM_MENU + EXIT_MENU)
        choice = input("Select an option: ").strip()

        if choice == "0":
            print("Goodbye!")
            break

        elif choice == "1":
            beta = ask_int("Brightness offset beta (-255..255)", 50)
            out = brightness_adjustment(original, beta)
            show_pair(original, out, f"Brightness Adjustment (beta={beta})")

        elif choice == "2":
            alpha = ask_float("Contrast gain alpha (0.0..3.0)", 1.5)
            out = contrast_adjustment(original, alpha)
            show_pair(original, out, f"Contrast Adjustment (alpha={alpha})")

        elif choice == "3":
            out = image_negative(original)
            show_pair(original, out, "Image Negative")

        elif choice == "4":
            out = log_transform(original)
            show_pair(original, out, "Log Transformation")

        elif choice == "5":
            gamma = ask_float("Gamma value (e.g. 0.4=brighten, 2.5=darken)", 0.5)
            out = gamma_transform(original, gamma)
            show_pair(original, out, f"Gamma Transformation (gamma={gamma})")

        elif choice == "6":
            t = ask_int("Threshold T (0..255)", 127)
            out = thresholding(original, t, 255)
            show_pair(cv2.cvtColor(original, cv2.COLOR_RGB2GRAY) if original.ndim == 3 else original,
                       out, f"Thresholding (T={t})", cmap="gray")

        elif choice == "7":
            r1 = ask_int("r1 (input control point 1)", 70)
            s1 = ask_int("s1 (output for r1)", 0)
            r2 = ask_int("r2 (input control point 2)", 180)
            s2 = ask_int("s2 (output for r2)", 255)
            out = contrast_stretching(original, r1, s1, r2, s2)
            show_pair(original, out, "Contrast Stretching")

        elif choice == "8":
            run_spatial_all(original)

        elif choice == "9":
            tx = ask_int("Translate tx (pixels, x-axis)", 40)
            ty = ask_int("Translate ty (pixels, y-axis)", 30)
            out = translation(original, tx, ty)
            show_pair(original, out, f"Translation (tx={tx}, ty={ty})")

        elif choice == "10":
            sx = ask_float("Scale factor sx", 1.5)
            sy = ask_float("Scale factor sy", 1.5)
            out = scaling(original, sx, sy)
            show_pair(original, out, f"Scaling (sx={sx}, sy={sy})")

        elif choice == "11":
            angle = ask_float("Rotation angle (degrees, CCW+)", 45)
            out = rotation(original, angle)
            show_pair(original, out, f"Rotation ({angle} deg)")

        elif choice == "12":
            out = horizontal_reflection(original)
            show_pair(original, out, "Horizontal Reflection")

        elif choice == "13":
            out = vertical_reflection(original)
            show_pair(original, out, "Vertical Reflection")

        elif choice == "14":
            out = reflection_about_origin(original)
            show_pair(original, out, "Reflection about Origin")

        elif choice == "15":
            shx = ask_float("Shear factor along x (shx)", 0.3)
            out = shear_x(original, shx)
            show_pair(original, out, f"Shear X (shx={shx})")

        elif choice == "16":
            shy = ask_float("Shear factor along y (shy)", 0.3)
            out = shear_y(original, shy)
            show_pair(original, out, f"Shear Y (shy={shy})")

        elif choice == "17":
            out = affine_transform(original)
            show_pair(original, out, "Affine Transformation")

        elif choice == "18":
            run_geom_all(original)

        else:
            print("Invalid option, please choose again.")


if __name__ == "__main__":
    main()
