# FTiAD23-Python-Linux_hw2
Python&amp;Linux Homework 2 calculator API

# Calculator App

This simple calculator app allows you to perform mathematical calculations through a RESTful API.

## Installation

1. Install the required dependencies by running the following command in your console:

    ```bash
    pip install -r /path/to/requirements.txt
    ```

2. Run the calculator app using the following command:

    ```bash
    python calculator.py
    ```

## Usage

You can make calculations by sending a JSON payload to the API endpoint using `curl`. Here's an example:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"expression": "(-3+4)*-3/15)"}' http://127.0.0.1:5000/calculate
