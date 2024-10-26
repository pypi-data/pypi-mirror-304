import onetouch as ot

list1 = [1, 2, 3]
list2 = [9, 8, 7]

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

ot.tools.prints(f'{987}测试文本', list1, list2, display=True,style='color:green;backgroundcolor:blue;', morphology=morphology, recover=True)
