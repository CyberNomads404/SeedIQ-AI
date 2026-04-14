<div align="center">

# 🔬 SeedIQ AI — API de Classificação

Serviço de visão computacional responsável por receber imagens de grãos, processar e retornar a classificação com contagem por categoria. Parte do ecossistema SeedIQ.

![Python](https://img.shields.io/badge/Python_3.11-3776AB?style=flat&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=flat&logo=opencv&logoColor=white)
![Celery](https://img.shields.io/badge/Celery-37814A?style=flat&logo=celery&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=flat&logo=redis&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)

</div>

---

## 📸 Resultado da análise

![ezgif com-animated-gif-maker](https://github.com/user-attachments/assets/c1686917-7446-4917-b122-475fac0f6c04)

| Imagem Original | Escala de Cinza | Blur Gaussiano |
|-----------------|-----------------|----------------|
| <img width="366" height="504" alt="image (8)" src="https://github.com/user-attachments/assets/bf28dc8b-e98e-4df3-828a-0451954e190c" /> | <img width="366" height="504" alt="image (7)" src="https://github.com/user-attachments/assets/ea219923-7849-4365-8742-6b0f260d4d5d" /> | <img width="366" height="504" alt="image (6)" src="https://github.com/user-attachments/assets/7ef500b6-9620-40f7-b04e-adb1a1602a91" /> |

| Limiarização | Morfologia | Erosão |
|--------------|------------|-------------------|
| <img width="366" height="504" alt="image (5)" src="https://github.com/user-attachments/assets/f832a340-55fc-4ece-af08-f5d46ac36537" /> | <img width="366" height="504" alt="image (4)" src="https://github.com/user-attachments/assets/ea5a10a6-87d1-4ade-8f70-637c19fde5c8" /> | <img width="366" height="504" alt="image (3)" src="https://github.com/user-attachments/assets/85f09820-6a03-4904-91ec-9d6e80d144f2" /> |

| Objetos Detectados |
|---------------------|
| <img width="366" height="504" alt="image (2)" src="https://github.com/user-attachments/assets/64e8b884-355c-4675-b2e1-c15edc33d88f" /> |

---

## 📌 Sobre o projeto

O SeedIQ é um projeto acadêmico desenvolvido no último semestre do curso de Sistemas de Informação (2025.2), integrando três disciplinas: Programação para Dispositivos Móveis, Segurança e Auditoria de Sistemas e Computação Gráfica e Processamento de Imagens.

Este repositório contém a **API de Classificação**, o coração técnico do ecossistema. Quando uma imagem chega, ela passa por um pipeline completo de visão computacional e retorna a contagem de grãos classificados por categoria.

O ecossistema completo é dividido em três repositórios:

| Parte | Repositório | Descrição |
|-------|-------------|-----------|
| 🖥️ Painel + API Central | [SeedIQ](https://github.com/CyberNomads404/SeedIQ) | Gestão, dashboard e orquestração |
| 🔬 API de Classificação | este repositório | Visão computacional com Python + OpenCV |
| 📱 App Mobile | [seediq_app](https://github.com/CyberNomads404/seediq_app) | App Flutter para operadores em campo |

---

## 🔁 Fluxo de funcionamento

<img width="1471" height="904" alt="Diagrama Caso de Uso drawio" src="https://github.com/user-attachments/assets/11afdcfc-fde9-4e9b-8165-fe6cb0fcf17f" />

1. API Central envia a imagem via webhook com `image_url` e `seed_category`
2. API cria o job e publica na fila via Celery + Redis
3. Worker baixa a imagem e carrega o analisador correspondente ao tipo de grão
4. Pipeline de visão computacional processa a imagem e classifica cada grão
5. Worker envia o resultado de volta para a API Central via webhook

---

## 🧠 Pipeline de processamento

O pipeline é composto por 5 etapas aplicadas em sequência a cada imagem recebida:

**1. Escala de cinza**
Conversão para canal único com `cvtColor(BGR2GRAY)`, reduzindo a complexidade computacional sem perder informações estruturais dos grãos.

**2. Blur Gaussiano**
Aplicação de kernel 5x5 com `GaussianBlur` para suavizar o ruído da imagem sem perder as bordas essenciais dos grãos.

**3. Limiarização binária**
Threshold fixo no valor 165 com `cv2.THRESH_BINARY` para separação binária entre grão e fundo, isolando os objetos de interesse.

**4. Morfologia — Close + Erosão (etapas separadas)**
Primeiro aplica `morphologyEx` com `MORPH_CLOSE` e kernel 5x5 para preencher buracos nos grãos. Em seguida aplica `erode` com kernel retangular 3x3 para separar grãos que estejam grudados entre si.

**5. Detecção de contornos**
`findContours` com `RETR_EXTERNAL` para isolar cada grão individualmente antes da classificação.

---

## 📐 Filtro dinâmico de área

Antes de classificar, o sistema calcula a média robusta das áreas dos contornos usando **IQR (Interquartile Range)** para ignorar outliers. A partir dessa média são definidos os limites dinâmicos:

- `min_avg_area` = média robusta × 0.50
- `max_avg_area` = média robusta × 1.75

Isso evita que variações de distância e tamanho de lote afetem a classificação, tornando o sistema adaptável a diferentes condições de captura.

---

## 🌽 Classificação por cor HSV

Cada grão isolado é classificado com base na cor média no espaço HSV:

| Classificação | Critério | Descrição |
|---------------|----------|-----------|
| ✅ Bom | Hue 18-35 e V > 100 | Grão amarelo/pérola saudável |
| 🔥 Queimado | V < 90 e S < 60 | Grão escuro com baixa luminosidade e saturação |
| 🌿 Esverdeado | Hue 40-80 | Grão imaturo com tonalidade verde |
| 📏 Pequeno | Área < min_avg_area | Grão abaixo do limiar dinâmico |
| ⚠️ Má detecção | Área > max_avg_area | Provavelmente múltiplos grãos grudados |
| ❓ Desconhecido | Nenhum padrão se encaixa | Cor fora dos intervalos definidos |

---

## ⚙️ Tecnologias

- **Linguagem:** Python 3.11
- **Visão computacional:** OpenCV
- **Fila assíncrona:** Celery + Redis
- **Monitoramento de filas:** Flower
- **Orquestração:** Docker + Docker Compose

---

## 🚀 Rodando localmente

### Opção A — Docker (recomendado)

```bash
# 1. Build e up
docker compose build --no-cache
docker compose up -d

# 2. Acompanhar logs
docker compose logs -f api
docker compose logs -f worker
```

### Opção B — Local com Python

```bash
# 1. Criar e ativar venv
python -m venv .venv
source .venv/bin/activate

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Exportar PYTHONPATH
export PYTHONPATH=$(pwd)/src:$PYTHONPATH

# 4. Rodar a API
python run.py

# 5. Rodar o worker Celery (outro terminal)
celery -A src.services.celery_service.celery_service worker -l info --concurrency=1
```

Variáveis de ambiente necessárias no `.env`:

```ini
API_PORT=8000
REDIS_HOST=redis
REDIS_PORT=6379
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/1
```

---

## 📖 Documentação da API

A documentação completa dos endpoints está disponível no Postman:

👉 [Acessar documentação](https://documenter.getpostman.com/view/44409413/2sB3WjzjEt)

---

## 👥 Equipe

Desenvolvido pela equipe **CyberNomads404** como Projeto Integrador do curso de Sistemas de Informação — 2025.2

- [@Erikli999](https://github.com/Erikli999) – Erikli999
- [@piedro404](https://github.com/piedro404) – Pedro Henrique Martins Borges
- [@thayna-bezerra](https://github.com/thayna-bezerra) – Thayna Bezerra

---

## 📬 Contato

pedro.henrique.martins404@gmail.com
