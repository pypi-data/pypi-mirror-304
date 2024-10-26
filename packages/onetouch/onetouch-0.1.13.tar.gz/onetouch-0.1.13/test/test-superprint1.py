import onetouch.tools as ot

a = [1, 2, 3, 4, 5, 6, 7, 8, 9]
b = [1, 2, 3, 4, 5, 6, 7, 8, 9]
aa = [1, 2, 3, 4, 5, 6, 7, 8, 9]

ot.printc(f'{123}绿色文本', a, aa, display=True, color='bright_magenta')

# ANSI escape codes for text formatting
reset = '\033[0m'
bold = '\033[1m'
blink = '\033[5m'
italic = '\033[3m'

# Single print statement with multiple styles
print(f"{bold}{blink}{italic}\033[91m\033[94m\033[106mThis is bold, blinking, and italic text{reset}.")


morphology = {
    'color': 'red',
    'backgroundcolor': 'yellow',
    'bold': True,
    'faint': True,
    'italic': True,
    'underline': True,
    'reverse': True,
    'crossed-out': True
}


ot.prints(f'{987}测试文本', a, b, display=True,
          style='color:green;backgroundcolor:blue;', morphology=morphology)
