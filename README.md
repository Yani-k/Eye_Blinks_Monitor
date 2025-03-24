# Intelligent Eye Blink Monitoring System

## Overview
This project implements an **Intelligent Eye Blink Monitoring System**, designed to track and analyze blinking rates to help prevent **Computer Vision Syndrome (CVS)**. The system detects blinks using **computer vision techniques** and provides real-time feedback via an **LCD display, buzzer, and LED indicators**. It also logs blink data into a **Google Spreadsheet** for further analysis.

## Project Contribution
I was **solely responsible for the coding** aspect of this project, developing the real-time blink detection system, hardware integration, and cloud-based data logging.

## Features
- **Real-time Blink Detection:** Uses OpenCV and dlib for facial landmark detection.
- **Blink Rate Analysis:** Calculates blinking frequency and provides alerts when the rate is too low.
- **Hardware Integration:** Works with **LCD display, buzzer, and LED indicators** to provide visual and auditory feedback.
- **Cloud Data Storage:** Logs blink counts in **Google Sheets** for trend analysis.
- **Standalone System:** Runs on a **Raspberry Pi**, making it independent of the user’s computer.

## Technology Stack
- **Programming Language:** Python
- **Libraries Used:**
  - OpenCV (for face detection)
  - dlib (for facial landmark detection)
  - imutils (for image processing)
  - gspread (for Google Sheets API integration)
  - gpiozero (for controlling buzzer & LED)
  - drivers (for LCD display control)
- **Hardware Components:**
  - Raspberry Pi 4
  - Pi Camera Module
  - LCD Display (I2C 1602)
  - Buzzer and LED

## Installation and Setup
### **1. Clone the Repository**
```bash
git clone https://github.com/yourusername/eye-blink-monitor.git
cd eye-blink-monitor
```

### **2. Install Dependencies**
Ensure you have Python installed, then run:
```bash
pip install opencv-python imutils dlib numpy gspread gpiozero
```

### **3. Set Up Google Sheets API**
- Create a Google Cloud project and enable the Sheets API.
- Download your `keys.json` credentials file and place it in the project directory.

### **4. Run the Program**
```bash
python eye_blink_detection.py
```

## Research Paper
This project was published in the **Journal of Eye Movement Research** under the title:
**"Intelligent Standalone Eye Blinking Monitoring System for Computer Users"** (https://doi.org/10.16910/jemr.17.5.1).

The paper details the motivation, methodology, and impact of the system in addressing **Computer Vision Syndrome (CVS)**.

## Future Improvements
- **Enhanced Accuracy:** Reduce false blink detections by refining the **Eye Aspect Ratio (EAR)** thresholding.
- **Support for Eyeglass Users:** Improve detection under occlusion conditions.
- **Mobile Integration:** Develop an app for real-time monitoring and personalized alerts.


---
For any questions or contributions, feel free to reach out or submit a pull request!

