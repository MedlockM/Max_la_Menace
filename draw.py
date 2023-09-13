import requests
import networkx as nx
import pandas as pd
import datetime
from flask import Flask, render_template, request, session


date_user = '2023-05-30'
# Make the request to download the CSV file
url = "https://ressources.data.sncf.com/api/explore/v2.0/catalog/datasets/tgvmax/exports/csv"
params = {
'delimiter': ';',
'list_separator': ',',
'quote_all': 'false',
'with_bom': 'false'
}
response = requests.get(url, params=params, verify=False)

# Check if the request was successful
if response.status_code == 200:
    # Save the response content to a file
    with open("tgvmax-auto.csv", "wb") as file:
        file.write(response.content)
    print("CSV file downloaded successfully.")
else:
    print("Failed to download the CSV file.")

# Load the downloaded CSV file into a pandas DataFrame
df = pd.read_csv("tgvmax-auto.csv", sep=';', encoding='utf-8')
# Get a list of all unique station names

# Filter the DataFrame based on user input and 'od_happy_card' column
df = df[(df['od_happy_card'] == 'OUI') & (df['date'] == date_user)]

# Drop unnecessary columns
df.drop(columns=['date', 'od_happy_card'], inplace=True)

# Create an empty multigraph
G = nx.MultiDiGraph()
stations = set(df["origine"]).union(set(df["destination"]))

# Add each station as a node in the graph
for station in stations:
    G.add_node(station)

# Iterate through each row and create edges in the graph
for _, row in df.iterrows():
    origin = row["origine"]
    dest = row["destination"]
    train_no = row["train_no"]
    heure_depart = row["heure_depart"]
    heure_arrivee = row["heure_arrivee"]
    if datetime.datetime.strptime(heure_arrivee, '%H:%M').time() > datetime.datetime.strptime(heure_depart,
                                                                                              '%H:%M').time():
        G.add_edge(origin, dest, train_no=train_no, heure_depart=heure_depart, heure_arrivee=heure_arrivee,
                   train_nuit=False)



# Function to find all paths from the start station to the end station with a maximum number of hops
def find_all_paths(G, start_station, end_station, max_hops):
    # List to store all paths
    all_paths = []

    # Recursive function to explore the graph
    def dfs(current_station, hops, path):
        # Base case: we've reached the end station
        if current_station == end_station:
            all_paths.append(path)
            hops = 0
            return

        # Explore the neighbors of the current station
        #print(G.edges(current_station, keys=True))
        for departure, neighbor, key in G.edges(current_station, keys=True):
            #print(f'neighbord {neighbor} & key {key}')
            if neighbor not in [step[0] for step in path]:
                # Check if we've exceeded the maximum number of hops
                if hops < max_hops:
                    if hops != 0:
                        last_train_arrival_time = datetime.datetime.strptime(G[path[-2][0]][path[-1][0]][path[-1][2]]["heure_arrivee"], '%H:%M').time()
                    else:
                        last_train_arrival_time = datetime.datetime.strptime('00:00', '%H:%M').time()
                    current_train_departure_time = datetime.datetime.strptime(G[current_station][neighbor][key]["heure_depart"], '%H:%M').time()
                    # print(current_train_departure_time)
                    # print(last_train_arrival_time)
                    if current_train_departure_time > last_train_arrival_time:
                        print('next step found')
                        print()
                        print(path + [(neighbor, current_train_departure_time, key)])
                        dfs(neighbor, hops + 1, path + [(neighbor, current_train_departure_time, key)])

    # Call the recursive function starting from the start station
    dfs(start_station, 0, [(start_station, datetime.time(0, 0), 0)])

    return all_paths

# Example usage
start_station = "MARSEILLE ST CHARLES"
end_station = "LYON (intramuros)"
max_hops = 6
paths = find_all_paths(G, start_station, end_station, max_hops)
if paths:
    for path in paths:
        print(f"Path: {path}")
else:
    print("No paths found")

