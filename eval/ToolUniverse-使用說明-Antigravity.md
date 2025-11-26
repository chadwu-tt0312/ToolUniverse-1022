# ToolUniverse-使用說明

## 1. 簡介

ToolUniverse 是一個致力於讓**「AI 輔助科學發現」**不再是少數人的特權，而是成為所有科學家都能隨手可得的基礎建設，透過標準化的介面將大型語言模型 (LLM) 與超過 600 種科學工具、數據集與 API 整合。本專案支援多種 LLM (如 OpenAI, Azure OpenAI, Claude 等) 並提供 Model Context Protocol (MCP) 伺服器，讓開發者能快速建構具備科學研究能力的 AI Agent。

**目標讀者**：負責部署 ToolUniverse 服務、維護基礎設施以及進行系統整合的 DevOps 工程師與技術人員。

## 2. 環境變數詳解 (Environment Variables)

請參考以下表格設定環境變數。建議複製 `.env.template` 為 `.env` 檔案進行設定。

| 變數名稱 | 預設值 | 必填 | 說明 |
| :--- | :--- | :--- | :--- |
| **Azure OpenAI 設定** | | | |
| `AZURE_OPENAI_API_KEY` | - | 是 (若使用 Azure) | Azure OpenAI 服務的 API Key。 |
| `AZURE_OPENAI_ENDPOINT` | - | 是 (若使用 Azure) | Azure OpenAI 的 Endpoint URL (例如 `https://<resource>.openai.azure.com`)。 |
| `AZURE_OPENAI_API_VERSION` | `2024-12-01-preview` | 否 | 指定使用的 API 版本。 |
| **其他 API Keys** | | | |
| `OPENAI_API_KEY` | - | 否 | 若使用 OpenAI 官方 API 則為必填。 |
| `HF_TOKEN` | - | 否 | Hugging Face Token，用於存取特定模型或數據集。 |
| `USPTO_API_KEY` | - | 否 | 若需使用 USPTO 專利檢索工具則為必填。 |
| **MCP 服務設定** | | | |
| `USPTO_MCP_SERVER_HOST` | `http://0.0.0.0:7000` | 否 | 指定 MCP Server 的監聽位址與埠號。 |

## 3. 安裝與部署 (Installation & Deployment)

本專案支援 Python 本機安裝與 Kubernetes 叢集部署。

### 3.1 Python 本機安裝 (Local Installation)

專案包含 `pyproject.toml`，可透過 `pip` 直接安裝：

```bash
# 建議使用虛擬環境
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 安裝 ToolUniverse
pip install tooluniverse

# 或者若在專案根目錄開發
pip install -e .
```

### 3.2 Kubernetes Helm 部署

專案內建 Helm Chart 位於 `k8s_helm/tooluniverse`。請依照以下步驟部署至 Kubernetes 叢集。

**部署前準備**：
確保已建立 Persistent Volume (PV) 或叢集支援動態 Provisioning (StorageClass)，以供 NFS 數據持久化使用。

**Helm 部署指令**：

建立 `custom-values.yaml` 以覆寫預設設定 (建議設定 Service 為 NodePort 並啟用 Persistence)：

```yaml
# custom-values.yaml
service:
  type: NodePort
  nodePort: 31903  # 可依需求調整

persistence:
  enabled: true
  storageClass: "nfs-client" # 請替換為您叢集的 NFS StorageClass 名稱
  size: 10Gi
  mountPath: /app/data

env:
  AZURE_OPENAI_API_KEY: "your-key-here"
  AZURE_OPENAI_ENDPOINT: "https://your-resource.openai.azure.com"
```

執行安裝：

```bash
helm install tooluniverse ./k8s_helm/tooluniverse -f custom-values.yaml
```

## 4. 操作指南 (Operations)

### 4.1 啟動服務

若使用本機安裝，可透過以下指令啟動 MCP Server：

```bash
# 預設監聽 0.0.0.0:7000
tooluniverse-mcp --host 0.0.0.0 --port 7000
```

### 4.2 進階設定：Azure OpenAI 整合

為了確保 ToolUniverse 能正確呼叫 Azure OpenAI 模型，請務必確認以下設定：

1.  **Deployment Name**：在 Azure Portal 中部署模型時，建議將 Deployment Name 設定為與模型名稱一致 (例如 `gpt-4o`)，或在呼叫工具時明確指定 `model` 參數對應您的 Deployment Name。
2.  **API Version**：若遇到 `404 Resource Not Found` 錯誤，通常是因為 `AZURE_OPENAI_API_VERSION` 與該模型支援的版本不符。請參考 Azure 官方文件確認適用版本。

### 4.3 故障排除 (Troubleshooting)

*   **Azure 連線錯誤 (401 Unauthorized)**：
    *   檢查 `AZURE_OPENAI_API_KEY` 是否正確。
    *   確認 `AZURE_OPENAI_ENDPOINT` 格式是否正確 (不應包含 `/openai/...` 路徑)。

*   **Azure 資源找不到 (404 Not Found)**：
    *   檢查 `AZURE_OPENAI_API_VERSION` 是否支援該區域/模型。
    *   確認 Deployment Name 是否正確。

*   **NFS 掛載失敗 (Kubernetes)**：
    *   檢查 PVC 狀態 (`kubectl get pvc`) 是否為 `Bound`。
    *   確認 StorageClass 是否存在且支援 NFS。
    *   檢查 Pod Events (`kubectl describe pod <pod-name>`) 查看 Mount 錯誤訊息。

*   **Python 套件相依性問題**：
    *   若遇到 `ModuleNotFoundError`，請確認是否已執行 `pip install tooluniverse`。
    *   部分科學工具可能需要額外的系統套件 (如 `libxrender1`)，請參考 `eval/Dockerfile` 中的 `apt-get install` 列表進行補安裝。

## 5. 範例與截圖 (Examples)

### 5.1 Azure OpenAI 模型列表測試

您可以使用 `examples/azure_openai_models_example.py` 來測試 Azure OpenAI 連線與模型列表：

> [圖片說明：此處應顯示執行 azure_openai_models_example.py 後，終端機列出 Azure OpenAI Deployments 的截圖，包含 Deployment Name, Model Name 與 Status]

**範例程式碼片段**：

```python
# 讀取環境變數
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_key = os.getenv("AZURE_OPENAI_API_KEY")

# 初始化 Azure OpenAI Client
client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=api_key,
    api_version="2024-12-01-preview",
)

# 列出模型
resp = client.models.list()
for m in resp:
    print(f"Model: {m.id}, Created: {m.created}")
```
