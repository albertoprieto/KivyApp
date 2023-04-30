from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.core.window import Window
from kivymd.icon_definitions import md_icons
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.uix.recycleview import RecycleView
from kivy.factory import Factory
from kivymd.uix.bottomsheet import MDCustomBottomSheet
from kivymd.uix.card import MDCard
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivymd.uix.card import MDCardSwipe
from kivymd.uix.card import MDCardSwipe



class Navigator(Screen):
    pass

class SplashScreen(Screen):
    pass

class FirstScreen(Screen):
    pass

class CustomWidget(MDCardSwipe):
    text = StringProperty()
    def remove_item(self, instance):
        App.get_running_app().root.get_screen('cartscreen').ids.grid_id.remove_widget(instance)
    def remove_fav_item(self, instance):
        App.get_running_app().root.get_screen('cartscreen').ids.grid_id.remove_widget(instance)

class SpeiView(Screen):
    pass



class PedidoItem(Screen):
    pass


class Favscreen(Screen):
    pass
class Cartscreen(Screen):
    def goto_store(self):
        App.get_running_app().root.current  = "newscreen"
class NewScreen(Screen):
    def change_theme_style(self):
        if App.get_running_app().theme_cls.theme_style == "Dark":
            App.get_running_app().theme_cls.theme_style = "Light"
        else:
            App.get_running_app().theme_cls.theme_style = "Dark"

class LoginScreen(Screen):
    dialog = None
    def back(self,*args):
        App.get_running_app().root.current  = "vault"

    def login(self):
        password = App.get_running_app().root.get_screen('login').ids.master_password.text
        user = App.get_running_app().root.get_screen('login').ids.master_user.text
        users_ref = db.reference('users')
        for item in users_ref.get().items(): 

            if user in item:
                currusr =users_ref.child(user)
                if password in currusr.child(user).child('password').get():
                    App.get_running_app().root.current  = "vault"
                    break
                if not password in currusr.child(user).child('password').get():
                    App.get_running_app().root.get_screen('login').show_alert_dialog_user('Datos no válidos')
            else:
                self.show_alert_dialog_user('Datos no válidos')

    def show_alert_dialog_user(self,error):
        if not self.dialog:
            self.dialog = MDDialog(
                text=error,
                buttons=[
                    MDFlatButton(
                        text="Registrar",
                        theme_text_color="Custom",
                        text_color=App.get_running_app().theme_cls.primary_color,
                        on_release=self.gotoregister
                    ),
                    MDFlatButton(
                        text="Cancelar",
                        theme_text_color="Custom",
                        text_color=App.get_running_app().theme_cls.primary_color,
                        on_release=self.close_dialog
                    ),
                ],
            )
        self.dialog.open()

    def close_dialog(self,args):
        self.dialog.dismiss()
        App.get_running_app().root.get_screen('login').ids.master_user.text = ''
        App.get_running_app().root.get_screen('login').ids.master_password.text = ''
        App.get_running_app().root.current  = "login"

    def gotoregister(self,args):
        self.dialog.dismiss()
        App.get_running_app().root.current  = "register"
        App.get_running_app().root.get_screen('login').ids.master_user.text = ''
        App.get_running_app().root.get_screen('login').ids.master_password.text = ''

class RegisterScreen(Screen):
    def register(self):
        #users_ref = ref.child('users')
        user = App.get_running_app().root.get_screen('register').ids.master_new_user.text
        password = App.get_running_app().root.get_screen('register').ids.master_new_password.text
        extra1 = App.get_running_app().root.get_screen('register').ids.master_new_extra1.text
        extra2 = App.get_running_app().root.get_screen('register').ids.master_new_extra2.text
        extra3 = App.get_running_app().root.get_screen('register').ids.master_new_extra3.text
        extra4 = App.get_running_app().root.get_screen('register').ids.master_new_extra4.text   
        if user != '' and password != '':
            
            #Agrega usuario
            tabla=db.reference('users')
            ref = tabla.child(user)
            ref.set(user)

            #Agrega datos al usuario
            users_ref = ref.child(user)
            #users_ref.set(user)
            
            ref_pwd = users_ref.child('password')
            ref_pwd.set(password)
            ref_extra1 = users_ref.child('extra1')
            ref_extra1.set(extra1)
            ref_extra2 = users_ref.child('extra2')
            ref_extra2.set(extra2)
            ref_extra3 = users_ref.child('extra3')
            ref_extra3.set(extra3)
            ref_extra4 = users_ref.child('extra4')
            ref_extra4.set(extra4)

    def back(self):
        App.get_running_app().root.current  = "login"

    def alta(self):
        pass
         
class VaultScreen(Screen):
    def goto_cart(self):
        App.get_running_app().root.current  = "cartscreen"

    def setvault(self):
        App.get_running_app().root.current  = "vault"
class PedidosScreen(Screen):
    all_users = StringProperty()
    profile_items = StringProperty()

class GpsScreen(Screen):
    def change_theme_style(self):
        if App.get_running_app().theme_cls.theme_style == "Dark":
            App.get_running_app().theme_cls.theme_style = "Light"
        else:
            App.get_running_app().theme_cls.theme_style = "Dark"

