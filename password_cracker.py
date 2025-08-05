#!/usr/bin/env python3
"""
Educational Password Cracking Tool
A comprehensive wordlist-based password hash cracking tool for educational purposes.

PURPOSE:
This tool demonstrates how weak passwords can be cracked using dictionary attacks.
It shows the importance of using strong, unique passwords for security.

EDUCATIONAL OBJECTIVES:
- Understand how password hashing works (MD5, SHA-1, SHA-256)
- Learn about wordlist/dictionary attacks
- See real-time password cracking statistics
- Appreciate the importance of strong password policies

HOW TO USE:
1. Run the program: python password_cracker_complete.py
2. Agree to use the tool responsibly
3. Choose a hash algorithm (MD5, SHA-1, or SHA-256)
4. Paste your target hash when prompted
5. Use default wordlist or specify a custom one
6. Watch as the tool attempts to crack the password

COMMAND LINE OPTIONS:
- --hash-type {1,2,3}: Skip hash selection (1=MD5, 2=SHA-1, 3=SHA-256)
- --target HASH: Provide hash directly via command line
- --wordlist PATH: Use custom wordlist file
- --verbose: Show detailed progress information

EXAMPLES:
python password_cracker_complete.py
python password_cracker_complete.py --hash-type 1 --target e10adc3949ba59abbe56e057f20f883e
python password_cracker_complete.py --wordlist /path/to/custom.txt --verbose

For educational and authorized testing purposes only.

Author: Oren Daniel Melake
Date: July 30, 2025
"""

import hashlib
import argparse
import time
import sys
from pathlib import Path
from typing import Optional, Callable, Generator

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    from rich.prompt import Prompt, Confirm
    from rich.table import Table
    from rich import print as rprint
    RICH_AVAILABLE = True
    # Initialize rich console
    console = Console()
except ImportError:
    RICH_AVAILABLE = False
    Console = None
    Panel = None
    Text = None
    Prompt = None
    Confirm = None
    Table = None
    print("Note: 'rich' library not found. Install with: pip install rich")
    print("Falling back to basic console output.\n")
    
    # Basic console fallback
    class BasicConsole:
        def print(self, text, **kwargs):
            # Remove rich markup for basic console
            import re
            clean_text = re.sub(r'\[/?[^\]]*\]', '', str(text))
            print(clean_text)
        
        def clear(self):
            import os
            os.system('cls' if os.name == 'nt' else 'clear')
    
    console = BasicConsole()

# Supported hash algorithms mapping
HASH_ALGORITHMS = {
    "1": {"name": "MD5", "func": hashlib.md5},
    "2": {"name": "SHA-1", "func": hashlib.sha1},
    "3": {"name": "SHA-256", "func": hashlib.sha256}
}

