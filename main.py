import sys
from pathlib import Path

import ruamel.yaml

INDENT = 4


def update(d, n):
    if isinstance(n, ruamel.yaml.comments.CommentedMap):
        for k in n:
            d[k] = update(d[k], n[k]) if k in d else n[k]
            if k in n.ca._items and \
                    ((n.ca._items[k][2] and n.ca._items[k][2].value.strip()) or \
                     n.ca._items[k][1]):
                d.ca._items[k] = n.ca._items[k]  # copy non-empty comment
    else:
        d = n
    return d


def move_comment(d, depth=0):
    # recursively adjust comment
    if isinstance(d, ruamel.yaml.comments.CommentedMap):
        for k in d:
            if isinstance(d[k], ruamel.yaml.comments.CommentedMap):
                if hasattr(d, 'ca'):
                    comment = d.ca.items.get(k)
                    if comment and comment[3] is not None:
                        # add to first key of the mapping that is the value
                        for k1 in d[k]:
                            d[k].yaml_set_comment_before_after_key(
                                k1,
                                before=comment[3][0].value.lstrip('#').strip(),
                                indent=INDENT * (depth + 1))
                            break
            move_comment(d[k], depth + 1)
    return d


data1 = ruamel.yaml.round_trip_load(Path('tests/input/files-4-1.yaml').read_text())
update(data1, move_comment(ruamel.yaml.round_trip_load(Path('tests/input/files-4-2.yaml').read_text())))
ruamel.yaml.round_trip_dump(data1, sys.stdout, indent=INDENT)

