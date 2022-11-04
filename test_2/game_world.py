#game world 

obj = [[],[],[]]

def add_obj(o,depth):
    obj[depth].append(o)

def add_objs(ol,depth):
    obj[depth] += ol

def remove_obj(o):
    for layer in obj:
        if o in layer:
            layer.remove(o)
            del o
            return
    raise ValueError('Trying destroy non existing object')

def all_objs():
    for layer in obj:
        for o in layer: 
            yield o

def clear():
    for o in all_objs():
        del o
    for layer in obj:
        layer.clear()