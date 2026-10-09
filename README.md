# Security Camera System

A Python-based smart security camera system that detects faces and full bodies in real time using a webcam. The application automatically starts recording when motion is detected and stops after a few seconds of inactivity.

## Features

- Real-time face and body detection
- Automatic video recording on detection
- Stops recording after inactivity
- Saves recordings with timestamped filenames
- Live webcam monitoring

## Tech Stack

- Python
- OpenCV (`cv2`)
- Haar Cascade Classifiers
- `datetime`
- `time`

## Installation

Install the required dependency:

```bash
pip install opencv-python
```

## Usage

Run the script:

```bash
python main.py
```

- The webcam will open automatically.
- Recording starts when a face or body is detected.
- Recording stops after **5 seconds** of no detection.
- Press `q` to exit.

## Output

Recorded videos are automatically saved with timestamps:

```text
24-08-2025-14-30-15.mp4
```

## How It Works

- The webcam continuously scans for:
  - Faces
  - Full body detection
- When detection occurs:
  - Recording starts automatically
- If no face or body is detected:
  - The system waits for a few seconds before stopping recording

## Customization

To change the recording delay after detection stops:

```python
SECONDS_TO_RECORD_AFTER_DETECTON = 5
```

Example:

```python
SECONDS_TO_RECORD_AFTER_DETECTON = 10
```

## Project Structure

```text
SECURITY_CAMERA/
│── main.py
│── README.md
```
