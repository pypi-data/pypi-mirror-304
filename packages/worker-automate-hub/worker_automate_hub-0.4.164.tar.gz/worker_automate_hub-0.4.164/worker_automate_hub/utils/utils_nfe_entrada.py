import getpass
import io
import os
import re
from pathlib import Path
from typing import List, Tuple

import pyautogui
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from pywinauto.application import Application
from pywinauto.keyboard import send_keys
from pywinauto_recorder.player import set_combobox
from rich.console import Console

from worker_automate_hub.models.dao.rpa_configuracao import RpaConfiguracao
from worker_automate_hub.models.dto.rpa_historico_request_dto import (
    RpaHistoricoStatusEnum,
    RpaRetornoProcessoDTO,
)
from worker_automate_hub.utils.get_creds_gworkspace import GetCredsGworkspace
from worker_automate_hub.utils.logger import logger
from worker_automate_hub.utils.util import worker_sleep

pyautogui.PAUSE = 0.5
import pyperclip

console = Console()


class EMSys:
    def __init__(self):
        self.scrolled_pixels = 0
        self.edited_sequences = set()

    async def click_itens_da_nota(self):
        console.print("Navegando pela Janela de Nota Fiscal de Entrada...\n")
        app = Application().connect(class_name="TFrmNotaFiscalEntrada")
        main_window = app["TFrmNotaFiscalEntrada"]

        main_window.set_focus()
        console.print("Acessando os itens da nota... \n")
        panel_TPage = main_window.child_window(class_name="TPage", title="Formulario")
        panel_TTabSheet = panel_TPage.child_window(class_name="TcxCustomInnerTreeView")
        panel_TTabSheet.wait("visible")
        panel_TTabSheet.click()
        send_keys("{DOWN " + ("5") + "}")
        if await self.is_itens_da_nota_accessed():
            console.print(f"Itens da nota acessados com sucesso...\n")
        # Caso False raise Exception com a mensagem?
        await worker_sleep(2)

    async def is_itens_da_nota_accessed(self):
        app = Application().connect(class_name="TFrmNotaFiscalEntrada")
        main_window = app["TFrmNotaFiscalEntrada"]
        panel_TPage = main_window.child_window(class_name="TPage", title="Formulario")
        panel_TPage.wait("visible")
        panel_TTabSheet = panel_TPage.child_window(class_name="TTabSheet")
        title_n_serie = panel_TPage.child_window(title="N° Série")

        console.print("Verificando se os itens foram abertos com sucesso... \n")
        if not title_n_serie:
            console.print(f"Não foi possivel acessar a aba de 'Itens da nota...\n")
            # poderia ser return False ?
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno="Não foi possivel acessar a aba de 'Itens da nota'",
                status=RpaHistoricoStatusEnum.Falha,
            )
        else:
            return True

    async def alterar_item(self):
        pyautogui.click(745, 486)
        await worker_sleep(2)
        set_combobox("||List", "UNIDADE")

        # Check Alterar Trib. Manual
        pyautogui.click(1177, 740)
        # pyautogui.moveTo(1177, 740)

        # Click Alterar
        await worker_sleep(1)
        pyautogui.click(1180, 776)
        await worker_sleep(1)

        await worker_sleep(1)
        await self.verify_warning_and_error("Confirm")
        await worker_sleep(1)

    async def verify_warning_and_error(self, warning_title, title="&Yes"):
        try:
            console.print("Verificando a existencia de warnings e errors\n")
            app = Application().connect(title=warning_title)
            main_window = app[warning_title]
            main_window.set_focus()

            console.print(f"Clicando em {title}, para andamento do processo...\n")
            btn_no = main_window.child_window(title=title)
            if btn_no.exists() and btn_no.is_enabled():
                btn_no.set_focus()
                btn_no.click()
                await worker_sleep(3)
            else:
                console.print(
                    "Warning - Erro durante a verificação de warnings e errors"
                )
                return {
                    "sucesso": False,
                    "retorno": "Erro durante a verificação de warnings e errors\n",
                }

        except:
            console.print("Não possui nenhum warning após a importação do xml...\n")

    async def percorrer_grid(self):
        await self.click_itens_da_nota()

        console.print("Acessando os itens indivualmente... \n")
        send_keys("{TAB 2}", pause=0.1)
        await worker_sleep(2)
        index_item_atual = 0
        index_ultimo_item = await self.get_ultimo_item()
        console.print(f"Index ultimo item: {index_ultimo_item}")

        try:
            while index_item_atual < index_ultimo_item:
                send_keys("^({HOME})")
                await worker_sleep(1)

                if index_item_atual > 0:
                    send_keys("{DOWN " + str(index_item_atual) + "}")

                await worker_sleep(2)
                send_keys("+{F10}")
                await worker_sleep(1)
                send_keys("{DOWN 2}")
                await worker_sleep(1)
                send_keys("{ENTER}")

                await worker_sleep(2)
                app = Application().connect(title="Alteração de Item")
                main_window = app["Alteração de Item"]

                main_window.set_focus()

                edit = main_window.child_window(
                    class_name="TDBIEditCode", found_index=0
                )

                console.print(f"edit text: {edit.window_text()}")

                # ITERANDO COM O ITEM
                tpage_item = main_window.child_window(
                    class_name="TPanel", found_index=0
                )
                item = tpage_item.child_window(
                    class_name="TDBIEditString", found_index=1
                )
                item_value = item.window_text()

                console.log(f"item name: {item_value}")

                # Verifica se o item é 'isqueiro'
                if "isqueiro" in item_value.lower():
                    try:
                        console.print(f"Trabalhando com os itens, alterando o código de tributação dos ISQUEIROS para manual \n")
                        console.print("Item encontrado: ISQUEIRO. Processando...\n")

                        await self.alterar_item()
                        await worker_sleep(3)
                        await self.click_itens_da_nota()
                    except Exception as error:
                        console.print(f"Erro ao alterar item: {error}")

                else:
                    console.print(
                        "Item não é isqueiro. Continuando para o próximo...\n"
                    )
                    # Fecha a janela de alteração de item
                    try:
                        pyautogui.hotkey('esc')
                        console.print("Apertando [ESC]", style="bold blue")
                    except Exception as e:
                        console.print(f"Erro ao cancelar edição de item: {e}", style="bold red")
                    await worker_sleep(3)

                index_item_atual += 1
                console.print(f"Item aual no final da execução: {index_item_atual}")
                await worker_sleep(1)
                pyautogui.click(1083, 682)

            pyautogui.click(586, 328)

        except Exception as e:
            return {
                "sucesso": False,
                "retorno": f"Erro aotrabalhar nas alterações dos itens: {e}",
            }

    async def click_principal(self):
        pyautogui.click(621, 327)
        await worker_sleep(2)

    async def select_tipo_cobranca(self):
        pyautogui.click(632, 384)
        await worker_sleep(2)
        pyautogui.click(893, 549)
        await worker_sleep(2)
        try:
            set_combobox("||List", "BANCO DO BRASIL BOLETO")
        except:
            set_combobox("||List", "BOLETO")

    async def inserir_vencimento_e_valor(self, data_vencimento, valor):
        pyautogui.click(1030, 648)
        send_keys('^c')
        await worker_sleep(1)
        current_content = pyperclip.paste().strip()
        date_pattern = re.search(r'\d{2}/\d{2}/\d{4}', current_content)

        if not date_pattern:
            pyautogui.click(891, 596)
            await worker_sleep(1)
            pyautogui.write(data_vencimento)
            await worker_sleep(1)
            pyautogui.click(881, 620)
            await worker_sleep(1)
            pyautogui.write(valor)
            await worker_sleep(1)

            pyautogui.click(1287, 547)

    async def incluir_registro(self):
        # Incluir registro de Nota Fiscal de Entrada
        pyautogui.click(593, 297)
        await worker_sleep(1)

    async def get_ultimo_item(self):
        send_keys("^({END})")
        await worker_sleep(2)
        send_keys("+{F10}")
        await worker_sleep(1)
        send_keys("{DOWN 2}")
        await worker_sleep(1)
        send_keys("{ENTER}")
        await worker_sleep(2)
        app = Application().connect(title="Alteração de Item")
        main_window = app["Alteração de Item"]
        main_window.set_focus()
        edit = main_window.child_window(class_name="TDBIEditCode", found_index=0)
        index_ultimo_item = int(edit.window_text())
        try:
            btn_cancelar = main_window.child_window(title="&Cancelar")
            btn_cancelar.click()
        except Exception as error:
            btn_cancelar = main_window.child_window(title="Cancelar")
            btn_cancelar.click()
            console.print(f"Erro ao realizar get_ultimo_item: {error}")
        await worker_sleep(1)
        return index_ultimo_item

    async def verify_max_variation(self):
        try:
            console.print("Iniciando a coleta de dados do grid...\n")
            app = Application(backend="uia").connect(class_name="TFrmTelaSelecao")
            main_window = app.window(class_name="TFrmTelaSelecao")
            grid = main_window.child_window(class_name="TcxGridSite")
            grid.set_focus()
            grid_wrapper = grid.wrapper_object()
            send_keys("^({HOME})")
            await worker_sleep(1)
            data_list = []
            last_content = ""
            repeat_count = 0
            max_repeats = 2
            while True:
                send_keys("^c")
                await worker_sleep(1)
                current_content = pyperclip.paste().strip()
                if not current_content:
                    console.print(
                        "Nenhum conteúdo copiado, encerrando loop.", style="bold red"
                    )
                    break
                item_data = await self.parse_copied_content(current_content)
                data_list.extend(item_data)
                last_content = current_content
                send_keys("{DOWN}")
                await worker_sleep(1)
                send_keys("^c")
                await worker_sleep(1)
                next_content = pyperclip.paste().strip()
                if next_content == last_content:
                    send_keys("{PGDN}")
                    await worker_sleep(1)
                    send_keys("{DOWN}")
                    await worker_sleep(1)
                    send_keys("^c")
                    await worker_sleep(1)
                    next_content = pyperclip.paste().strip()
                    if next_content == last_content:
                        repeat_count += 1
                        if repeat_count >= max_repeats:
                            console.print(
                                "Não há mais itens para processar. Fim do grid alcançado.",
                                style="bold green",
                            )
                            break
                    else:
                        repeat_count = 0
                else:
                    repeat_count = 0

            console.print(f"Dados coletados: {data_list}")

            itens_invalidos = []
            for item in data_list:
                if not (
                    item["custo_min"] - 4 <= item["curto"] <= item["custo_max"] + 4
                ):
                    itens_invalidos.append(item["codigo"])

            if itens_invalidos:
                console.print(
                    "Itens que Ultrapassaram a Variação Máxima de Custo",
                    style="bold yellow",
                )
                console.print(f"Códigos dos itens: {itens_invalidos}")
                send_keys("{ESC}")
                observacao = f"Itens que ultrapassaram a variação máxima de custo: {itens_invalidos}. Processo cancelado."
                return {"sucesso": False, "retorno": observacao}
            else:
                console.print(
                    "Todos os itens estão dentro da variação de custo permitida.",
                    style="bold green",
                )
                send_keys("{ENTER}")
                observacao = "Todos os itens estão dentro da variação de custo permitida. Processo concluído com sucesso."
                return {"sucesso": True, "retorno": observacao, "dados": data_list}
        except:
            ...

    async def parse_copied_content(self, content):
        lines = content.strip().split("\n")
        data_list = []
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if line.startswith("Código"):
                headers_line = line
                headers = headers_line.split("\t")
                i += 1
                if i < len(lines):
                    data_line = lines[i].strip()
                    data = data_line.split("\t")
                    if len(headers) == len(data):
                        item_dict = dict(zip(headers, data))
                        data_list.append(item_dict)
                    else:
                        console.print(
                            "Número de cabeçalhos e dados não correspondem.",
                            style="bold red",
                        )
                        console.print(f"Cabeçalhos: {headers}")
                        console.print(f"Dados: {data}")
                else:
                    console.print(
                        "Sem linha de dados após cabeçalho.", style="bold red"
                    )
                i += 1
            else:
                i += 1

        final_list = []
        for item in data_list:
            try:
                new_item = {
                    "codigo": int(item["Código"]),
                    "descricao": item["Descrição"],
                    "curto": float(item["R$ Curto"].replace(".", "").replace(",", ".")),
                    "custo_min": float(
                        item["R$ Custo Min."]
                        .replace("worker_automate_hub/utils/utils_nfe_entrada.py.", "")
                        .replace(",", ".")
                    ),
                    "custo_max": float(
                        item["R$ Custo Máx."].replace(".", "").replace(",", ".")
                    ),
                }
                final_list.append(new_item)
            except Exception as e:
                console.print(
                    f"Erro ao processar item: {item}. Erro: {e}", style="bold red"
                )
        return final_list

    async def download_xml(
        self, google_drive_folder_id: str, get_gcp_token: RpaConfiguracao, get_gcp_credentials: RpaConfiguracao, chave_nota: str
    ) -> dict:

        try:
            console.print("Verificando a existência do arquivo no Google Drive...\n")
            chave_nota = f"{chave_nota}.xml"
            gcp_credencial = GetCredsGworkspace(
                token_dict=get_gcp_token.conConfiguracao,
                credentials_dict=get_gcp_credentials.conConfiguracao,
            )
            creds = gcp_credencial.get_creds_gworkspace()

            if not creds:
                console.print(f"Erro ao obter autenticação para o GCP...\n")
                return {
                    "sucesso": False,
                    "retorno": f"Erro ao obter autenticação para o GCP",
                }

            # Inicializando o serviço do Google Drive
            drive_service = build("drive", "v3", credentials=creds)

            # Query para procurar o arquivo com o nome da chave da nota
            query = f"'{google_drive_folder_id}' in parents and name contains '{chave_nota}'"
            results = (
                drive_service.files()
                .list(
                    q=query,
                    pageSize=10,  # Reduzindo o número de resultados
                    supportsAllDrives=True,
                    includeItemsFromAllDrives=True,
                    fields="files(id, name)",
                )
                .execute()
            )

            # Verificando se o arquivo foi encontrado
            items = results.get("files", [])

            if not items:
                console.print(
                    f"Nenhum arquivo com o nome {chave_nota} foi encontrado...\n"
                )
                return {
                    "sucesso": False,
                    "retorno": f"Nenhum arquivo com o nome {chave_nota} foi encontrado no Google Drive",
                }

            # Pegando o primeiro arquivo encontrado
            file_id = items[0]["id"]
            file_name = items[0]["name"]
            console.print(f"Arquivo {file_name} encontrado. Iniciando o download...\n")

            # Definindo o caminho local para salvar o arquivo
            file_path = os.path.join(os.path.expanduser("~"), "Downloads", file_name)

            # Iniciando o download
            request = drive_service.files().get_media(fileId=file_id)
            fh = io.FileIO(file_path, "wb")
            downloader = MediaIoBaseDownload(fh, request)

            done = False
            while not done:
                status, done = downloader.next_chunk()
                console.print(f"Download {int(status.progress() * 100)}% concluído.")

            console.print(
                f"Arquivo {file_name} baixado com sucesso e salvo em {file_path}.\n"
            )
            return {
                "sucesso": True,
                "retorno": f"Arquivo {file_name} baixado com sucesso",
            }

        except Exception as e:
            console.print(f"Erro ao baixar o arquivo do Google Drive, erro: {e}...\n")
            return {
                "sucesso": False,
                "retorno": f"Erro ao baixar o arquivo do Google Drive, erro: {e}",
            }

    async def get_xml(self, xml_file):
        username = getpass.getuser()
        xml_name = f"{xml_file}.xml"
        path_to_xml = f"C:\\Users\\{username}\\Downloads\\{xml_name}"
        pyautogui.click(722, 792)
        await worker_sleep(2)
        pyautogui.write(path_to_xml)
        await worker_sleep(2)
        pyautogui.hotkey("enter")
        await worker_sleep(2)

    async def delete_xml(self, nfe_key: str) -> None:
        """
        Deletes an XML file for a given NFe key from the user's Downloads folder.

        Args:
            nfe_key: The key of the NFe to delete the XML file for.

        Returns:
            None
        """
        try:
            if not nfe_key:
                raise ValueError("nfe_key não pode ser nulo ou vazio")

            xml_filename = f"{nfe_key}.xml"
            download_folder = os.path.join(os.path.expanduser("~"), "Downloads")
            file_path = os.path.join(download_folder, xml_filename)

            if not os.path.exists(file_path):
                console.print(
                    f"Arquivo {xml_filename} não encontrado em {download_folder}.",
                    style="bold yellow",
                )
                return

            if not os.path.isfile(file_path):
                raise ValueError(f"{file_path} não é um arquivo")

            os.remove(file_path)
            console.print(
                f"Arquivo {xml_filename} deletado com sucesso.", style="bold green"
            )
        except Exception as e:
            console.print(
                f"Erro ao deletar o arquivo {xml_filename}: {str(e)}", style="bold red"
            )
            raise Exception(
                f"Erro ao deletar o arquivo {xml_filename}: {str(e)}"
            ) from e

    async def alterar_nop(self, cfop: str) -> RpaRetornoProcessoDTO | None:
        await self.click_principal()
        console.print("Alterando a NOP...\n")
        pyautogui.click(945, 543)
        await worker_sleep(2)

        if cfop:
            console.print(
                f"Inserindo a informação da NOP, caso se aplique {cfop} ...\n"
            )
            if cfop != "5910" and cfop != "6910":
                set_combobox("||List", "1403 - COMPRA DE MERCADORIA - 1.403")
                await worker_sleep(3)
                self.incluir_registro()
            else:
                pyautogui.hotkey("esc")
                observacao = f"Nota bonificada do tipo ({cfop}), está retornando diferença de itens sem o mesmo CFOP de capa. Por favor verifique a nota."
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=observacao,
                    status=RpaHistoricoStatusEnum.Falha,
                )