def display_banner():
    """Display welcome banner with educational disclaimer."""
    if RICH_AVAILABLE:
        banner = """
        ██████╗  █████╗ ███████╗███████╗██╗    ██╗ ██████╗ ██████╗ ██████╗ 
        ██╔══██╗██╔══██╗██╔════╝██╔════╝██║    ██║██╔═══██╗██╔══██╗██╔══██╗
        ██████╔╝███████║███████╗███████╗██║ █╗ ██║██║   ██║██████╔╝██║  ██║
        ██╔═══╝ ██╔══██║╚════██║╚════██║██║███╗██║██║   ██║██╔══██╗██║  ██║
        ██║     ██║  ██║███████║███████║╚███╔███╔╝╚██████╔╝██║  ██║██████╔╝
        ╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝ ╚══╝╚══╝  ╚═════╝  ╚═╝  ╚═╝╚═════╝ 
                                ██████╗██████╗  █████╗  ██████╗██║  ██╗███████╗██████╗ 
                               ██╔════╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗
                               ██║     ██████╔╝███████║██║     █████╔╝ █████╗  ██████╔╝
                               ██║     ██╔══██╗██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗
                               ╚██████╗██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║
                                ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
        """
        
        console.print(Panel(
            Text(banner, style="bold cyan"),
            title="[bold red]Educational Password Cracking Tool[/bold red]",
            subtitle="[yellow]For Educational and Authorized Testing Only[/yellow]",
            border_style="bright_blue"
        ))
        
        # Purpose and instructions
        purpose = """
        [bold blue]PURPOSE:[/bold blue]
        This tool demonstrates how weak passwords can be cracked using dictionary attacks.
        It teaches the importance of using strong passwords for cybersecurity.
        
        [bold green]HOW TO USE:[/bold green]
        1. Choose a hash algorithm (MD5, SHA-1, or SHA-256)
        2. Paste your target hash when prompted
        3. Use the default wordlist or specify a custom one
        4. Watch the cracking process with real-time statistics
        
        [bold yellow]FEATURES:[/bold yellow]
        • Support for MD5, SHA-1, and SHA-256 hashing
        • Paste-friendly hash input with validation
        • Real-time progress tracking and statistics
        • Comprehensive wordlist with 4,000+ passwords
        • Command-line options for automation
        """
        
        console.print(Panel(purpose, border_style="blue", padding=(1, 2)))
        
        # Educational disclaimer
        disclaimer = """
        [bold red]⚠️  EDUCATIONAL DISCLAIMER ⚠️[/bold red]
        
        This tool is designed for educational purposes and authorized security testing only.
        
        [bold yellow]Authorized Uses:[/bold yellow]
        • Learning about password security and hashing
        • Authorized penetration testing with proper permissions
        • Educational cybersecurity training
        • Testing your own systems and passwords
        
        [bold red]Prohibited Uses:[/bold red]
        • Cracking passwords without explicit authorization
        • Any illegal or malicious activities
        • Unauthorized access to systems or accounts
        
        [bold green]By using this tool, you agree to use it responsibly and legally.[/bold green]
        """
        
        console.print(Panel(disclaimer, border_style="red", padding=(1, 2)))
    else:
        print("=" * 70)
        print("           EDUCATIONAL PASSWORD CRACKING TOOL")
        print("         For Educational and Authorized Testing Only")
        print("=" * 70)
        print("\nPURPOSE:")
        print("This tool demonstrates how weak passwords can be cracked using dictionary attacks.")
        print("It teaches the importance of using strong passwords for cybersecurity.")
        print("\nHOW TO USE:")
        print("1. Choose a hash algorithm (MD5, SHA-1, or SHA-256)")
        print("2. Paste your target hash when prompted")
        print("3. Use the default wordlist or specify a custom one")
        print("4. Watch the cracking process with real-time statistics")
        print("\n" + "=" * 70)
        print("⚠️  EDUCATIONAL DISCLAIMER ⚠️")
        print("This tool is for educational purposes and authorized security testing only.")
        print("By using this tool, you agree to use it responsibly and legally.")
        print("=" * 70)

def get_user_confirmation():
    """Get user confirmation for responsible use."""
    if RICH_AVAILABLE:
        return Confirm.ask("[bold yellow]Do you understand and agree to use this tool responsibly?[/bold yellow]")
    else:
        while True:
            response = input("\nDo you understand and agree to use this tool responsibly? [y/n]: ").strip().lower()
            if response in ['y', 'yes']:
                return True
            elif response in ['n', 'no']:
                return False
            else:
                print("Please enter 'y' for yes or 'n' for no.")

def get_hash_algorithm() -> tuple[str, Callable]:
    """Get hash algorithm choice from user."""
    if RICH_AVAILABLE:
        console.print("\n[bold cyan]Available Hash Algorithms:[/bold cyan]")
        
        table = Table()
        table.add_column("Option", style="cyan", no_wrap=True)
        table.add_column("Algorithm", style="magenta")
        table.add_column("Description", style="green")
        
        table.add_row("1", "MD5", "128-bit hash (weak, fast)")
        table.add_row("2", "SHA-1", "160-bit hash (deprecated)")
        table.add_row("3", "SHA-256", "256-bit hash (secure, slower)")
        
        console.print(table)
        
        choice = Prompt.ask(
            "\n[bold yellow]Select hash algorithm[/bold yellow]",
            choices=["1", "2", "3"],
            default="1"
        )
    else:
        print("\nAvailable Hash Algorithms:")
        print("1. MD5 - 128-bit hash (weak, fast)")
        print("2. SHA-1 - 160-bit hash (deprecated)")
        print("3. SHA-256 - 256-bit hash (secure, slower)")
        
        while True:
            choice = input("\nSelect hash algorithm [1/2/3] (default: 1): ").strip()
            if not choice:
                choice = "1"
            if choice in ["1", "2", "3"]:
                break
            print("Invalid choice. Please enter 1, 2, or 3.")
    
    algo_info = HASH_ALGORITHMS[choice]
    if RICH_AVAILABLE:
        console.print(f"[green]✓ Selected: {algo_info['name']}[/green]")
    else:
        print(f"✓ Selected: {algo_info['name']}")
    
    return algo_info['name'], algo_info['func']

