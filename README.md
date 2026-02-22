# Agente_Flashcards_Mandarim

## PRIMEIRO DE TUDO VALE DESTACAR QUE É MUITO IMPORTANTE CRITICAR ESSE PLANO!!!
## QUERO VER A PRÁTICA DOS CONFLITOS PRODUTIVOS!!!

🚀 Status do Projeto: Agente de IA para Flashcards de Mandarim


🎯 Onde estamos agora: MVP Concluído 
Até o momento, construímos o "motor principal" do agente. Ele recebe uma lista de vocabulário e devolve um arquivo .csv perfeitamente formatado para o Anki.
O que já foi implementado no nosso backend em Python:

    Validação de Input (Hard Logic): Criamos uma trava de segurança no código que bloqueia requisições com mais de 10 palavras. Isso evita estourar custos da API caso haja uso indevido.

    Prompt Engineering Estruturado: O Agente de IA tem uma persona definida e regras rígidas (ex: tradução focada no aprendizado, filtro contra palavras ofensivas e proibição de vírgulas nas frases de exemplo para não quebrar o CSV).

    OpenAI Structured Outputs (Pydantic): Em vez de torcer para a IA não errar a formatação do texto, nós a obrigamos a preencher um schema de dados (JSON) tipado. O nosso script Python pega esse JSON e converte para CSV. Isso garante 100% de estabilidade no arquivo gerado.


🚧 Próximos Passos: Enriquecimento Multimídia 
Agora que o texto e o CSV estão sólidos, vamos adicionar mídia aos cards:

    Geração de Termos de Busca: O LLM precisa ser configurado configurado para traduzir a palavra para o inglês e sugerir o melhor termo de busca para a futura etapa de imagens. 

    Pipeline de Imagens (Integração Pexels API): Vamos usar a API gratuita do Pexels. O script vai pegar aquele "termo de busca em inglês" gerado pelo LLM, buscar a melhor foto, fazer o download para uma pasta local (media_anki) e inserir a tag HTML correta (<img src="...">) no CSV.

    Pipeline de Áudio (Hugging Face + FastAPI): Para gerar o áudio nativo em mandarim das palavras e frases, usaremos um modelo Open Source do Hugging Face. Para não depender da internet e fugir de limites gratuitos, a ideia é rodar esse modelo localmente, envelopado em uma API própria usando FastAPI. (Essa parte ainda está sujeita a muitas mudanças, tenho minhas dúvidas se essa é a melhor abordagem)

🔮 Futuro do projeto?

    Orquestração com n8n: Quando os scripts em Python (LLM, Imagens e a API local de Áudio) estiverem validados, vamos migrar o fluxo visual para o n8n. Isso vai criar uma interface muito mais amigável para o usuário final, orquestrando todas essas chamadas de forma automatizada. Minha ideia de implementar em n8n é para que futuramente fique mais fácil de tornar esse projeto um assistente em mais línguas além do mandarim.
