# ToolUniverse 使用說明

**文件版本**：v1.0  
**適用對象**：DevOps 工程師、系統管理員、技術維護人員

---

## 1. 簡介

### 1.1 專案概述

ToolUniverse 是一個自動化科學研究系統，提供標準化的 AI-Tool Interaction Protocol，整合超過 600 個科學工具，涵蓋：

- **科學資料庫**：UniProt、ChEMBL、OpenTargets、PubChem、FDA 等
- **機器學習模型**：蛋白質結構預測、藥物性質預測等
- **文獻搜尋**：PubMed、Europe PMC、Semantic Scholar
- **臨床資料**：臨床試驗、FDA 藥物標籤、不良事件

### 1.2 系統架構

```
┌────────────────────┐
│  AI Agents/LLMs    │  ← Claude Desktop, ChatGPT, Gemini 等
└──────────┬─────────┘
           │ MCP / Python API
┌──────────▼─────────┐
│  ToolUniverse Core │  ← 工具載入、註冊、路由、執行
└──────────┬─────────┘
           │ Registry/Config
┌──────────▼─────────┐
│  Tool Implementation│  ← 600+ 科學工具實作
└──────────┬─────────┘
           │ HTTP/GraphQL/Local
┌──────────▼─────────┐
│ External Services  │  ← 外部資料庫與 API
└────────────────────┘
```

### 1.3 主要功能

- **統一介面**：所有工具使用標準化的 AI-Tool Interaction Protocol
- **智能工具發現**：支援關鍵字、LLM 語義、嵌入向量三種搜尋方式
- **工具組合**：支援工具串接與科學工作流設計
- **多模型支援**：支援 GPT、Claude、Gemini、Qwen、DeepSeek 等主流 LLM
- **MCP 整合**：完整支援 Model Context Protocol，可與 Claude Desktop 等工具整合

---

## 2. 環境變數詳解 (Environment Variables)

### 2.1 LLM 整合相關環境變數

#### Azure OpenAI 配置

| 變數名稱 | 預設值 | 必填 | 說明 |
|---------|--------|------|------|
| `AZURE_OPENAI_API_KEY` | - | ✅ | Azure OpenAI 服務的 API 金鑰 |
| `AZURE_OPENAI_ENDPOINT` | `https://azure-ai.hms.edu` | ⚠️ | Azure OpenAI 服務端點 URL（格式：`https://<resource-name>.openai.azure.com`） |
| `AZURE_OPENAI_API_VERSION` | `2024-12-01-preview` | ⚠️ | Azure OpenAI API 版本（建議使用最新版本） |
| `AZURE_OPENAI_API_VERSION_BY_MODEL` | - | ⚠️ | JSON 格式，依模型指定 API 版本（例：`{"gpt-4o": "2024-12-01-preview"}`） |
| `AZURE_DEFAULT_MODEL_LIMITS` | - | ⚠️ | JSON 格式，設定模型的最大輸出與上下文視窗限制 |
| `AZURE_MAX_TOKENS_BY_MODEL` | - | ⚠️ | JSON 格式，依模型設定最大 token 數 |

**Azure OpenAI 部署名稱（Deployment Name）**：
- 部署名稱需在工具配置中指定，而非環境變數
- 在 AgenticTool 的 `configs` 中設定 `model_id`，對應 Azure 中的 Deployment Name

#### OpenRouter 配置

| 變數名稱 | 預設值 | 必填 | 說明 |
|---------|--------|------|------|
| `OPENROUTER_API_KEY` | - | ✅ | OpenRouter API 金鑰（用於存取 100+ 模型） |
| `OPENROUTER_SITE_URL` | - | ⚠️ | 網站 URL（用於使用追蹤與歸屬） |
| `OPENROUTER_SITE_NAME` | - | ⚠️ | 應用程式名稱（用於使用追蹤與歸屬） |

#### Google Gemini 配置

