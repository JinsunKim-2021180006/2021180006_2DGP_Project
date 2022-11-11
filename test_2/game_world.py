#game world 

obj = [[],[]]
collision_group = dict()

def add_obj(o,depth):
    obj[depth].append(o)

def add_objs(ol,depth):
    obj[depth] += ol

def remove_obj(o):
    for layer in obj:
        if o in layer:
            layer.remove(o)
            remove_collision_object(o)
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

def add_collision_group(a,b, group):
    if group not in collision_group:
        print('New Group Made')
        collision_group[group] = [[],[]]

    if a:
        if type(a) == list:
            collision_group[group][0] += a
        else:
            collision_group[group][0].append(a)

    if b:
        if type(b) == list:
            collision_group[group][1] += b
        else:
            collision_group[group][1].append(b)



def all_collision_pairs():
    for group, pairs in collision_group.items():
        for a in pairs[0]:
            for b in pairs[1]:
                yield a,b, group


def remove_collision_object(o):
    for pairs in collision_group.values():
        if o in pairs[0]: pairs[0].remove(o)
        elif o in pairs[1]: pairs[1].remove(o)