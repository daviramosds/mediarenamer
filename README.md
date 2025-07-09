# 📂 Media-Renamer

A Python script to recursively organize media files (photos, videos, and audio) within a directory, standardizing their names to the `YYYY-MM-DD_HHMMSS.ext` format.

## ✨ Features

-   **Recursive Renaming**: Scans the target directory and all its subdirectories.
-   **Smart Filtering**: Processes only image, video, and audio files based on their extensions, ignoring everything else.
-   **Dual Date Extraction**:
    1.  Attempts to extract the date from the filename itself (e.g., `IMG-20250709-WA0001.jpg`).
    2.  If not found, it falls back to using the file's modification date as a reliable alternative.
-   **Modern CLI**: Uses the `rich` library to provide an enhanced user experience in the terminal, including:
    -   A real-time progress bar.
    -   Color-coded output for easily identifying status.
    -   A clean summary table at the end of the operation.
-   **Simulation Mode (`DRY_RUN`)**: Allows you to run the script to see what changes would be made without actually altering any files.
-   **Detailed Logging**: Generates a comprehensive `log.txt` file that categorizes all actions (renamed, already correct, skipped).

## 🚀 Getting Started

Follow the steps below to set up and run the script.

### Prerequisites

-   Python 3.x

### Installation

This script depends on the `rich` library. Install it using pip:

```bash
pip install rich
```

### How to Use

**Step 1: Configure the Script**

Open the script file (`rename.py` or whatever you named it) in a text editor and configure the two variables at the top:

1.  `TARGET_DIR`: Set the full path to the folder you want to organize.
    ```python
    # Example for Windows:
    TARGET_DIR = Path('C:/Users/YourUser/Desktop/My Photos')

    # Example for Linux/macOS:
    TARGET_DIR = Path('/home/YourUser/Pictures')
    ```

2.  `DRY_RUN`: Define how the script should operate.
    -   `DRY_RUN = True`: **(Recommended for first use)** The script will **not** rename any files. It will only analyze everything and generate a `log.txt` file showing the actions it *would* have taken.
    -   `DRY_RUN = False`: The script will perform the renaming operations permanently.

**Step 2: Run the Script**

1.  Open your terminal or command prompt.
2.  Navigate to the folder where you saved the script.
3.  Run the command:
    ```bash
    python rename.py
    ```

**Step 3: Analyze the Results**

1.  After running with `DRY_RUN = True`, open the `log.txt` file that was created in the same folder as the script.
2.  Check if the proposed renames are correct. Pay special attention to files that will be renamed using their modification date.
3.  If everything looks as expected, change the variable to `DRY_RUN = False` in the script and run it again to apply the changes permanently.

## 📋 Log File Structure (`log.txt`)

The log file is divided into sections for easy verification:

-   **`# RENAMED FILES`**: Shows the files that had their names changed.
-   **`# FILES ALREADY NAMED CORRECTLY`**: Lists the files that were already in the standard format and did not need to be changed.
-   **`# SKIPPED OR ERRORED FILES`**: Includes media files that could not be processed due to a lack of valid date information or an error during the process.