| 變數名稱 | 預設值 | 必填 | 說明 |
|---------|--------|------|------|
| `GEMINI_API_KEY` | - | ✅ | Google Gemini API 金鑰 |

#### VLLM 配置

| 變數名稱 | 預設值 | 必填 | 說明 |
|---------|--------|------|------|
| `VLLM_SERVER_URL` | - | ✅ | VLLM 伺服器 URL（例：`http://localhost:8000/v1`） |

#### OpenAI（非 Azure）配置

| 變數名稱 | 預設值 | 必填 | 說明 |
|---------|--------|------|------|
| `OPENAI_API_KEY` | - | ⚠️ | OpenAI API 金鑰（用於 EmbeddingDatabase 等工具） |
| `OPENAI_BASE_URL` | `https://api.openai.com/v1` | ⚠️ | OpenAI API 基礎 URL |

### 2.2 工具相關環境變數

| 變數名稱 | 預設值 | 必填 | 說明 |
|---------|--------|------|------|
| `OPENTARGETS_API_KEY` | - | ⚠️ | OpenTargets 平台 API 金鑰（增強功能） |
| `USPTO_API_KEY` | - | ⚠️ | USPTO（美國專利商標局）API 金鑰 |
| `NCBI_API_KEY` | - | ⚠️ | NCBI API 金鑰 |
| `FDA_API_KEY` | - | ⚠️ | FDA API 金鑰 |

### 2.3 系統配置環境變數

| 變數名稱 | 預設值 | 必填 | 說明 |
|---------|--------|------|------|
| `TOOLUNIVERSE_CACHE_DIR` | - | ⚠️ | 快取目錄路徑（用於結果快取） |
| `TOOLUNIVERSE_TMPDIR` | - | ⚠️ | 臨時檔案目錄路徑 |
| `TOOLUNIVERSE_LIGHT_IMPORT` | `false` | ⚠️ | 啟用輕量級匯入模式（減少啟動時間） |
| `PLAYWRIGHT_SKIP_BROWSER_INSTALL` | - | ⚠️ | 跳過 Playwright 瀏覽器安裝（用於容器環境） |

### 2.4 遠端工具環境變數

| 變數名稱 | 預設值 | 必填 | 說明 |
|---------|--------|------|------|
| `TRANSCRIPTFORMER_DATA_PATH` | `/root/PrismDB` | ⚠️ | Transcriptformer 資料路徑 |
| `PINNACLE_DATA_PATH` | - | ⚠️ | Pinnacle 資料路徑 |
| `COMPASS_MODEL_PATH` | - | ⚠️ | Compass 模型路徑 |
| `DEPMAP_DATA_PATH` | - | ⚠️ | DepMap 資料路徑 |
| `EXPERT_FEEDBACK_MCP_SERVER_URL` | - | ⚠️ | Expert Feedback MCP 伺服器 URL |
| `EXPERT_FEEDBACK_API_HOST` | `localhost` | ⚠️ | Expert Feedback API 主機 |
| `EXPERT_FEEDBACK_API_PORT` | `9877` | ⚠️ | Expert Feedback API 端口 |

### 2.5 環境變數設定範例

```bash
# Azure OpenAI 配置
export AZURE_OPENAI_API_KEY="your-azure-api-key"
export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com"
export AZURE_OPENAI_API_VERSION="2024-12-01-preview"

# OpenRouter 配置（替代方案）
export OPENROUTER_API_KEY="your-openrouter-api-key"

# 工具 API 金鑰
export OPENTARGETS_API_KEY="your-opentargets-key"
export USPTO_API_KEY="your-uspto-key"
export NCBI_API_KEY="your-ncbi-key"

# 系統配置
export TOOLUNIVERSE_CACHE_DIR="/var/cache/tooluniverse"
export TOOLUNIVERSE_TMPDIR="/tmp/tooluniverse"
```

---

