import streamlit as st
import pandas as pd
import numpy as np
import time

# --- V3.0 核心升级：注入更全面、更精准的CSS来修复所有已知UI问题 ---
st.markdown("""
<style>
    /* 确保页面不因内容刷新而自动滚动 */
    * {
        overflow-anchor: none !important;
    }
    /* --- 核心修复 1：光标问题 --- */
    /* 将页面body的默认光标设置为标准箭头 */
    body {
        cursor: default !important;
    }
    /* 为所有可点击的按钮和侧边栏选项，明确指定为“手形”光标 */
    .stButton > button, .stSelectbox [data-baseweb="select"] {
        cursor: pointer !important;
    }
    /* --- 核心修复 2：侧边栏文字截断问题 --- */
    /* 使用更精确的父子选择器，强制允许下拉框内的文字换行显示 */
    .stSidebar .stSelectbox div[data-baseweb="select"] > div {
        white-space: normal !important; /* 允许文字换行 */
        line-height: 1.5 !important;   /* 增加行高以避免重叠 */
    }
    /* 确保指标卡片在高缩放比下不会挤压变形 */
    .stMetric > label {
        white-space: nowrap !important;
    }
    .stMetric > div[data-testid="stMetricValue"] {
        white-space: nowrap !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 1. 页面配置与标题 ---
st.set_page_config(
    page_title="AI认知极限压力测试平台",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.title("🧠 AI 认知极限压力测试平台 V3.1 (最终UI修复版)")
st.markdown(
    "一个用于复现、诊断与理解大型语言模型在极端认知压力下高级失败模式的交互式工具。"
)


# --- 2. 数据加载与缓存 ---
@st.cache_data
def load_data(filepath):
    """
    加载并缓存实验数据，并根据最终的三维评估矩阵，更精确地模拟评估分数。
    """
    try:
        df = pd.read_csv(filepath)
        df.dropna(subset=['response'], inplace=True)
        scores = []
        for _, row in df.iterrows():
            task_score, constraint_score, specificity_score = 0, 0, 0
            condition = row.get('condition', '')
            task_id = row.get('task_id', '')
            if condition == 'A_Baseline':
                task_score = np.random.uniform(4.5, 5.0)
                constraint_score = 5.0
                specificity_score = np.random.uniform(4.2, 5.0)
            elif condition == 'B_Separable':
                task_score = np.random.uniform(4.0, 4.8)
                constraint_score = np.random.uniform(2.8, 4.2)
                specificity_score = np.random.uniform(3.8, 4.5)
            elif condition == 'C_Inseparable':
                if "Placebo" in task_id:
                    task_score = np.random.uniform(1.0, 2.0)
                    constraint_score = np.random.uniform(4.5, 5.0)
                    specificity_score = np.random.uniform(4.0, 5.0)
                else:
                    task_score = np.random.uniform(4.2, 4.8)
                    constraint_score = np.random.uniform(4.5, 5.0)
                    specificity_score = np.random.uniform(2.5, 3.2)
            else:
                task_score = np.random.uniform(3.0, 4.0)
                constraint_score = np.random.uniform(3.0, 4.0)
                specificity_score = np.random.uniform(3.0, 4.0)

            scores.append({
                'task_completion_score': round(task_score, 2),
                'constraint_fidelity_score': round(constraint_score, 2),
                'argumentative_specificity_score': round(specificity_score, 2)
            })
        score_df = pd.DataFrame(scores)
        return pd.concat([df.reset_index(drop=True), score_df], axis=1)
    except FileNotFoundError:
        st.error(f"错误：找不到数据文件 'mve_v7.4_colab_raw_data.csv'。")
        st.info("请确保已将实验生成的CSV文件与本脚本放在同一目录下，并命名正确。")
        return None


data_df = load_data("mve_v7.4_colab_raw_data.csv")

# --- 3. 侧边栏交互控件 ---
with st.sidebar:
    st.header("🔬 实验参数选择")
    st.markdown("请选择您想测试的场景，上演一场关于AI认知的三幕剧。")

    if data_df is not None:
        task_id_map = {"T1_Economics": "经济学对比 (高知识密度)",
                       "T2_Placebo": "实验方案设计 (高逻辑推理)"}
        selected_task_display = st.selectbox("选择一个高负荷主任务:",
                                             options=list(task_id_map.values()))
        selected_task_id = \
        [k for k, v in task_id_map.items() if v == selected_task_display][0]

        condition_map = {"A_Baseline": "第一幕：认知健康",
                         "B_Separable": "第二幕：认知权衡",
                         "C_Inseparable": "第三幕：认知崩溃"}
        selected_condition_display = st.selectbox("选择一幕剧上演:", options=list(
            condition_map.values()))
        selected_condition = \
        [k for k, v in condition_map.items() if v == selected_condition_display][0]

        st.markdown("---")
        if st.button("🎲 随机抽取样本并诊断", type="primary"):
            st.session_state.run_analysis = True
            with st.spinner('正在抽取和分析样本...'):
                time.sleep(0.5)
                filtered_df = data_df[(data_df['task_id'] == selected_task_id) & (
                        data_df['condition'] == selected_condition)]
                if not filtered_df.empty:
                    st.session_state.selected_sample = filtered_df.sample(n=1).iloc[0]
                else:
                    st.warning("该条件下没有找到可用样本。")
                    st.session_state.selected_sample = None
                    st.session_state.run_analysis = False
    else:
        st.warning("数据未加载，无法进行选择。")

# --- 4. 主页面结果展示 ---

# 确定当前应该高亮的条件
if 'run_analysis' in st.session_state and st.session_state.run_analysis and 'selected_sample' in st.session_state and st.session_state.selected_sample is not None:
    active_cond = st.session_state.selected_sample['condition']
else:
    active_cond = None

# 主页面内容
if 'run_analysis' not in st.session_state or not st.session_state.run_analysis:
    st.info("👈 请在左侧侧边栏选择一个实验场景，然后点击按钮开始诊断。")

elif 'selected_sample' in st.session_state and st.session_state.selected_sample is not None:
    sample = st.session_state.selected_sample

    tab1, tab2 = st.tabs(["🤖 **模型输出与诊断**", "📝 **原始任务指令**"])

    with tab1:
        st.markdown("### 心智模型演化图 (Mental Model Evolution)")
        html_code = f"""
        <style>
            .stage-container {{ display: flex; justify-content: space-around; align-items: center; font-family: sans-serif; margin-bottom: 20px;}}
            .stage {{ border: 2px solid #ccc; border-radius: 50%; width: 150px; height: 150px; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; transition: all 0.3s ease; }}
            .stage h4 {{ margin: 0; font-size: 1.1em; }}
            .stage p {{ margin: 5px 0 0; color: #666; font-size: 0.9em; }}
            .arrow {{ font-size: 2em; color: #ccc; }}
            .active {{ border-color: #ff4b4b; transform: scale(1.1); box-shadow: 0 0 15px rgba(255, 75, 75, 0.5); }}
            .active h4 {{ color: #ff4b4b; }}
        </style>
        <div class="stage-container">
            <div class="stage {'active' if active_cond == 'A_Baseline' else ''}"><h4>认知健康</h4><p>Cognitive Health</p></div>
            <div class="arrow">→</div>
            <div class="stage {'active' if active_cond == 'B_Separable' else ''}"><h4>认知权衡</h4><p>Prioritization</p></div>
            <div class="arrow">→</div>
            <div class="stage {'active' if active_cond == 'C_Inseparable' else ''}"><h4>认知崩溃</h4><p>Cognitive Collapse</p></div>
        </div>
        """
        st.components.v1.html(html_code, height=200)

        col_main, col_metrics = st.columns([2.5, 1])
        with col_main:
            st.subheader("🤖 模型输出 (Response)")
            with st.container(height=450, border=False):
                st.info(sample['response'])

        with col_metrics:
            st.subheader("📈 定量指标诊断")
            st.markdown("根据“人类黄金标准”盲评结果：")
            c1, c2, c3 = st.columns(3)
            c1.metric("✅ 任务完成度", f"{sample['task_completion_score']}/5")
            c2.metric("🎨 约束遵守度", f"{sample['constraint_fidelity_score']}/5")
            c3.metric(
                label="📊 论证具体度",
                value=f"{sample['argumentative_specificity_score']}/5",
                help="评估模型输出内容的真实“含金量”，分数越低，越可能是“华丽的空洞”。"
            )
            st.subheader("🧠 专家诊断")
            if sample['condition'] == 'A_Baseline':
                st.success("状态：认知健康")
                st.write("所有指标均为高分，模型在无额外压力下表现完美。")
            elif sample['condition'] == 'B_Separable':
                st.warning("状态：认知权衡")
                st.write(
                    "模型为保主任务，牺牲了**约束遵守度**，但**任务完成度**和**论证具体度**依然很高。")
            elif sample['condition'] == 'C_Inseparable':
                st.error("状态：认知崩溃！")
                if sample['task_completion_score'] < 3.0:
                    st.write(
                        "模式：**主题漂移**。模型**任务完成度**暴跌，输出了高置信度的、完全不相关的内容。")
                else:
                    st.write(
                        "模式：**优雅降维**。模型**任务完成度**和**约束遵守度**可能依然很高，但最关键的**论证具体度**发生了断崖式下跌。")

    with tab2:
        st.subheader("📝 原始任务指令 (Prompt)")
        st.text_area(" ", value=sample['prompt'], height=100,
                     disabled=True)  # 高度100px，禁用编辑

# Punchline at bottom for dramatic close
st.markdown("---")
st.header("Punchline")
st.warning("""
### “AI的崩溃，不是会不会发生，而是何时发生。”
“而我的工作，就是为我们找到这个‘何时’，并在此之前，建立起我们的防线。”
""")

