# -*- coding:utf8 -*-

import os
import sys
import zlib
import time
import base64
import marshal
import py_compile,requests
try:
    import os,cython
    from Cython.Build.BuildExecutable import build
except:
    os.system('pip install cython > /dev/null')

M = '\x1b[1;97m'
A = '\x1b[1;91m'
H = '\x1b[1;92m'
D = '\x1b[1;93m'
I = '\x1b[1;94m'

H = '\x1b[1;95m' 
S = '\x1b[1;96m'
N = '\x1b[0m'

GREEN ='\x1b[38;5;46m'
RED = '\x1b[1;91m'
WHITE = '\033[1;97m'
YELLOW = '\033[1;33m'
BLUE = '\033[1;34m'
ORANGE = '\033[1;35m'
BLACK="\033[1;30m"
Z= "\033[1;30m"
sir = '\033[41m\x1b[1;97m'
x = '\33[m' # DEFAULT
m = '\x1b[1;91m' #RED +
k = '\033[93m' # KUNING +
xr = '\x1b[1;92m' # HIJAU +
u = '\033[32m' # HIJAU -
V = '\033[95m' # UNGU
O = '\033[33m' # KUNING -
OF = '\x1b[0m'   
BBL = '\x1b[1;106m' 
BP = '\x1b[1;105m' 
BB = '\x1b[1;104m' 
BK = '\x1b[1;103m' 
Madhi = '\x1b[1;102m' 
hasan = '\x1b[1;101m' 
shuvo = '\x1b[1;100m' 
# Select raw_input() or input()
if sys.version_info[0]==2:
    _input = "raw_input('%s')"
elif sys.version_info[0]==3:
    _input = "input('%s')"
else:
    sys.exit("\n Your Python Version is not Supported!")


def logo():
    os.system('clear')
    print (f"""\033[1;92m
\033[1;91m ##     ##    ###    ##     ##  ########  #### 
\033[1;92m ###   ###   ## ##   ##     ##  ##     ##  ##
\033[1;93m #### ####  ##   ##  ##     ##  ##     ##  ##  
\033[1;91m ## ### ## ##     ## #########  ##     ##  ##
\033[1;92m ##     ## ######### ##     ##  ##     ##  ##
\033[1;93m ##     ## ##     ## ##     ##  ##     ##  ##  
\033[1;91m ##     ## ##     ## ##     ##  ########  ####
\033[1;92m•••••••••••••••••••••••••••••••••••••••••••••••••••••••• 
     \033[1;92mM  \033[1;91mA  \033[1;93mH  \033[1;94mD  \033[1;95mI  \033[1;97m-  \033[1;92mT  \033[1;91mO  \033[1;93mO  \033[1;94mL  \033[1;95mS  \033[1;97m-  \033[1;92mF  \033[1;93mI  \033[1;94mR  \033[1;95mE
\033[1;92m••••••••••••••••••••••••••••••••••••••••••••••••••••••••
[\033[1;92m\033[1;31m1\033[1;92m]DEVOLPER   \033[1;91m:         \033[1;92mMAHDI HASAN SHUVO
[\033[1;92m\033[1;31m2\033[1;92m]FACEBOOK   \033[1;91m:         \033[1;92mMAHDI HASAN
[\033[1;92m\033[1;31m3\033[1;92m]WHATSAPP   \033[1;91m:         \033[1;92m01616406924
[\033[1;92m\033[1;31m4\033[1;92m]GITHUB     \033[1;91m:         \033[1;92mMAHDI HASAN SHUVO
[\033[1;92m\033[1;31m0\033[1;92m]TOOLS      \033[1;91m:         \033[1;92mHEARD ENC \033[1;94m[\033[1;95mV10.0\033[1;94m]
\033[1;92m••••••••••••••••••••••••••••••••••••••••••••••••••••••••
              {hasan}HEARD  ENCRIPTION{OF} """)

