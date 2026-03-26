# DisSModel Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker Compose](https://img.shields.io/badge/Docker-Compose-blue.svg)](https://docs.docker.com/compose/)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-green.svg)](https://www.python.org/)

Plataforma de execução escalável para o **DisSModel** (Distributed Spatial Simulation Model).

Ambiente integrado para desenvolvimento e execução de modelos geoespaciais, com JupyterLab, API REST e Workers distribuídos.

## 🌍 Onde Roda

- ✅ Servidor local (desktop/laptop)
- ✅ Cluster on-premise (INPE, universidades)
- ✅ Nuvem privada (OpenStack, etc.)
- ✅ Nuvem pública (AWS, GCP, Azure) - opcional

## 🚀 Quick Start

### Pré-requisitos

- Docker e Docker Compose instalados
- 8GB+ RAM recomendado
- 20GB+ espaço em disco

### Instalação Rápida

```bash
# 1. Clonar repositório
git clone https://github.com/LambdaGeo/dissmodel-platform.git
cd dissmodel-platform

# 2. Configurar variáveis de ambiente
cp .env.example .env

# 3. Subir plataforma
docker compose up --build

# 4. Acessar serviços
# JupyterLab: http://localhost:8888
# API Docs:   http://localhost:8000/docs
# MinIO:      http://localhost:9001
```

### Parar Plataforma

```bash
docker compose down
```

### Parar e Limpar Dados

```bash
docker compose down -v  # Remove volumes (cuidado!)
```

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────────────────┐
│                    DISSMODEL PLATFORM                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  [Pesquisador] → Navegador → JupyterLab (Container)             │
│                              │                                  │
│                              ├── Python Direto (imports)        │
│                              └── API REST (jobs pesados)        │
│                              │                                  │
│                              ▼                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              SERVIDOR / DOCKER HOST                      │   │
│  │                                                          │   │
│  │  🟦 Jupyter    🟩 API      🟥 Worker    🗄️ MinIO  🔄 Redis │   │
│  │  (Frontend)  (Gateway)   (Process.)   (Dados)   (Fila)   │   │
│  │                                                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Componentes

| Serviço | Porta | Descrição |
|---------|-------|-----------|
| **JupyterLab** | 8888 | Ambiente de desenvolvimento Python |
| **API Gateway** | 8000 | FastAPI para submissão de jobs |
| **Worker** | - | Processamento em background (escalável) |
| **MinIO** | 9000/9001 | Storage S3-compatible (dados) |
| **Redis** | 6379 | Fila de mensagens e cache |

## 📚 Documentação

- [Arquitetura](docs/architecture.md) - Detalhes técnicos e decisões
- [Deploy](docs/deployment.md) - Como implantar em diferentes ambientes
- [Guia do Usuário](docs/user-guide.md) - Para pesquisadores

## 📋 Exemplo de Uso

### Desenvolvimento Local (Python Direto)

```python
from dissmodel.core import Environment
from dissmodel.geo.raster import RasterBackend

# Carregar dados
backend = RasterBackend.from_file('/data/inputs/dem.tif')

# Configurar e executar modelo
env = Environment(end_time=100)
model = FloodModel(backend=backend, sea_level=0.05)
results = env.run()

# Visualizar
model.display()
```

### Execução via API (Jobs Pesados)

```python
import requests

payload = {
    "model_name": "FloodModel",
    "input_dataset": "dem.tif",
    "parameters": {"sea_level": 0.05, "steps": 1000}
}

response = requests.post(
    "http://api:8000/submit_job",
    json=payload
)

job_id = response.json()['job_id']
```

## 🔧 Configuração

### Variáveis de Ambiente

Copie `.env.example` para `.env` e ajuste:

```bash
# MinIO Credentials
MINIO_ROOT_USER=inpe_admin
MINIO_ROOT_PASSWORD=inpe_secret_2024

# DisSModel Config
DISSMODEL_LOG_LEVEL=INFO
DISSMODEL_CLOUD=false
```

### Escalar Workers

```bash
# Aumentar para 5 workers
docker compose up --scale worker=5
```

## 🤝 Contribuição

1. Fork o repositório
2. Crie uma branch (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Add nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

Veja [docs/developer-guide.md](docs/developer-guide.md) para mais detalhes.

## 📄 Licença

MIT License - ver [LICENSE](LICENSE)

## 🙏 Agradecimentos

- [DisSModel](https://github.com/LambdaGeo/dissmodel) - Biblioteca base de modelagem
- [Jupyter Project](https://jupyter.org/) - Ambiente de desenvolvimento
- [MinIO](https://min.io/) - Storage S3-compatible
- [Pangeo](https://pangeo.io/) - Inspiração para arquitetura cloud-native

## 📞 Contato

- **Organização:** LambdaGeo / INPE
- **Issues:** https://github.com/LambdaGeo/dissmodel-platform/issues
- **Discussões:** https://github.com/LambdaGeo/dissmodel-platform/discussions