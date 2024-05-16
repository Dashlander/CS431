from pwn import *

KEY_LEN = 50000
MAX_CHUNK = 10000
rem = remote('mercury.picoctf.net',64260)
rem.recvuntil('This is the encrypted flag!\n')
flag = rem.recvlineS(keepends = False)
print(flag)
bin_flag = unhex(flag)

cntr = KEY_LEN - len(bin_flag)

with log.progress('Decrypting') as p:
	while cntr > 0:
		p.status(f'{cntr} bytes left')
		cnksz = min(MAX_CHUNK,cntr)
		rem.sendlineafter("What data would you like to encrypt? ",'k'*cnksz)
		cntr -= cnksz
rem.sendlineafter("What data would you like to encrypt? ",bin_flag)
rem.recvlineS()
print(format(unhex(rem.recvlineS())))