# Encoding
zlb = lambda in_ : zlib.compress(in_)
b16 = lambda in_ : base64.b16encode(in_)
b32 = lambda in_ : base64.b32encode(in_)
b64 = lambda in_ : base64.b64encode(in_)
mar = lambda in_ : marshal.dumps(compile(in_,'<x>','exec'))
note = "# DEVOLPER  : MAHDI HASAN SHUVO\n# FACEBOOK  : MAHDI HASAN\n# WHATSAPP  : 01616406924\n# GITHUB    : Shuvo-BBHH\n"
def banner(): # Program Banner
   print (f"""\033[1;92m
\033[1;91m ##     ##    ###    ##     ##  ########  #### 
\033[1;92m ###   ###   ## ##   ##     ##  ##     ##  ##
\033[1;93m #### ####  ##   ##  ##     ##  ##     ##  ##  
\033[1;91m ## ### ## ##     ## #########  ##     ##  ##
\033[1;92m ##     ## ######### ##     ##  ##     ##  ##
\033[1;93m ##     ## ##     ## ##     ##  ##     ##  ##  
\033[1;91m ##     ## ##     ## ##     ##  ########  ####
\033[1;92m•••••••••••••••••••••••••••••••••••••••••••••••••••••••• 
     \033[1;92mM  \033[1;91mA  \033[1;93mH  \033[1;94mD  \033[1;95mI  \033[1;97m-  \033[1;92mT  \033[1;91mO  \033[1;93mO  \033[1;94mL  \033[1;95mS  \033[1;97m-  \033[1;92mF  \033[1;93mI  \033[1;94mR  \033[1;95mE
\033[1;92m••••••••••••••••••••••••••••••••••••••••••••••••••••••••
[\033[1;92m\033[1;31m1\033[1;92m]DEVOLPER   \033[1;91m:         \033[1;92mMAHDI HASAN SHUVO
[\033[1;92m\033[1;31m2\033[1;92m]FACEBOOK   \033[1;91m:         \033[1;92mMAHDI HASAN
[\033[1;92m\033[1;31m3\033[1;92m]WHATSAPP   \033[1;91m:         \033[1;92m01616406924
[\033[1;92m\033[1;31m4\033[1;92m]GITHUB     \033[1;91m:         \033[1;92mMAHDI HASAN SHUVO
[\033[1;92m\033[1;31m0\033[1;92m]TOOLS      \033[1;91m:         \033[1;92mHEARD ENC \033[1;94m[\033[1;95mV10.0\033[1;94m]
\033[1;92m••••••••••••••••••••••••••••••••••••••••••••••••••••••••
              {hasan}HEARD  ENCRIPTION{OF} """)
   print(f"""
 {xr}[01] {RED}Encode Marshal,base64,zlip,hex,lamda,cpython{OF} 
 {A}[02] {GREEN}Encode Zlib,base64,zlip,hex,lamda,cpython{OF} 
 {H}[03] {YELLOW}Encode Base16,base64,zlip,hex,lamda,cpython{OF} 
 {D}[04] {WHITE}Encode Base32,base64,zlip,hex,lamda,cpython{OF} 
 {I}[05] {RED}Encode Base64,base64,zlip,hex,lamda,cpython{OF} 
 {H}[06] {GREEN}Encode Zlib,Base16,base64,zlip,lamda,hex,cpython{OF} 
 {A}[07] {YELLOW}Encode Zlib,Base32,base64,zlip,lamda,hex,cpython{OF} 
 {S}[08] {WHITE}Encode Zlib,Base64,base64,zlip,lamda,hex,cpython{OF} 
 {A}[09] {YELLOW}Encode Marshal,Zlib,base64,zlip,lamda,hex,cpython{OF} 
 {N}[10] {RED}Encode Marshal,Base16,base64,zlip,hex,lamda,cpython{OF} 
 {S}[11] {GREEN}Encode Marshal,Base32,base64,zlip,hex,lamda,cpython{OF} 
 {H}[12] {WHITE}Encode Marshal,Base64,base64,zlip,hex,lamda,cpython{OF} 
 {u}[13] {YELLOW}Encode Marshal,Zlib,B16,base64,zlip,hex,lamda,cpython{OF} 
 {V}[14] {GREEN}Encode Marshal,Zlib,B32,base64,zlip,hex,lamda,cpython{OF} 
 {O}[15] {WHITE}Encode Marshal,Zlib,B64,base64,zlip,hex,lamda,cpython{OF}
 {x}[16] {RED}Simple Encode{OF} 
 {GREEN}['C'] Contact Me
 [17] {RED}Exit{OF}""")

