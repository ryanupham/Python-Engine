import itertools
from typing import List, Iterable

import engine.entity


def point_in_rect(point, rect):
    return rect[0] <= point[0] <= rect[2] and rect[1] <= point[1] <= rect[3]


def rectangles_intersect(rect1, rect2):
    return point_in_rect((rect1[0], rect1[1]), rect2) or point_in_rect((rect1[0], rect1[3]), rect2) or \
        point_in_rect((rect1[2], rect1[1]), rect2) or point_in_rect((rect1[2], rect1[3]), rect2)


def find_collisions(entities: Iterable[engine.entity.Entity]) -> List[List[engine.entity.Entity]]:
    collisions = []

    for e1, e2 in itertools.combinations(entities, 2):
        if e1.sprite is not None and e2.sprite is not None:
            e1p = e1.position
            e2p = e2.position

            if rectangles_intersect((e1p.x, e1p.y, e1p.x + e1.sprite.width - 1, e1p.y + e1.sprite.height - 1),
                                    (e2p.x, e2p.y, e2p.x + e2.sprite.width - 1, e2p.y + e2.sprite.height - 1)):
                collisions.append([e1, e2])

    return collisions
