C = 62324783949134119159408816513334912534343517300880137691662780895409992760262021
N = 1280678415822214057864524798453297819181910621573945477544758171055968245116423923
E = 65537

#from factordb.com; N = P * Q
P = 1899107986527483535344517113948531328331
Q = 674357869540600933870145899564746495319033

#find values of phi and d, as well as deciphered text
phi = (P-1) * (Q-1)
PrK = pow(E,-1,phi) # private key
M = pow(C,PrK,N)

print(phi)
print(PrK)
print(M)

#Ptxt is in numerals, assuming this to be coded in ascii, for each numeral representation:
from Crypto.Util.number import long_to_bytes
plaintext = long_to_bytes(M)
print(plaintext)