class FileSize: # Gets the File Size
    def datas(self,z):
        for x in ['Byte','KB','MB','GB']:
            if z < 1024.0:
                return "%3.1f %s" % (z,x)
            z /= 1024.0
    def __init__(self,path):
        if os.path.isfile(path):
            dts = os.stat(path).st_size
            print(f" {M}[-] Encoded File Size : {OF}%s\n" % self.datas(dts))
# FileSize('rec.py')

# Encode Menu
def Encode(option,data,output):
    loop = int(eval(_input % " \x1b[0m[-] Encode Count las than 10 :\x1b[1;91m "))
    if option == 1:
        xx = "mar(data.encode('utf8'))[::-1]"
        heading = "_ = lambda __ : __import__('marshal').loads(__[::-1]);"
    elif option == 2:
        xx = "zlb(data.encode('utf8'))[::-1]"
        heading = "_ = lambda __ : __import__('zlib').decompress(__[::-1]);"
    elif option == 3:
        xx = "b16(data.encode('utf8'))[::-1]"
        heading = "_ = lambda __ : __import__('base64').b16decode(__[::-1]);"
    elif option == 4:
        xx = "b32(data.encode('utf8'))[::-1]"
        heading = "_ = lambda __ : __import__('base64').b32decode(__[::-1]);"
    elif option == 5:
        xx = "b64(data.encode('utf8'))[::-1]"
        heading = "_ = lambda __ : __import__('base64').b64decode(__[::-1]);"
    elif option == 6:
        xx = "b16(zlb(data.encode('utf8')))[::-1]"
        heading = "_ = lambda __ : __import__('zlib').decompress(__import__('base64').b16decode(__[::-1]));"
    elif option == 7:
        xx = "b32(zlb(data.encode('utf8')))[::-1]"
        heading = "_ = lambda __ : __import__('zlib').decompress(__import__('base64').b32decode(__[::-1]));"
    elif option == 8:
        xx = "b64(zlb(data.encode('utf8')))[::-1]"
        heading = "_ = lambda __ : __import__('zlib').decompress(__import__('base64').b64decode(__[::-1]));"
    elif option == 9:
        xx = "zlb(mar(data.encode('utf8')))[::-1]"
        heading = "_ = lambda __ : __import__('marshal').loads(__import__('zlib').decompress(__[::-1]));"
    elif option == 10:
        xx = "b16(mar(data.encode('utf8')))[::-1]"
        heading = "_ = lambda __ : __import__('marshal').loads(__import__('base64').b16decode(__[::-1]));"
    elif option == 11:
        xx = "b32(mar(data.encode('utf8')))[::-1]"
        heading = "_ = lambda __ : __import__('marshal').loads(__import__('base64').b32decode(__[::-1]));"
    elif option == 12:
        xx = "b64(mar(data.encode('utf8')))[::-1]"
        heading = "_ = lambda __ : __import__('marshal').loads(__import__('base64').b64decode(__[::-1]));"
    elif option == 13:
        xx = "b16(zlb(mar(data.encode('utf8'))))[::-1]"
        heading = "_ = lambda __ : __import__('marshal').loads(__import__('zlib').decompress(__import__('base64').b16decode(__[::-1])));"
    elif option == 14:
        xx = "b32(zlb(mar(data.encode('utf8'))))[::-1]"
        heading = "_ = lambda __ : __import__('marshal').loads(__import__('zlib').decompress(__import__('base64').b32decode(__[::-1])));"
    elif option == 15:
        xx = "b64(zlb(mar(data.encode('utf8'))))[::-1]"
        heading = "_ = lambda __ : __import__('marshal').loads(__import__('zlib').decompress(__import__('base64').b64decode(__[::-1])));"
    elif option in['c','C']:
        logo()
        os.system('clear')
        os.system('xdg-open https://github.com/Shuvo-BBHH')
        banner()
        print('[1] Facebook \n[2] Whatapp')
        mahd = input('Chouse :')
        if mahd =='1':
            os.system("xdg-open https://facebook.com/bk4human")
        elif mahd =='2':
            os.system('xdg-open https://wa.me/+8801616406924')

    else:
        sys.exit("\n Invalid Option!")


    
    for x in range(loop):
        try:
            data = "exec((_)(%s))" % repr(eval(xx))
        except TypeError as s:
            sys.exit(" TypeError : " + str(s))
    with open(output, 'w') as f:
        f.write(note + heading + data)
        f.close()

