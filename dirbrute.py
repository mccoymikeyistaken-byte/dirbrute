import requests
import os
import sys
import time
import re
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from rich.console import Console

console = Console()

def prompt(label, default=None, cast=str, validator=None):
    hint = f" [{default}]" if default is not None else ""
    try:
        raw = input(f"  \033[92m[?]\033[0m {label}{hint} : ").strip()
    except KeyboardInterrupt:
        console.print("\n\n  [red]Aborted.[/red]\n")
        sys.exit(0)

    if not raw and default is not None:
        return default
    if not raw:
        console.print(f"  [red][!] This field is required.[/red]")
        return prompt(label, default, cast, validator)
    try:
        value = cast(raw)
    except ValueError:
        console.print(f"  [red][!] Expected a valid {cast.__name__}.[/red]")
        return prompt(label, default, cast, validator)
    if validator:
        error = validator(value)
        if error:
            console.print(f"  [red][!] {error}[/red]")
            return prompt(label, default, cast, validator)
    return value


def validate_url(val):
    if not re.match(r'^https?://', val):
        return "URL must start with http:// or https://"
    if len(val.split('/')[2]) < 3:
        return "URL doesn't look valid — check the domain."
    return None

def validate_threads(val):
    if val < 1 or val > 100:
        return "Threads must be between 1 and 100."
    return None

def validate_wordlist(val):
    if not os.path.isfile(val):
        return f"File not found: {val}"
    return None

def validate_extensions(val):
    if not re.match(r'^[\w]+(,[\w]+)*$', val):
        return "Extensions should be comma-separated without dots (e.g. php,html,txt)"
    return None

def get_config_interactive():
    DEFAULT_WORDLIST   = "wordLists.txt"
    DEFAULT_OUTPUT     = "results.txt"
    DEFAULT_THREADS    = 10
    DEFAULT_EXTENSIONS = "php,html,txt,aspx,jsp,log,js,css,xml,json,zip,tar,gz,bak,old,backup,inc,conf,config"
    
    url        = prompt("Target URL", validator=validate_url)
    threads    = prompt("Threads", DEFAULT_THREADS, int, validate_threads)
    wordlist   = prompt("Wordlist", DEFAULT_WORDLIST, validator=validate_wordlist)
    output     = prompt("Output file", DEFAULT_OUTPUT)
    extensions = prompt("Extensions", DEFAULT_EXTENSIONS, validator=validate_extensions)
    verbose_r  = prompt("Verbose [y/N]", "n").lower()
    verbose    = verbose_r == "y"

    console.print()

    class Config:
        pass

    cfg = Config()
    cfg.url        = url
    cfg.threads    = threads
    cfg.wordlist   = wordlist
    cfg.output     = output
    cfg.extensions = extensions
    cfg.verbose    = verbose
    return cfg 

def print_banner():
    banner = r"""
  ██████╗ ██╗██████╗ ██████╗ ██╗   ██╗███████╗████████╗███████╗██████╗ 
  ██╔══██╗██║██╔══██╗██╔══██╗██║   ██║██╔════╝╚══██╔══╝██╔════╝██╔══██╗
  ██║  ██║██║██████╔╝██████╔╝██║   ██║███████╗   ██║   █████╗  ██████╔╝
  ██║  ██║██║██╔══██╗██╔══██╗██║   ██║╚════██║   ██║   ██╔══╝  ██╔══██╗
  ██████╔╝██║██║  ██║██████╔╝╚██████╔╝███████║   ██║   ███████╗██║  ██║
  ╚═════╝ ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝"""
    console.print(banner, style="bold red")
    console.print("  " + "─" * 69, style="dim")
    console.print(
        "  [cyan]Web Directory Brute-Force Scanner[/cyan]  "
        "[dim]│[/dim]  [magenta]v1.0.2[/magenta]  [dim]│  by[/dim] [white]mike[/white]"
    )
    console.print("  " + "─" * 69 + "\n", style="dim")
    console.print("  [bold white]USAGE[/bold white]")
    console.print("    python app.py\n")
    console.print("  [bold white]OPTIONS[/bold white]")
    console.print("    [yellow]Target URL[/yellow]     Full URL including scheme  [dim](e.g. https://example.com)[/dim]")
    console.print("    [yellow]Threads[/yellow]        Concurrent threads         [dim](default: 10)[/dim]")
    console.print("    [yellow]Wordlist[/yellow]       Path to wordlist file      [dim](default: wordLists.txt)[/dim]")
    console.print("    [yellow]Output[/yellow]         Path to save results       [dim](default: results.txt)[/dim]")
    console.print("    [yellow]Extensions[/yellow]     Comma-separated file exts  [dim](default: php,html,txt...)[/dim]")
    console.print("    [yellow]Verbose[/yellow]        Show all attempts          [dim](y/N)[/dim]")
    console.print()
    console.print("  " + "─" * 69 + "\n", style="dim")

def print_options(args):
    console.print(f"  [yellow][TARGET][/yellow]  [white]{args.url}[/white]")
    console.print(
        f"  [yellow][THREADS][/yellow] [white]{args.threads}[/white]"
        f"   [yellow][WORDLIST][/yellow] [white]{args.wordlist}[/white]"
        f"   [yellow][OUTPUT][/yellow] [white]{args.output}[/white]"
    )
    ext_preview = args.extensions[:40] + " ..." if len(args.extensions) > 40 else args.extensions
    console.print(f"  [yellow][EXTS][/yellow]    [white]{ext_preview}[/white]")
    console.print(f"  [yellow][VERBOSE][/yellow] [white]{'On' if args.verbose else 'Off'}[/white]\n")

