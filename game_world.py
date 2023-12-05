objects = [[] for _ in range(4)]  # 시각적인 관점에서의 월드

# 충돌관점의 월드
collision_pairs = {}

def add_object(o, depth=0):
    objects[depth].append(o)


def add_objects(ol, depth=0):
    objects[depth] += ol


def update():
    for layer in objects:
        for o in layer:
            o.update()


def render():
    for layer in objects:
        for o in layer:
            o.draw()


def remove_collision_object(o):
    for pairs in collision_pairs.values():
        if o in pairs[0]:
            pairs[0].remove(o)
        if o in pairs[1]:
            pairs[1].remove(o)
    pass


def remove_object(o):
    for layer in objects:
        if o in layer:
            layer.remove(o)  # 시각적 월드에서 지운다
            remove_collision_object(o)  # 충돌 그룹에서 삭제 완료
            del o  # 객체 자체를 완전히 메모리에서 제거
            return
    raise ValueError('Cannot delete non existing object')


def clear():
    # for layer in objects:
    #     layer.clear()
    global objects, collision_pairs

    objects = [[] for _ in range(4)]
    collision_pairs = {}


def collide(a, b):
    la, ba, ra, ta = a.get_bb()
    lb, bb, rb, tb = b.get_bb()

    if la > rb: return False
    if ra < lb: return False
    if ta < bb: return False
    if ba > tb: return False

    return True


def add_collision_pair(group, a, b):
    if group not in collision_pairs:
        print(f'new group {group} added')
        collision_pairs[group] = [[], []]
    if a:
        collision_pairs[group][0].append(a)
    if b:
        collision_pairs[group][1].append(b)


def handle_collision():

    for group, pairs in collision_pairs.items():
        for a in pairs[0]:
            for b in pairs[1]:
                if collide(a, b):
                    a.handle_collision(group, b)
                    b.handle_collision(group, a)