# Special Encode
def SEncode(data,output):
    for x in range(5):
        method = repr(b64(zlb(mar(data.encode('utf8'))))[::-1])
        data = "exec(__import__('marshal').loads(__import__('zlib').decompress(__import__('base64').b64decode(%s[::-1]))))" % method
    z = []
    for i in data:
        z.append(ord(i))
    sata = "_ = %s\nexec(''.join(chr(__) for __ in _))" % z
    with open(output, 'w') as f:
        f.write(note + "exec(str(chr(35)%s));" % '+chr(1)'*10000)
        f.write(sata)
        f.close()
    py_compile.compile(output,output)

# Main Menu
def MainMenu():
    try:
        os.system('clear') # os.system('cls')
        banner()
       # menu()
        try:
            option = int(eval(_input % f"{OF} [-] \033[1;33mChouse : {GREEN}"))
        except ValueError:
            sys.exit(f"\n {RED}Invalid Option !{OF}")
        
        if option > 0 and option <= 17:
            if option == 17:
                sys.exit(f"\n {GREEN}Thanks For Mahdi Hasan Tool")
            os.system('clear') # os.system('cls')
            banner()
        else:
            sys.exit(f'\n {RED}Invalid Option !')
        try:
            file = eval(_input % f" [*] {GREEN}File Name :{GREEN} ")
            data = open(file).read()
        except IOError:
            sys.exit(f"\n{RED} File Not Found!{OF}")
        
        output = file.lower().replace('.py', '') + '_enc.py'
        if option == 16:
            SEncode(data,output)
        else:
            Encode(option,data,output)
        #print("\n [-] Successfully Encrypted %s" % file)
        #print(" [-] Saved as %s" % output)
        FileSize(output)
    except KeyboardInterrupt:
        time.sleep(1)
        sys.exit()

    # Define a lambda function to encrypt the input string

    encrypt = lambda s: base64.b64encode(zlib.compress(marshal.dumps(s))).hex()
    mahdi_f = output
    # Open the file to encrypt and read its contents
    with open(mahdi_f, 'r') as f:
        contents = f.read()

    # Encrypt the contents of the file
    for mahdi in range(5):
        encrypted = encrypt(contents)

    #with open('enccc_enc.py', 'w') as f:
    #   f.write
    bace = (f"import marshal\nimport zlib\nimport base64 \nexec(marshal.loads(zlib.decompress(base64.b64decode(bytes.fromhex('{encrypted}')))))")
    #f'import marshal\n import zlib\n import base64 \n exec({encrypted})'
    com = compile(bace, "", "exec")
    encrypt = marshal.dumps(com)
    baru = open("Hrd"+str(mahdi_f), "w")
    baru.write("# DEVOLPER  : MAHDI HASAN SHUVO\n# FACEBOOK  : MAHDI HASAN\n# WHATSAPP  : 01616406924\n# GITHUB    : Shuvo-BBHH\n#BEST ENCREPTION YOU CAN TRY TO DEC IT IF YOU DEC IT YOU ARE MY BOOSS\n\nimport marshal\n")
    baru.write("exec(marshal.loads("+repr(encrypt)+"))")
    logo()
    print(f"""{M}
    |{A}-{H}--{D}---{I}---{H}---{A}----{S}---{A}----{S}---{N}---{S}----{A}---{N}|
    {GREEN}|                                    {GREEN}|
    |{YELLOW}enc sucsses save as {GREEN}{baru}{OF}|
    |{M}___{A}__{H}__{D}___{I}___{H}___{A}__{S}__{A}___{N}____{S}___{H}___{A}____{N}|
    """)
    #print(f"{YELLOW}enc sucsses save as {GREEN}{baru}{OF}")
    print(f"{YELLOW}You can see your SC Enc oonly Marshal Bt all enc are useed {GREEN}{OF}")
    dlt = f'rm -rf {output}'
    os.system(dlt)
    print()
    cpy = input(f'{GREEN}DOY you want o to convert cpython : {YELLOW}')
    if cpy in['n','N','02']:
        exit()
    if cpy in['y','Y','1']:
        os.system('clear')
        logo()
        print(f'\033[1;37m 1 ->{GREEN} Compile Cython \n {OF}2 -> {YELLOW}Compile ELF (ex: \033[1;32m./run\033[1;37m)\n{OF} 0 -> {YELLOW}Exit ')
        x = input(f' -> {GREEN}INPUT: {RED}')
        if x =='1':
            os.system('clear')
            file = "Hrd"+str(mahdi_f)#baru
            try:
                open(file,'r').read()
            except:
                exit(' File Location Not Found ')
            os.system('cythonize -i -2 '+file+'> /dev/null')
            print(f"""{M}
            |{A}-{H}--{D}---{I}---{H}---{A}----{S}---{A}----{S}---{N}---{S}----{A}---{N}|
            {GREEN}|                                    {GREEN}|
            |{YELLOW}Your File Compile Done Enjoy {GREEN}{OF}       |
            |{M}___{A}__{H}__{D}___{I}___{H}___{A}__{S}__{A}___{N}____{S}___{H}___{A}____{N}|""")
            input(' Your File Compile Done Enjoy ')
        elif x =='2':
            os.system('clear')
            file=baru
            try:
                open(file,'r').read()
            except:
                exit(' File Location Not Found ')
            build(file)
            print(f"""{M}
            |{A}-{H}--{D}---{I}---{H}---{A}----{S}---{A}----{S}---{N}---{S}----{A}---{N}|
            {GREEN}|                                    {GREEN}|
            |{YELLOW}Your File Compile Done Enjoy {GREEN}{OF}       |
            |{M}___{A}__{H}__{D}___{I}___{H}___{A}__{S}__{A}___{N}____{S}___{H}___{A}____{N}|""")
            input(' Your File Compile Done Enjoy ')
        else:
            exit(' Successful exit ')


