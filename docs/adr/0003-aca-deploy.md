# Deploy via GitHub + Azure DevOps pipeline to ACR, then ACA; AKS as stretch

No Docker locally, so all image builds happen in CI: push to GitHub → Azure DevOps pipeline runs pytest, builds and pushes the image to Azure Container Registry, then deploys to Azure Container Apps via managed identity. Local dev runs FastAPI + Vite directly. AKS pod-per-run is the documented production hardening path.