def get_target_hash() -> str:
    """Get target hash from user with validation and paste support."""
    if RICH_AVAILABLE:
        console.print("\n[bold cyan]📋 Hash Input Instructions:[/bold cyan]")
        console.print("[yellow]• You can paste your hash directly (Ctrl+V or Cmd+V)[/yellow]")
        console.print("[yellow]• Hash should be in hexadecimal format (0-9, a-f)[/yellow]")
        console.print("[yellow]• Common hash lengths: MD5 (32 chars), SHA-1 (40 chars), SHA-256 (64 chars)[/yellow]")
    else:
        print("\n📋 Hash Input Instructions:")
        print("• You can paste your hash directly")
        print("• Hash should be in hexadecimal format (0-9, a-f)")
        print("• Common hash lengths: MD5 (32 chars), SHA-1 (40 chars), SHA-256 (64 chars)")
    
    while True:
        if RICH_AVAILABLE:
            target_hash = Prompt.ask(
                "\n[bold yellow]Paste or enter the target hash to crack[/bold yellow]"
            ).strip()
        else:
            target_hash = input("\nPaste or enter the target hash to crack: ").strip()
        
        if not target_hash:
            if RICH_AVAILABLE:
                console.print("[red]❌ Hash cannot be empty. Please try again.[/red]")
            else:
                print("❌ Hash cannot be empty. Please try again.")
            continue
        
        # Remove any whitespace or line breaks that might come from pasting
        target_hash = ''.join(target_hash.split())
            
        # Basic validation - ensure it's hexadecimal
        try:
            int(target_hash, 16)
            
            # Provide feedback on hash type based on length
            hash_length = len(target_hash)
            if hash_length == 32:
                hash_type = "MD5"
            elif hash_length == 40:
                hash_type = "SHA-1"
            elif hash_length == 64:
                hash_type = "SHA-256"
            else:
                hash_type = f"Unknown ({hash_length} characters)"
            
            if RICH_AVAILABLE:
                console.print(f"[green]✓ Target hash accepted: {target_hash}[/green]")
                console.print(f"[blue]ℹ️ Detected hash type: {hash_type}[/blue]")
            else:
                print(f"✓ Target hash accepted: {target_hash}")
                print(f"ℹ️ Detected hash type: {hash_type}")
            
            return target_hash.lower()
        except ValueError:
            if RICH_AVAILABLE:
                console.print("[red]❌ Invalid hash format. Hash should only contain hexadecimal characters (0-9, a-f).[/red]")
                console.print("[yellow]💡 Tip: Make sure you copied the complete hash without extra characters.[/yellow]")
            else:
                print("❌ Invalid hash format. Hash should only contain hexadecimal characters (0-9, a-f).")
                print("💡 Tip: Make sure you copied the complete hash without extra characters.")

def get_wordlist_path() -> Path:
    """Get wordlist path from user with validation."""
    # Use a relative path for the default wordlist, assuming it's in the same directory
    default_path = Path(__file__).parent / "rockyou.txt"
    
    if RICH_AVAILABLE:
        use_default = Confirm.ask(
            f"\n[bold yellow]Use default wordlist path '{default_path}'?[/bold yellow]",
            default=True
        )
    else:
        while True:
            response = input(f"\nUse default wordlist path '{default_path}'? [Y/n]: ").strip().lower()
            if response in ['', 'y', 'yes']:
                use_default = True
                break
            elif response in ['n', 'no']:
                use_default = False
                break
            else:
                print("Please enter 'y' for yes or 'n' for no.")
    
    if use_default:
        wordlist_path = default_path
    else:
        if RICH_AVAILABLE:
            custom_path = Prompt.ask("[bold yellow]Enter path to wordlist file[/bold yellow]").strip()
        else:
            custom_path = input("Enter path to wordlist file: ").strip()
        wordlist_path = Path(custom_path)
    
    # Validate file exists and is readable
    if not wordlist_path.exists():
        if RICH_AVAILABLE:
            console.print(f"[red]❌ Error: Wordlist file '{wordlist_path}' not found.[/red]")
            console.print("[yellow]Please ensure the wordlist file exists and try again.[/yellow]")
        else:
            print(f"❌ Error: Wordlist file '{wordlist_path}' not found.")
            print("Please ensure the wordlist file exists and try again.")
        sys.exit(1)
    
    if not wordlist_path.is_file():
        if RICH_AVAILABLE:
            console.print(f"[red]❌ Error: '{wordlist_path}' is not a valid file.[/red]")
        else:
            print(f"❌ Error: '{wordlist_path}' is not a valid file.")
        sys.exit(1)
    
    try:
        # Test if file is readable
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            f.readline()
        if RICH_AVAILABLE:
            console.print(f"[green]✓ Wordlist loaded: {wordlist_path}[/green]")
        else:
            print(f"✓ Wordlist loaded: {wordlist_path}")
        return wordlist_path
    except IOError as e:
        if RICH_AVAILABLE:
            console.print(f"[red]❌ Error reading wordlist file: {e}[/red]")
        else:
            print(f"❌ Error reading wordlist file: {e}")
        sys.exit(1)

