import platform
import psutil
import os
import socket
import time
import hashlib
from colorama import Fore, Style, init
import pyfiglet
import webbrowser

init(autoreset=True)

def get_hwid():
    try:
        hostname = socket.gethostname()
        mac_addresses = []
        for interface, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                if addr.family == psutil.AF_LINK:
                    mac_addresses.append(addr.address)

        hwid_str = f"{hostname}{''.join(mac_addresses)}"
        hwid_hash = hashlib.md5(hwid_str.encode()).hexdigest()
        return hwid_hash
    except Exception as e:
        return str(e)

def open_link(link):
    try:
        webbrowser.open(link)
    except Exception as e:
        print(f"{Fore.RED}An error occurred while opening the link: {str(e)}{Style.RESET_ALL}")

def get_system_info():
    try:
        while True:
            system_info = {}

            # Operating System Information
            system_info['Operating System'] = platform.system()
            system_info['OS Version'] = platform.version()
            system_info['Architecture'] = platform.architecture()

            # CPU Information
            system_info['Processor'] = platform.processor()
            system_info['CPU Cores'] = os.cpu_count()
            system_info['CPU Usage'] = f"{psutil.cpu_percent(interval=1)}%"

            # Memory Information
            virtual_memory = psutil.virtual_memory()
            swap_memory = psutil.swap_memory()
            system_info['Total Memory (RAM)'] = f"{virtual_memory.total / (1024 ** 3):.2f} GB"
            system_info['Available Memory'] = f"{virtual_memory.available / (1024 ** 3):.2f} GB"
            system_info['Memory Usage'] = f"{virtual_memory.percent}%"
            system_info['Swap Memory'] = f"{swap_memory.total / (1024 ** 3):.2f} GB"

            # GPU Information (if NVIDIA GPU is available)
            try:
                import py3nvml
                py3nvml.py3nvml.nvmlInit()
                device_count = py3nvml.py3nvml.nvmlDeviceGetCount()
                gpu_info = []
                for i in range(device_count):
                    handle = py3nvml.py3nvml.nvmlDeviceGetHandleByIndex(i)
                    gpu_name = py3nvml.py3nvml.nvmlDeviceGetName(handle)
                    gpu_memory_info = py3nvml.py3nvml.nvmlDeviceGetMemoryInfo(handle)
                    gpu_info.append({
                        'GPU Name': gpu_name,
                        'GPU Memory Total': f"{gpu_memory_info.total / (1024 ** 3):.2f} GB",
                        'GPU Memory Used': f"{gpu_memory_info.used / (1024 ** 3):.2f} GB",
                        'GPU Memory Free': f"{gpu_memory_info.free / (1024 ** 3):.2f} GB",
                        'GPU Memory Usage': f"{(gpu_memory_info.used / gpu_memory_info.total) * 100:.2f}%"
                    })
                system_info['GPU Information'] = gpu_info
            except Exception as e:
                system_info['GPU Information'] = f"No NVIDIA GPU found"

            # Disk Information
            partitions = psutil.disk_partitions()
            disk_info = []
            for partition in partitions:
                usage = psutil.disk_usage(partition.mountpoint)
                disk_info.append({
                    'Device': partition.device,
                    'Mount Point': partition.mountpoint,
                    'File System Type': partition.fstype,
                    'Total Size': f"{usage.total / (1024 ** 3):.2f} GB",
                    'Used Space': f"{usage.used / (1024 ** 3):.2f} GB",
                    'Free Space': f"{usage.free / (1024 ** 3):.2f} GB",
                    'Disk Usage Percentage': f"{usage.percent}%"
                })
            system_info['Disk Information'] = disk_info

            # Network Information
            network_info = []
            network_counters = psutil.net_if_addrs()
            for interface, addrs in network_counters.items():
                interface_info = {'Interface': interface}
                for addr in addrs:
                    if addr.family == socket.AF_INET:
                        interface_info['IPv4 Address'] = addr.address
                        interface_info['Subnet Mask'] = addr.netmask
                    elif addr.family == socket.AF_INET6:
                        interface_info['IPv6 Address'] = addr.address
                network_info.append(interface_info)
            system_info['Network Information'] = network_info

            # Additional Information
            system_info['Hostname'] = socket.gethostname()
            system_info['Current User'] = os.getlogin()
            system_info['HWID'] = get_hwid()

            yield system_info
            time.sleep(10)  # Update every 10 seconds

    except Exception as e:
        yield f"{Fore.RED}An error occurred: {str(e)}{Style.RESET_ALL}"

