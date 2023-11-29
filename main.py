from fastapi import FastAPI, File, Request, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
import openai
from dotenv import load_dotenv
import json
from app.utilities.transcriber import Transcriber
from app.utilities.llm import LLM
from app.utilities.weather import Weather
from app.utilities.tts import TTS
from app.utilities.pc_command import PcCommand

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
elevenlabs_key = os.getenv('ELEVENLABS_API_KEY')

app = FastAPI(title='Virtual Assitant')
templates = Jinja2Templates(directory="app/view")

app.mount("/app", StaticFiles(directory="app"), name="app")

@app.get('/')
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post('/audio')
def audio(request: Request, audio: UploadFile = File()):

    text = Transcriber().transcribe(audio)
    

    llm = LLM()
    function_name, args, message = llm.process_functions(text)
    if function_name is not None:

        if function_name == "get_weather":

            function_response = Weather().get(args["ubicacion"])
            function_response = json.dumps(function_response)
            print(f"Respuesta de la funcion: {function_response}")
            
            final_response = llm.process_response(text, message, function_name, function_response)
            tts_file = TTS().process(final_response)
            return {"result": "ok", "text": final_response, "file": tts_file}
        
        elif function_name == "send_email":

            print(args)
            PcCommand.open_mail(args["recipient"], args["subject"], args["body"])
            final_response = "Listo ya puedes enviar el correo"
            tts_file = TTS().process(final_response)
            return {"result": "ok", "text": final_response, "file": tts_file}
        
        elif function_name == "open_chrome":
            PcCommand().open_chrome(args["website"])
            final_response = "Listo, ya abrí chrome en el sitio " + args["website"]
            tts_file = TTS().process(final_response)
            return {"result": "ok", "text": final_response, "file": tts_file}
        
    else:
        final_response = "No se entendio lo requerido"
        tts_file = TTS().process(final_response)
        return {"result": "ok", "text": final_response, "file": tts_file}