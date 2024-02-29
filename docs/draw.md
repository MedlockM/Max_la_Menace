## `find_all_paths` Function

This function finds all paths from the start station to the end station with a maximum number of hops.

- **Parameters**
    - `G` (networkx.Multigraph): The multigraph representing the train network.
    - `start_station` (str): The name of the start station.
    - `end_station` (str): The name of the end station.
    - `max_hops` (int): The maximum number of hops allowed for the paths.
- **Returns**
    - `all_paths` (list): A list of all paths from the start station to the end station.
- **Errors/Exceptions**
    - None.