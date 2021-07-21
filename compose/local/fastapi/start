#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

alembic upgrade head
uvicorn main:app --reload --reload-dir project --host 0.0.0.0
