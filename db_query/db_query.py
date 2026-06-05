import os
from openai import OpenAI
import streamlit as st


def get_completion(messages):
    """
    调用大模型API获取生成结果
    :param messages: 对话消息列表
    :return: 模型生成的文本内容
    """
    # 初始化 OpenAI 客户端，使用阿里云 DashScope API
    client = OpenAI(api_key=os.getenv("DASHSCOPE_API_KEY"),
                    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

    # 调用通义千问模型生成响应
    response = client.chat.completions.create(
        model='qwen3-coder-plus',  # 使用通义千问编码增强模型
        messages=messages,
        temperature=0,  # 温度设为0，确保输出稳定一致
    )
    return response.choices[0].message.content


def gen_prompt(table_structures, sql_requirements, dbtype):
    """
    根据输入参数组装提示词并调用大模型生成SQL/Redis命令
    :param table_structures: 表结构或Redis数据结构描述
    :param sql_requirements: 用户查询需求（自然语言）
    :param dbtype: 数据库类型（MySQL/Redis/SQL Server/Oracle/SQLite）
    :return: 生成的SQL语句或Redis命令
    """
    # 根据数据库类型选择不同的角色设定和示例
    if dbtype == 'Redis':
        # Redis 不使用 SQL，使用 Redis 命令
        instruction = """
            # 角色: 你是一位专业的Redis命令编写工程师
            ## 技能: 可以根据Redis数据结构和用户输入，生成Redis命令。
            """
        examples = """
            Redis数据结构如下：
            # 用户信息（Hash类型）
            user:1 -> {name: "张三", age: 25, email: "zhangsan@example.com", city: "北京"}
            user:2 -> {name: "李四", age: 30, email: "lisi@example.com", city: "上海"}

            # 订单列表（List类型）
            user:1:orders -> [order:1, order:2, order:3]

            # 订单详情（Hash类型）
            order:1 -> {user_id: 1, product: "手机", amount: 5000, status: 1, create_time: "2024-01-01"}
            order:2 -> {user_id: 1, product: "电脑", amount: 8000, status: 2, create_time: "2024-02-01"}

            # 商品库存（String类型）
            inventory:phone -> 100
            inventory:computer -> 50

            # 用户消费排行榜（Sorted Set类型）
            user_spending -> {user:1: 13000, user:2: 5000}

            用户需求：
            获取用户1的所有信息

            生成的Redis命令：
            HGETALL user:1
        """
    else:
        # SQL数据库（MySQL、SQL Server、Oracle、SQLite）
        instruction = """
            # 角色: 你是一位专业的SQL编写工程师
            ## 技能: 可以根据表结构和用户输入，生成SQL语句。
            """
        examples = """
            表结构如下：
            orders (
                id INT PRIMARY KEY NOT NULL,
                customer_id INT NOT NULL,
                product_id INT NOT NULL,
                price DECIMAL(10, 2) NOT NULL,
                STATUS INT NOT NULL CHECK (STATUS IN (0, 1, 2)), -- 确保订单状态在0, 1, 2之间
                create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                pay_time TIMESTAMP NULL,
                FOREIGN KEY (customer_id) REFERENCES customers(id),
                FOREIGN KEY (product_id) REFERENCES products(id)
            );
            customers (
                id INT PRIMARY KEY NOT NULL, -- 主键，不允许为空
                customer_name VARCHAR(255) NOT NULL, -- 客户名，不允许为空
                email VARCHAR(255) UNIQUE, -- 邮箱，唯一
                register_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- 注册时间，默认为当前时间
            );
            products (
                id INT PRIMARY KEY NOT NULL, -- 主键，不允许为空
                product_name VARCHAR(255) NOT NULL, -- 产品名称，不允许为空
                price DECIMAL(10,2) NOT NULL -- 价格，不允许为空
            );
            用户需求：
            哪个用户消费最高？消费多少？
            生成的SQL：
            SELECT customer_id, SUM(price) AS total_spent FROM orders GROUP BY customer_id ORDER BY total_spent DESC LIMIT 1;
        """

    # 组装完整提示词：角色设定 + 目标数据库类型 + 示例 + 表结构 + 用户需求
    prompt = f"""
            {instruction}
            # 目标数据库类型：
            {dbtype}
            # 示例：
            {examples}
            # 表结构如下：
            {table_structures}
            # 用户输入：
            {sql_requirements}
        """
    print('-' * 100)
    print(prompt)
    print('-' * 100)
    messages = [{"role": "user", "content": prompt}]

    return get_completion(messages)


# 可视化界面
def main():
    """
    Streamlit 主界面函数
    提供用户交互界面，收集输入并调用大模型生成SQL/Redis命令
    """
    # 设置页面标题
    st.title("SQL语句生成器")

    # 初始化 session_state，用于控制按钮状态（防止生成期间重复点击）
    if 'generating' not in st.session_state:
        st.session_state.generating = False

    # 数据库类型选择下拉框
    dbtype = st.selectbox('请选择数据库类型:', ['MySQL', 'Redis', 'SQL Server', 'Oracle', 'SQLite'])

    # 获取用户输入的表结构数量（1-10）
    num_tables = st.number_input('请输入你需要填写的表结构数量:', min_value=1, max_value=10, step=1)

    # 根据表结构数量动态创建多个输入框
    table_structures = ""
    for i in range(num_tables):
        table_structure = st.text_area(f"请输入表结构，第 {i + 1} 张表:")
        table_structures += table_structure + "\n"

    # SQL需求输入框（用户用自然语言描述查询需求）
    sql_requirements = st.text_area("请输入生成SQL的需求:")

    # 提交按钮：生成期间禁用，防止重复点击
    if st.button("提交", disabled=st.session_state.generating):
        # 验证输入是否完整
        if all(table_structures) and sql_requirements:  # 检查是否所有的表结构和SQL需求都已经填写
            st.session_state.generating = True  # 开始生成，禁用按钮
            # 显示转圈动画，等待大模型生成结果
            with st.spinner('正在生成SQL，请稍候...'):
                output = gen_prompt(table_structures, sql_requirements, dbtype)
            st.success(output)  # 显示生成结果
            st.session_state.generating = False  # 生成完成，恢复按钮可点击
        else:
            st.warning("请确保所有表结构和SQL需求已经填写")  # 提示用户完善输入


if __name__ == '__main__':
    # 程序入口：启动 Streamlit 应用
    main()
