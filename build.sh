#!/usr/bin/env bash
# Build script for Render deployment

set -o errexit

echo "=== Installing frontend dependencies ==="
cd frontend
npm install

echo "=== Building React frontend ==="
npm run build

echo "=== Copying build to backend/static_build ==="
mkdir -p ../backend/static_build
cp -r build/* ../backend/static_build/

echo "=== Installing backend dependencies ==="
cd ../backend
pip install -r requirements.txt

echo "=== Build complete! ==="
