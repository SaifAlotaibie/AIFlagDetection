
# AIFlagDetection

## Overview
**AIFlagDetection** is a Python-based project that uses AI to detect flags in real-time from a live camera feed. It sends frames to a machine learning model hosted on Nyckel to classify the flags and display relevant information on the screen.

## Features
- **Real-time flag detection** using OpenCV and a machine learning model.
- **Supports multiple flags**, including but not limited to Saudi Arabia, Egypt, UAE, and more.
- **Displays country-specific information** when a flag is recognized.
- **Easy integration** with custom models on Nyckel.

## Setup

### Requirements
Make sure you have the following dependencies installed:

- `opencv-python`
- `pygame`
- `requests`
- `json`
- `time`
- `logging`

You can install them using pip:

```bash
pip install opencv-python pygame requests
```

### Clone the Repository

To clone this project, run:

```bash
git clone https://github.com/your-username/AIFlagDetection.git
cd AIFlagDetection
```

### Running the Project

Run the script to start detecting flags from your live camera feed:

```bash
python script.py
```

### Files

- **script.py**: Main file that captures video, processes it, and sends frames to the AI model.
- **anthems/**: A folder that stores national anthems (optional, can be removed if not used).
- **app.log**: Log file for debugging and tracking issues during execution.

## Usage

1. **Flag Recognition**: The script captures frames from your camera and sends them to the Nyckel model for flag classification.
2. **Information Display**: Based on the recognized flag, the script displays information about the country on the video feed.
3. **Error Handling**: Logs all interactions with the model and any errors in `app.log`.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributions
Feel free to open issues or submit pull requests if you want to improve this project.
