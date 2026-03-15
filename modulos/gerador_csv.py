import csv
from typing import List

def salvar_em_csv(flashcards_dados: List[dict], filepath: str = "meus_flashcards.csv"):
    """Escreve a lista de dicionários no arquivo CSV em modo append."""
    print(f"[CSV] Salvando {len(flashcards_dados)} flashcard(s) em '{filepath}'...")
    
    headers = [
        "ID_Unico", "Hanzi", "Pinyin", "Tradução_PT", 
        "Classe_Gramatical", "Frase_Exemplo_Hanzi", 
        "Frase_Exemplo_Pinyin", "Frase_Exemplo_Tradução", "Tags", "Imagem"
    ]
    
    with open(filepath, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL)
        
        if file.tell() == 0:
            writer.writerow(headers)
            
        for card in flashcards_dados:
            writer.writerow([
                card.get('id_unico', ''),
                card.get('hanzi', ''),
                card.get('pinyin', ''),
                card.get('traducao_pt', ''),
                card.get('classe_gramatical', ''),
                card.get('frase_exemplo_hanzi', ''),
                card.get('frase_exemplo_pinyin', ''),
                card.get('frase_exemplo_traducao', ''),
                card.get('tags', ''),
                card.get('imagem', '')
            ])
    print("[CSV] Arquivo atualizado com sucesso!")