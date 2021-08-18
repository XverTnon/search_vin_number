import os
import re

from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.properties import ObjectProperty, StringProperty

from kivymd.app import MDApp
from kivymd.material_resources import dp
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.list import OneLineListItem, MDList
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen
from kivymd.utils.fitimage import FitImage


Choice_Brand = ""
Choice_Model = ""
Choice_Equipment = ""

class SearchResultItemCarBrands(MDCard):
    def __init__(self, source_text, marker, **kwargs):
        super(SearchResultItemCarBrands, self).__init__(**kwargs)
        self.marker = marker
        self.add_widget(FitImage(source=source_text,
                                 size_hint_y=None,
                                 size_hint_x=None))

    def SearchResultItemCarBrands_NextScreen(self, marker):
        app = MDApp.get_running_app().root
        app.switch_to(ShowBrandModelsScreen())
        global Choice_Brand
        Choice_Brand = marker


class MainScreen(MDScreen):
    pass

class ShowCarsBrandsScreen(MDScreen):
    def on_enter(self):
        app = MDApp.get_running_app()
        result_list_widget = self.ids.result_car_brands
        # Получаем все файлы марок авто и записываем в словарь
        Files_Cars_Brands = os.listdir("ImagesCarsBrands")
        # Узнаём количество картинок с марками авто
        Amount_Files_Cars_Brands = len(Files_Cars_Brands)
        for i in range(0, Amount_Files_Cars_Brands):
            result_list_widget.add_widget(
                SearchResultItemCarBrands(source_text=f"ImagesCarsBrands/{Files_Cars_Brands[i]}",
                                          marker=Files_Cars_Brands[i].split(".")[0]))

    def clear_search_car_brands(self, **kwargs):
        app = MDApp.get_running_app()
        result_list_widget = self.ids.result_car_brands
        result_list_widget.clear_widgets()
        return result_list_widget

    def Input_Cars_Brands(self):
        input_search_cars_brands = ObjectProperty(None)
        # Получаем все файлы марок авто и записываем в словарь
        Files_Cars_Brands = os.listdir("ImagesCarsBrands")
        # Узнаём количество картинок с марками авто
        Amount_Files_Cars_Brands = len(Files_Cars_Brands)
        Input_Text = fr"{self.input_search_cars_brands.text.lower()}"
        result_list_widget = self.clear_search_car_brands()
        i = 0
        ammount = 0
        for i in range(0, Amount_Files_Cars_Brands):
            if re.search(Input_Text, Files_Cars_Brands[i]):
                result_list_widget.add_widget(
                    SearchResultItemCarBrands(source_text=f"ImagesCarsBrands/{Files_Cars_Brands[i]}",
                                              marker=Files_Cars_Brands[i].split(".")[0]))
                ammount += 1
            if i == int(Amount_Files_Cars_Brands) - 1 and ammount:
                return
        if i != 0 and ammount == 0:
            result_list_widget.add_widget(MDLabel(text="Марка не найдена"))

class SearchResultBrandModels(MDCard):
    def __init__(self, source_text, marker, **kwargs):
        super(SearchResultBrandModels, self).__init__(**kwargs)
        self.marker = marker
        self.add_widget(OneLineListItem(text=source_text))


    def SearchResultBrandModels_NextScreen(self, marker):
        app = MDApp.get_running_app().root
        app.switch_to(ShowModelEquipmentScreen())
        global Choice_Model
        Choice_Model = marker

