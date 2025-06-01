from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

print("Iniciando script: Abrir perfil, verificar login e clicar no link do Fortnite...")

# --- 1. Configuração do Perfil ---
# Use o caminho que funcionou para você.
# Este é baseado no nosso último teste bem-sucedido com a cópia isolada.
profile_user_data_dir = r"C:\TempChromeSeleniumProfile" # Ou o caminho do seu perfil funcional

options = Options()
options.add_argument(f"user-data-dir={profile_user_data_dir}")
# Se estiver usando um perfil nomeado DENTRO do User Data principal (ex: "Profile 3"),
# você também precisaria de:
# user_data_dir_principal = r"C:\Users\Administrador\AppData\Local\Google\Chrome\User Data"
# profile_a_usar = "Profile 3"
# options.add_argument(f"user-data-dir={user_data_dir_principal}")
# options.add_argument(f"profile-directory={profile_a_usar}")


options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--start-maximized")
options.add_argument('--disable-blink-features=AutomationControlled')

driver = None
try:
    service = ChromeService(executable_path=ChromeDriverManager().install())
    print(f"Tentando iniciar Chrome com User Data Dir: '{profile_user_data_dir}'")
    
    driver = webdriver.Chrome(service=service, options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    print("Navegador Chrome iniciado com o perfil.")
    
    # --- 2. Navegar e Verificar Login ---
    # Recomendo testar na página inicial primeiro, onde os jogos são listados.
    target_url = "https://www.repeat.gg/compete"
    print(f"Navegando para {target_url}...")
    driver.get(target_url) 
    print("Aguardando 7 segundos para a página carregar...")
    time.sleep(7) 
    
    print(f"Título da página: {driver.title}")
    
    is_logged_in = False
    login_indicator_xpath = "//h1[contains(@class, 'mui-65s56h') and normalize-space(text())='Competir']"
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, login_indicator_xpath))
        )
        print("INDICADOR DE LOGIN ENCONTRADO! Usuário está logado.")
        is_logged_in = True
    except TimeoutException:
        print("Indicador de login NÃO encontrado. O usuário pode não estar logado.")
    except Exception as e_login:
        print(f"Erro ao verificar o indicador de login: {e_login}")

    # --- 3. Se logado, encontrar e clicar no LINK do Fortnite ---
    if is_logged_in:
        print("Procurando pelo link do jogo Fortnite...")
        
        # Usar o XPath para o link com o href específico
        fortnite_link_xpath = "//a[@href='/pc/fortnite']"
        
        try:
            print(f"Procurando pelo link do Fortnite usando XPath: {fortnite_link_xpath}")
            
            # Esperar o elemento ser clicável
            fortnite_link_element = WebDriverWait(driver, 20).until( # Aumentei um pouco o timeout
                EC.element_to_be_clickable((By.XPATH, fortnite_link_xpath))
            )
            print("Link do Fortnite encontrado e está clicável!")

            print("Tentando clicar no link do Fortnite...")
            # Rolar para o elemento pode ajudar se ele estiver fora da tela
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", fortnite_link_element)
            time.sleep(0.5) # Pequena pausa após rolar
            
            fortnite_link_element.click()
            print("Link do Fortnite clicado com sucesso!")
            time.sleep(5) # Dar tempo para a navegação
            print(f"URL atual: {driver.current_url}")
            # Agora você deve estar na página de torneios do Fortnite
            # Verifique se a URL mudou para algo como https://www.repeat.gg/pc/fortnite/tournaments
            if "/pc/fortnite" in driver.current_url:
                print("Navegação para a página do Fortnite parece correta.")
            else:
                print("Atenção: A URL não mudou como esperado após o clique.")
            
        except TimeoutException:
            print("Link do Fortnite (com href='/pc/fortnite') não foi encontrado ou não se tornou clicável a tempo.")
            print("Verifique se o XPath está correto e se a página carregou completamente com os cards dos jogos visíveis.")
        except Exception as e_card:
            print(f"Ocorreu um erro ao procurar ou clicar no link do Fortnite: {e_card}")
    else:
        print("Usuário não está logado, portanto, a busca pelo link do jogo não será realizada.")
        
    print("Aguardando 10 segundos antes de fechar...")
    time.sleep(10)

except Exception as e:
    print(f"ERRO GERAL NO SCRIPT: {e}")

finally:
    if driver:
        print("Fechando o navegador.")
        driver.quit()
    print("Script finalizado.")