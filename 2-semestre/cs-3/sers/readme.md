# ⚡ REECHARGE - Sistema Inteligente de Gestão de Recarga para Veículos Elétricos

## 👥 Equipe
- **Enzo Posterlli Strinta** - RM570035
- **Giovanna Tristão Lopes** - RM572552

---

## 📖 Sobre o Projeto
O **REECHARGE** é uma plataforma simulada de gerenciamento de estações de recarga para Veículos Elétricos (VEs) com foco comercial. A solução integra automação de distribuição de energia (*Smart Charging*), sinergia com geração fotovoltaica (painéis solares), precificação dinâmica e insights gerados por Inteligência Artificial, tudo através de uma interface gráfica intuitiva e profissional desenvolvida em Python.

---

## 🧩 Esquema Detalhado de Integração dos Componentes

### 1. Diagrama de Blocos da Arquitetura (Hardware & Software)
```mermaid
graph TD
    subgraph Frontend [Front-End: Interface Tkinter]
        UI[Dashboard Interativo]
        Terminal[Terminal OCPP e IA]
        Pagamento[Módulo de Checkout]
    end

    subgraph Backend [Back-End: Regras de Negócio Python]
        MotorSC[Motor de Smart Charging]
        MotorTarifa[Cálculo de Tarifa Dinâmica]
        AgenteIA[Motor de IA Preditiva]
    end

    subgraph Infra [Infraestrutura Simulada]
        Solar[Geração Solar Fotovoltaica]
        Grid[Rede Elétrica Concessionária]
        Carregadores[Hub de 4 Vagas GoodWe]
    end

    subgraph Persistencia [Persistência de Dados]
        JSON[(Exportação de Dados .json)]
    end

    UI <--> MotorSC
    Terminal <--> AgenteIA
    Pagamento --> JSON
    
    Grid --> MotorSC
    Solar --> MotorSC
    MotorSC --> Carregadores
```
---
### 2. Fluxograma de Operação do Usuário

