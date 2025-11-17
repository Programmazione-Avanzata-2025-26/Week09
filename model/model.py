from database.meteo_dao import MeteoDao

class Model:
    def __init__(self):
        pass

    def calcola_umidità_media(self, mese):
        return MeteoDao.get_umidita_media_mese(mese)


    def calcola_sequenza(self, mese):
        situazioni_meta_mese = MeteoDao.get_umidita_media_mese(mese)
        self._ricorsione([], situazioni_meta_mese)


    def _ricorsione(self, parziale, situazioni):
        # Caso/Condiz. terminale
        if len(parziale) == 15:
            print(parziale)
        # Caso/cond. ricorsiva
        else:
            for situazione in situazioni: # 45 oggettii di tipo Situazione
                parziale.append(situazione)
                self._ricorsione(parziale, situazioni)
                parziale.pop()


    def vincoli_soddisfatti(self, parziale, situazione):
        # Vincolo sui tre giorni consecutivi
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
            if (contatore < 3): # Se il contatatore è minore di 3, non si è fermato il tempo necessario
                return False # Vincolo non soddisfatto

        # Se tutti i vincoli sono soddisfatti
        return True

