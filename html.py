import streamlit as st
from trident.account import Account
import time

# --- 网页标题 ---
st.set_page_config(page_title="波场靓号生成器", page_icon="🚀")
st.title("波场靓号生成器 🚀")
st.write("使用最新 trident 引擎，适配 Python 3.13。")

# --- 侧边栏配置 ---
st.sidebar.header("扫号设置")
suffix = st.sidebar.text_input("请输入想要查找的结尾（如：666）", "888")

# --- 开始按钮 ---
if st.button('开始扫号'):
    st.info(f"正在搜寻以 {suffix} 结尾的靓号... 发现后会立即显示在下方。")
    
    # 建立一个占位符，用来实时刷新显示进度
    status_text = st.empty()
    result_area = st.container()
    
    count = 0
    while True:
        # 使用 trident 库生成随机账号
        acc = Account.create()
        address = acc.address
        private_key = acc.private_key
        
        count += 1
        
        # 在网页上实时显示进度（每10次刷新一次界面，提高性能）
        if count % 10 == 0:
            status_text.text(f"已检查 {count} 个地址，当前：{address}")
        
        # 逻辑判断：是否以指定字符结尾
        if address.endswith(suffix):
            with result_area:
                st.success(f"✨ 找到靓号！(第 {count} 次尝试)")
                st.code(f"地址: {address}\n私钥: {private_key}")
            
            # 找到一个后停止，或者你可以注释掉 break 让它继续找
            break
