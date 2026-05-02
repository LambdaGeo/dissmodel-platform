# scripts/validate_executors.py
#
# Usado pelo CI quando não existe services/worker/tests/
# Valida que todos os executors registrados passam no contrato ABC.
#
# Execução local:
#   PYTHONPATH=services python3 scripts/validate_executors.py

import sys
import os

# O código em services/worker usa imports como `from worker.schemas import ...`
# então o PYTHONPATH precisa apontar para services/, não para a raiz do repo.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'services'))

from worker.executors.testing import ExecutorTestHarness
from worker.registry import ExecutorRegistry

executors = ExecutorRegistry._executors

if not executors:
    print("⚠️  Nenhum executor registrado até o momento. O CI continuará, mas lembre-se de registrar seus modelos em services/worker/executors/__init__.py")
    sys.exit(0)

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
