from core.frontend.parser import parse


code = """
func my_func() {
    return 5
}

response = my_func()
print(response)

for (i=0; i<5; i+=1) {
    print('hello,', i)
}

i = 0

while (i < 5) {
    print('i is', i)
}
"""

print(parse(code))
