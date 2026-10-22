import flet as ft
from flet import Button, value
from unicodedata import digit

from alert import AlertManager
from deposito_strumenti import DepositoStrumenti

FILE_STRUMENTI = "strumenti.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    def aumenta_prezzo(e):
        prezzo = int(numero_visualizzato.value)

        numero_visualizzato.value = prezzo + 10
        numero_visualizzato.update()

    def diminuisci_prezzo(e):
        prezzo = int(numero_visualizzato.value)

        if prezzo > 0:
            numero_visualizzato.value = prezzo - 10
        numero_visualizzato.update()

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DAL DEPOSITO DI STRUMENTI DEL LAB03 ---
    deposito = DepositoStrumenti("Deposito Strumenti Musicali", "Alessandro Visconti")
    try:
        deposito.carica_file_strumenti(FILE_STRUMENTI)  # Carica il file
    except FileNotFoundError as e:
        alert.show_alert(f"❌ {e}")  # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile del deposito
    txt_titolo = ft.Text(value=deposito.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {deposito.get_responsabile()}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=deposito.get_responsabile(), label="Responsabile")

    # ListView per mostrare la lista di strumenti aggiornata
    lista_strumenti = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere un nuovo strumento (tipo, marca, anno, contatore posti)
    input_tipo = ft.TextField("Tipo ")
    input_marca = ft.TextField("Marca ")
    input_anno_acquisto = ft.TextField("Anno acquisto ")

    btnMinus = ft.IconButton(icon=ft.Icons.REMOVE,
                             icon_color="red",
                             icon_size=24, on_click=diminuisci_prezzo)
    btnAdd = ft.IconButton(icon=ft.Icons.ADD,
                           icon_color="green",
                           icon_size=24, on_click=aumenta_prezzo)
    numero_visualizzato = ft.TextField(width=100, disabled=True,
                          value=0,
                          border={
                              ft.ControlState.DEFAULT: ft.OutlineInputBorder(
                                  side=ft.BorderSide(color="grey", width=1)),
                              ft.ControlState.DISABLED: ft.OutlineInputBorder(
                                  side=ft.BorderSide(color="grey", width=1))
                          },
                          text_align=ft.TextAlign.CENTER)
    # TODO
    #fatto

    # --- FUNZIONI APP ---
    def aggiorna_lista_strumenti():
        lista_strumenti.controls.clear()
        for strumento in deposito.strumenti_ordinati_per_marca():
            stato = "✅" if strumento.disponibile else "⛔"
            lista_strumenti.controls.append(ft.Text(f"{stato} {strumento}"))

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"

    def conferma_responsabile(e):
        deposito.set_responsabile(input_responsabile.value)
        txt_responsabile.value = f"Responsabile: {deposito.get_responsabile()}"

    # Handlers per la gestione dei pulsanti utili all'inserimento di un nuovo strumento
    def aggiorna_pagina(e):
        if input_tipo.value.isdigit() or input_marca.value.isdigit() or not input_anno_acquisto.value.isdigit():
            alert.show_alert("❌ Errore: inserisci valori numerici validi per anno e posti")
        else:
            strumento = deposito.aggiungi_strumento(
                input_tipo.value,
                input_marca.value,
                input_anno_acquisto.value,
                int(numero_visualizzato.value)
            )
            aggiorna_lista_strumenti()
            page.update()
        input_tipo.value = "Tipo"
        input_marca.value = "Marca"
        input_anno_acquisto.value = "Anno acquisto"

        page.update()
    # TODO
    #fatto

    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.Button("Conferma", on_click=conferma_responsabile)

    # Pulsanti per la gestione dell'inserimento di un nuovo strumento
    aggiunta_strumento = Button("Aggiungi strumento", on_click=aggiorna_pagina)
    # TODO
    #fatto

    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        ft.Divider(),
        ft.Text("Aggiungi nuovo strumento", size=20),
        ft.Row(spacing=20,
               controls=[input_tipo, input_marca, input_anno_acquisto, btnMinus, numero_visualizzato, btnAdd],
               alignment=ft.MainAxisAlignment.CENTER),
        ft.Row(spacing=20,
               controls=[aggiunta_strumento],
               alignment=ft.MainAxisAlignment.CENTER),
        # TODO
        #fatto

        # Sezione 4
        ft.Divider(),
        ft.Text("Strumenti", size=20),
        lista_strumenti,
    )
    aggiorna_lista_strumenti()


ft.run(main)