## 3. 安裝與部署 (Installation & Deployment)

### 3.1 本機安裝（Python 套件）

#### 前置需求

- Python 3.10 或更高版本
- pip 或 uv（推薦使用 uv）

#### 使用 pip 安裝

```bash
# 基本安裝
pip install tooluniverse

# 安裝包含開發工具
pip install "tooluniverse[dev]"

# 安裝包含嵌入功能（需要 GPU）
pip install "tooluniverse[embedding]"

# 安裝所有選用功能
pip install "tooluniverse[all]"
```

#### 使用 uv 安裝（推薦）

```bash
# 基本安裝
uv pip install tooluniverse

# 安裝包含開發工具
uv add "tooluniverse[dev]"

# 安裝包含嵌入功能
uv add "tooluniverse[embedding]"

# 安裝所有選用功能
uv add "tooluniverse[all]"
```

#### 驗證安裝

```python
import tooluniverse
print(f"ToolUniverse version: {tooluniverse.__version__}")
print("✅ Installation successful!")
```

### 3.2 Docker 容器化部署

#### 使用 Dockerfile 建置

專案根目錄包含 `Dockerfile`，可建置容器映像：

```bash
# 建置映像
docker build -t tooluniverse:latest .

# 執行容器
docker run -d \
  --name tooluniverse \
  -p 7000:7000 \
  -e AZURE_OPENAI_API_KEY="your-key" \
  -e AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com" \
  -v $(pwd)/data:/app/data \
  tooluniverse:latest
```

#### 使用 docker-compose 部署

專案包含 `docker-compose.yml` 配置檔：

```bash
# 設定環境變數
export OPENAI_API_KEY="your-openai-key"
export USPTO_API_KEY="your-uspto-key"

# 啟動服務
docker-compose up -d

# 查看日誌
docker-compose logs -f

# 停止服務
docker-compose down
```

**docker-compose.yml 配置說明**：
- 服務名稱：`tooluniverse`
- 容器端口映射：`31903:7000`（主機端口:容器端口）
- 資料卷掛載：`./data:/app/data`
- 環境變數：`OPENTARGETS_API_KEY`、`NCBI_API_KEY`

### 3.3 Kubernetes Helm 部署

#### 前置需求

- Kubernetes 1.19 或更高版本
- Helm 3.0 或更高版本
- NFS 伺服器（用於持久化儲存，可選）

#### 基本安裝

```bash
# 進入 Helm Chart 目錄
cd k8s_helm/tooluniverse

# 使用預設值安裝
helm install tooluniverse ./
```

#### 使用自訂值安裝

建立 `custom-values.yaml`：

```yaml
# custom-values.yaml
replicaCount: 2

image:
  repository: tooluniverse
  tag: "latest"

service:
  type: NodePort
  port: 7000
  nodePort: 31903

env:
  AZURE_OPENAI_API_KEY: "your-azure-api-key"
  AZURE_OPENAI_ENDPOINT: "https://your-resource.openai.azure.com"
  AZURE_OPENAI_API_VERSION: "2024-12-01-preview"
  OPENTARGETS_API_KEY: "your-opentargets-key"
  NCBI_API_KEY: "your-ncbi-key"

persistence:
  enabled: true
  storageClass: "nfs-client"  # 使用 NFS StorageClass
  accessMode: ReadWriteMany
  size: 10Gi
  mountPath: /app/data
```

安裝：

```bash
helm install tooluniverse ./ -f custom-values.yaml
```

#### NFS Persistent Volume 配置範例

若需使用 NFS 作為持久化儲存，需先建立 StorageClass：

```yaml
# nfs-storageclass.yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: nfs-client
provisioner: k8s-sigs.io/nfs-subdir-external-provisioner
parameters:
  archiveOnDelete: "false"
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: tooluniverse-nfs-pvc
spec:
  storageClassName: nfs-client
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 10Gi
```

套用配置：

