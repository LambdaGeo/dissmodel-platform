# DisSModel Platform - Guia do Usuário

## Acessando a Plataforma

1. Abra seu navegador
2. Acesse `http://localhost:8888` (ou URL do servidor)
3. Você verá o JupyterLab

## Estrutura de Diretórios

```
/home/jovyan/work/     # Seu espaço de trabalho
/data/inputs/          # Dados de entrada (somente leitura)
/data/outputs/         # Seus resultados
/examples/             # Exemplos e tutoriais
```

## Executando um Modelo

### Modo Local (Desenvolvimento)

```python
from dissmodel.core import Environment
from dissmodel.geo.raster import RasterBackend

backend = RasterBackend.from_file('/data/inputs/dem.tif')
env = Environment(end_time=100)
model = FloodModel(backend=backend, sea_level=0.05)
results = env.run()
model.display()
```

### Modo Cloud (Jobs Pesados)

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
print(f"Job ID: {job_id}")
```

## Verificando Status do Job

```python
import requests

response = requests.get("http://api:8000/job/{job_id}")
print(response.json())
```

## Salvando Resultados

```python
# No Jupyter
backend.to_geotiff('/data/outputs/result.tif')

# Via Worker (automático)
# Resultado salvo em MinIO: dissmodel-outputs/results/{job_id}/
```

## Dicas

- Use volumes para persistir dados
- Submeta jobs longos via API (não no notebook)
- Consulte `/docs` da API para referência completa