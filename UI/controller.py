import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


    def handleCreaGrafo(self, e):
        self._view._txt_result.controls.clear()

        try:
            self._model.buildGraph()
            self._view._txt_result.controls.append(ft.Text("Grafo correttamente creato."))
            self._view._txt_result.controls.append(ft.Text(f"Numero nodi: {self._model.getNumNodi()}"))
            self._view._txt_result.controls.append(ft.Text(f"Numero archi: {self._model.getNumEdges()}"))
            self.fillDD()
            self._view.update_page()

        except Exception as ex:
            self._view.create_alert(f"Errore nella creazione del grafo: {ex}")

    def handleStampaInfo(self,e):
        self._view._txt_result.controls.clear()
        if self._model.getNumNodi() == 0:
            self._view.create_alert(f"Creare prima il grafo")
            return

        try:
            self._model.buildGraph()
            nComp, maxComp = self._model.dettagliGrafo()
            self._view._txt_result.controls.append(ft.Text(f"Il grafo ha {nComp} componenti connesse"))
            self._view._txt_result.controls.append(ft.Text(f"La componente connessa più grande ha {len(maxComp)} album"))
            self._view._txt_result.controls.append(ft.Text(f"Dettagli degli album appartenenti alla componente connessa più grande:"))
            for n in maxComp:
                self._view._txt_result.controls.append(ft.Text(f"{n}: {len(n.Tracks)} brani"))

            self.fillDD()

            self._view.update_page()

        except Exception as ex:
            self._view.create_alert(f"Errore nella stampa dei dettagli: {ex}")

    def handleSelezione(self,e):
        self._view._txt_result.controls.clear()

        if len(self._model._grafo.nodes) == 0:
            self._view.create_alert("Creare prima il grafo.")
            return

        if self._AlbumValue is None:
            self._view._txt_result.controls.append(
                ft.Text("Seleziona un album dal menu a tendina.")
            )
            self._view.update_page()
            return

        try:
            N = int(self._view._txtInN.value)
        except ValueError:
            self._view._txt_result.controls.append(
                ft.Text("Inserisci un valore numerico valido per N.")
            )
            self._view.update_page()
            return

        try:
            best_selection, total_tracks = self._model.getBestSelection(self._AlbumValue, N)

            if not best_selection:
                self._view._txt_result.controls.append(
                    ft.Text("Nessuna selezione trovata.")
                )
                self._view.update_page()
                return

            # Sort albums by title
            sorted_selection = sorted(best_selection, key=lambda album: album.Title)

            self._view._txt_result.controls.append(
                ft.Text("Lista ordinata degli album selezionati:")
            )
            self._view._txt_result.controls.append(ft.Text(""))

            for album in sorted_selection:
                num_tracks = len(album.Tracks)
                # assumo che tutte le tracce abbiano lo stesso genere, per cui prendo il genere del primo brano

                self._view._txt_result.controls.append(
                    ft.Text(f"  - {album.Title}: genere {album.Tracks[0].GenreId}, {num_tracks} brani")
                )

            self._view._txt_result.controls.append(ft.Text(""))
            self._view._txt_result.controls.append(
                ft.Text(f"Numero totale di album selezionati: {len(best_selection)}")
            )
            self._view._txt_result.controls.append(
                ft.Text(f"Numero complessivo di brani: {total_tracks}")
            )

            self._view.update_page()

        except Exception as ex:
            self._view.create_alert(f"Errore nella ricerca della sequenza: {ex}")

    def fillDD(self):
        # Populate dropdown with clients
        self._view._ddAlbum.options.clear()
        all_albums = self._model.getAllNodes()

        albumsDDOptions = list(
            map(lambda x: ft.dropdown.Option(data=x, key=str(x), on_click=self._choiceAlbum), all_albums))

        self._view._ddAlbum.options = albumsDDOptions

        self._view.update_page()

    def _choiceAlbum(self, e):
        self._AlbumValue = e.control.data