```bash
kubectl apply -f nfs-storageclass.yaml
```

然後在 `custom-values.yaml` 中指定：

```yaml
persistence:
  enabled: true
  storageClass: "nfs-client"
  accessMode: ReadWriteMany
  size: 10Gi
```

#### 使用 Secret 管理敏感資訊

建立 Secret：

```bash
kubectl create secret generic tooluniverse-secrets \
  --from-literal=azure-openai-api-key="your-azure-key" \
  --from-literal=azure-openai-endpoint="https://your-resource.openai.azure.com" \
  --from-literal=opentargets-api-key="your-opentargets-key"
```

修改 `deployment.yaml` 模板以使用 Secret（需手動編輯）：

```yaml
env:
  - name: AZURE_OPENAI_API_KEY
    valueFrom:
      secretKeyRef:
        name: tooluniverse-secrets
        key: azure-openai-api-key
  - name: AZURE_OPENAI_ENDPOINT
    valueFrom:
      secretKeyRef:
        name: tooluniverse-secrets
        key: azure-openai-endpoint
```

#### 升級與卸載

```bash
# 升級部署
helm upgrade tooluniverse ./ -f custom-values.yaml

# 查看部署狀態
helm status tooluniverse

# 卸載
helm uninstall tooluniverse
```

#### 存取應用程式

**使用 NodePort**（預設配置）：

```bash
# 取得節點 IP 與 NodePort
kubectl get nodes -o wide
kubectl get svc tooluniverse

# 存取：http://<NODE_IP>:31903
```

**使用 Port Forward**：

```bash
kubectl port-forward svc/tooluniverse 7000:7000

# 存取：http://localhost:7000
```

---

## 4. 操作指南 (Operations)

### 4.1 基本操作

#### 啟動 MCP 伺服器

**使用命令列工具**：

```bash
# 基本啟動（HTTP 模式，端口 7000）
tooluniverse-smcp

# 指定端口與主機
tooluniverse-smcp --port 8000 --host 0.0.0.0

# 使用 stdio 模式（適用於 Claude Desktop）
tooluniverse-smcp --transport stdio

# 僅載入特定工具類別
tooluniverse-smcp --categories uniprot ChEMBL opentarget --port 7000

# 排除特定工具
tooluniverse-smcp --exclude-tools "ChEMBL_get_molecule_by_chembl_id" --port 7000

# 啟用詳細日誌
tooluniverse-smcp --verbose --port 7000
```

**使用 Python 模組**：

```bash
python -m tooluniverse.smcp_server
```

#### Python SDK 基本使用

```python
from tooluniverse import ToolUniverse

# 初始化並載入工具
tu = ToolUniverse()
tu.load_tools()  # 載入 600+ 工具

# 搜尋工具
tools = tu.run({
    "name": "Tool_Finder_Keyword",
    "arguments": {"description": "protein structure prediction", "limit": 10}
})

# 執行工具
result = tu.run({
    "name": "UniProt_get_function_by_accession",
    "arguments": {"accession": "P05067"}
})

print(result)
```

#### 工具發現範例

```python
from tooluniverse import ToolUniverse

tu = ToolUniverse()
tu.load_tools()

# 方式一：關鍵字搜尋（最快）
tools = tu.run({
    "name": "Tool_Finder_Keyword",
    "arguments": {"description": "disease target associations", "limit": 10}
})

# 方式二：LLM 語義搜尋（需配置 LLM）
tools = tu.run({
    "name": "Tool_Finder_LLM",
    "arguments": {"description": "Find tools for analyzing protein-protein interactions", "limit": 5}
})

# 方式三：嵌入向量搜尋（需 GPU）
tools = tu.run({
    "name": "Tool_Finder",
    "arguments": {"description": "drug discovery", "limit": 10}
})
```

### 4.2 進階設定（LLM Integration）

#### Azure OpenAI 整合設定

