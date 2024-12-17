import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from mpl_toolkits.axes_grid1 import make_axes_locatable
from sklearn.cluster import KMeans

    
        
def map(normalized_cluster_data):
    us_map = gpd.read_file("https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json")
    us_map.rename(columns={'name': 'state'}, inplace=True)

    state_cluster_map = []  
    cluster_list = []  
    
    for cluster_label, cluster_data in normalized_cluster_data.items():
        top_states = cluster_data.nlargest(10).index.tolist()  
        cluster_list.append(top_states)

    for cluster_id, states in enumerate(cluster_list):
        for state in states:
            state_cluster_map.append({'state': state, 'cluster': cluster_id})

    state_cluster_df = pd.DataFrame(state_cluster_map)
    
    draw_map_cluster(us_map, state_cluster_df)
    
    draw_map_reduced(us_map, state_cluster_df, cluster_list)
    
    dbscan_map(us_map)

    return


def draw_map_cluster(us_map, state_cluster_df):

    merged_map = us_map.merge(state_cluster_df, how='left', left_on='state', right_on='state')

    ax = merged_map.plot(column='cluster', cmap='tab20', figsize=(15, 10), legend=True)
    ax.set_title("US States by Cluster", fontsize=16)
    ax.axis('off')
    plt.show()

    return
    
    
def draw_map_reduced(us_map, state_cluster_df, cluster_list):
    
    state_cluster_df_copy = state_cluster_df
    
    unique_states = list({state for cluster in cluster_list for state in cluster})
    cluster_matrix = []

    for cluster in cluster_list:
        cluster_vector = [1 if state in cluster else 0 for state in unique_states]
        cluster_matrix.append(cluster_vector)

    cluster_df = pd.DataFrame(cluster_matrix, columns=unique_states)

    #not gonna import from elbow from kMeans to avoid circular imports
    inertia = []
    K_range = range(2, 15)
    for k in K_range:
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(cluster_df)
        inertia.append(kmeans.inertia_)

    plt.figure(figsize=(8, 4))
    plt.plot(K_range, inertia, 'bx-')
    plt.xlabel('Number of clusters K')
    plt.ylabel('Inertia')
    plt.title('Elbow Method for Optimal K')
    plt.show()

    reduced_kmeans = KMeans(n_clusters=6, random_state=42)  # Adjust `n_clusters` as needed
    cluster_df['reduced_cluster'] = reduced_kmeans.fit_predict(cluster_df)

    reduced_cluster_map = dict(zip(range(len(cluster_list)), cluster_df['reduced_cluster']))
    
    state_cluster_df_copy['reduced_cluster'] = state_cluster_df_copy['cluster'].map(reduced_cluster_map)

    merged_map = us_map.merge(state_cluster_df_copy, how='left', on='state')

    fig, ax = plt.subplots(figsize=(12, 8))
    merged_map.plot(column='reduced_cluster', cmap='tab10', legend=True, ax=ax)
    ax.set_title('US Map with Reduced Clusters', fontsize=15)
    plt.show()
    
    return


