import copy

from database.meteo_dao import MeteoDao

class Model:
    def __init__(self):
        # self._soluzioni = []
        self._costo_minimo = -1
        self._soluzione_ottima = []

    def calcola_umidità_media(self, mese):
        return MeteoDao.get_umidita_media_mese(mese)


    def calcola_sequenza(self, mese):
        situazioni_meta_mese = MeteoDao.get_situazione_meta_mese(mese)
        self._ricorsione([], situazioni_meta_mese)
        return self._soluzione_ottima, self._costo_minimo

    def _ricorsione(self, parziale, situazioni):
        # Caso/Condiz. terminale
        if len(parziale) == 15:
            print(parziale)
            costo = self._calcola_costo(parziale)
            if(self._costo_minimo==-1) or (costo < self._costo_minimo):
                self._costo_minimo = costo
                #self._soluzioni.append(copy.deepcopy(parziale))
                self._soluzione_ottima = copy.deepcopy(parziale)

        # Caso/cond. ricorsiva
        else:
            giorno = len(parziale)+1
            #for situazione in situazioni: # 45 oggetti di tipo Situazione
            # Altra ottimizzazione, lavorando su finestre di tre giorni rispetto al giorno considerato
            for situazione in situazioni[(giorno-1)*3:giorno*3]:
                if self.vincoli_soddisfatti(parziale, situazione):
                    parziale.append(situazione)
                    self._ricorsione(parziale, situazioni)
                    parziale.pop()


    def vincoli_soddisfatti(self, parziale, situazione):
        # Vincolo su non più di 6 giornate (anche non consecutive) stessa località
        contatore = 0
        for fermata in parziale:
            if fermata.localita == situazione.localita:
                contatore+=1
        if contatore>=6:
            return False

        # Vincolo su non più di tre giorni consecutivi stessa località
        if len(parziale) >0 and len(parziale) <=2:
            if situazione.localita != parziale[0].localita:
                return False
        elif len(parziale) > 2: # Se la sequenza ha almeno tre elementi occorre
                                # verificare che il tecnico si sa fermato almeno
                                #  tre giorni di fila nella stessa località
            sequenza_finale = parziale[-3:] # Ultimi tre giorni in parziale
            prima_fermata = sequenza_finale[0].localita # Località del primo di questi ultimi tre giorni
            contatore = 0
            for fermata in sequenza_finale: # Per ognuno di quei tre giorni
                if fermata.localita == prima_fermata: # Se il tecnico si è fermato nella località in questione
                    contatore += 1 # Incremento un contatore
            # Se il contatatore è minore di 3, non si è fermato il tempo necessario
            if (contatore < 3) and situazione.localita != sequenza_finale[-1].localita:
                return False # Vincolo non soddisfatto

        # Se tutti i vincoli sono soddisfatti
        return True

    def _calcola_costo(self, parziale):
        costo = 0
        for i in range(len(parziale)):
            # Costo dell'uimità
            costo += parziale[i].umidita

            if i == 2: # primi due giorni
                if (parziale[i].localita != parziale[0].localita):
                    costo += 100
            elif i > 2: # altri giorni
                ultime_fermate = parziale[i-2:i+1]
                if(ultime_fermate[2].localita != ultime_fermate[0].localita) or (ultime_fermate[2].localita != ultime_fermate[1].localita):
                    costo += 100
            return costo