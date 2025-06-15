# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Flask-based web application that calculates optimal climbing routes and times between mountain locations using Dijkstra's shortest path algorithm. The application is designed for Taiwan mountain climbing routes.

## Core Architecture

- **Backend**: Flask web server (`app.py`) with REST API endpoints
- **Frontend**: Single-page HTML application with vanilla JavaScript (`templates/index.html`)
- **Data**: Graph data stored in text files (`graphs/` directory) representing mountain locations and travel times
- **Algorithm**: Custom `MountainGraph` class implementing Dijkstra's algorithm for shortest path calculation

## Key Components

### MountainGraph Class
- Loads graph data from text files with format: `start_location end_location time1 time2`
- Implements bidirectional graphs (both directions with potentially different times)
- Uses Dijkstra's algorithm for shortest path calculation between locations

### API Endpoints
- `GET /api/locations` - Returns all available mountain locations
- `POST /api/calculate` - Calculates shortest path between two locations
- `GET /api/load_graph/<graph_name>` - Loads a specific graph file dynamically

## Common Development Commands

### Running the Application
```bash
python app.py
```
The app runs on http://127.0.0.1:5000 by default with debug mode enabled.

### Installing Dependencies
```bash
pip install -r requirements.txt
```

### Running Tests
```bash
python test_app.py
```
Note: The Flask app must be running on port 5000 for tests to work.

## Data Format

Graph files in `graphs/` directory use this format:
```
location1 location2 time_forward time_backward
```
- Times are in minutes
- Location names can contain spaces and Chinese characters
- Bidirectional edges are created automatically

## Development Notes

- The application defaults to loading `graphs/G02.txt` on startup
- Graph data can be switched dynamically via the `/api/load_graph` endpoint
- All location names are stored and handled as strings, supporting Unicode characters
- Error handling includes validation for missing locations and unreachable paths