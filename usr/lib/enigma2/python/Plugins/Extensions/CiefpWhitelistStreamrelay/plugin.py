import os
import shutil
from Plugins.Plugin import PluginDescriptor
from Screens.MessageBox import MessageBox  # Import za poruke korisniku
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.Pixmap import Pixmap
from Screens.Screen import Screen

# Naziv i opis plugina
PLUGIN_NAME = "CiefpWhitelistStreamrelay"
PLUGIN_DESC = "Kreira whitelist_streamrelay fajl iz userbouquet podataka"
PLUGIN_VERSION = "1.1"

# Putanje
WHITE_LIST_FILE = 'whitelist_streamrelay'
WHITE_LIST_PATH = '/etc/enigma2/whitelist_streamrelay'
USER_BOUQUET_DIR = '/etc/enigma2/'
PLUGIN_ICON = "/usr/lib/enigma2/python/Plugins/Extensions/CiefpWhitelistStreamrelay/icon.png"

# Lista userbouquet fajlova
USER_BOUQUETS = [
    'userbouquet.ciefp_19e_skydesport.tv',
    'userbouquet.ciefp_19e_skydemovies.tv',
    'userbouquet.ciefp_19e_skydedocu.tv',
    'userbouquet.ciefp_28e_skyuksports.tv',
    'userbouquet.ciefp_28e_skyukmovie.tv',
    'userbouquet.ciefp_28e_skyukdocuments.tv',
    'userbouquet.ciefp_28e_skyukkids.tv',
]

# Funkcija za obradu linija iz userbouquet

def process_bouquet_line(line):
    """ Obradjuje liniju - uklanja #SERVICE i proverava validnost """
    if line.startswith('#SERVICE 1:0:19:'):
        return line.replace('#SERVICE ', '').strip()
    return None


def filter_valid_lines(file_path):
    """ Filtrira validne linije iz userbouquet fajla """
    valid_lines = []
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            # Ignorisanje linija koje pocinju sa #NAME, #SERVICE 1:64, #DESCRIPTION
            if line.startswith(('#NAME', '#SERVICE 1:64', '#DESCRIPTION')):
                continue
            processed_line = process_bouquet_line(line)
            if processed_line:
                valid_lines.append(processed_line)
    return valid_lines


def process_bouquets():
    """ Prikuplja linije iz svih userbouquet fajlova """
    final_lines = []
    for bouquet in USER_BOUQUETS:
        bouquet_path = os.path.join(USER_BOUQUET_DIR, bouquet)
        if os.path.exists(bouquet_path):
            valid_lines = filter_valid_lines(bouquet_path)
            final_lines.extend(valid_lines)
    return final_lines


def create_whitelist_file():
    """ Kreira whitelist fajl sa filtriranim linijama """
    processed_lines = process_bouquets()
    if processed_lines:
        with open(WHITE_LIST_PATH, 'w') as f:
            for line in processed_lines:
                f.write(f"{line}\n")
    return len(processed_lines)
    
class WhitelistScreen(Screen):
    skin = """
    <screen name="WhitelistScreen" position="center,center" size="900,540" title="Ciefp Whitelist Streamrelay">
        <widget name="logo" position="10,10" size="900,400" transparent="1" alphatest="on" />
        <widget name="status" position="10,460" size="880,60" font="Regular;26" halign="center" valign="center" />
    </screen>
    """

    def __init__(self, session):
        Screen.__init__(self, session)
        self["status"] = Label("Pokretanje...")
        self["logo"] = Pixmap()  # Definišemo Pixmap za logo
        self["actions"] = ActionMap(
            ["OkCancelActions"], 
            {
                "cancel": self.close, 
                "ok": self.restart_enigma  # Dodajemo akciju za restart
            }, 
            -1
        )
        self.onLayoutFinish.append(self.set_logo)  # Poziv funkcije za postavljanje loga
        self.onLayoutFinish.append(self.run_plugin)

    def set_logo(self):
        logo_path = "/usr/lib/enigma2/python/Plugins/Extensions/CiefpWhitelistStreamrelay/logo.png"
        if os.path.exists(logo_path):
            self["logo"].instance.setPixmapFromFile(logo_path)  # Prikazujemo sliku ako postoji
        else:
            self["status"].setText("Logo nije pronađen!")
            
    def run_plugin(self):
        try:
            # Brisanje starog fajla
            if os.path.exists(WHITE_LIST_PATH):
                self["status"].setText("Brisanje starog fajla...")
                os.remove(WHITE_LIST_PATH)

            # Kreiranje novog fajla
            self["status"].setText("Generisanje whitelist fajla...")
            lines_created = create_whitelist_file()

            # Prikaz uspeha
            self["status"].setText(f"Whitelist file created with {lines_created} lines. Press OK to restart.")
        except Exception as e:
            self["status"].setText(f"Greška: {str(e)}")

    def restart_enigma(self):
        """Pokreće restart Enigma2 nakon korisničke potvrde"""
        self.session.openWithCallback(self.confirm_restart, MessageBox, "Do you want to restart Enigma2?", MessageBox.TYPE_YESNO)

    def confirm_restart(self, confirmed):
        if confirmed:
            self.close()
            os.system("killall -9 enigma2")  # Komanda za restart Enigma2

def run_plugin(session, **kwargs):
    """ Pokretanje glavnog ekrana """
    session.open(WhitelistScreen)


def Plugins(**kwargs):
    return [
        PluginDescriptor(
            name=f"{PLUGIN_NAME} v{PLUGIN_VERSION}",
            description=PLUGIN_DESC,
            where=PluginDescriptor.WHERE_PLUGINMENU,
            icon=PLUGIN_ICON,
            fnc=run_plugin,
        )
    ]
