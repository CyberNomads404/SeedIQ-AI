from typing import Dict
from flask import jsonify

class HttpResponse:
    '''
        Responsability for interacting with Response
    '''
        
    def __init__(
            self, 
            status_code: int,
            body: Dict
        ) -> None:
        self.status_code = status_code
        self.body = body

    # def to_dict(self):
    #     return jsonify(self.body), self.status_code