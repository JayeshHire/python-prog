# Online Python compiler (interpreter) to run Python online.
# Write Python 3 code in this online editor and run it.
import re

s = "User-Agent: Mozilla/5.0 , Google, Safari (Macintosh; Intel Mac OS X 10.9; rv:50.0) ; Gecko=20100101 ; Firefox=50.0 (hii)"

header_field = s.split(":")[0]
s = s.split(":")[1]

pattern = r"\(([^\(\)]*)\)"

patt_str = re.findall(pattern, s)
exp_split = re.split(pattern, s)

print(patt_str)
print(exp_split)

for patt in patt_str:
    m = re.search(f"\({patt}\)", s)
    print(f"{patt}: {m.span()}")

for s in patt_str:
    exp_split.remove(s)

print(exp_split)

new_exp = "".join(exp_split)
print(new_exp)

val = new_exp.split(";")[0]
attrs = new_exp.split(";")[1::]
attrs_grouped = {attr.split("=")[0]: attr.split("=")[1] for attr in attrs }

print(val)
vals = val.split(",")
print(vals)
print(attrs_grouped)