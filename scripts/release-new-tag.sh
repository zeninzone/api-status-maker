#!/usr/bin/env bash
set -euo pipefail

VERSION_FILE="VERSION"

if [[ ! -f "${VERSION_FILE}" ]]; then
  echo "VERSION file not found at ${VERSION_FILE}" >&2
  exit 1
fi

VERSION="$(tr -d '[:space:]' < "${VERSION_FILE}")"
TAG="v${VERSION}"

echo "Tagging repository with ${TAG}"
git tag "${TAG}"
git push origin "${TAG}"

echo "Done. Created and pushed tag ${TAG}."

