import flet as ft
from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        # other attributes
        self._mese = 0



    def handle_umidita_media(self, e):
        mese = self._view.dd_mese.value
        if mese == None:
            self._view.create_alert("Scegli un mese")
        else:
            results = self._model.calcola_umidità_media(mese)
            print(results)
            self._view.lst_result.clean()
            for result in results:
                self._view.lst_result.controls.append(ft.Text(result[0]+" "+str(result[1])))
            self._view.update_page()

    def handle_sequenza(self, e):
        mese = self._view.dd_mese.value
        if mese == None:
            self._view.create_alert("Scegli un mese")
        else:
            sequenza, costo = self._model.calcola_sequenza(mese)
            self._view.lst_result.clean()
            self._view.lst_result.controls.append(ft.Text(f"Il costo della soluzione è {costo}"))
            for fermata in sequenza:
                self._view.lst_result.controls.append(ft.Text(fermata))
            self._view.update_page()

    def read_mese(self, e):
        self._mese = int(e.control.value)

