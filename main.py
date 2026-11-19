import flet as ft
from alert import AlertManager
from deposito_strumenti import DepositoStrumenti

FILE_STRUMENTI = "strumenti.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

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

    # TextField per le info necessarie per aggiungere un nuovo strumento (tipo, marca, anno)
    tipo_input = ft.TextField(label="Tipo")
    marca_input = ft.TextField(label="Marca")
    anno_input = ft.TextField(label="Anno acquisto")

    # TextField per il Counter impiegato per il valore in euro
    txt_valore = ft.TextField(value='0', width=60, disabled=True, text_align=ft.TextAlign.CENTER)

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
    def aggiungi_strumento(e):
        try:
            anno = int(anno_input.value)
            valore = int(txt_valore.value)
            deposito.aggiungi_strumento(
                tipo_input.value,
                marca_input.value,
                anno,
                valore
            )
            tipo_input.value = marca_input.value = anno_input.value = ""
            txt_valore.value = "0"
            aggiorna_lista_strumenti()
        except ValueError:
            alert.show_alert("❌ Errore: inserisci valori numerici validi per anno e valore.")

    def incrementa_valore(e):
        current_val = txt_valore.value
        txt_valore.value = f"{int(current_val) + 1}"

    def decrementa_valore(e):
        current_val = txt_valore.value
        txt_valore.value = f"{int(current_val) - 1}"

    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.Button("Conferma", on_click=conferma_responsabile)

    # Pulsanti per la gestione dell'inserimento di un nuovo strumento
    pulsante_aggiungi_strumento = ft.Button("Aggiungi strumento", on_click=aggiungi_strumento)
    pulsante_incrementa_valore = ft.IconButton(icon=ft.Icons.ADD, icon_color="green", on_click=incrementa_valore)
    pulsante_decrementa_valore = ft.IconButton(icon=ft.Icons.REMOVE, icon_color="red", on_click=decrementa_valore)

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
        ft.Row(spacing=30,
               controls=[tipo_input, marca_input, anno_input,
                         ft.Row([pulsante_decrementa_valore, txt_valore, pulsante_incrementa_valore])],
               alignment=ft.MainAxisAlignment.CENTER),
        pulsante_aggiungi_strumento,

        # Sezione 4
        ft.Divider(),
        ft.Text("Strumenti", size=20),
        lista_strumenti,
    )
    aggiorna_lista_strumenti()

ft.run(main)
