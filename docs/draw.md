## Code Explanation

This code demonstrates how to download a CSV file from an API, load it into a pandas DataFrame, and perform graph operations using the NetworkX library.

1. Import necessary libraries:
   - `requests` for making HTTP requests to download the CSV file.
   - `networkx` as `nx` for creating and manipulating graphs.
   - `pandas` as `pd` for working with tabular data.
   - `datetime` for dealing with date and time operations.
   - `Flask` for building web applications.

2. Set the date for user input.

3. Make an HTTP request to download a CSV file from a specific URL using the `requests.get()` function. The response is saved in the `response` variable.

4. Check if the request was successful by verifying the status code of the response. If it is 200, save the response content to a file named "tgvmax-auto.csv". If it is not 200, print a failure message.

5. Load the downloaded CSV file into a pandas DataFrame using the `pd.read_csv()` function. The parameters `sep=';'` and `encoding='utf-8'` are provided to specify the delimiter and encoding of the CSV file, respectively.

6. Filter the DataFrame based on user input and specific columns.

7. Drop unnecessary columns from the DataFrame using the `df.drop()` function.

8. Create an empty multigraph using `nx.MultiDiGraph()`.

9. Get a set of all unique station names from the "origine" and "destination" columns of the DataFrame.

10. Add each station as a node in the graph using the `G.add_node(station)` function.

11. Iterate through each row of the DataFrame and create edges in the graph using the `G.add_edge()` function.

12. Define a function named `find_all_paths()` to find all paths from the start station to the end station with a maximum number of hops.

13. In the `find_all_paths()` function:
   - Declare an empty list to store all paths.
   - Define a recursive inner function named `dfs()` to explore the graph.
   - In the `dfs()` function:
     - Base case: if the current station is the end station, append the current path to the list of all paths and reset the number of hops.
     - Explore the neighbors of the current station by iterating through the outgoing edges using the `G.edges()` function.
     - Check if the neighbor station has not been visited previously in the current path.
     - Check if the number of hops is less than the maximum allowed hops.
     - Compare the departure and arrival times of the current train with the previous train to ensure a valid connection between stations.
     - Recursively call the `dfs()` function with the neighbor station, incremented hops, and updated path.
   - Call the `dfs()` function starting from the start station with initial hops as 0 and the path containing only the start station.

14. Return the list of all paths.

15. Example usage:
   - Set the start station, end station, and maximum number of hops.
   - Call the `find_all_paths()` function with the defined parameters.
   - If paths are found, print each path. Otherwise, print a message indicating that no paths were found.

---

## Example Output

Path: [('MARSEILLE ST CHARLES', datetime.time(0, 0), 0), ('AVIGNON TGV', datetime.time(15, 58), 0), ('LYON PART DIEU', datetime.time(17, 54), 0), ('LYON PERRACHE', datetime.time(19, 0), 0), ('〇 LYON (intramuros)', datetime.time(19, 2), 0), ('〇 LYON (...)
Path: [('MARSEILLE ST CHARLES', datetime.time(0, 0), 0), ('AVIGNON TGV', datetime.time(15, 58), 0), ('LYON PART DIEU', datetime.time(17, 54), 0), ('LYON PERRACHE', datetime.time(19, 0), 0), ('〇 LYON (intramuros)', datetime.time(19, 2), 1), ('LYON ((...)
Path: [('MARSEILLE ST CHARLES', datetime.time(0, 0), 0), ('AVIGNON TGV', datetime.time(15, 58), 0), ('LYON PART DIEU', datetime.time(17, 54), 0), ('LYON PERRACHE', datetime.time(19, 0), 0), ('〇 LYON (intramuros)', datetime.time(19, 2), 1), ('LYON ((...)
... (truncated for brevity)