# ArgoCD GitOps Implementation

## 🎯 ArgoCD Setup for Enterprise AI Platform

Arg    description: Admin access to enter```yaml
# production-application.yaml  
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: enterprise-platform-production
  namespace: argocd
spec:
  project: enterprise-platform
  source:
    repoURL: https://github.com/organization/enterprise-ai-platform.git
    targetRevision: HEAD
    path: gitops/manifests/production
  destination:
    server: https://kubernetes.default.svc
    namespace: enterprise-platform-production    policies: |
    - p, proj:enterprise-platform:admin, applications, *, enterprise-platform/*, allow
    groups:
    - enterprise-platform-adminsrovides a declarative, GitOps continuous delivery tool for Kubernetes.

## 📋 Prerequisites

- Kubernetes cluster (AKS, EKS, or local)
- kubectl configured
- Helm 3.x installed

## 🚀 Installation

### 1. Install ArgoCD

```bash
# Create namespace
kubectl create namespace argocd

# Install ArgoCD
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Wait for ArgoCD to be ready
kubectl wait --for=condition=available --timeout=300s deployment/argocd-server -n argocd
```

### 2. Access ArgoCD UI

```bash
# Port forward to access UI
kubectl port-forward svc/argocd-server -n argocd 8080:443

# Get initial admin password
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

Navigate to: https://localhost:8080
- Username: admin
- Password: (from command above)

### 3. Install ArgoCD CLI

```bash
# Windows (using chocolatey)
choco install argocd-cli

# Or download from: https://github.com/argoproj/argo-cd/releases
```

## 🏗️ Application Setup

### 1. Create ArgoCD Project

```yaml
# enterprise-ai-platform-project.yaml
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: enterprise-ai-platform
  namespace: argocd
spec:
  description: Enterprise AI Platform Project
  sourceRepos:
  - 'https://github.com/organization/enterprise-ai-platform.git'
  destinations:
  - namespace: enterprise-ai-platform-staging
    server: https://kubernetes.default.svc
  - namespace: enterprise-ai-platform-production  
    server: https://kubernetes.default.svc
  clusterResourceWhitelist:
  - group: ''
    kind: Namespace
  - group: 'apps'
    kind: Deployment
  - group: ''
    kind: Service
  namespaceResourceWhitelist:
  - group: ''
    kind: ConfigMap
  - group: ''
    kind: Secret
  - group: 'apps'
    kind: Deployment
  roles:
  - name: admin
    description: Admin access to enterprise platform
    policies:
    - p, proj:enterprise-platform:admin, applications, *, enterprise-platform/*, allow
    groups:
    - enterprise-platform-admins
```

### 2. Create Applications

```yaml
# staging-application.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: enterprise-platform-staging
  namespace: argocd
spec:
  project: enterprise-platform
  source:
    repoURL: https://github.com/organization/enterprise-ai-platform.git
    targetRevision: HEAD
    path: gitops/manifests/staging
  destination:
    server: https://kubernetes.default.svc
    namespace: enterprise-platform-staging
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
    - CreateNamespace=true
  revisionHistoryLimit: 3
```

```yaml
# production-application.yaml  
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: enterprise-platform-production
  namespace: argocd
spec:
  project: enterprise-platform
  source:
    repoURL: https://github.com/organization/enterprise-ai-platform.git
    targetRevision: HEAD
    path: gitops/manifests/production
  destination:
    server: https://kubernetes.default.svc
    namespace: enterprise-platform-production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
    - CreateNamespace=true
  revisionHistoryLimit: 5
```

## 🔄 Workflow Integration

### Modified GitHub Actions Workflow