**步驟 1：設定環境變數**

```bash
export AZURE_OPENAI_API_KEY="your-azure-api-key"
export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com"
export AZURE_OPENAI_API_VERSION="2024-12-01-preview"
```

**步驟 2：在工具配置中指定 Deployment Name**

在 AgenticTool 的配置中，`model_id` 需對應 Azure 中的 Deployment Name：

```python
tool_config = {
    "type": "AgenticTool",
    "name": "MyAnalysisTool",
    "configs": {
        "api_type": "CHATGPT",  # 使用 Azure OpenAI
        "model_id": "gpt-4o",  # 對應 Azure 中的 Deployment Name
        "temperature": 0.7,
        "max_new_tokens": 1024
    }
}
```

**步驟 3：依模型指定 API 版本**

若不同模型使用不同 API 版本：

```bash
export AZURE_OPENAI_API_VERSION_BY_MODEL='{"gpt-4o": "2024-12-01-preview", "gpt-4.1": "2024-11-20-preview"}'
```

**步驟 4：設定模型限制**

```bash
export AZURE_DEFAULT_MODEL_LIMITS='{"gpt-4o": {"max_output": 16384, "context_window": 128000}}'
```

#### OpenRouter 整合設定

```bash
export OPENROUTER_API_KEY="your-openrouter-api-key"
export OPENROUTER_SITE_URL="https://your-site.com"
export OPENROUTER_SITE_NAME="ToolUniverse Application"
```

在工具配置中使用：

```python
tool_config = {
    "type": "AgenticTool",
    "configs": {
        "api_type": "OPENROUTER",
        "model_id": "openai/gpt-4o",  # OpenRouter 模型 ID
        "temperature": 0.7
    }
}
```

#### Gemini 整合設定

```bash
export GEMINI_API_KEY="your-gemini-api-key"
```

在工具配置中使用：

```python
tool_config = {
    "type": "AgenticTool",
    "configs": {
        "api_type": "GEMINI",
        "model_id": "gemini-2.0-flash",
        "temperature": 0.7
    }
}
```

### 4.3 故障排除 (Troubleshooting)

#### Azure OpenAI 連線錯誤

**錯誤：401 Unauthorized**

- 檢查 `AZURE_OPENAI_API_KEY` 是否正確設定
- 確認 API 金鑰未過期
- 驗證金鑰權限是否包含所需模型

**錯誤：404 Not Found**

- 檢查 `AZURE_OPENAI_ENDPOINT` 是否正確（格式：`https://<resource-name>.openai.azure.com`）
- 確認 Deployment Name 在 Azure 中是否存在
- 驗證 `AZURE_OPENAI_API_VERSION` 是否支援該模型

**錯誤：模型不存在**

- 確認 Deployment Name 與 Azure 中的部署名稱完全一致（區分大小寫）
- 檢查模型是否已正確部署到 Azure OpenAI 資源

**除錯步驟**：

```bash
# 測試 Azure OpenAI 連線
python -c "
from openai import AzureOpenAI
import os

client = AzureOpenAI(
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT'),
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
    api_version=os.getenv('AZURE_OPENAI_API_VERSION', '2024-12-01-preview')
)

# 列出可用模型
models = client.models.list()
for model in models:
    print(model.id)
"
```

#### NFS 掛載失敗

**錯誤：無法掛載 NFS 卷**

- 確認 NFS 伺服器可從 Kubernetes 節點存取
- 檢查 NFS 伺服器路徑是否正確
- 驗證 StorageClass 配置是否正確

**除錯步驟**：

```bash
# 檢查 PVC 狀態
kubectl get pvc

# 查看 PVC 詳細資訊
kubectl describe pvc tooluniverse-nfs-pvc

# 檢查 Pod 中的掛載狀態
kubectl exec -it <pod-name> -- df -h

# 測試 NFS 連線（在節點上）
showmount -e <nfs-server-ip>
```

