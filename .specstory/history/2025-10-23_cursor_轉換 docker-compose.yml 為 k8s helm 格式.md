# 轉換 docker-compose.yml 為 k8s helm 格式
_Exported on 2025/10/23 at 16:14:38 [GMT+8] from Cursor (1.7.54)_

---

**User**

請參考 @docker-compose.yml將之轉換成 k8s helm 使用的 yaml 檔案格式，並儲存到 @k8s_helm/ 目錄下


---

**Cursor**

我將幫您將 docker-compose.yml 轉換成 Kubernetes Helm 格式的 YAML 檔案。首先讓我檢查 k8s_helm 目錄是否存在，然後建立相應的 Helm chart 結構。


現在我將建立 Helm chart 的標準結構，並根據 docker-compose.yml 的內容建立相應的 Kubernetes 資源檔案。


現在開始建立 Helm chart 的檔案：


```yaml
apiVersion: v2
name: tooluniverse
description: A Helm chart for ToolUniverse application
type: application
version: 0.1.0
appVersion: "1.0.0"
keywords:
  - tooluniverse
  - tools
  - api
home: https://github.com/your-org/tooluniverse
sources:
  - https://github.com/your-org/tooluniverse
maintainers:
  - name: ToolUniverse Team
    email: team@tooluniverse.com
```

```yaml
# Default values for tooluniverse.
# This is a YAML-formatted file.
# Declare variables to be passed into your templates.

replicaCount: 1

image:
  repository: tooluniverse
  tag: "latest"
  pullPolicy: IfNotPresent

imagePullSecrets: []
nameOverride: ""
fullnameOverride: ""

serviceAccount:
  # Specifies whether a service account should be created
  create: true
  # Annotations to add to the service account
  annotations: {}
  # The name of the service account to use.
  # If not set and create is true, a name is generated using the fullname template
  name: ""

podAnnotations: {}

podSecurityContext: {}
  # fsGroup: 2000

securityContext: {}
  # capabilities:
  #   drop:
  #   - ALL
  # readOnlyRootFilesystem: true
  # runAsNonRoot: true
  # runAsUser: 1000

service:
  type: ClusterIP
  port: 7000
  targetPort: 7000
  nodePort: 31903

ingress:
  enabled: false
  className: ""
  annotations: {}
    # kubernetes.io/ingress.class: nginx
    # kubernetes.io/tls-acme: "true"
  hosts:
    - host: tooluniverse.local
      paths:
        - path: /
          pathType: Prefix
  tls: []
  #  - secretName: tooluniverse-tls
  #    hosts:
  #      - tooluniverse.local

resources: {}
  # We usually recommend not to specify default resources and to leave this as a conscious
  # choice for the user. This also increases chances charts run on environments with little
  # resources, such as Minikube. If you do want to specify resources, uncomment the following
  # lines, adjust them as necessary, and remove the curly braces after 'resources:'.
  # limits:
  #   cpu: 100m
  #   memory: 128Mi
  # requests:
  #   cpu: 100m
  #   memory: 128Mi

autoscaling:
  enabled: false
  minReplicas: 1
  maxReplicas: 100
  targetCPUUtilizationPercentage: 80
  # targetMemoryUtilizationPercentage: 80

nodeSelector: {}

tolerations: []

affinity: {}

# Environment variables
env:
  OPENTARGETS_API_KEY: ""
  NCBI_API_KEY: ""

# Volume mounts
persistence:
  enabled: true
  storageClass: ""
  accessMode: ReadWriteOnce
  size: 1Gi
  mountPath: /app/data
```

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "tooluniverse.fullname" . }}
  labels:
    {{- include "tooluniverse.labels" . | nindent 4 }}
