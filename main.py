import os
import requests
from modulos.llm_agent import gerar_flashcards_json
from modulos.gerador_apkg import criar_baralho_apkg
from modulos.gerador_audio import gerar_audio_local # <-- Nosso novo módulo!

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "SUA_CHAVE_AQUI")

def baixar_imagem_pexels(termo_busca, id_unico):
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

def pipeline_principal(input_usuario: str):
    os.makedirs("media_temp", exist_ok=True)
    
    try:
        print("\n=== INICIANDO PIPELINE DE FLASHCARDS ===")
        flashcards = gerar_flashcards_json(input_usuario)
        
        for card in flashcards:
            print(f"\nProcessando mídia para o card: {card['hanzi']}")
            
            # 1. Imagem
            cam_img, nom_img = baixar_imagem_pexels(card['termo_busca_imagem_en'], card['id_unico'])
            card['caminho_imagem'] = cam_img
            card['nome_imagem'] = nom_img
            
            # 2. Áudio da Palavra (Agora usando o módulo direto)
            cam_aud_palavra, nom_aud_palavra = gerar_audio_local(card['hanzi'], card['id_unico'])
            card['caminho_audio_palavra'] = cam_aud_palavra
            card['nome_audio_palavra'] = nom_aud_palavra

            # 3. Áudio da Frase (Usando o sufixo _frase)
            cam_aud_frase, nom_aud_frase = gerar_audio_local(card['frase_exemplo_hanzi'], f"{card['id_unico']}_frase")
            card['caminho_audio_frase'] = cam_aud_frase
            card['nome_audio_frase'] = nom_aud_frase

        criar_baralho_apkg(flashcards, "Meus_Flashcards_Mandarim.apkg")
        print("\n=== PROCESSO FINALIZADO COM SUCESSO ===")
        
    except Exception as e:
        print(f"\n=== ERRO ===\n{e}\n")

if __name__ == "__main__":
    lista_teste = "livro, mesa"
    pipeline_principal(lista_teste)