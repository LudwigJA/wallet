import kivy
import sqlite3
kivy.require('2.0.0')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle, Line
from datetime import datetime


class MainScreen(Screen):
    pass

class NewTr(Screen):
        

        def on_button_release(self):
        # Chama as funções quando o botão é clicado
            self.salvar_operacao()
            self.manager.current = 'main'

        def voltar_main(self):
             self.manager.current = 'main'
    
        def salvar_operacao(self):
        # Obtém os dados preenchidos pelo usuário
            tipo_op = self.ids.tipo_op.text
            nome_op = self.ids.nome_op.text
            forma_op = self.ids.forma_op.text
            valor_op = float(self.ids.valor_op.text)
            data_op = datetime.now().date()
        # Conectar ao banco de dados
            conn = sqlite3.connect('wallet.db')
            c = conn.cursor()
        # Criar a tabela se ela não existir
            c.execute('''CREATE TABLE IF NOT EXISTS operacoes
                     (tipo TEXT, nome TEXT, forma TEXT, valor REAL, data TEXT)''')
        # Inserir o feedback do usuário na tabela
            c.execute("INSERT INTO operacoes VALUES (?, ?, ?, ?, ?)",
                    (tipo_op, nome_op, forma_op, valor_op, data_op))
        # Salvar as alterações e fechar a conexão com o banco de dados
            conn.commit()
            conn.close()
        
class Exibir_Op(Screen):
                
        label_entradas = "Entradas: "
        label_valor_entradas = "R$ 0,00"
        label_saidas = "Saídas: "
        label_valor_saidas = "R$ 0,00"
        label_total = "Resultado:  "
        label_valor_total = "R$ 0,00"

        
       

        
        def voltar_main(self):
            self.manager.current = 'main'

        def alterar_valor_label(self):

            filtra_data = "2023-08-13"

            conn = sqlite3.connect('wallet.db')
            c = conn.cursor()
            c.execute("SELECT * FROM operacoes WHERE data = ?", (filtra_data,))
            results = c.fetchall()

            somaEntrada = 0.0
            somaSaida = 0.0
            total = 0.0
            print(results)

            for row in results:
                tipo, nome, forma, valor, data = row
                if tipo == 'Entrada':
                    somaEntrada += valor
                elif tipo == 'Saída':
                    somaSaida += valor
            total = somaEntrada - somaSaida

            self.ids.label_entradas_valor.text = "R$ " + str(somaEntrada)  # Altera o valor da propriedade, que atualiza o Label
            self.ids.label_valor_saidas.text = "R$ " + str(somaSaida)
            self.ids.label_valor_total.text = "R$  " + str(int(total))
    


class Wallet(App):
    def build(self):
        # Criação do gerenciador de telas
        sm = ScreenManager()

        # Adicionando as telas ao gerenciador
        sm.add_widget(MainScreen(name='main'))       
        sm.add_widget(NewTr(name='newtr'))
        sm.add_widget(Exibir_Op(name='exibir_op'))


        return sm

if __name__ == '__main__':
    Wallet().run()
