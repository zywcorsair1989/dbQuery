# 数据库 SQL/命令生成工具 - 完整使用说明书

## 一、项目简介

本项目是一个基于大模型的数据库查询语句生成工具，由于前端开发人员和移动端开发人员，对于sql语句不是很熟练，以此为需求开发此工具
用户只需输入表结构和自然语言需求，即可自动生成对应的查询语句。

### 支持的数据库类型

| 数据库 | 查询语言 | 说明 |
|--------|---------|------|
| MySQL | SQL | 最流行的开源关系型数据库 |
| SQL Server | SQL | Microsoft 企业级数据库 |
| Oracle | SQL | 企业级商业数据库 |
| SQLite | SQL | 轻量级嵌入式数据库 |
| Redis | Redis命令 | 高性能键值存储数据库 |

---

## 二、环境要求

- Python 3.7+
- 操作系统：Windows / macOS / Linux

---

## 三、安装依赖（导包）

### 方法一：使用 requirements.txt 安装（推荐）

```bash
# 进入项目目录
cd db_query

# 安装所有依赖
pip install -r requirements.txt
```

### 方法二：手动安装核心依赖

```bash
pip install streamlit openai
```

### 注意事项

**openai 包版本问题**：

如果遇到 `ImportError: cannot import name 'OpenAI' from 'openai'` 错误，说明 openai 版本过低。请升级到 1.0+ 版本：

```bash
pip install openai --upgrade
```

或指定版本：

```bash
pip install openai>=1.0.0
```

---

## 四、配置 API 密钥

本项目使用阿里云 DashScope API（通义千问模型）。

### 方式一：设置环境变量（推荐）

**macOS / Linux**：
```bash
export DASHSCOPE_API_KEY="your_api_key_here"
```

**Windows（命令提示符）**：
```cmd
set DASHSCOPE_API_KEY=your_api_key_here
```

**Windows（PowerShell）**：
```powershell
$env:DASHSCOPE_API_KEY="your_api_key_here"
```

### 方式二：创建 .env 文件

在项目目录创建 `.env` 文件：

```env
DASHSCOPE_API_KEY=your_api_key_here
```

### 获取 API 密钥

1. 访问阿里云 DashScope 控制台：https://dashscope.console.aliyun.com/
2. 创建 API Key
3. 复制密钥并替换上述命令中的 `your_api_key_here`

---

## 五、启动应用

### 步骤 1：进入项目目录

```bash
cd db_query
```

### 步骤 2：启动 Streamlit 应用

```bash
streamlit run db_query.py
```

### 步骤 3：访问界面

启动成功后，终端会显示：

```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://xxx.xxx.xxx.xxx:8501
```

浏览器会自动打开，或手动访问 `http://localhost:8501`

---

## 六、使用指南

### 步骤 1：选择数据库类型

在下拉菜单中选择目标数据库类型：
- MySQL
- Redis
- SQL Server
- Oracle
- SQLite

### 步骤 2：输入数据结构数量

输入需要查询涉及的数据结构数量（1-10）：
- SQL数据库：输入表的数量
- Redis：输入 Key 的数量

### 步骤 3：输入数据结构

#### SQL 数据库表结构格式

```sql
表名 (
    字段名 字段类型 约束条件,  -- 字段注释
    ...
);
```

**示例**：
```sql
users (
    id INT PRIMARY KEY NOT NULL,
    name VARCHAR(100) NOT NULL,
    age INT,
    email VARCHAR(100) UNIQUE,
    create_time TIMESTAMP DEFAULT NOW()
);

orders (
    id INT PRIMARY KEY NOT NULL,
    user_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    status INT DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

#### Redis 数据结构格式

```redis
# Hash 类型
key名 -> {字段1: 值1, 字段2: 值2}

# List 类型
key名 -> [元素1, 元素2, 元素3]

# String 类型
key名 -> 值

