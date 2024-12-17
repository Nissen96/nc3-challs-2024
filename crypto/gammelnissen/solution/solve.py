from Crypto.Util.number import long_to_bytes
from gmpy2 import iroot

# From handout
n = 113911967470309902498408355902002849141315080752710385265970164128666973595176344769929712328073912045889359818114591877923052777733321490306146637488744172731692293178898440960409438792433505782977089979664244577305445285018320700759389078834385329224670109256967919368893276088261120001891752743010832994161
ct = 181418563625235140825700189846742192203761169128129988853260864253616933650143288011695280847386639743255770112135714678317911664798191379176143996036639508592464099027261445464652005100125349285229059123836955894715533222277904738129836808228104462852378456333009976696034882026353617159677318042624866664
e = 0x10001

p = iroot(n, 2)[0]
phi = p * (p - 1)
d = pow(e, -1, phi)

m = pow(ct, d, n)
flag = long_to_bytes(m).decode()

print(flag)