class ShowBrandModelsScreen(MDScreen):
    def on_enter(self, *args):
        app = MDApp.get_running_app()
        result_list_widget = self.ids.result_brand_models
        # Открываем файл со списком моделей
        File_Brand_Models = open("BrandModels.txt")
        for line in File_Brand_Models:
            if line.split("_")[0] == Choice_Brand:
                Models = line.split("_")[1]
                for i in range(0, len(Models.split(","))):
                    result_list_widget.add_widget(
                        SearchResultBrandModels(source_text=Models.split(",")[i],
                                                marker=Models.split(",")[i]))
    def clear_search_brand_models(self, **kwargs):
        app = MDApp.get_running_app()
        result_list_widget = self.ids.result_brand_models
        result_list_widget.clear_widgets()
        return result_list_widget

    def Input_Brand_Model(self):
        input_search_brand_models = ObjectProperty(None)
        result_list_widget = self.clear_search_brand_models()
        File_Brand_Models = open(f"BrandModels.txt")
        Input_Text = fr"{self.input_search_brand_models.text.lower()}"
        ammount = 0
        for line in File_Brand_Models:
            if line.split("_")[0] == Choice_Brand:
                Models = line.split("_")[1]
                for i in range(0, len(Models.split(","))):
                    if re.search(Input_Text, Models.split(",")[i].lower()):
                        result_list_widget.add_widget(
                            SearchResultBrandModels(source_text=Models.split(",")[i],
                                                    marker=Models.split(",")[i]))
                        ammount += 1
        if ammount == 0:
            result_list_widget.add_widget(MDLabel(text="Модель не найдена"))
    def ShowBrandModelsScreen_Back(self):
        app = MDApp.get_running_app().root
        app.switch_to(ShowCarsBrandsScreen())
        global Choice_Model
        Choice_Model = ""

class SearchResultModelEquipment(MDCard):
    def __init__(self, source_text, marker, **kwargs):
        super(SearchResultModelEquipment, self).__init__(**kwargs)
        self.marker = marker
        self.add_widget(OneLineListItem(text=source_text))


    def SearchResultModelEquipment_NextScreen(self, marker):
        app = MDApp.get_running_app().root
        app.switch_to(ShowVINNumber())
        global Choice_Model
        Choice_Model = marker
        print(marker)

class ShowModelEquipmentScreen(MDScreen):
    def on_enter(self, *args):
        app = MDApp.get_running_app()
        result_list_widget = self.ids.result_model_equipment
        # Открываем файл со списком комплектаций
        File_Models_Equpment = open("ModelsEquipments.txt", encoding="utf8")
        for line in File_Models_Equpment:
            if line.split("_")[0] == Choice_Brand and line.split("_")[1] == Choice_Model:
                Models = line.split("_")[2]
                for i in range(0, len(Models.split(","))):
                    result_list_widget.add_widget(
                        SearchResultModelEquipment(source_text=Models.split(",")[i],
                                                marker=Models.split(",")[i]))
    def clear_search_model_equipment(self, **kwargs):
        app = MDApp.get_running_app()
        result_list_widget = self.ids.result_model_equipment
        result_list_widget.clear_widgets()
        return result_list_widget

    def Input_Model_Equipment(self):
        input_search_model_equipment = ObjectProperty(None)
        result_list_widget = self.clear_search_model_equipment()
        # Открываем файл со списком комплектаций
        File_Models_Equpment = open("ModelsEquipments.txt", encoding="utf8")
        Input_Text = fr"{self.input_search_model_equipment.text.lower()}"
        ammount = 0
        for line in File_Models_Equpment:
            if line.split("_")[0] == Choice_Brand and line.split("_")[1] == Choice_Model:
                Models = line.split("_")[2]
                for i in range(0, len(Models.split(","))):
                    if re.search(Input_Text, Models.split(",")[i].lower()):
                        result_list_widget.add_widget(
                            SearchResultModelEquipment(source_text=Models.split(",")[i],
                                                       marker=Models.split(",")[i]))
                        ammount += 1
        if ammount == 0:
            result_list_widget.add_widget(MDLabel(text="Комплектация не найдена"))
    def ShowModelEquipmentScreen_Back(self):
        app = MDApp.get_running_app().root
        app.switch_to(ShowBrandModelsScreen())
        global Choice_Equipment
        Choice_Equipment = ""

class ShowVINNumber(MDScreen):
    pass

class Screens(ScreenManager):
    pass

class SearchVINNumberApp(MDApp):
    def build(self):
        # Устанавливаем тему Light или Dark
        self.theme_cls.theme_style = "Light"
        # Устанавливаем название окна
        self.title = "Самая лучшая программа"
        return Screens()

if __name__ == "__main__":
    SearchVINNumberApp().run()