# Sorted Set 类型
key名 -> {成员1: 分数1, 成员2: 分数2}
```

**示例**：
```redis
user:1 -> {name: "张三", age: 25, email: "zhangsan@example.com"}
user:1:orders -> [order:1, order:2, order:3]
inventory:phone -> 100
user_spending -> {user:1: 13000, user:2: 5000}
```

### 步骤 4：输入查询需求

用自然语言描述查询需求，例如：

| 需求类型 | 示例 |
|---------|------|
| 简单查询 | 查询所有年龄大于18的用户 |
| 条件筛选 | 查询2024年订单金额大于1000的订单 |
| 聚合统计 | 统计每个用户的消费总额 |
| 排序查询 | 查询消费金额最高的前10名用户 |
| 多表关联 | 查询每个用户的订单数量和总金额 |

### 步骤 5：点击提交

点击"提交"按钮，等待大模型生成查询语句。生成结果会显示在页面上。

---

## 七、使用示例

### 示例 1：MySQL 单表查询

| 输入项 | 内容 |
|--------|------|
| 数据库类型 | MySQL |
| 表结构数量 | 1 |
| 表结构 | `users (id INT PRIMARY KEY, name VARCHAR(100), age INT, city VARCHAR(50));` |
| SQL需求 | 查询年龄大于25岁的所有用户 |

**生成结果**：
```sql
SELECT * FROM users WHERE age > 25;
```

---

### 示例 2：MySQL 多表联合查询

| 输入项 | 内容 |
|--------|------|
| 数据库类型 | MySQL |
| 表结构数量 | 3 |
| 表结构1 | `orders (id INT PRIMARY KEY, user_id INT, product_id INT, amount DECIMAL(10,2), order_time TIMESTAMP);` |
| 表结构2 | `users (id INT PRIMARY KEY, name VARCHAR(100), email VARCHAR(100));` |
| 表结构3 | `products (id INT PRIMARY KEY, name VARCHAR(100), price DECIMAL(10,2));` |
| SQL需求 | 查询每个用户的总消费金额，按金额降序排列，只显示前10名 |

**生成结果**：
```sql
SELECT u.name, SUM(o.amount) AS total_amount
FROM orders o
JOIN users u ON o.user_id = u.id
GROUP BY u.id, u.name
ORDER BY total_amount DESC
LIMIT 10;
```

---

### 示例 3：Redis 查询

| 输入项 | 内容 |
|--------|------|
| 数据库类型 | Redis |
| 数据结构数量 | 2 |
| 数据结构1 | `user:1 -> {name: "张三", age: 25, city: "北京"}` |
| 数据结构2 | `user:1:orders -> [order:1, order:2, order:3]` |
| 操作需求 | 获取用户1的所有信息和订单列表 |

**生成结果**：
```redis
HGETALL user:1
LRANGE user:1:orders 0 -1
```

---

### 示例 4：复杂聚合查询

| 输入项 | 内容 |
|--------|------|
| 数据库类型 | MySQL |
| 表结构数量 | 2 |
| 表结构1 | `employees (id INT PRIMARY KEY, name VARCHAR(100), dept_id INT, salary DECIMAL(10,2));` |
| 表结构2 | `departments (id INT PRIMARY KEY, dept_name VARCHAR(100));` |
| SQL需求 | 统计每个部门的平均薪资，只显示平均薪资大于10000的部门，按平均薪资降序排列 |

**生成结果**：
```sql
SELECT d.dept_name, AVG(e.salary) AS avg_salary
FROM employees e
JOIN departments d ON e.dept_id = d.id
GROUP BY d.id, d.dept_name
HAVING AVG(e.salary) > 10000
ORDER BY avg_salary DESC;
```

---

## 八、常见问题

### Q1：ImportError: cannot import name 'OpenAI' from 'openai'

**原因**：openai 包版本低于 1.0

**解决方案**：
```bash
pip install openai --upgrade
```

### Q2：API 密钥报错

**原因**：未设置环境变量或密钥无效

**解决方案**：
1. 确认已设置 `DASHSCOPE_API_KEY` 环境变量
2. 检查密钥是否有效（登录阿里云控制台验证）

### Q3：生成结果不准确

**解决方案**：
1. 表结构描述更完整（包含字段类型、约束、注释）
2. 查询需求描述更具体（明确筛选条件、排序方式）
3. 多表查询时说明表之间的关联关系

### Q4：Streamlit 启动失败

**解决方案**：
```bash
# 确认 streamlit 已安装
pip install streamlit

# 重新安装
pip install streamlit --upgrade
```

### Q5：网络连接失败

**原因**：无法访问 DashScope API

**解决方案**：
1. 检查网络连接
2. 确认能访问 `https://dashscope.aliyuncs.com`

---

## 九、项目结构

```
项目根目录/
├── db_query/
│   ├── db_query.py        # 主程序
│   ├── README.md          # 使用说明
│   └── requirements.txt   # 依赖列表
├── README.md              # 产品说明书
└── .venv/                 # 虚拟环境（可选）
```

---

## 十、技术架构

```
用户输入 → 提示词组装 → 大模型API → 生成结果 → 界面展示
```

### API 配置

| 配置项 | 值 |
|--------|-----|
| API地址 | https://dashscope.aliyuncs.com/compatible-mode/v1 |
| 模型 | qwen3-coder-plus |
| Temperature | 0（保证输出稳定性） |

---

## 十一、注意事项

1. **API 密钥安全**：不要在代码中硬编码 API 密钥
2. **数据量控制**：单次请求数据结构不超过 10 个
3. **网络连接**：确保能访问 DashScope API
4. **结果验证**：生成结果需人工验证后使用

---

## 十二、停止应用

在终端按 `Ctrl + C` 停止 Streamlit 服务。

---

## 版本信息

- 版本：1.0
- 更新日期：2024-12
- 作者：Jerry老师课程案例

---

## 联系与反馈

如有问题或建议，请联系项目维护者。