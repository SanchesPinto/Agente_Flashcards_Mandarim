import os
import uuid
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import edge_tts

app = FastAPI(title="Microsserviço de Áudio Mandarim (Edge TTS)")

# Cria a pasta temporária se não existir
os.makedirs("audios_temp", exist_ok=True)

class TextoRequisicao(BaseModel):
    texto_mandarim: str

@app.post("/gerar-audio")
async def gerar_audio(req: TextoRequisicao):
    if not req.texto_mandarim:
        raise HTTPException(status_code=400, detail="Texto vazio.")

    try:
        # Gera um nome único, agora no formato .mp3
        nome_arquivo = f"audios_temp/{uuid.uuid4().hex}.mp3"
        
        # Voz selecionada: Xiaoxiao (Feminina, Mandarim da China Continental, super natural)
        # Se preferir uma voz masculina, você pode trocar por "zh-CN-YunxiNeural"
        voz = "zh-CN-XiaoxiaoNeural"
        
        # Comunica com a API do Edge e salva o arquivo
        communicate = edge_tts.Communicate(req.texto_mandarim, voz)
        await communicate.save(nome_arquivo)
        
        print(f"[Áudio] Arquivo gerado com sucesso: {nome_arquivo}")
        
        return FileResponse(
            path=nome_arquivo, 
            media_type="audio/mpeg", 
            filename="audio_mandarim.mp3"
        )

    except Exception as e:
        print(f"[Erro] Falha ao gerar áudio: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")