def hash_password(password: str, hash_func: Callable) -> str:
    """Hash a password using the specified hash function."""
    return hash_func(password.encode('utf-8')).hexdigest()

def count_wordlist_lines(wordlist_path: Path) -> int:
    """Count the number of lines in the wordlist for progress tracking."""
    try:
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            return sum(1 for _ in f)
    except IOError:
        return 0

def read_wordlist(wordlist_path: Path) -> Generator[str, None, None]:
    """Generator to read wordlist line by line with UTF-8 error handling."""
    try:
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                password = line.strip()
                if password:  # Skip empty lines
                    yield password
    except IOError as e:
        if RICH_AVAILABLE:
            console.print(f"[red]❌ Error reading wordlist: {e}[/red]")
        else:
            print(f"❌ Error reading wordlist: {e}")
        sys.exit(1)

def crack_password(target_hash: str, hash_func: Callable, wordlist_path: Path, verbose: bool = False) -> Optional[str]:
    """Attempt to crack the password using wordlist attack."""
    if RICH_AVAILABLE:
        console.print(f"\n[bold cyan]🚀 Starting password cracking attack...[/bold cyan]")
        console.print(f"[yellow]Target Hash: {target_hash}[/yellow]")
        console.print(f"[yellow]Wordlist: {wordlist_path}[/yellow]")
        
        # Count total lines for progress tracking
        console.print("[cyan]📊 Counting wordlist entries...[/cyan]")
    else:
        print(f"\n🚀 Starting password cracking attack...")
        print(f"Target Hash: {target_hash}")
        print(f"Wordlist: {wordlist_path}")
        print("📊 Counting wordlist entries...")

    total_words = count_wordlist_lines(wordlist_path)
    if total_words == 0:
        if RICH_AVAILABLE:
            console.print("[red]❌ Error: Wordlist is empty or unreadable. Cannot proceed.[/red]")
        else:
            print("❌ Error: Wordlist is empty or unreadable. Cannot proceed.")
        return None

    start_time = time.time()
    cracked_password = None
    attempt_count = 0

    if RICH_AVAILABLE:
        from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn, TimeElapsedColumn
        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
            TimeElapsedColumn(),
            TextColumn("[bold blue]{task.fields[speed]:.2f} words/sec[/bold blue]"),
            TextColumn("[bold green]{task.fields[attempts]} attempts[/bold green]"),
            console=console,
            transient=True
        ) as progress:
            task = progress.add_task("[cyan]Cracking...[/cyan]", total=total_words, speed=0.0, attempts=0)
            
            for password in read_wordlist(wordlist_path):
                attempt_count += 1
                hashed_password = hash_password(password, hash_func)
                
                if hashed_password == target_hash:
                    cracked_password = password
                    progress.update(task, advance=1, description="[green]Cracked![/green]")
                    break
                
                progress.update(task, advance=1, speed=attempt_count / (time.time() - start_time), attempts=attempt_count)
                
                if verbose and attempt_count % 1000 == 0:
                    progress.console.print(f"[dim]  Attempted {attempt_count} words...[/dim]")
    else:
        # Basic progress for non-rich users
        print(f"Total words to check: {total_words}")
        for password in read_wordlist(wordlist_path):
            attempt_count += 1
            hashed_password = hash_password(password, hash_func)
            
            if hashed_password == target_hash:
                cracked_password = password
                break
            
            if verbose and attempt_count % 1000 == 0:
                print(f"  Attempted {attempt_count} words...")
    
    end_time = time.time()
    duration = end_time - start_time
    
    if RICH_AVAILABLE:
        console.print("\n" + "=" * 70)
        if cracked_password:
            console.print(Panel(
                f"[bold green]🎉 Password Cracked! 🎉[/bold green]\n\n" +
                f"[bold white]Hash:[/bold white] [yellow]{target_hash}[/yellow]\n" +
                f"[bold white]Password:[/bold white] [green]{cracked_password}[/green]\n" +
                f"[bold white]Attempts:[/bold white] [cyan]{attempt_count}[/cyan]\n" +
                f"[bold white]Time Taken:[/bold white] [cyan]{duration:.2f} seconds[/cyan]",
                title="[bold green]CRACKING SUCCESS[/bold green]",
                border_style="green"
            ))
        else:
            console.print(Panel(
                f"[bold red]💔 Password Not Found in Wordlist 💔[/bold red]\n\n" +
                f"[bold white]Target Hash:[/bold white] [yellow]{target_hash}[/yellow]\n" +
                f"[bold white]Attempts:[/bold white] [cyan]{attempt_count}[/cyan]\n" +
                f"[bold white]Time Taken:[/bold white] [cyan]{duration:.2f} seconds[/cyan]\n\n" +
                f"[yellow]Consider using a larger wordlist or a different cracking method.[/yellow]",
                title="[bold red]CRACKING FAILED[/bold red]",
                border_style="red"
            ))
        console.print("=" * 70)
    else:
        print("\n" + "=" * 70)
        if cracked_password:
            print("🎉 Password Cracked! 🎉")
            print(f"Hash: {target_hash}")
            print(f"Password: {cracked_password}")
            print(f"Attempts: {attempt_count}")
            print(f"Time Taken: {duration:.2f} seconds")
        else:
            print("💔 Password Not Found in Wordlist 💔")
            print(f"Target Hash: {target_hash}")
            print(f"Attempts: {attempt_count}")
            print(f"Time Taken: {duration:.2f} seconds")
            print("Consider using a larger wordlist or a different cracking method.")
        print("=" * 70)
        
    return cracked_password

