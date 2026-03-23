import os
import requests
from modulos.llm_agent import gerar_flashcards_json
from modulos.gerador_apkg import criar_baralho_apkg

# Certifique-se de que a API do Pexels está configurada no seu ambiente
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "SUA_CHAVE_AQUI")

def baixar_imagem_pexels(termo_busca, id_unico):
    """Baixa a imagem e retorna o caminho e o nome do arquivo."""
    print(f"  -> [Imagem] Buscando: {termo_busca}")
    url_busca = f"https://api.pexels.com/v1/search?query={termo_busca}&per_page=1"
    headers = {"Authorization": PEXELS_API_KEY}
    
    try:
        resposta = requests.get(url_busca, headers=headers)
        if resposta.status_code == 200 and resposta.json().get("photos"):
            url_img = resposta.json()["photos"][0]["src"]["medium"]
            img_data = requests.get(url_img).content
            
            nome_arquivo = f"{id_unico}.jpg"
            caminho = os.path.join("media_temp", nome_arquivo)
            with open(caminho, "wb") as f: f.write(img_data)
            return caminho, nome_arquivo
    except Exception as e:
        print(f"  -> [Erro Imagem]: {e}")
    return None, None

def solicitar_audio_api_local(texto_mandarim, id_unico):
    """Faz um POST para o seu FastAPI e salva o .mp3 retornado."""
    print(f"  -> [Áudio] Gerando para: {texto_mandarim}")
    try:
        # Chama a API que está rodando no uvicorn
        resposta = requests.post(
            "http://127.0.0.1:8000/gerar-audio", 
            json={"texto_mandarim": texto_mandarim}
        )
        if resposta.status_code == 200:
            nome_arquivo = f"{id_unico}.mp3"
            caminho = os.path.join("media_temp", nome_arquivo)
            with open(caminho, "wb") as f: f.write(resposta.content)
            return caminho, nome_arquivo
    except Exception as e:
        print(f"  -> [Erro Áudio]: Certifique-se de que a API local está rodando. {e}")
    return None, None

def pipeline_principal(input_usuario: str):
    os.makedirs("media_temp", exist_ok=True)
    
    try:
        print("\n=== INICIANDO PIPELINE DE FLASHCARDS ===")
        
        # 1. IA gera os textos
        flashcards = gerar_flashcards_json(input_usuario)
        
        # 2. Enriquecimento de Mídia
        for card in flashcards:
            print(f"\nProcessando mídia para o card: {card['hanzi']}")
            
            # Baixa imagem
            cam_img, nom_img = baixar_imagem_pexels(card['termo_busca_imagem_en'], card['id_unico'])
            card['caminho_imagem'] = cam_img
            card['nome_imagem'] = nom_img
            
            # Gera Áudio (Mandamos a palavra e a frase para o áudio ficar completo!)
            texto_para_audio = f"{card['hanzi']}。 {card['frase_exemplo_hanzi']}"
            cam_aud, nom_aud = solicitar_audio_api_local(texto_para_audio, card['id_unico'])
            card['caminho_audio'] = cam_aud
            card['nome_audio'] = nom_aud

        # 3. Empacota tudo no .apkg
        criar_baralho_apkg(flashcards, "Meus_Flashcards_Mandarim.apkg")
        
        print("\n=== PROCESSO FINALIZADO COM SUCESSO ===")
        print("Dê um clique duplo no arquivo 'Meus_Flashcards_Mandarim.apkg' para abrir no Anki!")
        
    except Exception as e:
        print(f"\n=== ERRO ===\n{e}\n")

if __name__ == "__main__":
    lista_teste = "estudar, computador, maçã"
    pipeline_principal(lista_teste)