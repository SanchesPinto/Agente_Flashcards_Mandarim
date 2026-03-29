import genanki
import random

def criar_baralho_apkg(flashcards_dados: list, nome_arquivo_saida: str = "Baralho_Mandarim.apkg"):
    print("\n[Genanki] Empacotando flashcards com áudios separados...")
    
    estilo_css = """
    .card { font-family: arial; text-align: center; color: #333; background-color: #fcfcfc; padding: 15px; }
    .hanzi-gigante { font-size: 80px; font-weight: bold; color: #d32f2f; margin-bottom: 10px; }
    .pinyin { font-size: 26px; color: #555; margin-bottom: 5px; }
    .traducao { font-size: 22px; font-weight: bold; color: #1976d2; margin-bottom: 15px; }
    .instrucao { font-size: 14px; color: #999; margin-bottom: 15px; font-style: italic; letter-spacing: 1px; text-transform: uppercase; }
    .frase-hanzi { font-size: 36px; color: #222; margin-top: 20px; margin-bottom: 5px; line-height: 1.4; }
    .frase-pinyin { font-size: 22px; color: #666; margin-bottom: 5px; }
    .frase-traducao { font-size: 18px; color: #444; font-style: italic; margin-top: 5px; }
    .container-exemplo { background-color: #f0f0f0; border-radius: 8px; padding: 15px; margin-top: 20px; }
    img { max-width: 80%; height: auto; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); margin-top: 15px; }
    """

    modelo_id = 1607392330 # ID atualizado para evitar conflito de cache no Anki
    modelo_mandarim_multi = genanki.Model(
        modelo_id,
        'Modelo Mandarim IA - Áudio Duplo',
        fields=[
            {'name': 'Hanzi'}, {'name': 'Pinyin'}, {'name': 'Traducao_PT'},
            {'name': 'Classe_Gramatical'}, {'name': 'Frase_Hanzi'}, 
            {'name': 'Frase_Pinyin'}, {'name': 'Frase_Traducao'},
            {'name': 'Tags'}, {'name': 'Imagem'}, 
            {'name': 'Audio_Palavra'}, {'name': 'Audio_Frase'} # <-- Dois campos de áudio
        ],
        templates=[
            # 1. Leitura: Mostra a palavra e toca o áudio dela no verso. A frase fica numa caixa separada com o próprio áudio.
            {
                'name': '1. Leitura (Hanzi -> PT)',
                'qfmt': '<div class="instrucao">Leia e Traduza</div><div class="hanzi-gigante">{{Hanzi}}</div>',
                'afmt': '{{FrontSide}}<hr id="answer"><div class="pinyin">{{Pinyin}}</div><div class="traducao">{{Traducao_PT}} <i>({{Classe_Gramatical}})</i></div><div class="audio">{{Audio_Palavra}}</div><br>{{Imagem}}<div class="container-exemplo"><div class="frase-hanzi">{{Frase_Hanzi}}</div><div class="audio">{{Audio_Frase}}</div><div class="frase-pinyin">{{Frase_Pinyin}}</div><div class="frase-traducao">{{Frase_Traducao}}</div></div>',
            },
            # 2. Audição: Toca APENAS a palavra na frente!
            {
                'name': '2. Audição (Áudio -> Hanzi)',
                'qfmt': '<div class="instrucao">O que você ouviu?</div><br><br><div class="audio">{{Audio_Palavra}}</div>',
                'afmt': '{{FrontSide}}<hr id="answer"><div class="hanzi-gigante">{{Hanzi}}</div><div class="pinyin">{{Pinyin}}</div><div class="traducao">{{Traducao_PT}}</div><br>{{Imagem}}',
            },
            # 3. Visual
            {
                'name': '3. Visual (Imagem -> Hanzi)',
                'qfmt': '<div class="instrucao">Como se diz isto?</div>{{Imagem}}',
                'afmt': '{{FrontSide}}<hr id="answer"><div class="hanzi-gigante">{{Hanzi}}</div><div class="pinyin">{{Pinyin}}</div><div class="audio">{{Audio_Palavra}}</div>',
            },
            # 4. Tradução Reversa
            {
                'name': '4. Tradução (PT -> Hanzi)',
                'qfmt': '<div class="instrucao">Traduza para o mandarim</div><br><div class="traducao" style="font-size: 45px;">{{Traducao_PT}}</div>',
                'afmt': '{{FrontSide}}<hr id="answer"><div class="hanzi-gigante">{{Hanzi}}</div><div class="pinyin">{{Pinyin}}</div><div class="audio">{{Audio_Palavra}}</div>',
            },
            # 5. Contexto: Toca a FRASE inteira na frente.
            {
                'name': '5. Contexto (Frase -> Significado)',
                'qfmt': '<div class="instrucao">Entenda a Frase</div><div class="frase-hanzi">{{Frase_Hanzi}}</div><br><div class="audio">{{Audio_Frase}}</div>',
                'afmt': '{{FrontSide}}<hr id="answer"><div class="frase-pinyin">{{Frase_Pinyin}}</div><div class="frase-traducao">{{Frase_Traducao}}</div><br><hr><div class="instrucao">Vocabulário alvo nesta frase:</div><div style="font-size: 20px;"><b>{{Hanzi}}</b> ({{Pinyin}}) - {{Traducao_PT}} {{Audio_Palavra}}</div>',
            },
        ],
        css=estilo_css
    )

    baralho_id = random.randrange(1 << 30, 1 << 31)
    meu_baralho = genanki.Deck(baralho_id, '🇨🇳 Mandarim IA - Vocabulário')

    arquivos_midia = []

    for card in flashcards_dados:
        nota = genanki.Note(
            model=modelo_mandarim_multi,
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
                f"[sound:{card.get('nome_audio_palavra', '')}]" if card.get('nome_audio_palavra') else "",
                f"[sound:{card.get('nome_audio_frase', '')}]" if card.get('nome_audio_frase') else ""
            ],
            tags=[card.get('tags', 'IA')]
        )
        meu_baralho.add_note(nota)
        
        if card.get('caminho_imagem'): arquivos_midia.append(card['caminho_imagem'])
        if card.get('caminho_audio_palavra'): arquivos_midia.append(card['caminho_audio_palavra'])
        if card.get('caminho_audio_frase'): arquivos_midia.append(card['caminho_audio_frase'])

    pacote = genanki.Package(meu_baralho)
    pacote.media_files = list(set(arquivos_midia))
    pacote.write_to_file(nome_arquivo_saida)
    print(f"[Genanki] Sucesso! Baralho gerado: {nome_arquivo_saida}")