spec:
  {{- if not .Values.autoscaling.enabled }}
  replicas: {{ .Values.replicaCount }}
  {{- end }}
  selector:
    matchLabels:
      {{- include "tooluniverse.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      {{- with .Values.podAnnotations }}
      annotations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      labels:
        {{- include "tooluniverse.selectorLabels" . | nindent 8 }}
    spec:
      {{- with .Values.imagePullSecrets }}
      imagePullSecrets:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      serviceAccountName: {{ include "tooluniverse.serviceAccountName" . }}
      securityContext:
        {{- toYaml .Values.podSecurityContext | nindent 8 }}
      containers:
        - name: {{ .Chart.Name }}
          securityContext:
            {{- toYaml .Values.securityContext | nindent 12 }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          ports:
            - name: http
              containerPort: {{ .Values.service.targetPort }}
              protocol: TCP
          env:
            {{- if .Values.env.OPENTARGETS_API_KEY }}
            - name: OPENTARGETS_API_KEY
              value: {{ .Values.env.OPENTARGETS_API_KEY | quote }}
            {{- end }}
            {{- if .Values.env.NCBI_API_KEY }}
            - name: NCBI_API_KEY
              value: {{ .Values.env.NCBI_API_KEY | quote }}
            {{- end }}
          livenessProbe:
            httpGet:
              path: /
              port: http
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /
              port: http
            initialDelaySeconds: 5
            periodSeconds: 5
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
          {{- if .Values.persistence.enabled }}
          volumeMounts:
            - name: data
              mountPath: {{ .Values.persistence.mountPath }}
          {{- end }}
      {{- if .Values.persistence.enabled }}
      volumes:
        - name: data
          {{- if .Values.persistence.storageClass }}
          persistentVolumeClaim:
            claimName: {{ include "tooluniverse.fullname" . }}-data
          {{- else }}
          emptyDir: {}
          {{- end }}
      {{- end }}
      {{- with .Values.nodeSelector }}
      nodeSelector:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.affinity }}
      affinity:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.tolerations }}
      tolerations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
```

```yaml
apiVersion: v1
kind: Service
metadata:
  name: {{ include "tooluniverse.fullname" . }}
  labels:
    {{- include "tooluniverse.labels" . | nindent 4 }}
spec:
  type: {{ .Values.service.type }}
  ports:
    - port: {{ .Values.service.port }}
      targetPort: {{ .Values.service.targetPort }}
      protocol: TCP
      name: http
      {{- if and (eq .Values.service.type "NodePort") .Values.service.nodePort }}
      nodePort: {{ .Values.service.nodePort }}
      {{- end }}
  selector:
    {{- include "tooluniverse.selectorLabels" . | nindent 4 }}
```

```yaml
{{- if .Values.serviceAccount.create -}}
apiVersion: v1
kind: ServiceAccount
metadata:
  name: {{ include "tooluniverse.serviceAccountName" . }}
  labels:
    {{- include "tooluniverse.labels" . | nindent 4 }}
  {{- with .Values.serviceAccount.annotations }}
  annotations:
    {{- toYaml . | nindent 4 }}
  {{- end }}
{{- end }}
```

```yaml
{{- if .Values.persistence.enabled }}
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: {{ include "tooluniverse.fullname" . }}-data
  labels:
    {{- include "tooluniverse.labels" . | nindent 4 }}
