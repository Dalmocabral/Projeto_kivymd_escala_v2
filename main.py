from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFillRoundFlatIconButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from kivymd.uix.list import OneLineListItem, MDList
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.button import Button
from kivy.core.clipboard import Clipboard  # Importa o Clipboard
from datetime import datetime

# Configuração do banco de dados
DATABASE_URL = "sqlite:///colaboradores.db"
Base = declarative_base()

# Define o modelo do banco de dados
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    dataCreated = Column(DateTime, default=datetime.utcnow, nullable=False)
    afastado = Column(Boolean, default=False)
    dataDispensa = Column(DateTime, nullable=True)

# Cria o banco de dados e a tabela, se não existir
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base.metadata.create_all(bind=engine)

# Cria a sessão para interagir com o banco de dados
Session = sessionmaker(bind=engine)
session = Session()

# Função para adicionar um novo usuário
def adicionar_colaborador(nome):
    new_user = User(name=nome)
    session.add(new_user)
    session.commit()

# Cria a tela principal
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Layout para a tela principal
        box_layout = MDBoxLayout(
            orientation="vertical",
            pos_hint={"center_x": 0.5, "center_y": 0.9},
            padding=20,
            spacing=50,
        )

        # Botão para ir para a tela de cadastro
        button_01 = MDFillRoundFlatIconButton(
            icon="account-plus",
            text="Cadastro",
            pos_hint={"center_x": 0.5},
            on_release=self.go_to_cadastro
        )

        # Botão para ir para a tela de lista de colaboradores
        button_02 = MDFillRoundFlatIconButton(
            icon="account-group",
            text="Dispensas",
            pos_hint={"center_x": 0.5},
            on_release=self.go_to_lista
        )

        box_layout.add_widget(button_01)
        box_layout.add_widget(button_02)
        
        # Cria o layout para a tela principal
        layout = RelativeLayout()

        # Adiciona a imagem de fundo somente na tela principal
        background = Image(
            source="assets/01.png",  # Caminho da sua imagem
            allow_stretch=True,
            keep_ratio=False,
            opacity=0.3  # Ajuste de opacidade (0.0 é totalmente transparente, 1.0 é opaco)
        )

        # Adiciona a imagem de fundo ao layout
        layout.add_widget(background)
        
        # Adiciona o layout de botões à tela
        layout.add_widget(box_layout)

        # Adiciona o texto de rodapé
        footer_label = Label(
            text="Aplicativo criado por Dalmo do Santos Cabral - 2024",
            font_size="12sp",
            pos_hint={"center_x": 0.5, "y": -0.4}  # Posiciona o texto no rodapé
        )
        layout.add_widget(footer_label)


        self.add_widget(layout)

    # Função para mudar para a tela de cadastro
    def go_to_cadastro(self, instance):
        self.manager.current = 'cadastro_screen'

    # Função para mudar para a tela de lista de colaboradores
    def go_to_lista(self, instance):
        self.manager.current = 'lista_screen'


# Cria a tela de cadastro
class CadastroScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Layout para a tela de cadastro
        layout = FloatLayout()

        # Layout para centralizar o campo de entrada e o botão "Registrar"
        center_layout = MDBoxLayout(
            orientation="vertical",
            spacing=20,
            size_hint=(None, None),
            width="240dp",
            height="180dp",
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )

        # Campo de entrada para o nome do colaborador
        self.nome_input = MDTextField(
            hint_text="Nome do Colaborador",
            size_hint_x=1,
            width="240dp"
        )

        # Botão de "Registrar"
        button_register = MDFillRoundFlatIconButton(
            icon="check",
            text="Registrar",
            pos_hint={"center_x": 0.5},
            on_release=self.registrar_colaborador
        )

        # Adiciona o campo de entrada e o botão "Registrar" ao layout central
        center_layout.add_widget(self.nome_input)
        center_layout.add_widget(button_register)

        # Botão de "Voltar" no rodapé
        button_back = MDFillRoundFlatIconButton(
            icon="arrow-left",
            text="Voltar",
            pos_hint={"center_x": 0.5, "y": 0.05},
            on_release=self.go_back
        )

        # Adiciona o layout central e o botão "Voltar" ao FloatLayout principal
        layout.add_widget(center_layout)
        layout.add_widget(button_back)

        # Adiciona o layout principal à tela
        self.add_widget(layout)

    # Função para registrar o colaborador
    def registrar_colaborador(self, instance):
        nome = self.nome_input.text
        if nome:
            adicionar_colaborador(nome)  # Registra no banco de dados
            print(f"Colaborador '{nome}' registrado.")
            self.nome_input.text = ""  # Limpa o campo de entrada após registrar
        else:
            print("Por favor, insira o nome do colaborador.")

    # Função para voltar à tela principal
    def go_back(self, instance):
        self.manager.current = 'main_screen'


class ListaScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Layout principal
        box_layout = MDBoxLayout(
            orientation="vertical",
            padding=20,
            spacing=20,
        )

        # Cria um MDList para exibir os colaboradores
        self.lista_colaboradores = MDList()

        # Botão para voltar à tela principal
        button_back = MDFillRoundFlatIconButton(
            icon="arrow-left",
            text="Voltar",
            pos_hint={"center_x": 0.5},
            on_release=self.go_back
        )

        # Botão para copiar informações para a área de transferência
        button_copy = MDFillRoundFlatIconButton(
            icon="clipboard-outline",  # Ícone para o botão de copiar
            text="Copiar",
            pos_hint={"center_x": 0.5},
            on_release=self.copy_to_clipboard
        )

        # Adiciona a lista e os botões ao layout
        box_layout.add_widget(self.lista_colaboradores)
        box_layout.add_widget(button_copy)  # Botão de copiar
        box_layout.add_widget(button_back)  # Botão de voltar
        self.add_widget(box_layout)

    def on_pre_enter(self):
        self.carregar_colaboradores()

    def carregar_colaboradores(self):
        # Limpa a lista atual antes de adicionar os colaboradores
        self.lista_colaboradores.clear_widgets()
        
        # Recupera todos os colaboradores do banco de dados, com afastados no final
        colaboradores = session.query(User).order_by(User.afastado.asc(), User.dataDispensa.asc().nullsfirst()).all()

        # Organiza a lista para que afastados venham no final
        for idx, colaborador in enumerate(colaboradores, start=1):
            user_box = MDBoxLayout(size_hint_y=None, height=50, spacing=10)
            user_box.add_widget(Label(text=str(idx), size_hint_x=0.1))
            user_box.add_widget(Label(text=colaborador.name, size_hint_x=0.3))

            # Substitui o CheckBox pelo MDCheckbox
            afastado_checkbox = MDCheckbox(size_hint_x=0.1)
            afastado_checkbox.active = colaborador.afastado
            afastado_checkbox.bind(active=lambda checkbox, value, u=colaborador: self.set_afastado(u, value))
            user_box.add_widget(afastado_checkbox)

            # Substitui o Button pelo MDFillRoundFlatIconButton
            dispensa_button = MDFillRoundFlatIconButton(
                text="Dispensa",
                on_release=lambda btn, u=colaborador: self.marcar_dispensa(u),
                size_hint_x=0.2,
            )
            user_box.add_widget(dispensa_button)

            self.lista_colaboradores.add_widget(user_box)

    def set_afastado(self, colaborador, value):
        colaborador.afastado = value
        session.commit()
        
        # Recarrega a lista após a alteração
        self.carregar_colaboradores()

    def marcar_dispensa(self, colaborador):
        colaborador.dataDispensa = datetime.now()
        session.commit()
        self.carregar_colaboradores()

    def copy_to_clipboard(self, instance):  # Adiciona um argumento para receber o evento
        users = session.query(User).filter_by(afastado=False).all()  # Filtra apenas os não afastados
        date_str = datetime.now().strftime('%d/%m/%Y')
        text = f'*DISPENSA ATUALIZADA* {date_str}\n\n'
        for idx, user in enumerate(users, start=1):
            text += f'*{idx}* - _{user.name}_\n'
        Clipboard.copy(text)
        print('Texto copiado para a área de transferência')

    def go_back(self, instance):
        self.manager.current = 'main_screen'



class MyApp(MDApp):
    def build(self):
        screen_manager = ScreenManager()
        self.title = "Sistema de Escala"  # Define o nome do aplicativo
        # Adiciona as telas ao ScreenManager
        screen_manager.add_widget(MainScreen(name='main_screen'))
        screen_manager.add_widget(CadastroScreen(name='cadastro_screen'))
        screen_manager.add_widget(ListaScreen(name='lista_screen'))
        self.theme_cls.theme_style = "Dark"
        return screen_manager


if __name__ == '__main__':
    MyApp().run()
