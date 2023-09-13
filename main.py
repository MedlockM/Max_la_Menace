from flask import Flask, render_template, request
import pandas as pd
import networkx as nx
import datetime
import requests

app = Flask(__name__)


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
        # print(G.edges(current_station, keys=True))
        for departure, neighbor, key in G.edges(current_station, keys=True):
            # print(f'neighbord {neighbor} & key {key}')
            if neighbor not in [step[0] for step in path]:
                # Check if we've exceeded the maximum number of hops
                if hops < max_hops:
                    if hops != 0:
                        last_train_arrival_time = datetime.datetime.strptime(
                            G[path[-2][0]][path[-1][0]][path[-1][2]]["heure_arrivee"], '%H:%M').time()
                    else:
                        last_train_arrival_time = datetime.datetime.strptime('00:00', '%H:%M').time()
                    current_train_departure_time = datetime.datetime.strptime(
                        G[current_station][neighbor][key]["heure_depart"], '%H:%M').time()
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


@app.route('/', methods=['GET'])
def index():
    stations = ['ROCAMADOUR PADIRAC', 'NANCY', 'REIMS', 'VENDOME VILLIERS SUR LOIR', 'CHATELLERAULT', 'ST GEORGES DE LUZENCON', 'MILLAU', 'FREIBURG BREISGAU HBF', 'BAR LE DUC', 'MUENCHEN HBF', 'CERBERE', 'EVIAN LES BAINS', 'GRAMAT', 'BEZIERS', 'MOUCHARD', 'ANTIBES', 'EMBRUN', 'THONON LES BAINS', 'PORT VENDRES VILLE', 'SELESTAT', 'LA BAULE ESCOUBLAC', 'NEVERS', 'LA ROCHELLE VILLE', 'CALAIS VILLE', 'LENS', 'PERPIGNAN', 'KARLSRUHE HBF', 'BRUXELLES MIDI BRUSSEL ZUID', 'FUTUROSCOPE', 'MODANE', 'LAVAL', 'MULHOUSE VILLE', 'CANNES', 'BESANCON VIOTTE', 'LUZENAC GARANOU', 'ST MALO', 'BEDARIEUX', 'LES ARCS DRAGUIGNAN', 'MEUSE TGV', 'LUCON', 'ANCENIS', 'MASSY TGV', 'CAUSSADE TARN ET GARONNE', 'SETE', "LE BOUSQUET D'ORB", 'TARASCON SUR ARIEGE', 'TGV HAUTE PICARDIE', 'LANDERNEAU', 'SEDAN', 'LYON (intramuros)', 'EPINAL', 'VITRY LE FRANCOIS GARE', 'CLERMONT FERRAND', 'AEROPORT CDG2 TGV ROISSY', 'LE POULIGUEN', 'ST JEAN DE MAURIENNE ARVAN', 'LAMBALLE', 'AURAY', 'ANNEMASSE', 'BANYULS SUR MER', 'FRANKFURT MAIN HBF', 'LIMOGES BENEDICTINS', 'POITIERS', 'BORDEAUX ST JEAN', 'ARGELES SUR MER', 'CHATEAUROUX', 'BELFORT-MONTBELIARD TGV', 'ST PIERRE DES CORPS', 'ANGOULEME', 'BETHUNE', 'MONTAUBAN VILLE BOURBON', 'METZ VILLE', 'TARBES', 'LA ROCHE SUR YON', 'QUIMPERLE', 'OFFENBOURG/OFFENBURG', 'NIMES', 'TOULON', 'ST GAUDENS', 'LUNEVILLE', 'AGEN', 'ST DENIS PRES MARTEL', 'TBD', 'BIARRITZ', 'SARREBOURG', 'REMIREMONT', 'PARIS (intramuros)', 'LYON-SAINT EXUPERY TGV', 'ISSOIRE', 'ISSOUDUN', 'VIERZON VILLE', 'BESANCON - F COMTE TGV', "L'ARGENTIERE LES ECRINS   (05)", 'SAVERNE', 'NURIEUX', 'ST RAPHAEL VALESCURE', 'AX LES THERMES', 'BAYONNE', 'BANASSAC LA CANOURGUE', 'CARMAUX', 'STRASBOURG', 'VITRE', 'ST ETIENNE CHATEAUCREUX', 'ARGENTON SUR CREUSE', 'CHAMBERY CHALLES LES EAUX', 'VICHY', "ST CHELY D'APCHER", 'CHALONS EN CHAMPAGNE', 'CAHORS', 'MASSIAC BLESLE', 'HAZEBROUCK', 'QUIMPER', 'TOURCOING', 'ST JEAN DE LUZ CIBOURE', 'MONTDAUPHIN GUILLESTRE', 'BREST', 'AIX EN PROVENCE TGV', "LES SABLES D'OLONNE", 'LES CABANNES', 'SEVERAC LE CHATEAU', 'ETAPLES LE TOUQUET', 'AIX LES BAINS LE REVARD', 'DOLE VILLE', 'ST FLOUR CHAUDES AIGUES', 'MONTBARD', 'FORBACH', 'AUBIN', 'SURGERES', 'LUXEMBOURG', 'MASSY PALAISEAU', 'GUINGAMP', 'PLOUARET TREGOR', 'TOULOUSE MATABIAU', 'DAX', 'LE CROISIC', 'MANNHEIM HBF', 'NICE VILLE', 'ELNE', 'UZERCHE', 'FRASNE', 'BOULOGNE VILLE', 'CAPDENAC', 'BRIANCON', 'VEYNES DEVOLUY', 'ULM HBF', 'ALBI VILLE', 'CAMPAGNAC ST GENIEZ', 'RENNES', 'COLMAR', 'DIJON VILLE', 'BADEN BADEN', 'CASTELNAUDARY', 'RANG DU FLIERS VERTON', 'ROUEN RIVE DROITE', 'LATOUR DE CAROL ENVEITG', 'LORIENT', 'ARCACHON', 'RETHEL', 'SABLE SUR SARTHE', 'CHAMPAGNE-ARDENNE', 'ST NAZAIRE', 'SOUILLAC', 'CRANSAC', 'AUMONT AUBRAC', 'NANTES', 'ARLES', 'MACON LOCHE TGV', 'ST ROME DE CERNON', 'BARCELONA SANTS', 'VANNES', 'ST DIE DES VOSGES', 'CALAIS FRETHUN', 'TOURNEMIRE ROQUEFORT', 'MONTREJEAU GOURDAN POLIGNAN', 'MANTES LA JOLIE', 'COLLIOURE', 'MACON VILLE', 'ORANGE', 'ROANNE', 'ROSPORDEN', 'RODEZ', 'MOULINS SUR ALLIER', 'GENEVE', 'FACTURE BIGANOS', 'BOURG EN BRESSE', 'AGDE', 'MIRAMAS', 'LORRAINE TGV', 'ST MAIXENT DEUX SEVRES', 'CHARLEVILLE MEZIERES', 'MARMANDE', 'MAGALAS', 'FIGUERES VILA TGV', 'VERSAILLES CHANTIERS', 'ST CHRISTOPHE', 'MONTPELLIER SUD DE FRANCE', 'BOURGES', 'BASEL SBB', 'VIVIEZ DECAZEVILLE', 'CLISSON', 'BRASSAC LES MINES STE FLORINE', 'CHORGES', 'LANNION', 'ANNECY', 'SAUMUR', 'VALENCE VILLE', 'OULX CESANA CLAV SESTRIERE', 'LIBOURNE', 'CARCASSONNE', 'BEAUNE', 'TORINO PORTA SUSA', 'LANNEMEZAN', 'AUTERIVE', 'FOIX', 'KAISERSLAUTERN HBF', 'LILLE (intramuros)', 'ROCHEFORT', 'PAMIERS', 'LEZIGNAN-CORBIERES', 'JONZAC', 'LE CREUSOT MONTCEAU MONTCHANIN', 'PAU', 'MARVEJOLS', 'DOUAI', 'MERENS LES VALS', 'LA TESTE', 'MONTELIMAR GARE SNCF', 'NARBONNE', 'ARRAS', 'RIOM CHATEL GUYON', 'AUGSBURG HBF', 'DUNKERQUE', 'MARSEILLE BLANCARDE', 'PORNICHET', 'CREST', 'ST BRIEUC', 'LES AUBRAIS ORLEANS', 'ASSIER', 'CROIX WASQUEHAL', 'RINGSHEIM/EU-PARK', 'CHALON SUR SAONE', 'STUTTGART HBF', 'SARREBRUCK/SAARBRUECKEN', 'SAINTES', 'ARVANT', 'ROUBAIX', 'LE MONASTIER', 'SAVERDUN', 'ORTHEZ', 'GAP', 'DIE', 'HENDAYE', 'LUC EN DIOIS', 'MILANO P GARIBALDI', 'BRIVE LA GAILLARDE', 'MARNE LA VALLEE CHESSY', 'NIMES PONT DU GARD', 'BELLEGARDE', 'VALENCIENNES', 'DOL DE BRETAGNE', 'GRENOBLE', 'MONTPELLIER SAINT-ROCH', 'TOURS', 'CEILHES ROQUEREDONDE', 'GOURDON', 'REDON', 'ZUERICH HB', 'ST GERMAIN DES FOSSES', 'VALLORBE', 'AVIGNON TGV', 'LA SOUTERRAINE', 'VALENCE TGV RHONE-ALPES SUD', 'THIONVILLE', 'LAUSANNE', 'AVIGNON CENTRE', 'ALBI MADELEINE', 'LE HAVRE', 'MORLAIX', 'NEUSSARGUES', 'MARSEILLE ST CHARLES', 'PORTE PUYMORENS', 'FIGEAC', 'GIRONA', 'LOURDES', 'HYERES', 'LAHR SCHWARZW', 'LE MANS', 'ANGERS ST LAUD', 'NIORT', "ANDORRE - L'HOSPITALET"]
    sorted_stations = sorted(stations)
    return render_template('index.html', stations=sorted_stations)