def en():
    os.system("clear")
    logo()





def mahdienc():
    #e = base64.b64decode('aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL1NodXZvLUJCSEgvY250L21haW4vbWV4c2Vydi50eHQ='.encode("utf-8"))
    ckcrv = 'https://raw.githubusercontent.com/Shuvo-BBHH/cnt/main/enc.txt'
    print(f'{WHITE}Chaking to server')
    r = requests.get(ckcrv).text
    if 'UP' in r:
        logo()
        os.system('pip uninstall mahdienc')
        print(f"{WHITE}PLZ Update Command ")
        print(f"{GREEN}PLZ Update Command ")
        print(f"{YELLOW}PLZ Update Command ")
        print("\33[1;32mDo you update command ?  ")
        os.system("xdg-open https://facebook.com/groups/610487559129086")
        os.system("xdg-open https://facebook.com/ma4D1")
        os.system('pip uninstall mahdienc')
        input()
        os.system('pip uninstall mahdienc')
        mahdienc()

    if 'OF' in r:
        logo()
        os.system('pip uninstall mahdienc')
        print(f"{WHITE}TOOLS OFF")
        print(f"{GREEN}TOOLS OFF")
        print(f"{YELLOW}TOOLS OFF")
        print(f"{WHITE}WATE FOR UPDATE ")
        print(f"{WHITE}WATE FOR UPDATE ")
        print(f"{WHITE}WATE FOR UPDATE ")
        os.system('pip uninstall mahdienc')
        os.system('pip uninstall mahdienc')
        os.system("xdg-open https://facebook.com/ma4D1")
        os.system("xdg-open https://facebook.com/groups/610487559129086")
        input()
        mahdienc()


    if 'ON' in r:
        MainMenu()
    else:
        exit()

if __name__ == "__main__":
    mahdienc()


