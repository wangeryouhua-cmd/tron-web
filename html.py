import streamlit as st
import requests
import time
import pandas as pd

# --- 网页配置 ---
st.set_page_config(page_title="波场全网监控引擎", page_icon="📡", layout="wide")

# 初始化 Session State (存储监控名单和记录)
if 'watch_list' not in st.session_state:
    st.session_state.watch_list = set()  # 使用 set 提高查找速度
if 'found_txs' not in st.session_state:
    st.session_state.found_txs = []
if 'is_running' not in st.session_state:
    st.session_state.is_running = False

st.title("📡 波场万号充值实时监听引擎 (极速版)")
st.info("原理：每3秒拉取最新区块，扫描所有交易并比对你的名单。")

# --- 界面布局 ---
col_cfg, col_main = st.columns([1, 2])

with col_cfg:
    st.subheader("⚙️ 监控配置")
    
    # 地址导入
    input_type = st.radio("地址导入方式", ["手动输入", "批量上传"])
    if input_type == "手动输入":
        addr_input = st.text_area("输入地址 (一行一个)", placeholder="TXXXX...\nTYYYY...")
        if st.button("更新监控名单"):
            addrs = {a.strip() for a in addr_input.split('\n') if a.strip()}
            st.session_state.watch_list = addrs
            st.success(f"已加载 {len(addrs)} 个地址")
    else:
        uploaded_file = st.file_uploader("上传 TXT 地址文件", type=['txt'])
        if uploaded_file:
            addrs = {line.decode("utf-8").strip() for line in uploaded_file if line.strip()}
            st.session_state.watch_list = addrs
            st.success(f"已从文件加载 {len(addrs)} 个地址")

    st.markdown("---")
    if st.button("🔴 启动/重置 监听引擎"):
        st.session_state.is_running = True
        st.session_state.found_txs = []
        st.rerun()

# --- 核心监控逻辑 ---
with col_main:
    st.subheader("🚀 实时账变流")
    log_area = st.empty()
    table_area = st.empty()
    
    if st.session_state.is_running:
        if not st.session_state.watch_list:
            st.warning("请先加载监控名单！")
        else:
            last_block_id = 0
            # 建立一个持续运行的循环
            while True:
                try:
                    # 1. 获取最新区块数据 (官方 API)
                    resp = requests.post("https://api.trongrid.io/wallet/getnowblock")
                    block_data = resp.json()
                    
                    curr_block_id = block_data['block_header']['raw_data']['number']
                    timestamp = block_data['block_header']['raw_data']['timestamp']
                    
                    # 只有发现新块才处理
                    if curr_block_id > last_block_id:
                        tx_list = block_data.get('transactions', [])
                        tx_count = len(tx_list)
                        last_block_id = curr_block_id
                        
                        # 在界面显示当前扫描状态
                        log_area.markdown(f"📦 **正在扫描区块**: `{curr_block_id}` | 包含交易: `{tx_count}` 笔")
                        
                        # 2. 扫描区块内的每一笔交易
                        for tx in tx_list:
                            tx_id = tx['txID']
                            # 这里主要演示普通 TRX 转账监控
                            # TRC20 (USDT) 监控需要解析 TriggerSmartContract 字段，逻辑更复杂
                            contract = tx['raw_data']['contract'][0]
                            if contract['type'] == 'TransferContract':
                                value = contract['parameter']['value']
                                to_addr_hex = value.get('to_address')
                                # 将十六进制地址转为波场 T 地址（此处简化逻辑）
                                # 真实场景建议引用 tronpy 库进行转换
                                
                                # 模拟比对逻辑：如果在名单中
                                # if to_addr in st.session_state.watch_list:
                                #     amount = value.get('amount') / 1_000_000
                                #     st.session_state.found_txs.append(...)
                    
                    # 3. 每3秒查一次 (波场产块时间)
                    time.sleep(3)
                    
                    # 刷新显示历史记录表格
                    if st.session_state.found_txs:
                        df = pd.DataFrame(st.session_state.found_txs)
                        table_area.table(df)
                    else:
                        table_area.write("等待充值信号中...")

                except Exception as e:
                    st.error(f"引擎异常: {e}")
                    time.sleep(5)
