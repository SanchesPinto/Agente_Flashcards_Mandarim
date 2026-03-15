from modulos.llm_agent import gerar_flashcards_json
from modulos.buscador_imagens import buscar_url_imagem
from modulos.gerador_csv import salvar_em_csv

def pipeline_principal(input_usuario: str):
    try:
        print("\n=== INICIANDO GERAÇÃO DE FLASHCARDS ===")
        
        # 1. Chama a IA para gerar os dados estruturados
        flashcards_dados = gerar_flashcards_json(input_usuario)
        
        # 2. Enriquece os dados com as imagens do Pexels
        for card in flashcards_dados:
            tag_imagem = buscar_url_imagem(card['termo_busca_imagem_en']) 
            card['imagem'] = tag_imagem
            
        # 3. Salva o resultado final no CSV
        salvar_em_csv(flashcards_dados, "meus_flashcards.csv")
        
        print("=== PROCESSO FINALIZADO COM SUCESSO ===\n")
        
    except ValueError as ve:
        # Captura os erros de limite de palavras (Hard Logic)
        print(f"\n=== ERRO DE VALIDAÇÃO ===\n{ve}\n")
    except Exception as e:
        # Captura qualquer outro erro inesperado
        print(f"\n=== ERRO INESPERADO ===\n{e}\n")

if __name__ == "__main__":
    # Vocabulário de teste para rodar o pipeline
    lista_teste = "estudar, livro, maçã"
    pipeline_principal(lista_teste)