def get_process_info():
    try:
        while True:
            process_info = []
            for process in psutil.process_iter(attrs=['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    process_info.append({
                        'Process ID': process.info['pid'],
                        'Name': process.info['name'],
                        'CPU Usage': f"{process.info['cpu_percent']:.2f}%",
                        'Memory Usage': f"{process.info['memory_percent']:.2f}%"
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
            yield process_info
    except Exception as e:
        yield f"{Fore.RED}An error occurred: {str(e)}{Style.RESET_ALL}"

def display_colored_system_info(system_info):
    os.system('cls' if os.name == 'nt' else 'clear')
    ascii_banner = pyfiglet.figlet_format("WICK TOOL", font="slant")
    print(f"{Fore.CYAN}{ascii_banner}{Style.RESET_ALL}")

    for category, info in system_info.items():
        print(f"{Fore.YELLOW}{category}:{Style.RESET_ALL}")
        if isinstance(info, list):
            for item in info:
                for key, value in item.items():
                    print(f"  {key}: {Fore.CYAN}{value}{Style.RESET_ALL}")
        else:
            print(f"  {info}")

def display_colored_process_info(process_info):
    os.system('cls' if os.name == 'nt' else 'clear')
    ascii_banner = pyfiglet.figlet_format("WICK TOOL", font="slant")
    print(f"{Fore.CYAN}{ascii_banner}{Style.RESET_ALL}")

    print(f"{Fore.YELLOW}Process Information:{Style.RESET_ALL}")
    if not process_info:
        print(f"  No running processes")
    else:
        for process in process_info:
            for key, value in process.items():
                print(f"  {key}: {Fore.CYAN}{value}{Style.RESET_ALL}")

def main():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        ascii_banner = pyfiglet.figlet_format("WICK TOOL", font="slant")
        print(f"{Fore.CYAN}{ascii_banner}{Style.RESET_ALL}")

        print(f"{Fore.GREEN}Main Menu:{Style.RESET_ALL}")
        print(f"  {Fore.MAGENTA}1. Display System Information{Style.RESET_ALL}")
        print(f"  {Fore.MAGENTA}2. Display Process Information{Style.RESET_ALL}")
        print(f"  {Fore.MAGENTA}3. Contact Info{Style.RESET_ALL}")
        print(f"  {Fore.MAGENTA}4. Exit{Style.RESET_ALL}")
        choice = input(f"{Fore.YELLOW}Enter your choice: {Style.RESET_ALL}")
        if choice == '1':
            system_info_generator = get_system_info()
            system_info = next(system_info_generator)
            display_colored_system_info(system_info)
            input("Press Enter to go back to main menu...")
        elif choice == '2':
            process_info_generator = get_process_info()
            while True:
                process_info = next(process_info_generator)
                display_colored_process_info(process_info)
                option = input(f"{Fore.YELLOW}Enter '1' to go back to the main menu : {Style.RESET_ALL}")
                if option == '1':
                    break
        elif choice == '3':
            while True:
                os.system('cls' if os.name == 'nt' else 'clear')
                ascii_banner = pyfiglet.figlet_format("WICK TOOL", font="slant")
                print(f"{Fore.CYAN}{ascii_banner}{Style.RESET_ALL}")

                print(f"{Fore.GREEN}Contact Info:{Style.RESET_ALL}")
                print(f"  {Fore.MAGENTA}1. My Website{Style.RESET_ALL}")
                print(f"  {Fore.MAGENTA}2. My GitHub{Style.RESET_ALL}")
                print(f"  {Fore.MAGENTA}3. My Instagram{Style.RESET_ALL}")
                print(f"  {Fore.MAGENTA}4. Go Back to Main Menu{Style.RESET_ALL}")
                contact_choice = input(f"{Fore.YELLOW}Enter a number : {Style.RESET_ALL}")
                if contact_choice == '1':
                    open_link("https://wickdev.xyz/")
                elif contact_choice == '2':
                    open_link("https://github.com/Wickdev077")
                elif contact_choice == '3':
                    open_link("https://www.instagram.com/mik__subhi/")
                elif contact_choice == '4':
                    break
                else:
                    print(f"{Fore.RED}Invalid choice. Please enter a valid option.{Style.RESET_ALL}")
        elif choice == '4':
            break

if __name__ == "__main__":
    main()