class App(MDApp):
    cred = credentials.Certificate("")
    firebase_admin.initialize_app(cred, {
        ''
        })
    num_item=StringProperty()
    mpago=StringProperty()
    qroot=ObjectProperty()
    dialog = None

    sm = ScreenManager()
    sm.add_widget(FirstScreen(name='firstscreen'))
    sm.add_widget(SplashScreen(name='splashscreen'))
    sm.add_widget(LoginScreen(name='login'))
    sm.add_widget(VaultScreen(name='vault'))
    sm.add_widget(RegisterScreen(name='register'))
    sm.add_widget(PedidosScreen(name='pedidosscreen'))
    sm.add_widget(GpsScreen(name='gpsscreen'))
    sm.add_widget(NewScreen(name='newscreen'))
    sm.add_widget(Cartscreen(name='cartscreen'))
    sm.add_widget(Favscreen(name='favscreen'))
    sm.add_widget(NewScreen(name='customwidget'))
    
    def build(self):
        Window.size = (320,520)
        #self.num_item='1'
        num_item=StringProperty('')
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.primary_palette = "LightGreen"
        self.theme_cls.accent_palette = "LightGreen"
        self.theme_cls.theme_style = "Light"
        screen = Builder.load_file('kv.kv')
        return screen

    def on_start(self):
        self.num_item='1'
        Clock.schedule_once(self.splash, 2)

    def splash(self,*args):
        self.root.current  = "vault"

    def show_custom_bottom_sheet(self,image,price,rate):
            bottom_sheet=Factory.ContentCustomSheet()
            bottom_sheet.rate=rate
            bottom_sheet.image=image
            bottom_sheet.price=price
            self.custom_sheet = MDCustomBottomSheet(screen=bottom_sheet)
            self.custom_sheet.open()

    def checkout_screen(self,image,cmnt,instance):
            self.qroot=instance
            bottom_sheet=Factory.CheckoutView()
            bottom_sheet.rate=cmnt
            bottom_sheet.image=image
            bottom_sheet.price=''
            self.custom_sheet = MDCustomBottomSheet(screen=bottom_sheet)
            self.custom_sheet.open()

    def plus(self):
        if self.num_item=='':
            self.num_item='1'
        elif self.num_item=='9':
            pass

        else:
            value = int(self.num_item)
            self.num_item = str(int(value) + 1)

    def minus(self):
        if self.num_item=='':
            self.num_item='1'
        elif self.num_item=='1':
            pass
        else:
            value = int(self.num_item)
            self.num_item = str(int(value) - 1)
    def goto_cart(self):
        App.get_running_app().root.current  = "cartscreen"
    
    def addtocart(self,iimage,num_item):

        image=StringProperty('')
        cmnt=StringProperty('')
        self.show_alert_dialog_user('Agregado a tu carrito')
        dialog = None
        self.image=iimage
        self.cmnt='Unidades: '+str(num_item)
        self.num_item='1'
        new_cart=CustomWidget()
    
        #App.get_running_app().root.get_screen('cartscreen').ids.grid_id.add_widget(new_cart)
        App.get_running_app().root.get_screen('cartscreen').ids.grid_id.add_widget(CustomWidget(text=""))
        #App.get_running_app().root.get_screen('cartscreen').ids.grid_id.add_widget(TotalWidget, len(self.children))
    def addtofav(self,iimage,num_item):
        image=StringProperty('')
        cmnt=StringProperty('')
        dialog = None
        self.image=iimage
        self.cmnt=str(num_item)
        self.num_item='1'
        self.show_alert_dialog_user('Agregado a favoritos')
        dialog = None
        new_fav=CustomWidget()
        #App.get_running_app().root.get_screen('favscreen').ids.grid_id.add_widget(new_fav)
        App.get_running_app().root.get_screen('favscreen').ids.grid_id.add_widget(CustomWidget(text=""))
    

    def show_alert_dialog_user(self,text_action):
        self.dialog = MDDialog(
            text=text_action,
            buttons=[
                MDFlatButton(
                    text="OK",
                    theme_text_color="Custom",
                    text_color=App.get_running_app().theme_cls.primary_color,
                    on_release=self.close_dialog
                ),
            ],
        )
        self.dialog.open()

    def close_dialog(self,args):
        self.dialog.dismiss()

    def on_checkbox_active(self,value,instance):
        if value == 'spei':
            self.mpago='spei'

        if value == 'deposito':
            self.mpago='deposito'

    def proceed(self,instance):
        if self.mpago == 'spei':
            App.get_running_app().root.get_screen('cartscreen').ids.grid_id.remove_widget(self.qroot)
            instance.ids.check_grid.clear_widgets()
            speiview=SpeiView()
            instance.ids.check_grid.add_widget(speiview)
        if self.mpago == 'deposito':
            pass

    def goto_pedidos(self):
        
        App.get_running_app().root.get_screen('pedidosscreen').ids.grid_pedidos.add_widget(CustomWidget(text=""))
        App.get_running_app().root.current  = "pedidosscreen"

    def descarga_orden(self):
        pass

App().run()