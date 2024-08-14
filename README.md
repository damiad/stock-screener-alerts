# Stock Screener and Alerts

## Overview

This project provides a simple tool to fetch stock recommendations from various sources like Finnhub and Zacks. It calculates scores based on the recommendations and can send notifications via Pushover if a specified condition is met.

## Features

- **Fetch Stock Recommendations:** Get daily stock recommendations from Finnhub and Zacks.
- **Score Calculation:** Calculate scores for each stock based on the fetched recommendations.
- **Alerts:** Send alerts via Pushover if certain conditions are met.
- **Environment Variables:** Use a `.env` file to manage API keys and other sensitive information.

## Project Structure

```
project_root/
│
├── fetchers/
│   ├── finnhub.py
│   ├── zacks.py
│   └── # Future integrations
│
├── alerts/
│   ├── pushover.py
│   └── # Future integrations
│
├── main.py
├── .env
├── .gitignore
└── requirements.txt
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/damiad/stock-screener-alerts.git
cd stock-screener-alerts
```

### 2. Create and activate a virtual environment (optional but recommended)

```bash
python3 -m venv .venv
source .venv/bin/activate  
# On Windows use `.venv\Scripts\activate`
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your environment variables

Create a `.env` file in the project root and add the required variables according to the `.env.example` file:

### 5. Run the script

```bash
python3 main.py
```

## How It Works

- **Fetchers**: The `fetchers/` directory contains modules to fetch stock recommendations from different sources like Finnhub and Zacks. Each module has its own scoring algorithm.
  
- **Alerts**: The `alerts/pushover.py` module sends notifications via Pushover when triggered by the main script.

- **Main Script**: The `main.py` script fetches stock recommendations for a list of stock symbols, calculates scores, and optionally sends alerts based on the recommendations.

## Example Output

When you run `main.py`, you will see output similar to:

```
AAPL:
 finnhub: [{95.0, '2024-08-14'}, ...] 
 zacks: [{80, 'Aug 14, 2024 10:44 AM'}]

MSFT:
 finnhub: [{80.0, '2024-08-14'}, ...] 
 zacks: [{95, 'Aug 14, 2024 10:44 AM'}]

...
```

## Contributing

Feel free to submit issues or pull requests if you have any improvements or additional features you'd like to see.

## Contact

If you have any questions or suggestions, feel free to contact me at [Instagram: @dadabrowski](https://www.instagram.com/dadabrowski/).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Future Enhancements

- **Additional Data Sources**: Integration with SimplyWall Street, IEX, Yahoo Finance, etc.
- **Improved Scoring Algorithms**: Enhance the scoring methodology for better accuracy.
- **AWS Lambda Integration**: Set up the script to run on AWS Lambda and send alerts automatically.
- **Web Interface**: Add a simple web interface for non-developers to use the tool.
- **Error handling and query limit protections**: Add more robust error handling and logging.
