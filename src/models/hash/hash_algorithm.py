from enum import Enum

class HashAlgorithm(str, Enum):
    md5 = "md5"
    sha1 = "sha1"
    sha256 = "sha256"