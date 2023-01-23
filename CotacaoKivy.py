# -*- coding: utf-8 -*-

import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from functools import partial
import requests

class MeuApp(App):
    def build(self):
        self.layout = GridLayout(cols=2, row_force_default=True, row_default_height=40)

        #Menu Dropdown
        self.layout.add_widget(self.create_dropdown("Moeda", ["BTC", "USD", "EUR"]))
        self.vlr = 'BTC'

        self.btn = Button(text='Pegar Cotação', size=(200, 50))
        self.btn.bind(on_press=self.pegar_cotacao)
        self.layout.add_widget(self.btn)

        self.lbl1 = Label(text='Valor Atual:', size_hint=(1.0, 1.0), halign="center", valign="middle")
        self.lbl1.text_size=(200, None)
        self.layout.add_widget(self.lbl1)

        self.lbl = Label(text='', size_hint=(1.0, 1.0), halign="center", valign="middle")
        self.lbl.text_size = (200, None)
        self.layout.add_widget(self.lbl)


        return self.layout

    def change_select(self, wid, text, *largs):
        wid.text = text
        self.vlr=text
    def open_dropdown(self, wid, drpdn, *largs):
        drpdn.open(wid)
    def create_dropdown(self, text, options):
        selection_button = Button(text=text)
        drpdn = DropDown()
        for o in options:
            btn = Button(text=o, size_hint_y=None, height=44)
            btn.bind(on_release=partial(self.change_select,
                                        selection_button,
                                        btn.text
                                        )
                     )
            btn.bind(on_release=drpdn.dismiss)
            drpdn.add_widget(btn)
        selection_button.bind(on_release=partial(self.open_dropdown,
                                                 selection_button,
                                                 drpdn
                                                 )
                              )
        return selection_button
    def printselecao(self):
        print(self.layout.mainbutton.select)
    def pegar_cotacao(self, event):
        moeda = self.vlr.upper()
        link = f"https://economia.awesomeapi.com.br/last/{moeda}-BRL"
        req = requests.get(link).json()
        valor = req[f'{moeda}BRL']['bid']
        print(valor)
        self.lbl.text = valor
        self.btn.text = "Mudou"

if __name__ == '__main__':
    MeuApp().run()
