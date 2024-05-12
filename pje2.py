# import requests as rq
# from requests import Session
# from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException, TimeoutException, NoSuchElementException
# import undetected_chromedriver as uc
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome

from time import sleep
import glob
import pandas as pd
import sqlite3
import os
import logging
from dotenv import load_dotenv, set_key

# @merinte35

class Pje():
    def __init__(self) -> None:
        load_dotenv('auth/.env')

        self.login = os.getenv('login')
        self.senha = os.getenv('senha')

        def salvar_login():
            while True:
                print('Informe o login:')
                login = str(input())
                if login == '':
                    print('É preciso informar o login!')
                    sleep(1)
                    continue
                break
            while True:
                print('Agora, informe a senha:')
                senha = str(input())
                if senha == '':
                    print('É preciso informar uma senha!')
                    sleep(1)
                    continue
                break

            set_key('auth/.env', 'login', login)
            set_key('auth/.env', 'senha', senha)

            print()
            print('Pronto! Agora os dados de login estão salvos.')
            sleep(2)
            print('Continuando com o bot...')
            print()
            sleep(1)

        if self.login == '' or self.senha == '':
            print('! ! ! ! ! ! ! ! ! ! ! ! ! ! ! !')
            print('Falta dados de login ou senha.')
            print('! ! ! ! ! ! ! ! ! ! ! ! ! ! ! !')

            salvar_login()

        else:
            print('Deseja seguir com o login atual? [s/n]')
            while True:
                r = str(input())
                if r.lower() not in 'sn' or r.lower() == '':
                    print('Somente é válido "s" para SIM e "n" para NÃO.')
                    print('Tente novamente.')
                    continue
                if r.lower() == 's':
                    break
                elif r.lower() == 'n':
                    print()
                    salvar_login()
                    break

        logging.basicConfig(level=logging.INFO, filemode='w', format='%(asctime)s - %(levelname)s - %(message)s', filename='log.log')

        arquivos = glob.glob('read/*')
        arquivo = arquivos[0]
        self.nome_arquivo = arquivo.removeprefix('read\\')
        self.nome_arquivo = self.nome_arquivo.removesuffix('.xlsx')

        try:
            os.makedirs(f'results/{self.nome_arquivo}')
        except FileExistsError:
            pass

        self.chaves = ['NOME', 'CPF', 'NÚMERO DO PROCESSO', 'DATA DE DISTRIBUIÇÃO', 'NB', 'DATA DE INDEFERIMENTO', 'DATA DER', 'ESPÉCIE', 'MOTIVO DO INDEFERIMENTO', 'CLASSE JUDICIAL', 'LOCALIDADE', 'TIPO DE SISTEMA', 'ADVOGADOS', 'FASE']

        self.conn = sqlite3.connect(f'results/{self.nome_arquivo}/dados.db')
        self.cursor = self.conn.cursor()

        self.cursor.execute('CREATE TABLE IF NOT EXISTS ativos (nome TEXT, cpf TEXT, processo TEXT, data_dis TEXT, nb TEXT, data_inder TEXT, data_der TEXT, especie TEXT, motivo TEXT, classe TEXT, local TEXT, tipo TEXT, advogados TEXT, fase TEXT)')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS arquivados (nome TEXT, cpf TEXT, processo TEXT, data_dis TEXT, nb TEXT, data_inder TEXT, data_der TEXT, especie TEXT, motivo TEXT, classe TEXT, local TEXT, tipo TEXT, advogados TEXT, fase TEXT)')

        self.conn.commit()

        self.df = pd.read_excel(arquivo, dtype=str)
        self.cpf_list = self.df['CPF'].to_list()
        try:    
            self.nome_list = self.df['NOME'].to_list()
        except KeyError:
            self.nome_list = self.df['Nome'].to_list()

        try:
            self.df['DATA DA DER'] = pd.to_datetime(self.df['DATA DA DER'])
            self.df['DATA DA DER'] = self.df['DATA DA DER'].dt.strftime('%d/%m/%Y')
        except KeyError:
            pass

        try:
            self.df['DATA DE INDEFERIMENTO'] = pd.to_datetime(self.df['DATA DE INDEFERIMENTO'])
            self.df['DATA DE INDEFERIMENTO'] = self.df['DATA DE INDEFERIMENTO'].dt.strftime('%d/%m/%Y')
        except KeyError:
            pass

        try:
            self.nb_list = self.df['NB'].to_list()
            self.data_inder_list = self.df['DATA DE INDEFERIMENTO'].to_list()
            self.data_der_list = self.df['DATA DA DER'].to_list()
            self.especie_list = self.df['ESPÉCIE'].to_list()
            self.motivo_inder_list = self.df['MOTIVO DO INDEFERIMENTO'].to_list()
        except:
            pass

        try:
            with open(f'results/{self.nome_arquivo}/processos.txt') as file:
                processos = file.read()
                self.proc_list = processos.split(';')
        except FileNotFoundError:
            self.proc_list = []

    def abrir(self):
        url = 'https://pje1g.trf5.jus.br/pje/login.seam'

        options = Options()        
        options.add_argument("--password-store=basic")
        options.add_argument("--headless=new")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option(
            "prefs",
            {
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False,
            },
        )
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        logging.info('Entrando no site...')
        print('Entrando no site...')

        self.driver = Chrome(service=Service(ChromeDriverManager().install()), options=options)

        self.driver.maximize_window()
        self.driver.get(url)

    def logar(self):
        self.wa = WebDriverWait(self.driver, 120)

        self.wa.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#ssoFrame")))

        iframe = self.driver.find_element(By.CSS_SELECTOR, "#ssoFrame")
        self.driver.switch_to.frame(iframe)

        # password = str(input('Digite a senha: '))

        logging.info('Fazendo login...')
        print('Fazendo login...')
        print()

        login = self.driver.find_element(By.ID, 'username')
        login.send_keys(self.login)
        sleep(1)

        senha = self.driver.find_element(By.ID, 'password')
        senha.send_keys(self.senha)
        sleep(1)

        btn_entrar = self.driver.find_element(By.ID, 'kc-login')
        btn_entrar.click()

        # input('Após clicar em entrar, verifique se o login foi efetuado corretamente. Então, tecle ENTER para continuar')

        # self.wa.until(EC.presence_of_element_located((By.XPATH, '//*[@id="barraSuperiorPrincipal"]/div/div[1]/div/span')))

        sleep(2)

    def coletar(self):
        url2 = 'https://pje1g.trf5.jus.br/pje/Processo/ConsultaProcesso/listView.seam'

        self.driver.get(url2)

        try:
            with open(f'results/{self.nome_arquivo}/index.txt') as file:
                ini = file.read()
                ini = int(ini)
            logging.info(f'Continuando trabalho na planilha {self.nome_arquivo}')
            print(f'Continuando trabalho na planilha {self.nome_arquivo}')
            print()
        except FileNotFoundError:
            ini = 0
            logging.info(f'Iniciando trabalho na planilha {self.nome_arquivo}')
            print(f'Iniciando trabalho na planilha {self.nome_arquivo}')
            print()

        for i in range(ini, len(self.cpf_list)):
            cpf = str(self.cpf_list[i])
        
            while len(cpf) < 11:
                cpf = list(cpf)
                cpf.insert(0, '0')
                cpf = ''.join(cpf)

            self.df['CPF'].loc[i] = cpf

            # cpf = f'{c[:3]}.{c[3:6]}.{c[6:9]}-{c[9:]}'

            with open(f'results/{self.nome_arquivo}/index.txt', 'w') as file:
                file.write(str(i))

            nome = self.nome_list[i]
            try:
                nb = self.nb_list[i]
                data_inder = self.data_inder_list[i]
                data_der = self.data_der_list[i]
                especie = self.especie_list[i]
                motivo = self.motivo_inder_list[i]
            except:
                nb = data_der = data_inder = especie = motivo = ''

            logging.info(f'{i+1} - {cpf} - {nome}')
            print(f'{i+1} - {cpf} - {nome}')

            while True:
                try:
                    self.wa.until(EC.presence_of_element_located((By.XPATH, '//*[@id="fPP:dpDec:documentoParte"]')))

                    cpf_input = self.driver.find_element(By.XPATH, '//*[@id="fPP:dpDec:documentoParte"]')
                    cpf_input.clear()
                    sleep(1)
                    cpf_input.click()
                    cpf_input.send_keys(cpf)
                    sleep(0.5)
                    cpf_input.send_keys(Keys.ENTER)
                    sleep(1)

                    try:
                        self.driver.find_element(By.CLASS_NAME, 'rich-messages-label')
                        sleep(2)
                        continue
                    except:
                        pass

                    # wa2 = WebDriverWait(self.driver, 3)
                    # wa2.until(EC.presence_of_element_located((By.CLASS_NAME, 'rich-table-row')))
                    linhas = self.driver.find_elements(By.CLASS_NAME, 'rich-table-row')
                    sleep(0.5)

                    if linhas == []:
                        logging.info('Sem processos.')
                        print('\tSem processos.')

                        self.proc_list.append('-')  
                    else:
                        client_procs = []
                        for linha in linhas:
                            
                            sleep(1)
                            processo_link = linha.find_element(By.CLASS_NAME, 'btn-condensed')

                            processo = processo_link.text
                            logging.info(f'Processo: {processo}')
                            print(f'\tProcesso: {processo}')
                            processo_link.click()

                            wa_alert = WebDriverWait(self.driver, 3)

                            try:
                                wa_alert.until(EC.alert_is_present())
                                sleep(0.5)

                                alert = self.driver.switch_to.alert

                                sleep(1)

                                alert.accept()
                            except TimeoutException:
                                pass

                            sleep(1)

                            try:
                                janelas = self.driver.window_handles
                                self.driver.switch_to.window(janelas[1])
                            except IndexError:
                                pass

                            sleep(1)

                            menu_detalhes_btn = self.driver.find_element(By.XPATH, '//*[@id="navbar"]/ul/li/a[1]')
                            menu_detalhes_btn.click()

                            sleep(0.5)

                            detalhes = self.driver.find_element(By.ID, 'maisDetalhes')
                            dts = detalhes.find_elements(By.TAG_NAME, 'dt')
                            dds = detalhes.find_elements(By.TAG_NAME, 'dd')

                            classe_judicial = dds[0].text
                            assunto = dds[1].text
                            local = dds[2].text
                            autuacao = dds[3].text
                            ultima_distri = dds[4].text
                            orgao = dds[10].text

                            ativo = self.driver.find_element(By.ID, 'poloAtivo')
                            lista = ativo.find_elements(By.TAG_NAME, 'li')

                            advogados_list = set()
                            for li in lista:
                                if '(ADVOGADO)' in li.text:
                                    advogados_list.add(li.text)
                            
                            advogados = '\n'.join(advogados_list)
                            
                            movimentos = self.driver.find_element(By.ID, 'divTimeLine:eventosTimeLineElement')
                            ultima_list = movimentos.find_elements(By.CLASS_NAME, 'texto-movimento')
                            mov_list = [mov.text for mov in ultima_list]

                            if 'BAIXA DEFINITIVA' in mov_list or 'ARQUIVADO DEFINITIVAMENTE' in mov_list:
                                ultima_mov = 'BAIXA DEFINITIVA'

                                dados = [nome, cpf, processo, ultima_distri, nb, data_inder, data_der, especie, motivo, classe_judicial, local, 'PJE', advogados, ultima_mov]

                                self.conn.execute('INSERT INTO arquivados (nome, cpf, processo, data_dis, nb, data_inder, data_der, especie, motivo, classe, local, tipo, advogados, fase) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', dados)

                                client_procs.append(f'***{processo}/PJE')
                            else:
                                ultima_mov = ultima_list[0].text

                                dados = [nome, cpf, processo, ultima_distri, nb, data_inder, data_der, especie, motivo, classe_judicial, local, 'PJE', advogados, ultima_mov]

                                self.conn.execute('INSERT INTO ativos (nome, cpf, processo, data_dis, nb, data_inder, data_der, especie, motivo, classe, local, tipo, advogados, fase) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', dados)
                            
                                client_procs.append(f'***{processo}/PJE(ATIVO)')

                            self.conn.commit()

                            self.driver.close()
                            self.driver.switch_to.window(janelas[0])

                            processo_final = '\n'.join(client_procs)

                            sleep(1)
                        
                        self.proc_list.append(processo_final)

                    processos = ';'.join(self.proc_list)

                    with open(f'results/{self.nome_arquivo}/processos.txt', 'w') as file:
                        file.write(processos)

                    break
                except StaleElementReferenceException as er:
                    logging.exception(er)
                    print(er)
                    sleep(1)
                    continue
                except ElementClickInterceptedException as err:
                    logging.exception(err)
                    print("Erro ao clicar no elemento")
                    self.driver.refresh()
                    sleep(1)
                    continue
                except NoSuchElementException as nosuch:
                    logging.exception(nosuch)
                    print('Elemento não encontrado')
                    sleep(1)
                    continue
                except TimeoutException as time:
                    logging.exception(time)
                    print('Página demorou para carregar. Tentando de novo')
                    self.driver.refresh()
                    sleep(1)
                    continue

            sleep(1)

        self.driver.quit()

    def save(self):
        logging.info('Processo concluído.')
        print('Processo concluído.')
        logging.info('Salvando em nova planilha...')
        print('Salvando em nova planilha...')

        ativos = self.cursor.execute('SELECT * FROM ativos').fetchall()
        self.df_ativos = pd.DataFrame(ativos, columns=self.chaves)
        writer = pd.ExcelWriter(f'results/{self.nome_arquivo}/ativos.xlsx', engine='xlsxwriter')
        self.df_ativos.to_excel(writer, sheet_name='Planilha1', index=False)

        writer.close()

        logging.info(f'Planilha de ativos criada.')
        print(f'Planilha de ativos criada.')

        arquivados = self.cursor.execute('SELECT * FROM arquivados').fetchall()
        self.df_arquivos = pd.DataFrame(arquivados, columns=self.chaves)
        writer = pd.ExcelWriter(f'results/{self.nome_arquivo}/arquivados.xlsx', engine='xlsxwriter')
        self.df_arquivos.to_excel(writer, sheet_name='Planilha1', index=False)

        writer.close()

        logging.info(f'Planilha de arquivados criada.')
        print(f'Planilha de arquivados criada.')

        with open(f'results/{self.nome_arquivo}/processos.txt') as file:
            processos = file.read()
            proc_list = processos.split(';')

        self.df['PROCESSOS'] = proc_list
        writer = pd.ExcelWriter(f'results/{self.nome_arquivo}/{self.nome_arquivo} - processos.xlsx', engine='xlsxwriter')
        self.df.to_excel(writer, sheet_name='Planilha1', index=False)

        logging.info(f'Planilha {self.nome_arquivo} com processos criada')
        print(f'Planilha {self.nome_arquivo} com processos criada')

        logging.info('Trabalho finalizado.')
        print('Trabalho finalizado.')

        writer.close()
        self.conn.close()
        os.remove(f'results/{self.nome_arquivo}/index.txt')
        os.remove(f'results/{self.nome_arquivo}/dados.db')
        os.remove(f'results/{self.nome_arquivo}/processos.txt')

if __name__=='__main__':
    pje = Pje()
    while True:
        try:
            if len(pje.proc_list) < len(pje.cpf_list):
                pje.abrir()
                pje.logar()
                pje.coletar()
            pje.save()
            break
        except Exception as e:
            logging.exception('Ocorreu um erro')
            print('Ocorreu um erro', e)
            pje.driver.quit()
            sleep(1)
