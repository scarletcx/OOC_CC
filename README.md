要同时监听多个智能合约，你需要在子图配置文件 (`subgraph.yaml`) 中为每个智能合约添加一个 `dataSource` 条目，并在 `schema.graphql` 和 `mapping.ts` 文件中相应地添加处理逻辑。以下是一个示例项目结构和配置，展示如何同时监听多个智能合约。

### 项目结构

```
flask_graph_project/
│
├── app.py
├── requirements.txt
├── subgraph/
│   ├── subgraph.yaml
│   ├── schema.graphql
│   ├── src/
│   │   └── mapping.ts
│   └── abis/
│       ├── ContractA.json
│       └── ContractB.json
└── README.md
```

### 1. `app.py`

```python
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

SUBGRAPH_URL = 'https://api.thegraph.com/subgraphs/name/YOUR_GITHUB_USERNAME/YOUR_SUBGRAPH_NAME'

def query_subgraph(query):
    response = requests.post(SUBGRAPH_URL, json={'query': query})
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Query failed with status code {response.status_code}: {response.text}")

@app.route('/')
def index():
    query = """
    {
      entitiesA(first: 5) {
        id
        value
        description
      }
      entitiesB(first: 5) {
        id
        amount
        detail
      }
    }
    """
    result = query_subgraph(query)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### 2. `requirements.txt`

```
Flask
requests
```

### 3. `subgraph/subgraph.yaml`

```yaml
specVersion: 0.0.2
description: Example subgraph for multiple contracts
repository: https://github.com/YOUR_GITHUB_USERNAME/YOUR_SUBGRAPH_NAME
schema:
  file: ./schema.graphql
dataSources:
  - kind: ethereum/contract
    name: ContractA
    network: mainnet
    source:
      address: "0xContractAAddress"
      abi: ContractA
      startBlock: 12345678
    mapping:
      kind: ethereum/events
      apiVersion: 0.0.5
      language: wasm/assemblyscript
      entities:
        - EntityA
      abis:
        - name: ContractA
          file: ./abis/ContractA.json
      eventHandlers:
        - event: EventA(indexed uint256, string)
          handler: handleEventA
      file: ./src/mapping.ts

  - kind: ethereum/contract
    name: ContractB
    network: mainnet
    source:
      address: "0xContractBAddress"
      abi: ContractB
      startBlock: 12345678
    mapping:
      kind: ethereum/events
      apiVersion: 0.0.5
      language: wasm/assemblyscript
      entities:
        - EntityB
      abis:
        - name: ContractB
          file: ./abis/ContractB.json
      eventHandlers:
        - event: EventB(indexed uint256, string)
          handler: handleEventB
      file: ./src/mapping.ts
```

### 4. `subgraph/schema.graphql`

```graphql
type EntityA @entity {
  id: ID!
  value: BigInt!
  description: String!
}

type EntityB @entity {
  id: ID!
  amount: BigInt!
  detail: String!
}
```

### 5. `subgraph/src/mapping.ts`

```typescript
import { EventA } from "../generated/ContractA/ContractA"
import { EventB } from "../generated/ContractB/ContractB"
import { EntityA, EntityB } from "../generated/schema"

export function handleEventA(event: EventA): void {
  let entity = new EntityA(event.transaction.hash.toHex())
  entity.value = event.params.value
  entity.description = event.params.description
  entity.save()
}

export function handleEventB(event: EventB): void {
  let entity = new EntityB(event.transaction.hash.toHex())
  entity.amount = event.params.amount
  entity.detail = event.params.detail
  entity.save()
}
```

### 6. `subgraph/abis/ContractA.json`

假设你从 Etherscan 或其他来源获取了这个文件。

```json
[
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "name": "value",
        "type": "uint256"
      },
      {
        "indexed": false,
        "name": "description",
        "type": "string"
      }
    ],
    "name": "EventA",
    "type": "event"
  }
]
```

### 7. `subgraph/abis/ContractB.json`

同样地，假设你从 Etherscan 或其他来源获取了这个文件。

```json
[
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "name": "amount",
        "type": "uint256"
      },
      {
        "indexed": false,
        "name": "detail",
        "type": "string"
      }
    ],
    "name": "EventB",
    "type": "event"
  }
]
```

### 8. `README.md`

```markdown
# Flask Graph Project

This project demonstrates how to use Flask with The Graph to listen to and query smart contract events from multiple contracts.

## Setup

1. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2. Configure and deploy the subgraph:
    ```bash
    cd subgraph
    graph auth https://api.thegraph.com/deploy/ YOUR_DEPLOY_KEY
    graph codegen
    graph build
    graph deploy --node https://api.thegraph.com/deploy/ YOUR_GITHUB_USERNAME/YOUR_SUBGRAPH_NAME
    ```

3. Run the Flask application:
    ```bash
    python app.py
    ```

Replace `YOUR_GITHUB_USERNAME`, `YOUR_SUBGRAPH_NAME`, `YOUR_CONTRACT_ADDRESS`, and `YOUR_DEPLOY_KEY` with your actual values.
```

### 替换内容

- `YOUR_GITHUB_USERNAME`: 替换为你的 GitHub 用户名。
- `YOUR_SUBGRAPH_NAME`: 替换为你希望为子图命名的名称。
- `0xContractAAddress` 和 `0xContractBAddress`: 替换为你要监听的智能合约地址。
- `YOUR_DEPLOY_KEY`: 替换为你的 The Graph 部署密钥。
- `EventA` 和 `EventB`: 替换为你要监听的智能合约事件名称。
- `12345678`: 替换为你的智能合约开始部署的区块号。
- `entitiesA`, `entitiesB`, `value`, `description`, `amount`, 和 `detail`: 替换为你在 `schema.graphql` 文件中定义的实体和字段名称。

### 运行项目

1. 安装依赖：
    ```bash
    pip install -r requirements.txt
    ```

2. 配置并部署子图：
    ```bash
    cd subgraph
    graph auth https://api.thegraph.com/deploy/ YOUR_DEPLOY_KEY
    graph codegen
    graph build
    graph deploy --node https://api.thegraph.com/deploy/ YOUR_GITHUB_USERNAME/YOUR_SUBGRAPH_NAME
    ```

3. 运行 Flask 应用：
    ```bash
    python app.py
    ```

通过这些步骤，你就可以在本地运行一个完整的 Flask 项目，并通过 The Graph 监听和查询多个智能合约事件。