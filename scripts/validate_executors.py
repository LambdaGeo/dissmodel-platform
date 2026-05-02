# scripts/validate_executors.py
#
# Usado pelo CI quando não existe services/worker/tests/
# Valida que todos os executors registrados passam no contrato ABC.
#
# Execução local:
#   PYTHONPATH=. python3 scripts/validate_executors.py

from services.worker.executors.testing import ExecutorTestHarness
from services.worker.registry import ExecutorRegistry

executors = ExecutorRegistry._executors

if not executors:
    print("⚠️  Nenhum executor registrado — verifique services/worker/executors/__init__.py")
    raise SystemExit(1)

failed = []

for name, cls in executors.items():
    try:
        ExecutorTestHarness(cls).run_contract_tests()
        print(f"✅ {name} OK")
    except Exception as e:
        print(f"❌ {name} FALHOU: {e}")
        failed.append(name)

if failed:
    print(f"\n{len(failed)} executor(s) falharam: {', '.join(failed)}")
    raise SystemExit(1)

print(f"\n{len(executors)} executor(s) validados com sucesso.")
