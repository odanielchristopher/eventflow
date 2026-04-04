import hashlib

from src.models.hash.create_hash import CreateHashDto
from src.models.hash.hash_info import HashInfoDto

class CreateHashUseCase:

    @staticmethod
    def execute(dto: CreateHashDto):
        algorithm = dto.algorithm

        input_bytes = dto.text.encode('utf-8')

        if algorithm == "md5":
            h = hashlib.md5(input_bytes).hexdigest()
        elif algorithm == "sha1":
            h = hashlib.sha1(input_bytes).hexdigest()
        elif algorithm == "sha256":
            h = hashlib.sha256(input_bytes).hexdigest()
        else:
            raise ValueError("Unsupported algorithm") 
    
        return HashInfoDto(hash=h) 