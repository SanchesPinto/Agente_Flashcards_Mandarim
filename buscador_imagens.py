import os
import requests

# Pega a chave da variável de ambiente (ou você pode colar a string aqui para testes rápidos)
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

def buscar_e_baixar_imagem(termo_em_ingles: str, id_unico: str) -> str:
    """
    Busca a melhor imagem no Pexels, faz o download e retorna a tag HTML para o Anki.
    """
    print(f"  -> Buscando imagem para: '{termo_em_ingles}'...")
    
    # 1. Configura a URL de busca. Limitamos a 1 resultado (per_page=1) para economizar dados.
    url_busca = f"https://api.pexels.com/v1/search?query={termo_em_ingles}&per_page=1"
    
    # O Pexels exige a chave de API no cabeçalho 'Authorization'
    headers = {
        "Authorization": PEXELS_API_KEY
    }
    
    try:
        # 2. Faz a requisição de busca
        resposta = requests.get(url_busca, headers=headers, timeout=10)
        resposta.raise_for_status() # Lança um erro se o status não for 200 OK
        dados = resposta.json()
        
        # 3. Verifica se a API retornou alguma foto
        if not dados.get("photos"):
            print(f"     [Aviso] Nenhuma imagem encontrada para '{termo_em_ingles}'.")
            return "" # Retorna vazio para o Anki não mostrar um ícone quebrado
            
        # 4. Extrai a URL da imagem. 
        # O Pexels oferece vários tamanhos. 'medium' (largura de 350px) é ideal para flashcards.
        url_imagem = dados["photos"][0]["src"]["medium"]
        
        # 5. Faz o download do arquivo da imagem
        resposta_img = requests.get(url_imagem, timeout=10)
        resposta_img.raise_for_status()
        
        # 6. Salva localmente
        nome_arquivo = f"{id_unico}.jpg"
        pasta_destino = "media_anki"
        os.makedirs(pasta_destino, exist_ok=True)
        caminho_salvamento = os.path.join(pasta_destino, nome_arquivo)
        
        with open(caminho_salvamento, "wb") as f:
            f.write(resposta_img.content)
            
        print(f"     [Sucesso] Imagem salva: {nome_arquivo}")
        
        # 7. Retorna a tag HTML formatada para o Anki
        return f'<img src="{nome_arquivo}">'
        
    except requests.exceptions.RequestException as e:
        print(f"     [Erro] Falha na rede ou na API: {e}")
        return ""
    except Exception as e:
        print(f"     [Erro] Inesperado ao processar imagem: {e}")
        return ""