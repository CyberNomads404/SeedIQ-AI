# 🚜✨ SeedIQ — API de Análise (IA / Visão Computacional)

SeedIQ é um serviço modular para análise e classificação de grãos por imagem (milho, soja etc.).
Este repositório contém a API de análise (backend Python) responsável por receber jobs,
enfileirar/executar tarefas e retornar resultados ao sistema central via webhook.

Escolha abaixo como deseja rodar: via Docker (recomendado para desenvolvimento/integração) ou localmente (direto com Python e Celery).

## 🚀 Opção A — Rodar com Docker / docker-compose (recomendado)

Use esta opção quando quiser levantar todos os serviços (API, worker, Redis e Flower) isolados em containers.

Passos rápidos:

```bash
# 1. Build e up (modo dev)
docker compose build --no-cache
docker compose up -d

# 2. Ver logs
docker compose logs -f api
docker compose logs -f worker
docker compose logs -f flower

# 3. Parar e remover
docker compose down
```

Notas:
- Garanta que o arquivo `docker-compose.yaml` e o `.env` tenham as variáveis corretas:
	- `REDIS_HOST` / `REDIS_PORT` (dentro do compose o host do Redis é `redis` e a porta interna é `6379`).
	- `CELERY_BROKER_URL` e `CELERY_RESULT_BACKEND` podem ser definidos explicitamente, ex: `redis://redis:6379/0`.
- Se você usa uma network externa (`shared_net`) defina ou crie a network localmente: `docker network create shared_net`.

## 🧪 Opção B — Rodar localmente (venv) + Celery

Use quando estiver desenvolvendo localmente sem Docker.

Pré-requisitos:
- Python 3.11 (recomendado)
- Virtualenv/venv
- Redis rodando localmente (ou um Redis acessível)

Exemplo de instruções:

```bash
# 1. Criar e ativar venv
python -m venv .venv
source .venv/bin/activate

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Exportar PYTHONPATH para que imports do pacote 'src' funcionem
export PYTHONPATH=$(pwd)/src:$PYTHONPATH

# 4. Rodar a API (modo desenvolvimento)
python run.py

# 5. Rodar worker Celery (execute em outra aba/terminal)
# Ajuste o -A para o módulo correto do projeto. Exemplo provável:
celery -A src.services.celery_service.celery_service worker -l info --concurrency=1

# 6. (Opcional) Rodar Flower para monitorar
celery -A src.services.celery_service.celery_service flower --broker=redis://redis:6379/0 --address=0.0.0.0 --port=5555
```

Observação importante: o caminho do aplicativo Celery (-A) depende do nome/estrutura do módulo no projeto. Se o seu arquivo é `src/services/celery_service.py` e exporta a instância `celery_service`, o target pode ser `src.services.celery_service.celery_service` (veja os logs se houver erro `ModuleNotFoundError` e ajuste conforme necessário).

## ✅ Recomendações de configuração e troubleshooting

- Variáveis de ambiente úteis (adicione ao `.env`):

```ini
API_PORT=8000
REDIS_HOST=redis
REDIS_PORT=6379
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/1
FLOWER_PORT=5555
API_SERVICE_HOST=api
API_SERVICE_PORT=3000
```

- OpenCV em containers: se ao importar `cv2` aparecer erro `libGL.so.1: cannot open shared object file`, prefira instalar `opencv-python-headless` no `requirements.txt` ou adicionar as libs do sistema no `Dockerfile`:

	- Instalar headless (Python): `pip install opencv-python-headless`
	- Ou no Dockerfile (Debian/Ubuntu):

		```dockerfile
		RUN apt-get update && apt-get install -y --no-install-recommends libgl1-mesa-glx libglib2.0-0 && rm -rf /var/lib/apt/lists/*
		```

- Porta já ocupada (ex: Flower na 5555): identifique o processo/container que está usando a porta e pare-o:

```bash
docker ps --format "table {{.ID}}\t{{.Names}}\t{{.Ports}}" | grep 5555 || true
# se não for um container:
sudo lsof -iTCP:5555 -sTCP:LISTEN -P -n
sudo kill <PID>
```

- DNS de serviços no Compose: dentro dos containers, use `redis` como hostname (não `localhost`). Se estiver usando uma network externa (`shared_net`), garanta que todos os serviços estejam conectados a ela.

## 🔁 Fluxo típico de processamento (alto nível)

1. API recebe requisição (webhook ou enfileiramento) com `image_url` e `seed_category`.
2. API cria job e publica na fila (Celery / Redis) ou chama serviço de análise.
3. Worker baixa a imagem, carrega o analyzer adequado (ex: `corn_ai`), processa e gera resultado.
4. Worker envia callback para a URL informada (normalmente `http://api:3000/api/webhook/analyze` no ambiente Compose).

## 🧰 Execução de testes (local)

```bash
# Exemplos básicos
PYTHONPATH=./src .venv/bin/python src/tests/analyze_ai_test.py

# Testes unitários (se houver integração com pytest/unittest)
pytest
```

## Contribuição

1. Abra uma issue para descrever a mudança/bug.
2. Crie uma branch a partir de `develop`.
3. Faça PR com descrição e testes.

---

Se quiser, eu atualizo automaticamente o `docker-compose.yaml` para garantir que `redis` esteja na mesma network dos serviços ou corro um fix no `src/services/celery_service.py` para usar `REDIS_PORT` do `.env` — diga qual prefere e eu aplico as mudanças.

---

_Última atualização: documentação simplificada com opções Docker e local — escolha a que preferir e eu te guio nos próximos passos._
