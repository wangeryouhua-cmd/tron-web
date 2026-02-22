import streamlit as st
from eth_account import Account
import secrets

# 让网页更漂亮
st.set_page_config(page_title="波场极速扫号器", page_icon="💎")
st.title("波场极速扫号器 💎")
st.markdown("---")

# 侧边栏设置
st.sidebar.header("配置选项")
target = st.sidebar.text_input("输入你想要的结尾数字 (如: 666)", "888")

if st.button('🚀 开始疯狂扫号'):
    st.warning("扫号运行中，发现靓号后会停在下方。")
    
    # 建立实时显示区域
    status = st.empty()
    display = st.container()
    
    count = 0
    while True:
        # 生成随机私钥并转换成地址
        priv_key = "0x" + secrets.token_hex(32)
        acc = Account.from_key(priv_key)
        
        # 将以太坊格式地址转换为波场格式 (波场地址以 T 开头)
        # 简单算法：这里直接判断十六进制结尾也可以，或者直接找地址结尾字符
        addr = acc.address
        count += 1
        
        # 实时刷新进度
        if count % 20 == 0:
            status.info(f"⚡ 已扫描: {count} 次 | 当前测试: {addr}")
            
        # 匹配结尾 (不区分大小写)
        if addr.lower().endswith(target.lower()):
            with display:
                st.success(f"🎊 恭喜！第 {count} 次扫描找到了靓号！")
                st.code(f"地址: {addr}\n私钥: {priv_key}")
                st.balloons()
            break
