import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._idMap = {}
        self._maxTracks = 0
        self._best = []

    def getBestSelection(self, starting_album, N):

        if starting_album not in self._grafo.nodes:
            return []

        connected_components = list(nx.connected_components(self._grafo))

        # Find which component contains the starting album
        starting_component = self._getConnectedComponent(starting_album)

        parziale = [starting_album]

        comp_rimanenti = copy.deepcopy(connected_components)
        comp_rimanenti.remove(starting_component)

        self._ricorsione(parziale, N, comp_rimanenti)

        return self.bestSelection, self.max_tracks

    def _ricorsione(self, parziale, N, comp_rimanenti):
        print(len(parziale))
        # condizione di terminazione
        if len(parziale) == N:
            total_tracks = self._getTotalTracks(parziale)
            if total_tracks > self._maxTracks:
                self.max_tracks = total_tracks
                self.bestSelection = copy.deepcopy(parziale)
            return

        if not comp_rimanenti or N - len(parziale) > len(comp_rimanenti):
            return

        # provo ad aggiungere album da altre componenti che non ho ancora aggiunto

        # prendo il primo
        nextComp = comp_rimanenti[0]

        # Prima opzione: non prendo nessun album da questa componente, chiamo il metodo ricorsivo
        # passandogli tutte le rimanenti comp connesse tranne nextComp
        # versione verbosa
        # comp_rimanenti_aggiornate = copy.deepcopy(comp_rimanenti)
        # comp_rimanenti_aggiornate.remove(nextComp)
        # self._ricorsione(parziale, N, comp_rimanenti_aggiornate)
        self._ricorsione(parziale, N, comp_rimanenti[1:])

        # Seconda opzione: prendo l'album con più tracce da questa componente e vado avanti, chiamo il metodo ricorsivo
        # passandogli tutte le rimanenti comp connesse tranne nextComp
        best_album = self._getAlbumWithMostTracks(nextComp)

        if best_album is not None:
            parziale.append(best_album)
            # comp_rimanenti_aggiornate = copy.deepcopy(comp_rimanenti)
            # comp_rimanenti_aggiornate.remove(nextComp)
            # comp_rimanenti_aggiornate = copy.deepcopy(comp_rimanenti)
            # comp_rimanenti_aggiornate.remove(nextComp)

            # self._ricorsione(parziale, N, comp_rimanenti_aggiornate)
            self._ricorsione(parziale, N, comp_rimanenti[1:])
            parziale.pop()

    def _getConnectedComponent(self, album):
        # get the connected component that contains the album
        connected_components = list(nx.connected_components(self._grafo))
        for component in connected_components:
            if album in component:
                return component
        return None

    def _getTotalTracks(self, albums):
        total = 0
        for album in albums:
            if album.Tracks is not None:
                total += len(album.Tracks)
        return total

    def _getAlbumWithMostTracks(self, albums):
        best_album = None
        max_tracks_in_component = 0
        for album in albums:
            num_tracks = len(album.Tracks)  # if album.Tracks is not None else 0
            if num_tracks > max_tracks_in_component:
                max_tracks_in_component = num_tracks
                best_album = album
        return best_album





    def getAllNodes(self):
        return DAO.getAllNodes()

    def buildGraph(self):
        grafo = self._grafo
        grafo.clear()
        nodes = DAO.getAllNodes()
        grafo.add_nodes_from(nodes)
        for n in nodes:
            self._idMap[n.AlbumId] = n

        for row in DAO.getAlbumTracks():
            id = row["AlbumId"]
            track = row["TrackId"]
            if id in self._idMap:
                self._idMap[id].Tracks.append(track)

        edges = DAO.getAllEdges()
        for e in edges:
            grafo.add_edge(self._idMap[e["a1"]], self._idMap[e["a2"]])

    def dettagliGrafo(self):
        grafo = self._grafo
        compConn = list(nx.connected_components(grafo))
        nComp = len(compConn)
        maxComp = max(compConn, key=len)
        maxCompOrdinata = sorted(maxComp, key=lambda x: x.Title)
        return nComp, maxCompOrdinata

    def getNumNodi(self):
        return len(self._grafo.nodes)

    def getNumEdges(self):
        return len(self._grafo.edges)

    def getTotTracks(self,parziale):
        tot = 0
        for a in parziale:
            if a.Tracks is not None:
                tot += len(a.Tracks)
        return tot





