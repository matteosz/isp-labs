# R.string.last_part = 0x7f0b0028
#char at y * x^y (24) == char at 17
x = 2
y = 3
z = 5
#BAM(sub(18, 24)) == ERNYYL

flag = 'MOBISEC{this_is_a_ERNYYL_ba???????}'

assert len(flag) == 35

mex = list(flag)

offset = 8
upper = True
for i in range(26):
    if upper is True:
        mex[offset + i] = mex[offset + i].upper()
    else:
        mex[offset + i] = mex[offset + i].lower()
    upper = not upper
    
print(''.join(mex))