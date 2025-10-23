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
