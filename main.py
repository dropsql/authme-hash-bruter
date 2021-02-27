import pyperclip
import hashlib
import sys, re

from rich.console import Console    
from rich.progress import Progress 

console = Console(
)

banner = '''
[white]
      ,-~~-.___.
     / [red]()=(()[/red]   \\
    (   (        0
     \._\, ,----'
[yellow]##XXXxxxxxxx[/yellow]        Simple Authme hash bruter
       /  ---'~;    Made by ❤ by drops (on valentins day lol)
      /    /~|-     https://github.com/dropsql
    =(   ~~  |
[/white]
'''

console.print(banner)

if len(sys.argv) != 3:
    console.log(f'usage: py {sys.argv[0]} <authme hash> <wordlist>')
    sys.exit(-1)

authme_hash = sys.argv[1]
wordlist = sys.argv[2]

match = __import__('re').match(
    r'\$SHA\$(?P<salt>[a-f0-9]{16})\$(?P<hash>[a-f0-9]{64})',
    authme_hash
)

if not match:
    console.log(f'seems like {authme_hash} isn\'t an Authme hash.')
    sys.exit(-1)

console.log('loading passwords from %s' % wordlist)
try:
    passwords = [x.strip() for x in open(file=wordlist, encoding='utf-8', mode='r', errors='ignore').readlines()]
except:
    console.log('can\'t open the wordlist.')
    sys.exit(-1)

console.log(f'{len(passwords)} passwords loaded.')

if not len(passwords):
    sys.exit(-1)

hash = match.group('hash')
salt = match.group('salt')

tries = 0
with Progress(transient=True) as progress:
    task = progress.add_task(total=len(passwords), description='bruteforcing hash', start=True)    

    for password in passwords:
        tries += 1

        generated_hash = hashlib.sha256(hashlib.sha256(password.encode('utf-8')).hexdigest().encode('utf-8') + salt.encode('utf-8')).hexdigest()

        if generated_hash == hash:
            progress.log(f'![blink cyan]password found[/blink cyan]! → [green]{password}[/green] [magenta](copied into clipboard)[/magenta]')
            pyperclip.copy(text=password)
            progress.update(task, advance=(len(passwords) - tries))
            progress.stop()
            sys.exit(-1)

        progress.update(task, advance=1)
    progress.log('password not found.')
    progress.stop()