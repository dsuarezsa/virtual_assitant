import openai
import json


class LLM():
    def __init__(self):
        pass
    
    def process_functions(self, text):
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=[
                    {"role": "system", "content": "Eres un asistente muy servicial"},
                    {"role": "user", "content": text},
            ], functions=[
                {
                    "name": "get_weather",
                    "description": "Obtener el clima actual",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "ubicacion": {
                                "type": "string",
                                "description": "La ubicación, debe ser una ciudad",
                            }
                        },
                        "required": ["ubicacion"],
                    },
                },
                {
                    "name": "send_email",
                    "description": "Enviar un correo",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "recipient": {
                                "type": "string",
                                "description": "La dirección de correo que recibirá el correo electrónico",
                            },
                            "subject": {
                                "type": "string",
                                "description": "El asunto del correo",
                            },
                            "body": {
                                "type": "string",
                                "description": "El texto del cuerpo del correo",
                            }
                        },
                        "required": ["recipient", "subject", "body"],
                    },
                },
                {
                    "name": "open_chrome",
                    "description": "Abrir el explorador Chrome en un sitio específico",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "website": {
                                "type": "string",
                                "description": "El sitio al cual se desea ir"
                            }
                        }
                    }
                },
            ],
            function_call="auto",
        )
        
        message = response["choices"][0]["message"]
        
        if message.get("function_call"):

            function_name = message["function_call"]["name"]
            args = message.to_dict()['function_call']['arguments']
            print("Funcion a llamar: " + function_name)
            args = json.loads(args)
            return function_name, args, message
        
        return None, None, message

    def process_response(self, text, message, function_name, function_response):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=[
                {"role": "system", "content": "Eres un asistente servicial"},
                {"role": "user", "content": text},
                message,
                {
                    "role": "function",
                    "name": function_name,
                    "content": function_response,
                },
            ],
        )
        return response["choices"][0]["message"]["content"]