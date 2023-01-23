from functools import partial
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout


class TestApp(App):

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

    def create_dropdown2(self, text, options):
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
        selection_button.bind(on_release=drpdn.open)
        return selection_button

    def change_select(self, wid, text, *largs):
        wid.text = text

    def open_dropdown(self, wid, drpdn, *largs):
        drpdn.open(wid)

    def build(self):
        root = BoxLayout(orientation="vertical")

        for _ in range(3):
            root.add_widget(self.create_dropdown("Works",
                                                 ["yes", "no"]
                                                 )
                            )

        for _ in range(4):
            root.add_widget(self.create_dropdown2("Does not work",
                                                  ["yes", "no"]
                                                  )
                            )

        return root


if __name__ == '__main__':
    TestApp().run()