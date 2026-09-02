# 虚拟币行情分析演示系统

> ⚠ **重要声明**：本项目仅用于**技术学习演示**。所有行情数据、技术分析、AI预测结果均为**模拟生成**，**绝对不构成任何投资建议**。我国不承认虚拟货币的法定地位，禁止虚拟货币交易行为。请遵守当地法律法规。

---

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | Vue 3 (Composition API) + Element Plus + Chart.js (K线/走势图) |
| 后端 | Python FastAPI + SQLAlchemy + SQLite |

## 项目结构

`
├── backend/
│   ├── main.py              # FastAPI 入口
│   ├── database.py           # SQLite 数据库配置
│   ├── models.py             # 数据模型
│   ├── simulated_data.py     # 模拟数据生成 & AI分析
│   ├── routes.py             # API 路由
│   └── requirements.txt      # Python 依赖
├── frontend/
│   ├── package.json
│   ├── vite.config.js
│   ├── index.html
│   └── src/
│       ├── main.js
│       ├── App.vue
│       ├── styles/global.css     # 深色科技风全局样式
│       ├── utils/api.js          # API 封装
│       ├── views/Dashboard.vue   # 主页面
│       └── components/
│           ├── RiskWarning.vue   # 风险提示栏
│           ├── CoinSelector.vue  # 币种选择器
│           ├── KLineChart.vue    # K线图 (Chart.js Financial)
│           ├── PriceChart.vue    # 价格走势图
│           ├── NewsInput.vue     # 新闻输入框
│           └── AIAnalysisPanel.vue  # AI分析结果展示
└── README.md
`

## 快速启动

### 1. 启动后端

`ash
# 进入后端目录
cd backend

# 安装依赖
pip install -r requirements.txt

# 启动服务 (默认端口 8000)
uvicorn main:app --reload --host 0.0.0.0 --port 8000
`

启动后访问 http://127.0.0.1:8000/docs 可查看 API 文档。

### 2. 启动前端

`ash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器 (默认端口 5173)
npm run dev
`

启动后访问 http://localhost:5173 即可使用。

> 前端开发服务器已配置代理，/api 请求会自动转发到后端 http://127.0.0.1:8000。

## 接口说明

### GET /api/coins
获取支持的币种列表。

### GET /api/history/{coin}?days=90
获取模拟历史行情数据（K线 OHLCV）。

### POST /api/analyze
提交新闻文本进行模拟AI分析。

**请求体：**
`json
{
  "coin": "BTC",
  "news": "某机构宣布推出比特币ETF..."
}
`

**返回包含：** 当前价格、趋势、RSI、情绪分析、模拟预测、支撑/阻力位、综合评述。

## 功能说明

- **K线图**：支持 7/30/90/365 天时间范围切换，使用 Chart.js Financial 插件渲染
- **价格走势图**：闭合曲线填充，涨绿跌红
- **模拟AI分析**：基于新闻关键词情绪打分 + 近期技术指标（RSI、MA），生成综合评述
- 所有数据均为纯模拟生成，随机种子每次不同

## 免责声明

**本项目及所有输出内容均为模拟推演，不能作为交易依据。**
虚拟货币交易在我国不受法律保护，请勿参与任何形式的虚拟货币交易活动。