def dbscan_map(us_map):

    cluster_data = {
        -1: ['North Dakota', 'Delaware', 'Nebraska', 'Mississippi', 'Arkansas', 'Hawaii', 'Rhode Island', 'Oregon', 'Alabama', 'Vermont'],
        0: ['New Mexico', 'Massachusetts', 'Montana', 'Washington', 'Rhode Island', 'New Hampshire', 'California', 'New Jersey', 'Alaska', 'Oregon'],
        1: ['Wyoming', 'Alaska', 'Louisiana', 'Oregon', 'Colorado', 'Vermont', 'Montana', 'Arizona', 'Utah', 'Pennsylvania'],
        2: ['Montana', 'Hawaii', 'Georgia', 'Colorado', 'Wyoming', 'West Virginia', 'California', 'South Carolina', 'Pennsylvania', 'Utah'],
        3: ['Wisconsin', 'Illinois', 'Montana', 'Iowa', 'Vermont', 'Minnesota', 'Wyoming', 'South Dakota', 'Utah', 'Missouri'],
        4: ['Utah', 'Delaware', 'Maine', 'Virginia', 'Hawaii', 'Pennsylvania', 'Arizona', 'North Carolina', 'Idaho', 'New York'],
        5: ['Hawaii', 'Maine', 'Utah', 'Massachusetts', 'Connecticut', 'Rhode Island', 'Alaska', 'Idaho', 'New Hampshire', 'New York'],
        6: ['Wisconsin', 'Minnesota', 'New Hampshire', 'South Dakota', 'West Virginia', 'Illinois', 'Montana', 'Connecticut', 'Rhode Island', 'Tennessee'],
        7: ['Wisconsin', 'Minnesota', 'Illinois', 'Iowa', 'Indiana', 'Alaska', 'South Dakota', 'Colorado', 'Missouri', 'Montana'],
        8: ['South Dakota', 'Minnesota', 'North Dakota', 'Iowa', 'Texas', 'Louisiana', 'Missouri', 'Tennessee', 'Indiana', 'New Jersey'],
        9: ['South Dakota', 'Wisconsin', 'Iowa', 'North Dakota', 'Nebraska', 'Minnesota', 'Michigan', 'Indiana', 'Illinois', 'Nevada'],
        10: ['South Dakota', 'Utah', 'Wisconsin', 'Minnesota', 'Iowa', 'Illinois', 'West Virginia', 'Nebraska', 'Indiana', 'Oklahoma'],
        11: ['Mississippi', 'Wisconsin', 'Alaska', 'Washington', 'Oregon', 'South Carolina', 'Georgia', 'Iowa', 'Tennessee', 'Florida'],
        12: ['Michigan', 'Nevada', 'Washington', 'West Virginia', 'North Carolina', 'Florida', 'Nebraska', 'Virginia', 'Maryland', 'Texas'],
        13: ['North Dakota', 'Washington', 'Maine', 'Wyoming', 'Idaho', 'Nevada', 'Rhode Island', 'New Hampshire', 'California', 'Alaska'],
        14: ['Mississippi', 'Maine', 'Kentucky', 'West Virginia', 'Tennessee', 'Florida', 'North Dakota', 'Michigan', 'Missouri', 'Iowa'],
        15: ['Arkansas', 'Montana', 'South Dakota', 'Mississippi', 'Utah', 'Louisiana', 'Kansas', 'West Virginia', 'Tennessee', 'North Dakota'],
        16: ['Washington', 'West Virginia', 'Alaska', 'Oregon', 'New Mexico', 'Nebraska', 'Georgia', 'Delaware', 'Montana', 'Florida'],
        17: ['Georgia', 'Alabama', 'South Carolina', 'Tennessee', 'North Carolina', 'Florida', 'Mississippi', 'Delaware', 'Nebraska', 'Idaho'],
        18: ['California', 'New Mexico', 'North Dakota', 'Nevada', 'Hawaii', 'Arizona', 'Idaho', 'Vermont', 'Alaska', 'North Carolina'],
        19: ['Washington', 'Louisiana', 'Idaho', 'West Virginia', 'Oregon', 'Vermont', 'Arizona', 'Montana', 'Tennessee', 'Kentucky'],
        20: ['Wisconsin', 'Utah', 'Kansas', 'California', 'Arkansas', 'New Mexico', 'Nevada', 'Wyoming', 'Iowa', 'North Dakota'],
        21: ['Rhode Island', 'Oklahoma', 'South Dakota', 'Massachusetts', 'Arizona', 'Utah', 'Ohio', 'North Dakota', 'Missouri', 'Virginia'],
        22: ['Wyoming', 'Hawaii', 'Georgia', 'Tennessee', 'Arizona', 'Wisconsin', 'Iowa', 'New Hampshire', 'Texas', 'West Virginia'],
        23: ['West Virginia', 'Georgia', 'Mississippi', 'South Dakota', 'Tennessee', 'North Dakota', 'Florida', 'Maryland', 'Washington', 'Alabama'],
        24: ['Massachusetts', 'New Mexico', 'Georgia', 'Maine', 'Rhode Island', 'Alabama', 'Nebraska', 'Nevada', 'Vermont', 'New Hampshire'],
        25: ['South Dakota', 'Massachusetts', 'Rhode Island', 'Washington', 'New Hampshire', 'Utah', 'Idaho', 'Vermont', 'Oregon', 'Maine'],
        26: ['Mississippi', 'Louisiana', 'Oklahoma', 'Kentucky', 'Kansas', 'Utah', 'Vermont', 'Wyoming', 'Alabama', 'Rhode Island'],
        27: ['Louisiana', 'Mississippi', 'Missouri', 'Indiana', 'Iowa', 'Ohio', 'Rhode Island', 'Alabama', 'Nebraska', 'South Dakota'],
        28: ['Louisiana', 'Mississippi', 'Arkansas', 'Montana', 'Oklahoma', 'North Dakota', 'Texas', 'South Dakota', 'Tennessee', 'Michigan'],
        29: ['Arkansas', 'Massachusetts', 'Connecticut', 'Maine', 'New Hampshire', 'Rhode Island', 'Utah', 'Nebraska', 'Vermont', 'Michigan'],
        30: ['Hawaii', 'Michigan', 'Missouri', 'Delaware', 'California', 'Wyoming', 'Arizona', 'Alabama', 'Nebraska', 'South Carolina'],
        31: ['West Virginia', 'Louisiana', 'Hawaii', 'Utah', 'Nebraska', 'Tennessee', 'Alabama', 'Kentucky', 'Indiana', 'Arkansas'],
        32: ['Vermont', 'Montana', 'Arkansas', 'Kentucky', 'Mississippi', 'Tennessee', 'New Hampshire', 'Utah', 'Missouri', 'Indiana'],
        33: ['Idaho', 'Hawaii', 'Nevada', 'West Virginia', 'Oregon', 'Missouri', 'Louisiana', 'North Carolina', 'Arkansas', 'Florida'],
        34: ['Hawaii', 'Wyoming', 'West Virginia', 'Louisiana', 'Arizona', 'Indiana', 'Nevada', 'Rhode Island', 'Wisconsin', 'Pennsylvania'],
        35: ['Alaska', 'Oklahoma', 'Arkansas', 'Nebraska', 'Iowa', 'Connecticut', 'Minnesota', 'Kansas', 'Missouri', 'Alabama'],
        36: ['Hawaii', 'Alaska', 'Rhode Island', 'Maine', 'New Mexico', 'Wyoming', 'Missouri', 'Arizona', 'Georgia', 'Oregon'],
        37: ['North Dakota', 'Wyoming', 'South Dakota', 'Oklahoma', 'Louisiana', 'Kansas', 'Iowa', 'Montana', 'Minnesota', 'California'],
        38: ['Delaware', 'West Virginia', 'Utah', 'Arkansas', 'Kentucky', 'Vermont', 'South Dakota', 'Montana', 'Connecticut', 'Idaho'],
        39: ['West Virginia', 'Louisiana', 'Alabama', 'Kentucky', 'Indiana', 'Minnesota', 'Delaware', 'Mississippi', 'Nebraska', 'New York'],
        40: ['Washington', 'Wisconsin', 'Louisiana', 'Wyoming', 'Hawaii', 'Utah', 'Virginia', 'Texas', 'Mississippi', 'New York'],
        41: ['Louisiana', 'Idaho', 'Georgia', 'Washington', 'Oregon', 'Hawaii', 'Utah', 'Wisconsin', 'Mississippi', 'Colorado'],
        42: ['North Dakota', 'Delaware', 'West Virginia', 'Wyoming', 'New Hampshire', 'Nevada', 'Arkansas', 'Kansas', 'Mississippi', 'Nebraska'],
        43: ['Nebraska', 'California', 'Connecticut', 'New York', 'Utah', 'Maine', 'Arizona', 'New Jersey', 'West Virginia', 'Hawaii'],
        44: ['West Virginia', 'Louisiana', 'Mississippi', 'Rhode Island', 'New Mexico', 'Maine', 'Missouri', 'North Dakota', 'Arizona', 'Oregon'],
        45: ['Utah', 'North Dakota', 'Wyoming', 'Louisiana', 'Mississippi', 'Rhode Island', 'South Dakota', 'Montana', 'Indiana', 'Tennessee'],
        46: ['Mississippi', 'South Dakota', 'Nebraska', 'New Mexico', 'West Virginia', 'Rhode Island', 'Oklahoma', 'New Hampshire', 'Indiana', 'Alabama'],
        47: ['South Dakota', 'West Virginia', 'Colorado', 'Hawaii', 'New Mexico', 'Minnesota', 'Connecticut', 'Kansas', 'Maryland', 'Virginia'],
        48: ['Louisiana', 'West Virginia', 'Nevada', 'Virginia', 'Wisconsin', 'Oregon', 'Indiana', 'Maryland', 'Texas', 'Missouri'],
        49: ['Rhode Island', 'Louisiana', 'Michigan', 'Massachusetts', 'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado'],
        50: ['Maryland', 'Georgia', 'Minnesota', 'Florida', 'Wisconsin', 'Illinois', 'Alabama', 'Alaska', 'Arizona', 'Arkansas'],
        51: ['Arkansas', 'West Virginia', 'Wyoming', 'Indiana', 'Michigan', 'Mississippi', 'Georgia', 'New Mexico', 'Louisiana', 'New York'],
        52: ['Idaho', 'Oklahoma', 'Wyoming', 'North Dakota', 'Delaware', 'Mississippi', 'Georgia', 'Texas', 'North Carolina', 'Maine'],
        53: ['Montana', 'Wyoming', 'Nevada', 'Arkansas', 'Iowa', 'Missouri', 'Alabama', 'Mississippi', 'New Mexico', 'Connecticut'],
        54: ['Wisconsin', 'Minnesota', 'Illinois', 'New York', 'Pennsylvania', 'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California'],
        55: ['Arkansas', 'Georgia', 'Utah', 'Oklahoma', 'Mississippi', 'South Carolina', 'Oregon', 'Wyoming', 'Tennessee', 'Vermont'],
        56: ['Oregon', 'Arkansas', 'Delaware', 'Kansas', 'Mississippi', 'West Virginia', 'Louisiana', 'Connecticut', 'Maine', 'Kentucky'],
        57: ['Arkansas', 'North Dakota', 'Delaware', 'Montana', 'Mississippi', 'Louisiana', 'Tennessee', 'Rhode Island', 'Alabama', 'Michigan'],
        58: ['Hawaii', 'Alaska', 'Vermont', 'Missouri', 'Iowa', 'Maine', 'New Hampshire', 'Wisconsin', 'New Jersey', 'Illinois'],
        59: ['Indiana', 'Virginia', 'New Jersey', 'California', 'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'Colorado', 'Connecticut'],
        60: ['Idaho', 'West Virginia', 'Nebraska', 'Delaware', 'Arkansas', 'Alaska', 'Maine', 'South Carolina', 'Louisiana', 'Ohio'],
        61: ['North Dakota', 'Montana', 'Iowa', 'Alaska', 'Indiana', 'Oklahoma', 'Maine', 'Nevada', 'Idaho', 'Arkansas'],
        62: ['West Virginia', 'Delaware', 'Iowa', 'South Carolina', 'Tennessee', 'Oregon', 'Colorado', 'New Mexico', 'Connecticut', 'Louisiana'],
        63: ['West Virginia', 'Alabama', 'Nevada', 'Idaho', 'Arkansas', 'Delaware', 'New Jersey', 'Mississippi', 'New York', 'Tennessee'],
        64: ['Utah', 'Montana', 'Louisiana', 'Oklahoma', 'Iowa', 'Virginia', 'Maine', 'Ohio', 'Pennsylvania', 'Kansas'],
        65: ['Utah', 'Illinois', 'Iowa', 'Delaware', 'Indiana', 'Michigan', 'Wyoming', 'Minnesota', 'Nebraska', 'Wisconsin'],
        66: ['West Virginia', 'Arkansas', 'Kansas', 'Oklahoma', 'Indiana', 'New Hampshire', 'Nevada', 'Virginia', 'Minnesota', 'Oregon'],
        67: ['Montana', 'Nevada', 'Michigan', 'Delaware', 'Kansas', 'Maryland', 'Mississippi', 'Colorado', 'West Virginia', 'Indiana'],
        68: ['New Mexico', 'Louisiana', 'Maryland', 'Maine', 'Minnesota', 'Rhode Island', 'Wisconsin', 'New Jersey', 'Connecticut', 'Kentucky'],
        69: ['South Dakota', 'West Virginia', 'Oklahoma', 'Kentucky', 'Georgia', 'Rhode Island', 'Kansas', 'Florida', 'Alabama', 'Pennsylvania'],
        70: ['North Carolina', 'Maine', 'Idaho', 'Tennessee', 'West Virginia', 'Wisconsin', 'Oklahoma', 'Vermont', 'Connecticut', 'Minnesota'],
        71: ['Hawaii', 'Mississippi', 'Wyoming', 'Rhode Island', 'Oklahoma', 'Kansas', 'Arizona', 'Maine', 'Nevada', 'Idaho'],
        72: ['Kansas', 'Louisiana', 'Missouri', 'Georgia', 'North Carolina', 'Illinois', 'Massachusetts', 'Alabama', 'Alaska', 'Arizona'],
        73: ['Utah', 'Montana', 'Nevada', 'West Virginia', 'Mississippi', 'Indiana', 'North Carolina', 'Oklahoma', 'Wisconsin', 'New Hampshire'],
        74: ['Montana', 'Louisiana', 'North Dakota', 'New Hampshire', 'Vermont', 'Michigan', 'Missouri', 'West Virginia', 'Hawaii', 'Alabama'],
        75: ['Utah', 'Rhode Island', 'South Dakota', 'Oklahoma', 'Arkansas', 'Kentucky', 'Oregon', 'Wisconsin', 'Minnesota', 'Connecticut'],
        76: ['Oregon', 'Illinois', 'Virginia', 'Wisconsin', 'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado'],
        77: ['Hawaii', 'Alaska', 'Missouri', 'Mississippi', 'New Mexico', 'Kentucky', 'Louisiana', 'Maryland', 'Oklahoma', 'Tennessee'],
        78: ['Utah', 'Alaska', 'Oklahoma', 'Alabama', 'Idaho', 'Tennessee', 'Michigan', 'Delaware', 'New Mexico', 'Ohio'],
        79: ['South Carolina', 'North Carolina', 'Virginia', 'Florida', 'Washington', 'Massachusetts', 'New York', 'Alabama', 'Alaska', 'Arizona'],
        80: ['Utah', 'Delaware', 'Rhode Island', 'Alabama', 'West Virginia', 'Colorado', 'Vermont', 'New Hampshire', 'Pennsylvania', 'Nevada'],
        81: ['Iowa', 'Kentucky', 'Arizona', 'Florida', 'New York', 'Colorado', 'Washington', 'Michigan', 'Alabama', 'Alaska'],
        82: ['Kansas', 'Massachusetts', 'Washington', 'Michigan', 'Virginia', 'Minnesota', 'Ohio', 'Pennsylvania', 'Texas', 'Illinois'],
        83: ['South Carolina', 'Oregon', 'Massachusetts', 'New York', 'Illinois', 'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California'],
        84: ['Alabama', 'Georgia', 'Arizona', 'North Carolina', 'New Jersey', 'Pennsylvania', 'Alaska', 'Arkansas', 'California', 'Colorado'],
        85: ['Georgia', 'California', 'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'Colorado', 'Connecticut', 'Delaware', 'Florida'],
        86: ['Georgia', 'South Carolina', 'Mississippi', 'Alabama', 'Tennessee', 'Kentucky', 'Florida', 'Utah', 'Nebraska', 'Virginia'],
        87: ['Georgia', 'Maryland', 'Florida', 'Alabama', 'South Dakota', 'Pennsylvania', 'North Carolina', 'Virginia', 'Mississippi', 'New Mexico'],
        88: ['South Carolina', 'Kansas', 'Virginia', 'Texas', 'Michigan', 'Georgia', 'Colorado', 'Florida', 'Ohio', 'Wisconsin'],
        89: ['Vermont', 'Florida', 'Texas', 'New York', 'California', 'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'Colorado'],
        90: ['Arkansas', 'North Carolina', 'Michigan', 'Minnesota', 'New York', 'Alabama', 'Alaska', 'Arizona', 'California', 'Colorado'],
        91: ['Kansas', 'Tennessee', 'Oregon', 'Minnesota', 'New Jersey', 'Ohio', 'Wisconsin', 'Washington', 'Pennsylvania', 'Alabama'],
        92: ['Kentucky', 'North Carolina', 'Georgia', 'Ohio', 'Wisconsin', 'Texas', 'New York', 'Pennsylvania', 'California', 'Alabama'],
        93: ['Alabama', 'Nevada', 'Michigan', 'Kansas', 'Massachusetts', 'Virginia', 'Kentucky', 'Florida', 'Ohio', 'Missouri'],
        94: ['Alabama', 'Georgia', 'South Carolina', 'Tennessee', 'North Carolina', 'Kentucky', 'Florida', 'Wyoming', 'Mississippi', 'Louisiana'],
        95: ['Mississippi', 'Florida', 'Ohio', 'Texas', 'New York', 'California', 'Alabama', 'Alaska', 'Arizona', 'Arkansas'],
        96: ['Virginia', 'Texas', 'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware'],
        97: ['Arizona', 'Georgia', 'Massachusetts', 'Alabama', 'Alaska', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware'],
        98: ['Hawaii', 'Texas', 'California', 'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'Colorado', 'Connecticut', 'Delaware'],
        99: ['Maryland', 'Ohio', 'California', 'Illinois', 'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'Colorado', 'Connecticut'],
        100: ['West Virginia', 'Virginia', 'Massachusetts', 'Illinois', 'California', 'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'Colorado'],
        101: ['Rhode Island', 'Louisiana', 'Iowa', 'Georgia', 'Indiana', 'Virginia', 'Minnesota', 'Illinois', 'New York', 'Pennsylvania'],
        102: ['Oklahoma', 'Maine', 'Kansas', 'Alabama', 'New Hampshire', 'Kentucky', 'Oregon', 'Georgia', 'Virginia', 'Florida'],
        103: ['Alaska', 'Montana', 'Vermont', 'Maryland', 'Maine', 'New Hampshire', 'Iowa', 'Nevada', 'Idaho', 'Arkansas'],
        104: ['California', 'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia'],
        105: ['New Jersey', 'Minnesota', 'New York', 'Illinois', 'Pennsylvania', 'California', 'Alabama', 'Alaska', 'Arizona', 'Arkansas'],
        106: ['Wyoming', 'Alabama', 'New Hampshire', 'Indiana', 'Michigan', 'Virginia', 'Minnesota', 'New Jersey', 'Ohio', 'Massachusetts'],
        107: ['Delaware', 'Rhode Island', 'Pennsylvania', 'Oklahoma', 'Kansas', 'Michigan', 'Ohio', 'Massachusetts', 'North Carolina', 'Nevada'],
        108: ['Illinois', 'Massachusetts', 'Pennsylvania', 'California', 'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'Colorado', 'Connecticut'],
        109: ['Ohio', 'Maryland', 'Texas', 'Massachusetts', 'New York', 'California', 'Alabama', 'Alaska', 'Arizona', 'Arkansas'],
        110: ['Louisiana', 'Iowa', 'Texas', 'Missouri', 'Minnesota', 'Oregon', 'Indiana', 'Connecticut', 'Maryland', 'Georgia'],
        111: ['Maine', 'New York', 'California', 'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'Colorado', 'Connecticut', 'Delaware'],
        112: ['Kansas', 'Missouri', 'California', 'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'Colorado', 'Connecticut', 'Delaware'],
        113: ['Connecticut', 'Colorado', 'Michigan', 'Virginia', 'Illinois', 'Texas', 'Massachusetts', 'New York', 'California', 'Alabama'],
        114: ['Vermont', 'New York', 'California', 'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'Colorado', 'Connecticut', 'Delaware'],
        115: ['Hawaii', 'Kentucky', 'Connecticut', 'Michigan', 'Texas', 'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California'],
        116: ['Alaska', 'New Hampshire', 'Iowa', 'Minnesota', 'Nebraska', 'Missouri', 'Connecticut', 'New Jersey', 'Michigan', 'South Carolina'],
        117: ['Maryland', 'Colorado', 'Pennsylvania', 'Virginia', 'Minnesota', 'Washington', 'Illinois', 'California', 'Alabama', 'Alaska'],
        118: ['Iowa', 'Delaware', 'New Hampshire', 'Colorado', 'Alaska', 'Oregon', 'Rhode Island', 'California', 'Arizona', 'Oklahoma'],
        119: ['Virginia', 'Oregon', 'New York', 'California', 'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'Colorado', 'Connecticut'],
        120: ['Oklahoma', 'Tennessee', 'Iowa', 'Arizona', 'Missouri', 'Ohio', 'Wisconsin', 'Colorado', 'Texas', 'California'],
        121: ['Colorado', 'California', 'Oregon', 'Delaware', 'Pennsylvania', 'Nevada', 'New Jersey', 'Wyoming', 'Kansas', 'Maryland'],
        122: ['Maine', 'Delaware', 'Colorado', 'Pennsylvania', 'California', 'Utah', 'Oregon', 'Texas', 'North Dakota', 'Nevada'],
        123: ['Wyoming', 'Idaho', 'Alaska', 'Delaware', 'Vermont', 'Missouri', 'Arizona', 'Colorado', 'California', 'Indiana'],
        124: ['Utah', 'Nebraska', 'Oklahoma', 'Vermont', 'Louisiana', 'Pennsylvania', 'Connecticut', 'Michigan', 'Illinois', 'Virginia'],
        125: ['West Virginia', 'Arizona', 'Oregon', 'Colorado', 'Wisconsin', 'Pennsylvania', 'California', 'Alabama', 'Alaska', 'Arkansas'],
        126: ['Oklahoma', 'Oregon', 'Florida', 'California', 'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'Colorado', 'Connecticut'],
        127: ['Ohio', 'Wisconsin', 'California', 'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'Colorado', 'Connecticut', 'Delaware'],
        128: ['Nevada', 'Texas', 'Massachusetts', 'New York', 'California', 'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'Colorado'],
        129: ['Tennessee', 'North Carolina', 'Ohio', 'New York', 'California', 'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'Colorado'],
        130: ['Maine', 'Texas', 'California', 'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'Colorado', 'Connecticut', 'Delaware'],
        131: ['Mississippi', 'South Carolina', 'Maryland', 'Ohio', 'New York', 'California', 'Alabama', 'Alaska', 'Arizona', 'Arkansas'],
        132: ['Maryland', 'Virginia', 'New Jersey', 'New York', 'California', 'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'Colorado'],
        133: ['West Virginia', 'Oklahoma', 'Louisiana', 'Colorado', 'South Carolina', 'New Hampshire', 'Arizona', 'Massachusetts', 'Ohio', 'Connecticut'],
        134: ['Oklahoma', 'Kansas', 'Oregon', 'North Carolina', 'Washington', 'Massachusetts', 'California', 'Alabama', 'Alaska', 'Arizona'],
        135: ['Nevada', 'Iowa', 'New Hampshire', 'Kentucky', 'Maryland', 'New York', 'Florida', 'New Jersey', 'Alabama', 'Alaska'],
        136: ['Oklahoma', 'North Dakota', 'New Mexico', 'Montana', 'Michigan', 'Indiana', 'Vermont', 'Nebraska', 'Tennessee', 'Kentucky'],
        137: ['Nevada', 'New Hampshire', 'Virginia', 'Minnesota', 'Pennsylvania', 'California', 'Alabama', 'Alaska', 'Arizona', 'Arkansas'],
        138: ['Oklahoma', 'South Dakota', 'Montana', 'Alabama', 'Hawaii', 'Indiana', 'West Virginia', 'Utah', 'Vermont', 'Florida'],
        139: ['Montana', 'Utah', 'South Dakota', 'Indiana', 'Mississippi', 'Nebraska', 'Vermont', 'Arkansas', 'Tennessee', 'Rhode Island'],
        140: ['Washington', 'New York', 'California', 'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'Colorado', 'Connecticut', 'Delaware'],
        141: ['Ohio', 'Pennsylvania', 'Washington', 'California', 'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'Colorado', 'Connecticut'],
        142: ['Connecticut', 'Virginia', 'Pennsylvania', 'California', 'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'Colorado', 'Delaware'],
        143: ['Indiana', 'Colorado', 'Minnesota', 'Florida', 'New Jersey', 'Massachusetts', 'California', 'Alabama', 'Alaska', 'Arizona'],
        144: ['Delaware', 'South Carolina', 'Minnesota', 'New York', 'Pennsylvania', 'California', 'Alabama', 'Alaska', 'Arizona', 'Arkansas'],
        145: ['Tennessee', 'Pennsylvania', 'New York', 'California', 'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'Colorado', 'Connecticut'],
        146: ['Utah', 'Virginia', 'Wyoming', 'New Mexico', 'Colorado', 'Maryland', 'Delaware', 'Iowa', 'Florida', 'Ohio'],
        147: ['Montana', 'Arizona', 'Massachusetts', 'Ohio', 'Florida', 'Pennsylvania', 'Colorado', 'New York', 'Virginia', 'Maryland'],
        148: ['Colorado', 'South Carolina', 'Alaska', 'Pennsylvania', 'Idaho', 'New York', 'North Dakota', 'Oregon', 'Massachusetts', 'California'],
        149: ['California', 'Nevada', 'Arizona', 'Hawaii', 'New Mexico', 'West Virginia', 'Montana', 'Oklahoma', 'Texas', 'Utah'],
        150: ['Iowa', 'North Carolina', 'Minnesota', 'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut'],
        151: ['Rhode Island', 'Kentucky', 'New Jersey', 'Indiana', 'New York', 'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California'],
        152: ['Maine', 'Kentucky', 'Minnesota', 'Pennsylvania', 'California', 'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'Colorado'],
        153: ['Rhode Island', 'Florida', 'Wisconsin', 'Texas', 'California', 'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'Colorado'],
        154: ['Florida', 'Ohio', 'Washington', 'New York', 'California', 'Illinois', 'Alabama', 'Alaska', 'Arizona', 'Arkansas'],
        155: ['Alaska', 'Oklahoma', 'Arizona', 'Washington', 'Michigan', 'Massachusetts', 'New York', 'California', 'Alabama', 'Arkansas'],
        156: ['Kansas', 'Virginia', 'Texas', 'Pennsylvania', 'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado'],
        157: ['Nevada', 'Indiana', 'New York', 'Pennsylvania', 'Washington', 'Texas', 'California', 'Alabama', 'Alaska', 'Arizona'],
        158: ['Alabama', 'Iowa', 'Maryland', 'Michigan', 'New Jersey', 'Pennsylvania', 'New York', 'Alaska', 'Arizona', 'Arkansas'],
        159: ['Rhode Island', 'Kentucky', 'New Jersey', 'Michigan', 'Illinois', 'Washington', 'Texas', 'Pennsylvania', 'Alabama', 'Alaska'],
        160: ['Iowa', 'Michigan', 'California', 'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'Colorado', 'Connecticut', 'Delaware'],
    }

    state_cluster_map = []
    for cluster_id, states in cluster_data.items():
        for state in states:
            state_cluster_map.append({'state': state, 'cluster': cluster_id})

    state_cluster_df = pd.DataFrame(state_cluster_map)

    merged_map = us_map.merge(state_cluster_df, how='left', left_on='state', right_on='state')

    fig, ax = plt.subplots(figsize=(15, 10))
    merged_map.plot(column='cluster', cmap='tab20', legend=True, ax=ax)
    ax.set_title("US States by Cluster", fontsize=16)
    ax.axis('off')
    plt.show()

    unique_states = list({state for states in cluster_data.values() for state in states})
    cluster_matrix = []

    for cluster_id, states in cluster_data.items():
        cluster_vector = [1 if state in states else 0 for state in unique_states]
        cluster_matrix.append(cluster_vector)

    cluster_df = pd.DataFrame(cluster_matrix, columns=unique_states)

    inertia = []
    K_range = range(2, 15)
    for k in K_range:
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(cluster_df)
        inertia.append(kmeans.inertia_)

    plt.figure(figsize=(8, 4))
    plt.plot(K_range, inertia, 'bx-')
    plt.xlabel('Number of clusters K')
    plt.ylabel('Inertia')
    plt.title('Elbow Method for Optimal K')
    plt.show()

    reduced_kmeans = KMeans(n_clusters=6, random_state=42)  
    cluster_df['reduced_cluster'] = reduced_kmeans.fit_predict(cluster_df)

    reduced_cluster_map = dict(zip(cluster_data.keys(), cluster_df['reduced_cluster']))
    state_cluster_df['reduced_cluster'] = state_cluster_df['cluster'].map(reduced_cluster_map)

    merged_map = us_map.merge(state_cluster_df, how='left', on='state')

    fig, ax = plt.subplots(figsize=(12, 8))
    merged_map.plot(column='reduced_cluster', cmap='tab10', legend=True, ax=ax)
    ax.set_title('US Map with Reduced Clusters', fontsize=15)
    plt.show()
    
    return
    