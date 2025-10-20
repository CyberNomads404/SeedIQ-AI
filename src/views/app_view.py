from src.views.http_types.http_request import HttpRequest
from src.views.http_types.http_response import HttpResponse

class AppView:

    def home(self) -> HttpResponse:
        formatted_response = {
            "status": True,
            "message": "Welcome to the SEEDIQ-AI API!",
            "version": "1.0.0v",
            "documentation": "/docs",
            "contact": {
                "name": "CyberNomads404",
                "github_organization": "https://github.com/CyberNomads404",
                "authors": [
                    { 
                        "name": 'Erikli Arruda' , 
                        "github": 'https://github.com/Erikli999',
                        "picture": 'https://avatars.githubusercontent.com/u/138739176?v=4'
                    },
                    { 
                        "name": 'Pedro Henrique Martins Borges', 
                        "github": 'https://github.com/piedro404',
                        "picture": 'https://avatars.githubusercontent.com/u/88720549?v=4'
                    },
                    { 
                        "name": 'Thayna Bezerra', 
                        "github": 'https://github.com/thayna-bezerra',
                        "picture": 'https://avatars.githubusercontent.com/u/58120519?v=4'
                    },
                ],
            },
        }

        return HttpResponse(status_code=200, body=formatted_response)