print_banner()
args = get_config_interactive()
print_options(args)


HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"
}

session = requests.Session()
session.headers.update(HEADERS)

class BaseLineDetails:
  def __init__(self,status,length,location,wc,lc):
    self.status = status
    self.length = length
    self.location = location
    self.wc = wc
    self.lc = lc

class PathDetails:
  def __init__(self,path,status,length,location,wc,lc):
    self.path = path
    self.status = status
    self.length = length  
    self.location = location
    self.wc = wc
    self.lc = lc

def print_baseDetails(b):
    console.print("  [green][*][/green] Baseline fingerprint:", style="bold")
    console.print(f"      Status : [cyan]{b.status}[/cyan]  │  Length : [cyan]{b.length}[/cyan]  │  Words : [cyan]{b.wc}[/cyan]  │  Lines : [cyan]{b.lc}[/cyan]\n")


console.print("  " + "─" * 69 + "\n", style="dim")
def get_baseline_details(url):
  try:
    baseline_req = session.get(
       f"{url}/randomjunk",
       timeout=3,
       allow_redirects=False
       )
    baseline_status_code = baseline_req.status_code
    baseline_textlength = len(baseline_req.text)
    baseline_location = baseline_req.headers.get("Location")
    baseline_wc = len(baseline_req.text.split())
    baseline_lc = len(baseline_req.text.splitlines())
  except Exception as e:
    print(f"Couldn't fetch due to {e}")
    return None
  
  baselinedetails = BaseLineDetails(baseline_status_code,baseline_textlength,baseline_location,baseline_wc,baseline_lc)
  print_baseDetails(baselinedetails)
  return baselinedetails

def start_bruteforce(url,base,path):
      if args.verbose:
        console.print(f"  [dim][DEBUG] Trying: {path}[/dim]")
      try:
        response = session.get(
           f"{url.rstrip('/')}/{path.lstrip('/')}",
           timeout=3,
           allow_redirects=False
           )
        currStatusCode = response.status_code
        currtextlength = len(response.text)
        currLocation = response.headers.get("Location")
        currWC = len(response.text.split())
        currLC = len(response.text.splitlines())
        if response.status_code in [301, 302, 303, 307, 308]:
          if args.verbose:
           console.print(f"  [yellow][REDIR][/yellow]  {path} [dim]→ {currLocation}[/dim]")
      except Exception as e:
        if args.verbose:
         console.print(f"  [red][ERROR][/red] {path} → {e}")
        return 
      
      length_diff = abs(currtextlength - base.length)
      wc_diff = abs(currWC - base.wc)
      lc_diff = abs(currLC - base.lc)

      if (
        currStatusCode != base.status
        or length_diff > 40
        or currLocation != base.location
        or wc_diff > 10
        or lc_diff > 5
        ):
       status_color = "green" if currStatusCode == 200 else "yellow" if currStatusCode in [301,302,303,307,308] else "red"
       console.print(
        f"  [{status_color}][FOUND][/{status_color}]  "
        f"[white]{path}[/white]  "
        f"[dim][{currStatusCode} │ {currtextlength}B │ {currWC}w │ {currLC}L → {currLocation or '—'}][/dim]"
       )
       potentialPath = PathDetails(path,currStatusCode,currtextlength,currLocation,currWC,currLC)
       save_output(potentialPath)
  
def print_FinalResults():
    console.print("\n  [green][*][/green] Scan complete!", style="bold")
    with open(args.output, "r") as f:
     lines = f.read().strip().splitlines()
    results = lines[1:]  # skip the header
    if results:
      console.print("\n  [yellow]Paths found:[/yellow]")
      for line in results:
        console.print(f"  [green]→[/green] {line}")
    else:
        console.print("  [dim]No paths found.[/dim]")
    console.print(f"\n  [dim]Results saved to[/dim] [white]{args.output}[/white]")
    console.print(f"  [dim]Time elapsed:[/dim] [yellow]{time.time() - start_time:.2f}s[/yellow]\n")

lock = Lock()
def save_output(path):
    with lock:
        with open(args.output, "a") as f:
            f.write(f"Possible path found: {path.path} => {path.status} | {path.length} | {path.location} | {path.wc} words | {path.lc} lines\n")

def has_extension(path):
    name = path.split('/')[-1]      # get last segment e.g. "backup.bak"
    return '.' in name       

seen = set()
start_time = time.time()

with open(args.output, "w") as f:
    f.write(f"Scan recorded at {time.ctime(start_time)}\n")

base = get_baseline_details(args.url)
if base is None:
    console.print("  [red][FATAL][/red] Failed to get baseline. Exiting.")
    exit(1)

if args.extensions:
    extensions = [""] + [f".{ext.strip().lstrip('.')}" for ext in args.extensions.split(",")]
else:
    extensions = [""]

with ThreadPoolExecutor(max_workers=args.threads) as executors:
    with open(args.wordlist,"r") as f:
      for currPath in f:
        currPath = currPath.strip()
        if not currPath:
            continue
        for ext in extensions:
          if ext == "":
           full_path = currPath        
          elif has_extension(currPath):
           continue                    
          else:
           full_path = currPath + ext  
    
          if full_path in seen:
           continue
          seen.add(full_path)
          executors.submit(start_bruteforce, args.url, base, full_path)

console.print("\n  " + "─" * 69, style="dim")  
print_FinalResults()