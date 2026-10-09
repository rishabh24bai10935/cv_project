# Project Statement: Security Camera System Using Computer Vision

## 1. Project Title
**Real-Time Security Camera System Using Python and OpenCV**

## 2. Problem Statement
Monitoring an area continuously requires attention and time, making manual surveillance less convenient. This project explores a computer vision-based approach to automate basic surveillance by identifying visible faces and full-body figures through a webcam and recording video when either is detected.

## 3. Project Objective
The main objective is to develop a webcam-based security application that combines real-time visual detection with automatic video recording. The system aims to reduce the need for continuous manual monitoring and maintain timestamped video files for later review.

## 4. Proposed Solution
The application uses Python and OpenCV to process webcam frames continuously. Haar Cascade classifiers are used to detect faces and full-body figures. When either type of detection occurs, the application starts saving video frames to an MP4 file. If detection disappears, recording continues for an additional five seconds before stopping.

Detected regions are marked with rectangles in the live camera window, allowing the user to observe the system's output in real time.

## 5. Scope of the Project
The project demonstrates the practical application of introductory computer vision techniques in a basic surveillance scenario. It includes live camera monitoring, face and body detection, event-triggered video recording, timestamp-based file naming, and a user-controlled exit option.

The current implementation is intended for educational purposes. Its detection accuracy depends on factors such as lighting, camera position, visibility, and the limitations of Haar Cascade classifiers.

## 6. Expected Outcome
The expected result is a working prototype that monitors a camera feed, highlights detected faces and bodies, and automatically stores video recordings when detection occurs. This project provides practical experience with image processing, object detection, video handling, and automation using Python.

## 7. Conclusion
This project demonstrates how computer vision can support basic automated surveillance. By combining webcam input, Haar Cascade detection, and conditional video recording, it provides a foundation for exploring more advanced security applications.