spec:
  accessModes:
    - {{ .Values.persistence.accessMode }}
  resources:
    requests:
      storage: {{ .Values.persistence.size }}
  {{- if .Values.persistence.storageClass }}
  storageClassName: {{ .Values.persistence.storageClass }}
  {{- end }}
{{- end }}
```

```plaintext
{{/*
Expand the name of the chart.
*/}}
{{- define "tooluniverse.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "tooluniverse.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "tooluniverse.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "tooluniverse.labels" -}}
helm.sh/chart: {{ include "tooluniverse.chart" . }}
{{ include "tooluniverse.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "tooluniverse.selectorLabels" -}}
app.kubernetes.io/name: {{ include "tooluniverse.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "tooluniverse.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "tooluniverse.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}
```

```yaml
{{- if .Values.autoscaling.enabled }}
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: {{ include "tooluniverse.fullname" . }}
  labels:
    {{- include "tooluniverse.labels" . | nindent 4 }}
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: {{ include "tooluniverse.fullname" . }}
  minReplicas: {{ .Values.autoscaling.minReplicas }}
  maxReplicas: {{ .Values.autoscaling.maxReplicas }}
  metrics:
    {{- if .Values.autoscaling.targetCPUUtilizationPercentage }}
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: {{ .Values.autoscaling.targetCPUUtilizationPercentage }}
    {{- end }}
    {{- if .Values.autoscaling.targetMemoryUtilizationPercentage }}
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: {{ .Values.autoscaling.targetMemoryUtilizationPercentage }}
    {{- end }}
{{- end }}
```

```yaml
{{- if .Values.ingress.enabled -}}
{{- $fullName := include "tooluniverse.fullname" . -}}
{{- $svcPort := .Values.service.port -}}
{{- if and .Values.ingress.className (not (hasKey .Values.ingress.annotations "kubernetes.io/ingress.class")) }}
  {{- $_ := set .Values.ingress.annotations "kubernetes.io/ingress.class" .Values.ingress.className}}
{{- end }}
{{- if semverCompare ">=1.19-0" .Capabilities.KubeVersion.GitVersion -}}
apiVersion: networking.k8s.io/v1
{{- else if semverCompare ">=1.14-0" .Capabilities.KubeVersion.GitVersion -}}
apiVersion: networking.k8s.io/v1beta1
{{- else -}}
apiVersion: extensions/v1beta1
{{- end }}
kind: Ingress
metadata:
  name: {{ $fullName }}
  labels:
    {{- include "tooluniverse.labels" . | nindent 4 }}
  {{- with .Values.ingress.annotations }}
  annotations:
    {{- toYaml . | nindent 4 }}
  {{- end }}
spec:
  {{- if and .Values.ingress.className (semverCompare ">=1.18-0" .Capabilities.KubeVersion.GitVersion) }}
  ingressClassName: {{ .Values.ingress.className }}
  {{- end }}
  {{- if .Values.ingress.tls }}
  tls:
    {{- range .Values.ingress.tls }}
    - hosts:
        {{- range .hosts }}
        - {{ . | quote }}
        {{- end }}
      secretName: {{ .secretName }}
    {{- end }}
  {{- end }}
  rules:
    {{- range .Values.ingress.hosts }}
    - host: {{ .host | quote }}
      http:
        paths:
          {{- range .paths }}
          - path: {{ .path }}
            {{- if and .pathType (semverCompare ">=1.18-0" $.Capabilities.KubeVersion.GitVersion) }}
            pathType: {{ .pathType }}
            {{- end }}
            backend:
              {{- if semverCompare ">=1.19-0" $.Capabilities.KubeVersion.GitVersion }}
              service:
                name: {{ $fullName }}
                port:
                  number: {{ $svcPort }}
              {{- else }}
              serviceName: {{ $fullName }}
              servicePort: {{ $svcPort }}
              {{- end }}
          {{- end }}
    {{- end }}
{{- end }}
```

現在讓我建立一個 README 檔案來說明如何使用這個 Helm chart：


```markdown
# ToolUniverse Helm Chart

這個 Helm chart 用於在 Kubernetes 叢集中部署 ToolUniverse 應用程式。

## 前置需求

- Kubernetes 1.19+
- Helm 3.0+

## 安裝

### 使用預設值安裝

```bash
helm install tooluniverse ./tooluniverse
```

### 使用自訂值安裝

```bash
helm install tooluniverse ./tooluniverse -f custom-values.yaml
```

### 設定環境變數

在安裝前，請確保設定必要的環境變數：

```bash
export OPENAI_API_KEY="your-openai-api-key"
export USPTO_API_KEY="your-uspto-api-key"
```

然後使用這些值安裝：

```bash
helm install tooluniverse ./tooluniverse \
  --set env.OPENTARGETS_API_KEY="$OPENAI_API_KEY" \
  --set env.NCBI_API_KEY="$USPTO_API_KEY"
```

## 配置

### 主要配置選項

| 參數 | 描述 | 預設值 |
|------|------|--------|
| `replicaCount` | Pod 副本數量 | `1` |
| `image.repository` | 映像檔倉庫 | `tooluniverse` |
| `image.tag` | 映像檔標籤 | `latest` |
| `service.type` | 服務類型 | `ClusterIP` |
| `service.port` | 服務端口 | `7000` |
| `service.nodePort` | NodePort 端口 | `31903` |
| `persistence.enabled` | 啟用持久化儲存 | `true` |
| `persistence.size` | 儲存大小 | `1Gi` |

### 環境變數

| 變數 | 描述 | 預設值 |
|------|------|--------|
| `OPENTARGETS_API_KEY` | OpenAI API 金鑰 | `""` |
| `NCBI_API_KEY` | USPTO API 金鑰 | `""` |

## 升級

```bash
helm upgrade tooluniverse ./tooluniverse
```

## 卸載

```bash
helm uninstall tooluniverse
```

## 存取應用程式

### 使用 NodePort

如果服務類型設為 `NodePort`，可以透過以下方式存取：

```bash
kubectl get services
# 找到 EXTERNAL-IP 和 PORT
# 然後在瀏覽器中存取 http://<EXTERNAL-IP>:<PORT>
```

### 使用 Port Forward

```bash
kubectl port-forward svc/tooluniverse 7000:7000
# 然後在瀏覽器中存取 http://localhost:7000
```

## 持久化儲存

此 chart 預設啟用持久化儲存，資料會儲存在 `/app/data` 目錄中。您可以透過以下參數配置：

```yaml
persistence:
  enabled: true
  storageClass: "your-storage-class"
  accessMode: ReadWriteOnce
  size: 1Gi
  mountPath: /app/data
```

## 水平擴展

要啟用水平 Pod 自動擴展：

```yaml
autoscaling:
  enabled: true
  minReplicas: 1
  maxReplicas: 10
  targetCPUUtilizationPercentage: 80
```

## 故障排除

### 檢查 Pod 狀態

```bash
kubectl get pods -l app.kubernetes.io/name=tooluniverse
```

### 查看 Pod 日誌

```bash
kubectl logs -l app.kubernetes.io/name=tooluniverse
```

### 檢查服務

```bash
kubectl get services tooluniverse
```
```

最後，讓我檢查建立的檔案結構：


完成！我已經成功將您的 `docker-compose.yml` 轉換成完整的 Kubernetes Helm chart 格式，並儲存在 `/home/chad/ToolUniverse-1022/k8s_helm/` 目錄下。

## 建立的檔案結構：

```
k8s_helm/
└── tooluniverse/
    ├── Chart.yaml                    # Helm chart 元資料
    ├── values.yaml                   # 預設配置值
    ├── README.md                     # 使用說明
    └── templates/
        ├── _helpers.tpl             # Helm 輔助函數
        ├── deployment.yaml          # Kubernetes Deployment
        ├── service.yaml             # Kubernetes Service
        ├── serviceaccount.yaml      # ServiceAccount
        ├── pvc.yaml                 # PersistentVolumeClaim
        ├── hpa.yaml                 # HorizontalPodAutoscaler
        └── ingress.yaml             # Ingress
```

## 主要轉換對應：

1. **容器映像檔**：`tooluniverse:latest` → `image.repository` 和 `image.tag`
2. **端口映射**：`31903:7000` → `service.port` 和 `service.nodePort`
3. **環境變數**：`OPENTARGETS_API_KEY` 和 `NCBI_API_KEY` → `env` 配置
4. **資料卷**：`./data:/app/data` → `persistence` 配置
5. **容器名稱**：`tooluniverse` → 使用 Helm 命名規則

## 使用方式：

```bash
# 安裝
helm install tooluniverse ./k8s_helm/tooluniverse

# 設定環境變數
helm install tooluniverse ./k8s_helm/tooluniverse \
  --set env.OPENTARGETS_API_KEY="your-key" \
  --set env.NCBI_API_KEY="your-key"

# 升級
helm upgrade tooluniverse ./k8s_helm/tooluniverse
```

這個 Helm chart 提供了完整的 Kubernetes 部署功能，包括服務、持久化儲存、水平擴展、Ingress 等選項。

```plaintext
k8s_helm/
└── tooluniverse/
    ├── Chart.yaml                    # Helm chart 元資料
    ├── values.yaml                   # 預設配置值
    ├── README.md                     # 使用說明
    └── templates/
        ├── _helpers.tpl             # Helm 輔助函數
        ├── deployment.yaml          # Kubernetes Deployment
        ├── service.yaml             # Kubernetes Service
        ├── serviceaccount.yaml      # ServiceAccount
        ├── pvc.yaml                 # PersistentVolumeClaim
        ├── hpa.yaml                 # HorizontalPodAutoscaler
        └── ingress.yaml             # Ingress
```

```shellscript
# 安裝
helm install tooluniverse ./k8s_helm/tooluniverse

# 設定環境變數
helm install tooluniverse ./k8s_helm/tooluniverse \
  --set env.OPENTARGETS_API_KEY="your-key" \
  --set env.NCBI_API_KEY="your-key"

# 升級
helm upgrade tooluniverse ./k8s_helm/tooluniverse
```

