from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import time

print("Iniciando script: Processar TODOS os torneios 'Entrada Livre' do Fortnite...")

# --- 1. Configuração do Perfil ---
profile_user_data_dir = r"C:\TempChromeSeleniumProfile" 

options = Options()
options.add_argument(f"user-data-dir={profile_user_data_dir}")

# --- Opções para MODO HEADLESS ---
options.add_argument("--headless")
options.add_argument("--disable-gpu") # Opcional, mas frequentemente usado com headless
options.add_argument("--window-size=1920,1080") # Define um tamanho de janela virtual
# --- Fim das Opções para MODO HEADLESS ---

options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--start-maximized") # Esta opção pode ser redundante ou conflitar com window-size em headless, mas geralmente não causa problemas.
options.add_argument('--disable-blink-features=AutomationControlled')
driver = None
try:
    service = ChromeService(executable_path=ChromeDriverManager().install())
    print(f"Tentando iniciar Chrome com User Data Dir: '{profile_user_data_dir}'")
    
    driver = webdriver.Chrome(service=service, options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    print("Navegador Chrome iniciado com o perfil.")
    
    fortnite_tournaments_url = "https://www.repeat.gg/pc/fortnite"
    print(f"Navegando para a página de torneios do Fortnite: {fortnite_tournaments_url}")
    driver.get(fortnite_tournaments_url)
    print("Aguardando 10 segundos para a página de torneios carregar...")
    time.sleep(10) 
    
    print(f"Título da página atual: {driver.title}")
    print("Assumindo que o usuário está logado se o perfil foi carregado corretamente.")
    is_logged_in = True 

    if not is_logged_in:
        print("Problema com o login. Saindo.")
        # exit() 

    print("Procurando por torneios 'Entrada Livre'...")
    tournament_row_selector_xpath = "//a[@data-testid='tournament row']"
    
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, tournament_row_selector_xpath))
        )
        print("Cards de torneio encontrados na página.")
    except TimeoutException:
        print("Nenhum card de torneio encontrado com o seletor. Verifique o seletor e a página.")
        # exit() # Você pode querer sair aqui se nenhum card for encontrado

    all_tournament_cards = driver.find_elements(By.XPATH, tournament_row_selector_xpath)
    print(f"Total de cards de torneio encontrados: {len(all_tournament_cards)}")

    free_entry_tournament_links = []
    for card in all_tournament_cards:
        try:
            card_text_content = card.text 
            is_free_entry = "Entrada livre" in card_text_content
            is_not_closed = "Fechado" not in card_text_content 
            # Você pode adicionar mais verificações aqui, ex: se o status é "Abrir"
            # is_open = "Abrir" in card_text_content 
            # if is_free_entry and is_not_closed and is_open:
            if is_free_entry and is_not_closed:
                tournament_link = card.get_attribute('href')
                if tournament_link:
                    cleaned_card_text = card_text_content[:100].replace('\n', ' ')
                    print(f"  Encontrado torneio 'Entrada Livre' elegível: {tournament_link} (Texto: {cleaned_card_text}...)")
                    free_entry_tournament_links.append(tournament_link)
        except StaleElementReferenceException:
            print("  Elemento do card tornou-se obsoleto durante a coleta de links. Pulando.")
            continue
        except Exception as e_card_check:
            print(f"  Erro ao verificar um card durante a coleta de links: {e_card_check}")

    print(f"\nTotal de links de torneios 'Entrada Livre' e abertos para processar: {len(free_entry_tournament_links)}")

    if not free_entry_tournament_links:
        print("Nenhum torneio 'Entrada Livre' e aberto encontrado para se inscrever.")
    
    for i, t_link in enumerate(free_entry_tournament_links):
        print(f"\n--- Processando torneio {i+1}/{len(free_entry_tournament_links)}: {t_link} ---")
        try:
            driver.get(t_link)
            print(f"  Navegou para: {driver.current_url}")
            print(f"  Título da página do torneio: {driver.title}")
            print("  Aguardando 7 segundos para a página do torneio carregar completamente...")
            time.sleep(7)

            join_button_xpath = "//section[@data-testid='tournament-phases']//button[normalize-space()='Junte-se ao torneio']"
            print(f"  Tentando encontrar o botão específico 'Junte-se ao torneio' com XPath: {join_button_xpath}")

            try:
                join_button = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, join_button_xpath))
                )
                button_text = join_button.text.strip() if join_button.text else "Junte-se ao torneio"
                print(f"  Botão específico '{button_text}' encontrado e está clicável.")
                
                driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", join_button)
                time.sleep(1) 
                
                print(f"  >>> TENTANDO CLICAR no botão específico '{button_text}'...")
                join_button.click() 
                print(f"  <<< Botão específico '{button_text}' CLICADO.")
                time.sleep(5) 
                print(f"  URL atual após clique: {driver.current_url}")
                # Adicione verificações aqui, por exemplo, se o botão desapareceu ou mudou de texto
                try:
                    # Tenta encontrar o botão novamente, se não encontrar, pode ser um sinal de sucesso
                    WebDriverWait(driver, 3).until_not(
                         EC.element_to_be_clickable((By.XPATH, join_button_xpath))
                    )
                    print("  Botão 'Junte-se ao torneio' não está mais clicável (bom sinal após clique).")
                except TimeoutException:
                    # Se o botão ainda estiver lá, verifique o texto ou outras pistas
                    print("  Botão 'Junte-se ao torneio' ainda parece estar presente/clicável. Verifique manualmente.")


            except TimeoutException:
                print(f"  Botão específico 'Junte-se ao torneio' (XPath: {join_button_xpath}) não encontrado ou não clicável.")
                page_content_lower = driver.page_source.lower()
                if "inscrição termina em" in page_content_lower or "inscrições encerradas" in page_content_lower:
                    print("  INFO: A inscrição para este torneio pode ter um tempo limite ou já estar encerrada.")
                elif "você já está neste torneio" in page_content_lower or "já inscrito" in page_content_lower:
                    print("  INFO: Parece que você já está inscrito neste torneio.")
                else:
                    # Tentar o botão mais genérico (pode ser o do topo da página)
                    generic_join_button_xpath = "//button[normalize-space()='Junte-se ao torneio']"
                    print(f"  Tentando encontrar um botão 'Junte-se ao torneio' mais genérico com XPath: {generic_join_button_xpath}")
                    try:
                        generic_join_button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, generic_join_button_xpath))
                        )
                        g_button_text = generic_join_button.text.strip() if generic_join_button.text else "Junte-se ao torneio"
                        print(f"  Botão GENÉRICO '{g_button_text}' encontrado e clicável.")
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", generic_join_button)
                        time.sleep(1)
                        print(f"  >>> TENTANDO CLICAR no botão GENÉRICO '{g_button_text}'...")
                        generic_join_button.click() 
                        print(f"  <<< Botão GENÉRICO '{g_button_text}' CLICADO.")
                        time.sleep(5)
                        print(f"  URL atual APÓS clique no botão GENÉRICO: {driver.current_url}")
                    except TimeoutException:
                        print("  Nenhum botão 'Junte-se ao torneio' (nem o específico, nem o genérico) foi encontrado ou não era clicável.")
                    except Exception as e_generic_click:
                        print(f"  Erro ao tentar clicar no botão GENÉRICO: {e_generic_click}")
            except Exception as e_specific_click:
                print(f"  Erro ao tentar clicar no botão específico: {e_specific_click}")

            # Pequena pausa entre o processamento de cada torneio para não sobrecarregar o site
            print("  Pausa de 5 segundos antes de ir para o próximo torneio...")
            time.sleep(5)
            
            # REMOVIDO o "break" para processar todos os torneios:
            # if i == 0: 
            #      print("\nExemplo processou o primeiro torneio encontrado. Saindo do loop de torneios para teste.")
            #      break 

        except Exception as e_nav:
            print(f"  Erro ao processar o link {t_link}: {e_nav}")
        
    print("\nTodos os torneios elegíveis foram processados.")
    print("Aguardando 10 segundos antes de fechar...")
    time.sleep(10)

except Exception as e:
    print(f"ERRO GERAL NO SCRIPT: {e}")

finally:
    if driver:
        print("Fechando o navegador.")
        driver.quit()
    print("Script finalizado.")
    