```mermaid
flowchart LR
    A([Início]) --> B[Monitoramento: Grid + Solar]
    B --> C{O que fazer?}
    
    C -- "Conectar" --> D[Definir Bateria]
    D --> E[Simular Recarga]
    E --> F{Fim da Carga?}
    F -- "Não" --> E
    F -- "Sim" --> G[Módulo Pagamento]
    
    C -- "Sistema" --> L[Acionar IA / Tempo]
    L --> B
    
    G --> H[PIX ou Cartão]
    H --> I[Gerar Relatório JSON]
    I --> J([Liberar Vaga])
    J -. "Retorna ao início" .-> B
````
---

### 3. Protótipo Simulado

* **Tela Inicial**
<img width="1365" height="767" alt="image" src="https://github.com/user-attachments/assets/4f902b6a-6bb3-4489-b537-9026af6b0214" />

* **Simulação de Pagamento**
<img width="1365" height="767" alt="image" src="https://github.com/user-attachments/assets/5a79623c-5d5c-43e7-8740-2837e8afd7be" />

<img width="1365" height="767" alt="image" src="https://github.com/user-attachments/assets/0147456e-0b11-4272-9dc3-e89f01f17f9d" />

---

## 🛠 Justificativa Técnica das Escolhas
Para atender aos requisitos de automação e integração técnica de forma otimizada e acessível, adotamos as seguintes tecnologias:

* **Linguagem (Python):** Escolhida por sua versatilidade e facilidade na manipulação de estruturas de dados e criação de lógicas complexas de automação.

* **Interface Gráfica (Tkinter):** Utilizamos uma biblioteca nativa do Python. Isso justifica-se para garantir que o software rode em qualquer ambiente sem necessidade de instalações complexas via pip, mantendo o código leve e focado no Pensamento Computacional.

* **Comunicação (Padrão OCPP 1.6J):** O sistema simula mensagens desse protocolo aberto, pois é o padrão global adotado pela indústria (vendors como a GoodWe). Isso torna a lógica de negócio do software compatível com a realidade do mercado.

* **Armazenamento de Dados (JSON):** A persistência de dados de faturamento no formato JSON é o formato universal de troca de informações moderno, facilitando integrações futuras com APIs, bancos de dados NoSQL e Web Dashboards.

* **Design Visual (Preto e Vermelho):** Adotado para conferir um aspecto profissional, tecnológico e de fácil leitura (Dark Mode).
---

## 🌱 Contribuição para Sustentabilidade, Automação Inteligente e Eficiência Energética

O projeto foi arquitetado para que cada tecnologia aplicada atue diretamente nos três pilares exigidos para a infraestrutura moderna de cidades inteligentes:

### 1. Sustentabilidade (Integração Fotovoltaica Simulada)
* **Tecnologia:** Lógica de injeção de energia renovável baseada em horário (Simulação de Inversores Híbridos).
* **Contribuição:** O sistema reduz a dependência de combustíveis fósseis e da rede elétrica convencional ao priorizar a energia solar. Ao detectar alta geração (ex: entre 10h e 14h), a plataforma orienta o consumo de energia limpa, reduzindo a pegada de carbono da operação do hub de recarga.

### 2. Automação Inteligente (Motor Python e IA Preditiva)
* **Tecnologia:** Algoritmos em Python e Processamento de Regras Preditivas.
* **Contribuição:** O sistema elimina a necessidade de microgerenciamento humano. A automação inteligente monitora em tempo real a ocupação das vagas, a tarifa do momento (Demand Response) e a geração solar. Além disso, o Agente de IA toma decisões de negócio de forma autônoma, sugerindo ao operador aplicar tarifas promocionais ou alertando sobre sobrecargas iminentes antes que elas afetem a infraestrutura.

### 3. Eficiência Energética (Smart Charging e OCPP 1.6J)
* **Tecnologia:** Algoritmo de *Load Balancing* (Balanceamento de Carga) e mensagens do padrão OCPP.
* **Contribuição:** A eficiência energética é garantida pelo *Smart Charging*. Em vez de sobrecarregar a rede ou precisar de cabos e transformadores superdimensionados (o que seria caro e ineficiente), o algoritmo divide dinamicamente a potência exata disponível (Rede + Solar) entre os veículos conectados. Isso garante que nenhum watt seja desperdiçado e que o limite contratado da distribuidora de energia nunca seja estourado, garantindo máxima eficiência com os recursos físicos disponíveis.
---

## 📊 Resultados e Dados Funcionais Apresentados
O protótipo simulado entrega, em tempo real, os seguintes resultados funcionais operacionais:

* **Smart Charging em Ação:** Se a capacidade somada de recarga dos carros exceder o limite do Hub (Grid 15kW + Solar Variável), o sistema restringe automaticamente a potência enviada (Ex: reduz de 7kW para 3.5kW por vaga), evitando multas na conta de luz comercial.

* **Uso de Energia Limpa:** O sistema reconhece a "hora do dia" e simula a entrada de energia solar, diminuindo a dependência da rede local.

* **Módulo de Pagamento Funcional:** O operador calcula o custo real da recarga considerando Tarifas de Pico (acréscimo de 30% entre 18h e 21h) e efetua "baixa" via PIX ou Cartão.

* **Coleta de Dados:** O encerramento das vagas gera automaticamente o arquivo físico "relatorio_financeiro_[DATA].json" contendo ID da vaga, energia consumida, valor pago e forma de pagamento.

* **Variação da Matriz de Suprimento:** O usuário visualiza o relógio avançar e a geração solar subir e descer, alterando diretamente a potência máxima do hub em tempo real.

* **Rateio de Potência (Gargalo Físico):** A simulação prova que conectar múltiplos VEs não causa colapso (Blackout local), mas sim uma desaceleração controlada da recarga, mantendo a operação segura e dentro da norma técnica.

* **Métricas Financeiras Atreladas à Energia:** O sistema exporta faturas (.json) relacionando a quantidade exata de energia consumida (kWh) com o custo do horário da tomada, evidenciando o modelo de negócios viável de um eletroposto sustentável.
--- 

## 🧠 Conexão com os Conteúdos da Disciplina
Este projeto engloba de forma prática os pilares da disciplina de Pensamento Computacional e Automação com Python:

* **Decomposição:** O problema de gestão de frota foi quebrado em módulos menores (Cálculo de Tarifa, IA Preditiva, Interface Visual, Simulador OCPP).

* **Reconhecimento de Padrões e Algoritmos:** A lógica de Smart Charging é um algoritmo clássico de balanceamento de carga, distribuindo recursos (potência) com base em variáveis dinâmicas (carros ativos vs energia total).

* **Automação:** O sistema automatiza o faturamento baseado em horário comercial e a aplicação de energia solar na equação de disponibilidade da rede.

* **Programação Orientada a Objetos (POO):** O código GUI foi encapsulado na classe ReechargeGUI, gerindo os estados das variáveis globais do hub de recarga de maneira limpa.
---

## ⚙️ Estrutura do Repositório e Instruções de Funcionamento
### Arquivos no Repositório:
* codigo: Código-fonte principal com a Interface Gráfica e regras de negócio.

* readme.md: Documentação atual do projeto.

### Como Executar a Aplicação:
1. Certifique-se de ter o Python 3.8 ou superior instalado em sua máquina.

2. Clone o repositório ou faça o download do arquivo app_gui.py.

3. Abra o terminal na pasta onde o arquivo está salvo.

4. Execute o comando: python codigo.py

5. Interaja com a interface gráfica, crie sessões, teste o módulo de pagamento e verifique o arquivo .json gerado ao final das operações na mesma pasta do executável.
