from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen

# Karbon ayak izi hesaplama fonksiyonu
def karbon_ayak_izi_hesapla(enerji, ulasim, et, atik, yas, cinsiyet, aktivite_seviyesi):
    enerji_faktoru = 0.4  # kWh başına kg CO2
    ulasim_faktoru = 0.2  # km başına kg CO2
    et_faktoru = 27  # kg başına kg CO2
    atik_faktoru = 0.1  # kg atık başına kg CO2

    # Aktivite seviyesine göre daha fazla hesaplama eklemek
    aktivite_faktoru = {"düşük": 1, "orta": 1.2, "yüksek": 1.5}.get(aktivite_seviyesi, 1)

    # Karbon ayak izini hesapla
    return (enerji * enerji_faktoru) + (ulasim * ulasim_faktoru) + (et * et_faktoru) + (atik * atik_faktoru) * aktivite_faktoru

# Kullanıcı verilerini sözlükle yönetme
kullanicilar = {}

# Ekranlar arasında geçişi yönetmek için ScreenManager
class GirisEkrani(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", padding=10)

        self.add_widget(Label(text="Kullanıcı Adı:", size_hint=(1, 0.2)))
        self.kullanici_adi_input = TextInput(size_hint=(1, 0.2))
        layout.add_widget(self.kullanici_adi_input)

        self.add_widget(Label(text="Şifre:", size_hint=(1, 0.2)))
        self.sifre_input = TextInput(size_hint=(1, 0.2), password=True)
        layout.add_widget(self.sifre_input)

        giris_btn = Button(text="Giriş Yap", size_hint=(1, 0.2))
        giris_btn.bind(on_press=self.giris)
        layout.add_widget(giris_btn)

        kayit_btn = Button(text="Kayıt Ol", size_hint=(1, 0.2))
        kayit_btn.bind(on_press=self.kayit)
        layout.add_widget(kayit_btn)

        self.add_widget(layout)

    def giris(self, instance):
        kullanici_adi = self.kullanici_adi_input.text
        sifre = self.sifre_input.text

        if kullanici_adi in kullanicilar and kullanicilar[kullanici_adi] == sifre:
            self.manager.current = "calculator"
        else:
            self.goster_popup("Hata", "Kullanıcı adı veya şifre hatalı!")

    def kayit(self, instance):
        kullanici_adi = self.kullanici_adi_input.text
        sifre = self.sifre_input.text

        if kullanici_adi in kullanicilar:
            self.goster_popup("Hata", "Bu kullanıcı adı zaten alınmış!")
        elif kullanici_adi.strip() == "" or sifre.strip() == "":
            self.goster_popup("Hata", "Kullanıcı adı ve şifre boş olamaz!")
        else:
            kullanicilar[kullanici_adi] = sifre
            self.goster_popup("Başarılı", "Kayıt tamamlandı!")

    def goster_popup(self, baslik, mesaj):
        popup = Popup(title=baslik, content=Label(text=mesaj), size_hint=(0.6, 0.4))
        popup.open()

# Önerileri oluşturacak fonksiyon
def oneriler_olustur(karbon_ayak_izi):
    if karbon_ayak_izi > 1000:
        oneriler = "Karbon ayak izinizi önemli ölçüde azaltmanız gerekebilir. İşte bazı öneriler:\n"
        oneriler += "- Et tüketiminizi azaltın veya bitkisel ürünleri tercih edin.\n"
        oneriler += "- Ulaşımda daha fazla toplu taşıma veya bisiklet kullanın.\n"
        oneriler += "- Enerji verimliliği yüksek cihazlar kullanın.\n"
        oneriler += "- Çöplerinizi geri dönüştürmeye özen gösterin."
    elif 500 <= karbon_ayak_izi <= 1000:
        oneriler = "Karbon ayak izinizi azaltmak için birkaç küçük adım atabilirsiniz:\n"
        oneriler += "- Bazı günlerde araba yerine yürümeyi ya da bisiklete binmeyi deneyin.\n"
        oneriler += "- Geri dönüştürülebilir atıklarınızı dikkatlice ayırın.\n"
        oneriler += "- Enerji tüketiminizi azaltmak için cihazlarınızı kapalı tutun.\n"
    else:
        oneriler = "Harika! Karbon ayak iziniz düşük seviyelerde. Ancak, devam edebileceğiniz bazı yollar:\n"
        oneriler += "- Tüketiminizi sürdürülebilir enerji ile dengeleyin.\n"
        oneriler += "- Vegan ya da vejetaryen beslenme alışkanlıklarını artırabilirsiniz.\n"
        oneriler += "- Daha da fazla bisiklet veya yürüyüş yaparak çevreye katkı sağlayabilirsiniz."

    return oneriler

class HesaplayiciEkrani(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", padding=10)

        # Yeni bilgiler için girişler
        self.yas_input = self.add_input_field(layout, "Yaş:")
        self.cinsiyet_input = self.add_input_field(layout, "Cinsiyet (erkek/kadın):")
        self.aktivite_input = self.add_input_field(layout, "Aktivite Seviyesi (düşük/orta/yüksek):")
        
        # Eski bilgiler için girişler
        self.enerji_input = self.add_input_field(layout, "Enerji Tüketimi (kWh):")
        self.ulasim_input = self.add_input_field(layout, "Ulaşım (km):")
        self.et_input = self.add_input_field(layout, "Et Tüketimi (kg):")
        self.atik_input = self.add_input_field(layout, "Atık Üretimi (kg):")

        hesapla_btn = Button(text="Karbon Ayak İzi Hesapla", size_hint=(1, 0.2))
        hesapla_btn.bind(on_press=self.hesapla)
        layout.add_widget(hesapla_btn)

        self.sonuc_label = Label(text="", size_hint=(1, 0.4))
        self.oneri_label = Label(text="", size_hint=(1, 0.4))
        
        layout.add_widget(self.sonuc_label)
        layout.add_widget(self.oneri_label)

        self.add_widget(layout)

    def add_input_field(self, layout, label_text):
        layout.add_widget(Label(text=label_text, size_hint=(1, 0.2)))
        input_field = TextInput(size_hint=(1, 0.2))
        layout.add_widget(input_field)
        return input_field

    def hesapla(self, instance):
        try:
            # Kullanıcıdan alınan yeni veriler
            yas = int(self.yas_input.text)
            cinsiyet = self.cinsiyet_input.text.lower().strip()
            aktivite_seviyesi = self.aktivite_input.text.lower().strip()

            # Kullanıcıdan alınan eski veriler
            enerji = float(self.enerji_input.text)
            ulasim = float(self.ulasim_input.text)
            et = float(self.et_input.text)
            atik = float(self.atik_input.text)

            # Karbon ayak izi hesaplama
            karbon_ayak_izi = karbon_ayak_izi_hesapla(enerji, ulasim, et, atik, yas, cinsiyet, aktivite_seviyesi)
            self.sonuc_label.text = f"Toplam Karbon Ayak İzi: {karbon_ayak_izi:.2f} kg CO2"
            
            # Öneri oluşturma
            oneri = oneriler_olustur(karbon_ayak_izi)
            self.oneri_label.text = f"Öneriler:\n{oneri}"
        
        except ValueError:
            self.sonuc_label.text = "Lütfen geçerli sayılar girin!"
            self.oneri_label.text = ""

class KarbonAyakIziApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(GirisEkrani(name="login"))
        sm.add_widget(HesaplayiciEkrani(name="calculator"))
        return sm

if __name__ == "__main__":
    KarbonAyakIziApp().run()
