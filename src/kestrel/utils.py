import pathlib
import os
import uuid


def remove_empty_dicts(ds):
    # remove dict with all values as None in list({string:string})
    # this is the results from SQL query
    return [d for d in ds if set(d.values()) != {None}]


def dedup_dicts(ds):
    # deduplicate list({string:string})
    # this is the results from SQL query
    return [dict(s) for s in set(frozenset(d.items()) for d in ds)]


def dedup_ordered_dicts(ds):
    # deduplicate list({string:string})
    # maintain the order if seen
    res = []
    seen = set()
    for d in ds:
        s = str(d)
        if s not in seen:
            res.append(d)
        seen.add(s)
    return res


def subgroup_list(xs, gsize):
    return [xs[i : i + gsize] for i in range(0, len(xs), gsize)]


def mkdtemp():
    # create a temporary directory and return it (named after a random uuid)
    ps = None
    while not ps or pathlib.Path(ps).exists():
        ps = str(uuid.uuid4())
    p = pathlib.Path(ps)
    p.mkdir(parents=True, exist_ok=True)
    return p


class set_current_working_directory:
    def __init__(self, new_cwd):
        self.tmp_cwd = new_cwd

    def __enter__(self):
        self.cwd = os.getcwd()
        os.chdir(self.tmp_cwd)

    def __exit__(self, exception_type, exception_value, traceback):
        os.chdir(self.cwd)
