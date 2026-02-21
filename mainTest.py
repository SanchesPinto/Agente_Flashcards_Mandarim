import os
import csv

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List

# Inicializa o cliente (Certifique-se de ter a variável de ambiente OPENAI_API_KEY configurada)
load_dotenv()
client = OpenAI()


# ==========================================
# 1. DEFINIÇÃO DO SCHEMA (Pydantic)
# Isso obriga a OpenAI a retornar exatamente esta estrutura
# ==========================================
class Flashcard(BaseModel):
    id_unico: str = Field(description="ID único, ex: CARD-01")
    hanzi: str = Field(description="Apenas os caracteres em mandarim")
    pinyin: str = Field(description="Pinyin com as marcações de tom corretas")
    traducao_pt: str = Field(description="Tradução contextualizada para o português")
    classe_gramatical: str = Field(description="Classe gramatical abreviada (ex: v., n., adj.)")
    frase_exemplo_hanzi: str = Field(description="Frase curta em Hanzi. PROIBIDO O USO DE VÍRGULAS.")
    frase_exemplo_pinyin: str = Field(description="Pinyin da frase. PROIBIDO O USO DE VÍRGULAS.")
    frase_exemplo_traducao: str = Field(description="Tradução da frase. PROIBIDO O USO DE VÍRGULAS.")
    tags: str = Field(description="Nível de dificuldade HSK (ex: HSK1, HSK2)")

class FlashcardList(BaseModel):
    flashcards: List[Flashcard]

# ==========================================
# 2. LÓGICA PRINCIPAL DO AGENTE
# ==========================================
def gerar_flashcards(input_usuario: str, filepath: str = "flashcards_gerados.csv"):
    
    # Pré-processamento e Limpeza
    palavras = [p.strip() for p in input_usuario.split(',') if p.strip()]
    qtd_palavras = len(palavras)
    
    # Hard Logic: Regra de Negócio (Limite de Segurança)
    if qtd_palavras == 0:
        return "Erro: Nenhuma palavra identificada."
    if qtd_palavras > 10:
        return f"Erro: Limite excedido. Você enviou {qtd_palavras} palavras. O máximo é 10."
    
    input_limpo = ", ".join(palavras)
    print(f"Processando {qtd_palavras} palavra(s)...")

    # Prompt de Sistema (Simplificado, pois o Pydantic já dita as regras do formato)
    system_prompt = """
    Você é um Agente Especialista em Educação de Idiomas (Mandarim).
    Crie flashcards de alta qualidade para as palavras fornecidas.
    ATENÇÃO: É estritamente proibido usar vírgulas nas frases de exemplo (hanzi, pinyin ou tradução).
    Filtro de Segurança: Ignore palavras ofensivas.
    """

    try:
        # Chamada à API usando o método "parse" para garantir a saída estruturada
        response = client.beta.chat.completions.parse(
            model="gpt-4o-mini", # Rápido e de baixo custo
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Gere flashcards para o seguinte vocabulário: {input_limpo}"}
            ],
            response_format=FlashcardList,
            temperature=0.3 # Baixa temperatura para respostas mais determinísticas e precisas
        )

        # Extrai o objeto validado pelo Pydantic
        resultado_json = response.choices[0].message.parsed
        
        # Converte o resultado estruturado para CSV
        salvar_em_csv(resultado_json.flashcards, filepath)
        
        return f"Sucesso! {len(resultado_json.flashcards)} flashcards salvos em '{filepath}'."

    except Exception as e:
        return f"Erro na comunicação com a API: {str(e)}"

# ==========================================
# 3. EXPORTAÇÃO SEGURA PARA CSV
# ==========================================
def salvar_em_csv(flashcards: List[Flashcard], filepath: str):
    # Cabeçalho baseado no seu modelo do Anki
    headers = [
        "ID_Unico", "Hanzi", "Pinyin", "Tradução_PT", 
        "Classe_Gramatical", "Frase_Exemplo_Hanzi", 
        "Frase_Exemplo_Pinyin", "Frase_Exemplo_Tradução", "Tags"
    ]
    
    # 'a' para append (adicionar ao fim do arquivo) em vez de sobrescrever
    with open(filepath, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL)
        
        # Se o arquivo estiver vazio, escreve o cabeçalho primeiro
        if file.tell() == 0:
            writer.writerow(headers)
            
        for card in flashcards:
            writer.writerow([
                card.id_unico,
                card.hanzi,
                card.pinyin,
                card.traducao_pt,
                card.classe_gramatical,
                card.frase_exemplo_hanzi,
                card.frase_exemplo_pinyin,
                card.frase_exemplo_traducao,
                card.tags
            ])

# ==========================================
# EXECUÇÃO (TESTE)
# ==========================================
if __name__ == "__main__":
    teste_input = "estudar, computador, inteligência artificial"
    resultado = gerar_flashcards(teste_input)
    print(resultado)