@app.route('/search', methods=['POST'])
def search():
    date_user = request.form['date']
    start_station = request.form['start_station']
    end_station = request.form['end_station']
    max_hops = int(request.form['max_hops'])
    print('max hops :', max_hops)
    # Download the CSV file from the API URL and build the dataframe
    url = "https://ressources.data.sncf.com/api/explore/v2.0/catalog/datasets/tgvmax/exports/csv?delimiter=%3B&list_separator=%2C&quote_all=false&with_bom=false"
    params = {
        'delimiter': ';',
        'list_separator': ',',
        'quote_all': 'false',
        'with_bom': 'false'
    }
    #response = requests.get(url, params=params, verify=False)

    df = pd.read_csv(url, sep=';')
    print(df)
    print(df[df['date']=="2023-06-28"])
    print(df[df['date']=="2023-06-16"])
    # Filter the dataframe based on user inputs and desired criteria
    df = df[(df['date'] == date_user) & (df['od_happy_card'] == 'OUI')]

    # Drop unnecessary columns
    df.drop(['date', 'od_happy_card'], axis=1, inplace=True)
    print(df)
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

    # Call the find_all_paths() function
    paths = find_all_paths(G, start_station, end_station, max_hops)

    return render_template('search.html', paths=paths)


if __name__ == '__main__':
    app.run(debug=True)
