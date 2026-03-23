# modulos/gerador_apkg.py
import genanki
import random

def criar_baralho_apkg(flashcards_dados: list, nome_arquivo_saida: str = "Baralho_Mandarim.apkg"):
    print("\n[Genanki] Empacotando flashcards e mídias...")
    
    # 1. Cria o Modelo Visual do Flashcard (HTML/CSS)
    # IDs precisam ser números únicos e consistentes
    modelo_id = 1607392319
    modelo_mandarim = genanki.Model(
        modelo_id,
        'Modelo Mandarim IA',
        fields=[
            {'name': 'Hanzi'}, {'name': 'Pinyin'}, {'name': 'Traducao_PT'},
            {'name': 'Classe_Gramatical'}, {'name': 'Frase_Hanzi'}, 
            {'name': 'Frase_Pinyin'}, {'name': 'Frase_Traducao'},
            {'name': 'Tags'}, {'name': 'Imagem'}, {'name': 'Audio'}
        ],
        templates=[
            {
                'name': 'Reconhecimento (Hanzi -> PT)',
                'qfmt': '<div style="font-size: 60px; text-align: center;">{{Hanzi}}</div><br><div style="text-align: center;">{{Audio}}</div>',
                'afmt': '{{FrontSide}}<hr id="answer"><div style="font-size: 20px; text-align: center;"><b>Pinyin:</b> {{Pinyin}}<br><b>Tradução:</b> {{Traducao_PT}} <i>({{Classe_Gramatical}})</i><br><br><b>Exemplo:</b><br>{{Frase_Hanzi}}<br>{{Frase_Pinyin}}<br>{{Frase_Traducao}}</div><br><div style="text-align: center;">{{Imagem}}</div>',
            },
        ],
        css='.card { font-family: arial; font-size: 20px; text-align: center; color: black; background-color: white; }'
    )

    # 2. Cria o Baralho
    baralho_id = random.randrange(1 << 30, 1 << 31)
    meu_baralho = genanki.Deck(baralho_id, '🇨🇳 Mandarim IA - Vocabulário')

    arquivos_midia = [] # Lista para guardar os caminhos das imagens e áudios

    # 3. Adiciona as Notas (Cards) ao Baralho
    for card in flashcards_dados:
        nota = genanki.Note(
            model=modelo_mandarim,
            fields=[
                card.get('hanzi', ''),
                card.get('pinyin', ''),
                card.get('traducao_pt', ''),
                card.get('classe_gramatical', ''),
                card.get('frase_exemplo_hanzi', ''),
                card.get('frase_exemplo_pinyin', ''),
                card.get('frase_exemplo_traducao', ''),
                card.get('tags', ''),
                f"<img src='{card.get('nome_imagem', '')}'>" if card.get('nome_imagem') else "",
                f"[sound:{card.get('nome_audio', '')}]" if card.get('nome_audio') else ""
            ],
            tags=[card.get('tags', 'IA')]
        )
        meu_baralho.add_note(nota)
        
        # Registra os arquivos físicos que precisam ir dentro do .apkg
        if card.get('caminho_imagem'): arquivos_midia.append(card['caminho_imagem'])
        if card.get('caminho_audio'): arquivos_midia.append(card['caminho_audio'])

    # 4. Gera o Pacote Final
    pacote = genanki.Package(meu_baralho)
    pacote.media_files = list(set(arquivos_midia)) # Remove duplicatas, se houver
    pacote.write_to_file(nome_arquivo_saida)
    
    print(f"[Genanki] Sucesso! Baralho gerado: {nome_arquivo_saida}")