#### Python 套件相依性問題

**錯誤：ModuleNotFoundError**

- 確認已安裝所有必要套件：`pip install tooluniverse[all]`
- 檢查 Python 版本是否符合需求（≥3.10）
- 驗證虛擬環境是否正確啟用

**錯誤：版本衝突**

```bash
# 使用 uv 管理依賴（推薦）
uv pip install tooluniverse

# 或建立新的虛擬環境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
pip install tooluniverse
```

#### MCP 伺服器無法啟動

**錯誤：端口已被佔用**

```bash
# 檢查端口使用情況
lsof -i :7000  # Linux/Mac
netstat -ano | findstr :7000  # Windows

# 使用不同端口
tooluniverse-smcp --port 8000
```

**錯誤：工具載入失敗**

```bash
# 啟用詳細日誌
tooluniverse-smcp --verbose --port 7000

# 僅載入特定類別進行測試
tooluniverse-smcp --categories uniprot --port 7000
```

#### 記憶體不足

**錯誤：OOMKilled（Kubernetes）**

調整資源限制：

```yaml
# custom-values.yaml
resources:
  limits:
    memory: 4Gi
    cpu: 2
  requests:
    memory: 2Gi
    cpu: 1
```

#### 工具執行超時

增加超時設定或檢查網路連線：

```python
from tooluniverse import ToolUniverse

tu = ToolUniverse()
tu.load_tools()

# 設定超時（如工具支援）
result = tu.run({
    "name": "some_tool",
    "arguments": {...},
    "timeout": 300  # 5 分鐘
})
```

---

## 5. 範例與截圖 (Examples)

### 5.1 基本工具查詢範例

**輸入**：

```python
from tooluniverse import ToolUniverse

tu = ToolUniverse()
tu.load_tools()

# 查詢與疾病相關的工具
tools = tu.run({
    "name": "Tool_Finder_Keyword",
    "arguments": {"description": "disease target associations", "limit": 10}
})

print(f"找到 {len(tools['data'])} 個工具")
for tool in tools['data']:
    print(f"- {tool['name']}: {tool['description']}")
```

**預期輸出**：

```
找到 10 個工具
- OpenTargets_get_associated_targets_by_disease_efoId: Get targets associated with a disease
- OpenTargets_get_associated_drugs_by_target_ensemblID: Get drugs associated with a target
- OpenTargets_get_disease_info_by_efoId: Get disease information by EFO ID
...
```

> [圖片說明：此處應顯示工具搜尋結果的終端機輸出截圖]

### 5.2 UniProt 蛋白質查詢範例

**輸入**：

```python
result = tu.run({
    "name": "UniProt_get_function_by_accession",
    "arguments": {"accession": "P05067"}
})

print(result)
```

**預期輸出**：

```json
{
  "data": {
    "accession": "P05067",
    "function": "Functions as a cell surface receptor and performs physiological functions on the surface of neurons in the central nervous system...",
    "protein_name": "Amyloid-beta A4 protein"
  }
}
```

> [圖片說明：此處應顯示 UniProt 查詢結果的 JSON 輸出截圖]

### 5.3 工具組合工作流範例

**輸入**：

```python
# 步驟 1：查詢疾病相關的目標
targets = tu.run({
    "name": "OpenTargets_get_associated_targets_by_disease_efoId",
    "arguments": {"efoId": "EFO_0000537"}  # 高血壓
})

# 步驟 2：對每個目標查詢相關藥物
if targets['data'] and 'rows' in targets['data']:
    first_target = targets['data']['rows'][0]
    target_id = first_target.get('target', {}).get('id')
    
    if target_id:
        drugs = tu.run({
            "name": "OpenTargets_get_associated_drugs_by_target_ensemblID",
            "arguments": {"ensemblId": target_id}
        })
        print(f"目標 {target_id} 的相關藥物：")
        print(drugs)
```

