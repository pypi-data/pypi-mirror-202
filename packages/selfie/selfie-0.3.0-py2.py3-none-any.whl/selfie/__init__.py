import os
import re

DEFAULT_MASK = [
    r'.*PASS.*'
]

def getenv(mask=None, default_mask=True, mask_file='~/.config/selfie/ignore'):
    if not mask:
        mask = list()
    if default_mask:
        mask.extend(DEFAULT_MASK)
    if mask_file:
        mask_file = os.path.expanduser(mask_file)
        if os.path.exists(mask_file):
            with open(mask_file) as fo:
                mask.extend(fo.read().splitlines())
    environ = dict()
    for k,v in os.environ.items():
        for pattern in mask:
            if re.match(pattern, k):
                v = '********'
        environ[k] = v
    return environ