```yaml
# .github/workflows/gitops-cd.yml
name: GitOps CD Pipeline

on:
  push:
    branches: [ main, develop ]

jobs:
  build-and-update-manifests:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
      
    - name: Build and test
      run: |
        # Your existing build and test steps
        cd ui && npm ci && npm run build
        cd ../backend && dotnet build && dotnet test
        
    - name: Build Docker images
      run: |
        # Build frontend
        docker build -t organization/enterprise-platform-ui:${{ github.sha }} ./ui
        
        # Build backend  
        docker build -t organization/enterprise-platform-api:${{ github.sha }} ./backend
        
    - name: Push images
      run: |
        echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
        docker push organization/enterprise-platform-ui:${{ github.sha }}
        docker push organization/enterprise-platform-api:${{ github.sha }}
        
    - name: Update GitOps manifests
      run: |
        # Update image tags in manifests
        sed -i "s|image: organization/enterprise-platform-ui:.*|image: organization/enterprise-platform-ui:${{ github.sha }}|" gitops/manifests/staging/frontend-deployment.yaml
        sed -i "s|image: organization/enterprise-platform-api:.*|image: organization/enterprise-platform-api:${{ github.sha }}|" gitops/manifests/staging/backend-deployment.yaml
        
        # For production, only update on main branch
        if [ "${{ github.ref }}" == "refs/heads/main" ]; then
          sed -i "s|image: enterprise/enterprise-platform-ui:.*|image: enterprise/enterprise-platform-ui:${{ github.sha }}|" gitops/manifests/production/frontend-deployment.yaml
          sed -i "s|image: enterprise/enterprise-platform-api:.*|image: enterprise/enterprise-platform-api:${{ github.sha }}|" gitops/manifests/production/backend-deployment.yaml
        fi
        
    - name: Commit updated manifests
      run: |
        git config --local user.email "enterprise-platform@your-domain.com"
        git config --local user.name "GitHub Action"
        git add gitops/manifests/
        git commit -m "Update image tags to ${{ github.sha }}" || exit 0
        git push
```

## 🎛️ ArgoCD Configuration

### RBAC Configuration

```yaml
# argocd-rbac-cm.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-rbac-cm
  namespace: argocd
data:
  policy.default: role:readonly
  policy.csv: |
    # Admin role for enterprise platform team
    p, role:enterprise-platform-admin, applications, *, enterprise-platform/*, allow
    p, role:enterprise-platform-admin, repositories, *, *, allow
    p, role:enterprise-platform-admin, clusters, *, *, allow
    
    # Developer role - can sync apps
    p, role:enterprise-platform-developer, applications, sync, enterprise-platform/*, allow
    p, role:enterprise-platform-developer, applications, get, enterprise-platform/*, allow
    
    # Bind roles to groups (configure with your SSO)
    g, enterprise-platform-admins, role:enterprise-platform-admin
    g, enterprise-platform-developers, role:enterprise-platform-developer
```

### Notifications Configuration

```yaml
# argocd-notifications-cm.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-notifications-cm
  namespace: argocd
data:
  service.slack: |
    token: $slack-token
  template.app-deployed: |
    message: |
      {{if eq .serviceType "slack"}}:white_check_mark:{{end}} Application {{.app.metadata.name}} is now running new version.
  template.app-health-degraded: |
    message: |
      {{if eq .serviceType "slack"}}:exclamation:{{end}} Application {{.app.metadata.name}} has degraded.
  trigger.on-deployed: |
    - when: app.status.operationState.phase in ['Succeeded'] and app.status.health.status == 'Healthy'
      send: [app-deployed]
  trigger.on-health-degraded: |
    - when: app.status.health.status == 'Degraded'
      send: [app-health-degraded]
  subscriptions: |
    - recipients:
      - slack:enterprise-platform-alerts
      triggers:
      - on-deployed
      - on-health-degraded
```

## 🔧 Commands

### Deploy ArgoCD Setup

```bash
# Apply project and applications
kubectl apply -f applications/enterprise-platform-project.yaml
kubectl apply -f applications/staging-application.yaml
kubectl apply -f applications/production-application.yaml

# Configure RBAC
kubectl apply -f config/argocd-rbac-cm.yaml

# Setup notifications
kubectl apply -f config/argocd-notifications-cm.yaml
```

### CLI Operations

```bash
# Login to ArgoCD
argocd login localhost:8080

# List applications
argocd app list

# Sync application manually
argocd app sync enterprise-platform-staging

# Check application status
argocd app get enterprise-platform-staging

# View application logs
argocd app logs enterprise-platform-staging

# Rollback to previous version
argocd app rollback enterprise-platform-staging
```

## 📊 Monitoring & Observability

ArgoCD provides built-in metrics and can integrate with:
- Prometheus for metrics
- Grafana for dashboards  
- Jaeger for tracing
- Your existing Azure monitoring stack

## 🔒 Security Best Practices

1. **Repository Access**: Use deploy keys instead of personal tokens
2. **RBAC**: Configure proper role-based access control
3. **Secrets Management**: Use external secret operators (Azure Key Vault, etc.)
4. **Network Policies**: Restrict network access between namespaces
5. **Image Scanning**: Integrate with security scanning tools

## 🎯 Benefits for Enterprise Platform

1. **Accessibility Testing**: Staged deployments with rollback
2. **Compliance**: Full audit trail in Git
3. **Security**: No cluster credentials in CI/CD
4. **Reliability**: Automatic drift detection and correction
5. **Team Collaboration**: Declarative infrastructure everyone can understand
