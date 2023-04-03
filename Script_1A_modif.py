import os
import pandas as pd
import scapy
from scapy.all import *
from Builder.helpers_pcap import findTags, createTagsDictionnary


tag = createTagsDictionnary()

#p = rdpcap("pole-iot\Captures/test_00001_20220527132309.pcap")


def create_csv(directory, filename):
    p = rdpcap(f'{directory}/{filename}')

    F = p.filter(lambda x: x.haslayer(IP) and (
        x[IP].sport == 80 or x[IP].dport == 80))

    S = F.sessions()  # manipule les sessions au sens scapy donc sur un seul sens de com

    csion = []
    byte = []
    horo = []
    src = []
    dst = []
    id = []
    p_load = []

    for k, v in S.items():  # S est un dictionnaire. k est la cle donc la connexion TCP; v est l'ensemble des paquets sur k
        for pkt in v:
            csion.append(k)
        # initialement on a pkt[IP][TCP].payload mais ça ne marche pas sur toutes les plateformes
            p_load.append(bytes(pkt[IP][TCP].payload).decode())
            byte.append(pkt.len)
            time = pd.Timestamp(float(pkt.time), unit='s', tz='Europe/Paris')
            horo.append(time)
            src.append(pkt.sport)
            dst.append(pkt.dport)
        # initialement on a str(pkt) mais ça ne marche pas sur toutes les plateformes
            id.append(findTags(str(bytes(pkt)), tag))

# print(id)

    session = pd.Series(csion).astype(str)
    taille = pd.Series(byte).astype(int)
    date = pd.to_datetime(pd.Series(horo).astype(str), errors='coerce')
    Src = pd.Series(src).astype(int)
    Dst = pd.Series(dst).astype(int)
    Id = pd.Series(id).astype(str)
    P_load = pd.Series(p_load).astype(str)

    df = pd.DataFrame({"Session": session, "Taille": taille, "Date": date,
                       "Source": Src, "Destination": Dst, "ID": Id, "Information": P_load})

    df["Max"] = df.apply(lambda x: x["Source"] if x["Source"]
                         > x["Destination"] else x["Destination"], axis=1)

    # df.to_csv('dfincsv\df1')

    data = []

    for s in df["Max"].unique():
        pkt = df[df["Max"] == s]
        session = pkt["Session"].min()
        taille_sup = pkt[pkt["Source"] > pkt["Destination"]]["Taille"].sum()
        taille_inf = pkt[pkt["Source"] < pkt["Destination"]]["Taille"].sum()
        taille = pkt["Taille"].sum()
        startTime = pkt["Date"].min()
        endTime = pkt["Date"].max()
        delta = pkt["Date"].max()-pkt["Date"].min()
        startTime_sup = pkt[pkt["Source"] > pkt["Destination"]]["Date"].min()
        startTime_inf = pkt[pkt["Source"] < pkt["Destination"]]["Date"].min()
        endTime_sup = pkt[pkt["Source"] > pkt["Destination"]]["Date"].max()
        endTime_inf = pkt[pkt["Source"] < pkt["Destination"]]["Date"].max()
        delta_sup = pkt[pkt["Source"] > pkt["Destination"]]["Date"].max(
        ) - pkt[pkt["Source"] > pkt["Destination"]]["Date"].min()
        delta_inf = pkt[pkt["Source"] < pkt["Destination"]]["Date"].max(
        ) - pkt[pkt["Source"] < pkt["Destination"]]["Date"].min()
        donglePort = pkt["Max"].max()
    # permet de taguer tous les paquets y compris ceux qui n'ont pas l'info
        sensorId = pkt["ID"].min()
        NumberOfPackets = pkt.shape[0]
        Info = pkt["Information"].max()
        data.append([session, taille_sup, taille_inf, taille, delta, startTime, endTime, startTime_sup, endTime_sup,
                    startTime_inf, endTime_inf, delta_sup, delta_inf, donglePort, sensorId, NumberOfPackets, Info])

    df2 = pd.DataFrame(data, columns=['Session', 'Taille_up', 'Taille_down', 'Taille', 'Delta', 'StartTime', 'EndTime', 'StartTime_sup',
                       'EndTime_sup', 'StartTime_inf', 'EndTime_inf', 'Delta_sup', 'Delta_inf', 'Dongle_port', 'SensorId', 'NumberOfPackets', 'Info'])

    df2["sleep"] = df2.groupby(["SensorId"])[
        "StartTime"].diff().dt.total_seconds()

    newfilename = filename[:-5]
    print(newfilename)
    df2.to_csv(f'dfincsv\df{newfilename}.csv')
    print(filename+'is created')


directory = 'pole-iot\Captures'


if __name__ == "__main__":
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            newdirectory = 'pole-iot\dfincsv'
            create_csv(directory, filename)