**預期輸出**：

```
目標 ENSG00000130208 的相關藥物：
{
  "data": {
    "rows": [
      {
        "drug": {
          "id": "CHEMBL25",
          "name": "Losartan"
        },
        "association_score": 0.95
      },
      ...
    ]
  }
}
```

> [圖片說明：此處應顯示工具組合工作流的執行流程截圖]

### 5.4 MCP 伺服器啟動範例

**啟動命令**：

```bash
tooluniverse-smcp --port 7000 --verbose
```

**預期輸出**：

```
🚀 Starting ToolUniverse SMCP Server...
📦 Loading tools...
✅ Loaded 356 tools from 8 categories
🔍 ToolFinderLLM (cost-optimized) available for advanced search
🌐 Server running on http://0.0.0.0:7000
📡 MCP endpoint: http://0.0.0.0:7000/mcp
```

> [圖片說明：此處應顯示 MCP 伺服器啟動成功的終端機輸出截圖]

### 5.5 Kubernetes 部署狀態檢查

**檢查命令**：

```bash
kubectl get pods,svc,pvc -l app=tooluniverse
```

**預期輸出**：

```
NAME                              READY   STATUS    RESTARTS   AGE
pod/tooluniverse-7d8f9c4b5-abc12  1/1     Running   0          5m

NAME                     TYPE       CLUSTER-IP    EXTERNAL-IP   PORT(S)          AGE
service/tooluniverse     NodePort   10.96.1.100   <none>        7000:31903/TCP   5m

NAME                                    STATUS   VOLUME   CAPACITY   ACCESS MODES   STORAGECLASS   AGE
persistentvolumeclaim/tooluniverse-data Bound    pvc-xxx  10Gi       RWO            nfs-client     5m
```

> [圖片說明：此處應顯示 Kubernetes 資源狀態的 kubectl 輸出截圖]

### 5.6 Azure OpenAI 整合測試

**測試腳本**：

```python
import os
from tooluniverse.llm_clients import AzureOpenAIClient
from tooluniverse.logging_config import get_logger

logger = get_logger(__name__)

# 初始化 Azure OpenAI 客戶端
client = AzureOpenAIClient(
    model_id="gpt-4o",  # 對應 Azure Deployment Name
    api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview"),
    logger=logger
)

# 測試 API 連線
try:
    client.test_api()
    print("✅ Azure OpenAI 連線成功")
except Exception as e:
    print(f"❌ Azure OpenAI 連線失敗: {e}")
```

**預期輸出**：

```
✅ Azure OpenAI 連線成功
```

> [圖片說明：此處應顯示 Azure OpenAI 連線測試成功的輸出截圖]

---

## 附錄

### A. 常用命令速查

```bash
# 安裝
pip install tooluniverse
uv pip install tooluniverse

# 啟動 MCP 伺服器
tooluniverse-smcp --port 7000
tooluniverse-smcp --transport stdio  # Claude Desktop

# Docker
docker-compose up -d
docker-compose logs -f

# Kubernetes
helm install tooluniverse ./k8s_helm/tooluniverse
helm upgrade tooluniverse ./k8s_helm/tooluniverse
kubectl port-forward svc/tooluniverse 7000:7000
```

### B. 相關資源

- **官方文件**：https://zitniklab.hms.harvard.edu/ToolUniverse/
- **GitHub 倉庫**：https://github.com/mims-harvard/ToolUniverse
- **Slack 社群**：https://join.slack.com/t/tooluniversehq/shared_invite/zt-3dic3eoio-5xxoJch7TLNibNQn5_AREQ
- **工具清單**：https://zitniklab.hms.harvard.edu/ToolUniverse/tools/tools_config_index.html

### C. 支援與回報問題

- **GitHub Issues**：https://github.com/mims-harvard/ToolUniverse/issues
- **聯絡方式**：shanghuagao@gmail.com

---

**文件結束**