def main():
    parser = argparse.ArgumentParser(
        description="Educational Password Cracking Tool",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '--hash-type', 
        type=int, 
        choices=[1, 2, 3], 
        help='Skip hash selection (1=MD5, 2=SHA-1, 3=SHA-256)'
    )
    parser.add_argument(
        '--target', 
        type=str, 
        help='Provide hash directly via command line'
    )
    parser.add_argument(
        '--wordlist', 
        type=str, 
        help='Use custom wordlist file'
    )
    parser.add_argument(
        '--verbose', 
        action='store_true', 
        help='Show detailed progress information'
    )
    
    args = parser.parse_args()

    display_banner()

    if not get_user_confirmation():
        if RICH_AVAILABLE:
            console.print("[bold red]Exiting: User did not agree to responsible use.[/bold red]")
        else:
            print("Exiting: User did not agree to responsible use.")
        sys.exit(0)

    hash_name, hash_func = None, None
    if args.hash_type:
        if str(args.hash_type) in HASH_ALGORITHMS:
            hash_name = HASH_ALGORITHMS[str(args.hash_type)]['name']
            hash_func = HASH_ALGORITHMS[str(args.hash_type)]['func']
            if RICH_AVAILABLE:
                console.print(f"[green]✓ Hash algorithm set from command line: {hash_name}[/green]")
            else:
                print(f"✓ Hash algorithm set from command line: {hash_name}")
        else:
            if RICH_AVAILABLE:
                console.print("[red]❌ Invalid hash-type provided via command line. Please choose 1, 2, or 3.[/red]")
            else:
                print("❌ Invalid hash-type provided via command line. Please choose 1, 2, or 3.")
            sys.exit(1)
    else:
        hash_name, hash_func = get_hash_algorithm()

    target_hash = args.target if args.target else get_target_hash()

    wordlist_path = Path(args.wordlist).resolve() if args.wordlist else get_wordlist_path()
    
    # Validate the wordlist file exists
    if not wordlist_path.exists():
        if RICH_AVAILABLE:
            console.print(f"[red]❌ Error: Wordlist file '{wordlist_path}' not found.[/red]")
        else:
            print(f"❌ Error: Wordlist file '{wordlist_path}' not found.")
        sys.exit(1)

    cracked_password = crack_password(target_hash, hash_func, wordlist_path, args.verbose)

if __name__ == "__main__":
    try:
        while True:
            main()

            retry = input("\n🔁 Try another hash? (y/n): ").lower().strip()
            if retry == 'n':
                if RICH_AVAILABLE:
                    console.print("👋 [bold yellow]Exiting. Stay safe![/bold yellow]")
                else:
                    print("👋 Exiting. Stay safe!")
                break
            elif retry != 'y':
                print("❌ Invalid input. Please type 'y' or 'n'.")
                continue  # Ask again

    except KeyboardInterrupt:
        if RICH_AVAILABLE:
            console.print("\n[bold yellow]Operation interrupted by user. Exiting.[/bold yellow]")
        else:
            print("\nOperation interrupted by user. Exiting.")
        sys.exit(0)
