# Declaração uso de Inteligência Artificial

A inteligência artificial serviu como suporte, agindo tanto como uma revisora quanto como auxiliar para ajudar na tomada de decisões e agilizar o trabalho repetitivo.
Um bom exemplo foi durante a mudança estrutural quando ao invés de uma string, criei a enum para ser um tipo mais representativo de status das reservas. A IA é extremamente eficaz em trabalhos do tipo, encontrar as ocorrências da string literal é trabalhoso e passível de esquecer para trás algum, enquanto que a IA resolve em segundos essa análise de forma extremamente confiável.
A IA utilizada foi a versão gratuita do ChatGPT durante a maioria do tempo, que introduz algumas limitações, uma delas que é válido mencionar é a janela de contexto extremamente limitada comparada a versões pagas dos principais modelos existentes. Como por exemplo na quantidade de tokens disponíveis para as tarefas que é muito reduzida e a janela de contexto que se esgota rapidamente.
Tendo essa limitação em mente, não é possível simplesmente enviar todo o código do projeto para contextualizar a IA e esperar que ela resolva o problema. A abordagem utilizada foi de eu identificar as lacunas, propor maneiras de solucioná-las e pedir a LLM para esclarecer dúvidas de sintaxe e mudanças em escopos bem definidos, para diminuir a degradação das respostas e a alucinação.
Apesar disso, ela é capaz de acelerar muito o desenvolvimento e dar respostas muito satisfatórias, o problema é que as vezes ela esquece muito rápido e você tem que ficar carregando essa informação em novos prompts.

Como mencionado, utilizei a versão gratuita e nela ocorre o problema de encher rapidamente a janela de contexto e você é obrigado a abrir um novo chat com o resumo do anterior, sem a opção de continuar na conversa. Por conta disso, existem três conversas diferentes, que deixarei o link abaixo:

Onfly      - https://chatgpt.com/share/6af9a317-8f90-83e9-b3a2-400b45fb085c

Onfly (1)  - https://chatgpt.com/share/6af9a31f-6244-83e9-acae-f6691063fc20

Onfly (2)  - https://chatgpt.com/share/6af9a33c-cca4-83ea-82dc-2fab422b1246

O log consolidado foi elaborado a partir da terceira conversa, que continha resumos das duas anteriores. Portanto, ele não reproduz integralmente o histórico original. Para uma conferência mais completa das interações e do contexto em que as decisões foram tomadas, recomendo consultar diretamente os links das conversas.


Ao final, utilizei também o Antigravity do Google na versão de estudantes, com o modelo Gemini 3.8 flash - Medium Effort para acabar os últimos detalhes dos novos testes que eu introduzi e ficar tudo conforme descrito no README, me ajudando principalmente na formatação dos commmits dos testes que eu já tinha elaborado e na adição de testes que ele sugeriu nas partes de conversão de moedas e testes por mês, que eu considerei válidos, o log se encontra no arquivo abaixo:

[Log consolidado](./sessao-02.jsonl)
