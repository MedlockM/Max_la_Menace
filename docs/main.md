# Flask App

This is a Flask web application that allows users to search for train paths between two stations. It uses the `pandas` library to read train data from a CSV file, and the `networkx` library to represent the train network as a graph.

## Installation

To run this app, you need to have Flask, pandas, networkx, and requests installed. You can install them using the following command:

```shell
pip install flask pandas networkx requests
```

## Usage

To run the app, execute the following command in your terminal:

```shell
python app.py
```

This will start the Flask development server, and the app will be available at `http://localhost:5000`.

## API Endpoints

### `/`

This endpoint displays the home page of the app. It renders the `index.html` template and passes a list of station names to the template.

### `/search`

This endpoint is triggered when the user submits the search form on the home page. It reads the user's inputs and performs a search for train paths between the specified start and end stations. 

The train data is downloaded from the SNCF API and stored in a pandas DataFrame. The search is then performed using the `find_all_paths()` function, which uses a recursive depth-first search algorithm to explore the train network graph.

The search results are rendered in the `search.html` template and displayed to the user.

## Function: `find_all_paths()`

This function takes in a network graph `G`, a start station name, an end station name, and the maximum number of hops, and returns a list of all paths between the start and end stations within the specified maximum number of hops.

It uses a recursive depth-first search algorithm to explore the graph and find all possible paths. The algorithm keeps track of the number of hops made so far and the path taken. When the end station is reached, the current path is added to the list of all paths found.

## Templates

The app uses two HTML templates: `index.html` and `search.html`.

The `index.html` template displays a form for the user to enter their search criteria, and a dropdown menu to select the start and end stations.

The `search.html` template displays the search results in a table format.

## Dependencies

This app has the following dependencies:

- Flask: A micro web framework for Python
- pandas: A library for data manipulation and analysis
- networkx: A library for the creation, manipulation, and study of the structure, dynamics, and functions of complex networks
- requests: A library for making HTTP requests