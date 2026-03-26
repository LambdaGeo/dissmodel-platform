
# DisSModel Platform

Plataforma de execução escalável para o **DisSModel** (Distributed Spatial Simulation Model).

Ambiente integrado para desenvolvimento e execução de modelos geoespaciais, com JupyterLab, API REST e Workers distribuídos.

## 🌍 Onde Roda

- ✅ Servidor local (desktop/laptop)
- ✅ Cluster on-premise (INPE, universidades)
- ✅ Nuvem privada (OpenStack, etc.)
- ✅ Nuvem pública (AWS, GCP, Azure) - opcional

## 🚀 Quick Start

```bash
# Clonar repositório
git clone https://github.com/LambdaGeo/dissmodel-platform.git
cd dissmodel-platform

# Configurar variáveis de ambiente
cp .env.example .env

# Subir plataforma
docker compose up --build

# Acessar JupyterLab
open http://localhost:8888
```

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────┐
│  JupyterLab (Frontend)                  │
│  • Desenvolvimento de modelos           │
│  • Visualização interativa              │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│  API Gateway + Workers (Backend)        │
│  • Filas Redis                          │
│  • Execução distribuída                 │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│  MinIO (Storage)                        │
│  • Inputs/Outputs                       │
│  • S3-compatible                        │
└─────────────────────────────────────────┘
```

## 📚 Documentação

- [Arquitetura](docs/architecture.md)
- [Deploy](docs/deployment.md)
- [Guia do Usuário](docs/user-guide.md)

## 🤝 Contribuição

Veja [developer-guide.md](docs/developer-guide.md) para informações sobre como contribuir.

## 📄 Licença

MIT License - ver [LICENSE](LICENSE)
