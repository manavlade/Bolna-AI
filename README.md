# OpenAI Status Tracker

A lightweight, efficient Python script to track real-time service status updates, incidents, and outages from the [OpenAI Status Page](https://status.openai.com/).

## Features

- **No External Dependencies**: Uses only Python's standard library (`urllib`, `json`, `time`, `datetime`).
- **Efficient Polling**: Implements Conditional GET requests (ETags/Last-Modified) to minimize bandwidth and only parse data when changes occur.
- **Real-time Alerts**: Detects and prints new maintainance updates, incidents, or outages to the console as they happen.
- **Duplicate Prevention**: Tracks processed update IDs to ensure each alert is shown only once.

## Requirements

- Python 3.7+

## Installation

1. Clone or download this repository.
2. Navigate to the directory:
   ```bash
   cd openai_status_tracker
   ```

## Usage

Run the script directly using Python:

```bash
python tracker.py
```

The tracker will start and print a confirmation message. It will then run indefinitely, checking for updates every 60 seconds.

**Example Output:**

```text
Starting OpenAI Status Tracker...
Tracking: https://status.openai.com/api/v2/incidents.json
Press Ctrl+C to stop.

[2024-05-20 10:00:00] Tracker Initialized. Waiting for updates...
[2024-05-20 10:15:30] Product: API
Status: investigating - We are investigating reports of elevated error rates.
----------------------------------------
```

## Configuration

You can modify the configuration variables at the top of `tracker.py`:

- **STATUS_URL**: The endpoint for the status JSON (default: official OpenAI Status API).
- **CHECK_INTERVAL**: Time in seconds between checks (default: `60`).

## License

This project is open-source and available under the MIT License.
