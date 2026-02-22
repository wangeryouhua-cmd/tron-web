import streamlit as st
from eth_account import Account
import secrets
import base58
import hashlib

# 1. 核心转换函数：将以太坊地址转为波场 T 开头地址
def to_tron_address(eth_address):
    # 去掉 0x，补上波场前缀 41
    hex_addr = "41" + eth_address[2:]
    addr_byte = bytes.fromhex(hex_addr)
    # 计算两次 SHA256 校验码
    hash1 = hashlib.sha256(addr_byte).digest()
    hash2 = hashlib.sha256(hash1).digest()
    # 拼接前缀与校验码的前4位
    raw_data = addr_byte + hash2[:4]
    return base58.b58encode(raw_data).decode()

# --- 网页配置 ---
st.set_page_config(page_title="波场极速扫号专业版", page_icon="🔥", layout="wide")

# 初始化历史记录存储（如果不存在）
if 'history' not in st.session_state:
    st.session_state.history = []

st.title("🔥 波场极速扫号专业版")
st.markdown("---")

# 侧边栏设置
st.sidebar.header("⚙️ 扫号配置")
target = st.sidebar.text_input("想要匹配的结尾 (例如: 666)", "888")
show_all = st.sidebar.checkbox("实时显示扫描详情 (勾选会略微降低速度)", True)

col1, col2 = st.columns([2, 1])

with col1:
    start_btn = st.button('🚀 开始无间断扫号')
    stop_btn = st.button('🛑 停止扫描')
    
    status_area = st.empty()
    latest_result = st.container()

with col2:
    st.subheader("📋 历史保存记录")
    history_display = st.empty()

# --- 扫号逻辑 ---
if start_btn:
    st.toast("引擎已启动，正在疯狂搜索中...", icon='🚀')
    count = 0
    
    while True:
        # 1. 生成新账号
        priv_key = "0x" + secrets.token_hex(32)
        acc = Account.from_key(priv_key)
        tron_addr = to_tron_address(acc.address)
        count += 1
        
        # 2. 实时进度展示
        if count % 10 == 0 and show_all:
            status_area.info(f"⚡ 已扫描: `{count}` 次 | 当前测试: `{tron_addr}`")
            
        # 3. 匹配逻辑
        if tron_addr.endswith(target):
            res_msg = f"✨ 找到靓号！第 {count} 次尝试"
            with latest_result:
                st.success(res_msg)
                st.code(f"波场地址: {tron_addr}\n私钥明文: {priv_key}")
            
            # 保存到历史记录（添加到列表首位）
            st.session_state.history.insert(0, f"地址: {tron_addr} | 私钥: {priv_key}")
            
            # 更新历史显示
            with history_display.container():
                for item in st.session_state.history:
                    st.text(item)
            
            st.balloons()
            # 注意：这里不再使用 break，它会一直扫下去
