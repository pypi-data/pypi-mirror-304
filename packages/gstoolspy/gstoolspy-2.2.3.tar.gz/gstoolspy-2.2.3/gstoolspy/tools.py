import pprint
import gspread
import time
import yaml


class GsTools:
    def __init__(self, credentials_file, sheet_name):
        # Autenticar usando o arquivo JSON da conta de serviço
        try:
            # Autenticar usando o arquivo JSON da conta de serviço
            client = gspread.service_account(filename=credentials_file)
        except:
            print("*** Erro ao autenticar ***")

            print("""
            Para usar a API do Google Sheets, você precisa de um arquivo JSON com as credenciais da conta de serviço.

            Siga as instruções abaixo para configurar a API do Google Sheets:

            Crie um Projeto no Google Cloud Platform
            - Acesse o Google Cloud Console.
            - Crie um novo projeto ou use um existente.
            - Ative a Google Sheets API:
            - Vá em APIs e Serviços > Biblioteca.
            - Pesquise por "Google Sheets API" e ative-a.

            Configure as Credenciais da Conta de Serviço
            - Ainda em APIs e Serviços, vá para Credenciais.
            - Clique em Criar credenciais > Conta de serviço.
            - Preencha as informações necessárias e crie a conta.
            - Após criada, vá em Gerenciar chaves e adicione uma nova chave do tipo JSON.
            - Baixe o arquivo JSON e salve-o em um local seguro.

            Compartilhe a Planilha com a Conta de Serviço
            - Abra a planilha que deseja manipular no Google Sheets.
            - Compartilhe a planilha com o e-mail da conta de serviço (encontrado no arquivo JSON na chave "client_email").

            """)
            exit(1)

        # Pegar planilha pelo nome
        check = False

        # Listar todas as planilhas acessíveis
        spreadsheets = client.list_spreadsheet_files()

        # Verificar se a planilha existe
        for spreadsheet in spreadsheets:
            if spreadsheet['name'] == sheet_name:
                check = True
                break

        # Abrir a planilha
        if not check:
            print(f"Planilha '{sheet_name}' não encontrada.")

            print("""
            Confirme o Compartilhamento Direto com a Conta de Serviço:


                Passo 1: Obtenha o E-mail da Conta de Serviço

                    Localize o Arquivo JSON das Credenciais: Abra o arquivo hilton-413618-4d93bb5c43bd.json que você está usando para autenticação.

                    Encontre o Campo client_email: Dentro desse arquivo JSON, localize o valor da chave "client_email". Será algo semelhante a:

                        {
                          "type": "service_account",
                          "project_id": "seu-projeto-id",
                          "private_key_id": "sua-chave-id",
                          "private_key": "-----BEGIN PRIVATE KEY----- [...] -----END PRIVATE KEY-----",
                          "client_email": "sua-conta-de-servico@seu-projeto.iam.gserviceaccount.com",
                        }

                    Exemplo:

                    "client_email": "my-service-account@my-project.iam.gserviceaccount.com"


                Passo 2: Compartilhe a Planilha Diretamente com a Conta de Serviço

                    Abra a Planilha no Google Sheets: Vá para o Google Sheets e abra a planilha "Fatura Locação Gamatel".

                    Clique em "Compartilhar": No canto superior direito, clique no botão "Compartilhar".

                    Adicione o E-mail da Conta de Serviço: No campo de e-mail, insira o client_email que você obteve no Passo 1 (por exemplo, my-service-account@my-project.iam.gserviceaccount.com).

                    Defina as Permissões: Selecione "Editor" para garantir que a conta de serviço possa ler e escrever na planilha.

                    Confirme o Compartilhamento: Clique em "Enviar" ou "Compartilhar" para finalizar.

                    ⚠️ Importante:

                        Evite usar atalhos ou compartilhamentos indiretos. A planilha deve ser compartilhada diretamente com o e-mail da conta de serviço.
            """)

            exit(1)
        else:
            print(f"Planilha '{sheet_name}' encontrada.")
            self.spreadsheet = client.open(sheet_name)
            print("Planilha aberta com sucesso.")

            print("Pegando as abas da planilha:")
            self.worksheets = self.spreadsheet.worksheets()
            pprint.pprint(f"Planilhas encontradas: {[worksheet.title for worksheet in self.worksheets]}", width=250)

    def worksheet_data(self, worksheet, debug=True):
        """
        Converte os dados de uma aba (worksheet) do Google Sheets para o formato YAML,
        garantindo a codificação UTF-8.

        :param worksheet: Objeto Worksheet do gspread.
        :param debug: Se True, imprime o YAML gerado.
        :return: Dicionário contendo o ID, nome e dados da aba.
        """
        try:
            aba_id = worksheet.id
            aba_nome = worksheet.title

            # Extrair dados e garantir a codificação UTF-8
            dados = worksheet.get_all_values()
            dados_utf8 = [[str(cell).encode('utf-8').decode('utf-8') for cell in row] for row in dados]

            aba_dict = {
                'aba_id': aba_id,
                'aba_nome': aba_nome,
                'dados': dados_utf8  # Usar dados com codificação UTF-8
            }

            if debug:
                yaml_data = yaml.dump(aba_dict, sort_keys=False, allow_unicode=True)
                print(f"Dados: {yaml_data}")

            return aba_dict

        except Exception as e:
            print(f"Erro ao converter a aba para YAML: {e}")
            return None

    def get_worksheets_data(self, debug=False, delay=1):
        """
        Salva os dados de todas as abas da planilha em um arquivo YAML com codificação UTF-8.

        :param output_file: Nome do arquivo de saída.
        :param debug: Se True, imprime os dados no console.
        :param delay: Tempo de espera em segundos entre as solicitações de leitura.
        :return: None
        """
        try:
            all_worksheets_data = {}

            for worksheet in self.worksheets:
                print(f"Lendo dados da aba: {worksheet.title}")
                worksheet_data = self.worksheet_data(worksheet, debug=debug)

                if worksheet_data:
                    all_worksheets_data[worksheet_data['aba_id']] = {
                        'aba_nome': worksheet_data['aba_nome'],
                        'dados': worksheet_data['dados']
                    }

                time.sleep(delay)

            return all_worksheets_data

        except Exception as e:
            print(f"Erro ao salvar os dados das abas: {e}")
            exit(1)