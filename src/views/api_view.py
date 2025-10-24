from src.views.http_types.http_response import HttpResponse
from flask import current_app

class ApiView:

    def home(self) -> HttpResponse:
        formatted_response = {
            "status": True,
            "message": "Welcome to the SEEDIQ-AI API!",
            "data": {
                "version": "1.0.0v",
                "contact": {
                    "name": "CyberNomads404",
                    "github_organization": "https://github.com/CyberNomads404",
                    "authors": [
                            { 
                                "name": 'Erikli Arruda' , 
                                "github": 'https://github.com/Erikli999',
                                "picture": 'https://avatars.githubusercontent.com/u/138739176?v=4',
                            },
                            { 
                                "name": 'Pedro Henrique Martins Borges', 
                                "github": 'https://github.com/piedro404',
                                "picture": 'https://avatars.githubusercontent.com/u/88720549?v=4',
                            },
                            { 
                                "name": 'Thayna Bezerra', 
                                "github": 'https://github.com/thayna-bezerra',
                                "picture": 'https://avatars.githubusercontent.com/u/58120519?v=4',
                            },
                        ],
                    },
                },
            }

        return HttpResponse(status_code=200, body=formatted_response)
    
    def list_routes(self) -> HttpResponse:
        data = []
        for rule in current_app.url_map.iter_rules():
            data.append({
                "rule": str(rule),
                "methods": sorted(m for m in rule.methods if m not in ("HEAD", "OPTIONS")),
                "endpoint": rule.endpoint
            })
            
        return HttpResponse(status_code=200, body={
            "status": True,
            "message": "List of all available routes",
            "data": {
                "routes": data
            }
        })
