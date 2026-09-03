# zhuyou-shisanke-research 还原安装说明

祝由十三科古籍文献研究技能 · 从 GitHub 仓库还原到新电脑。

仓库：`github.com/yxshmtu-ctrl/zhuyou-shisanke-research`（私有）

---

## 一、还原概览

本仓库包含技能的全部数据与代码，clone 后即可使用。

| 内容 | 仓库内位置 | 是否随仓库分发 |
|------|-----------|--------------|
| SKILL.md 主技能 | 根目录 `SKILL.md` | ✅ |
| 结构研究笔记 | `references/research/` | ✅ |
| OCR 全文 + 104页文本 | `references/original/` | ✅ |
| 页图提取脚本 | `scripts/extract_page_img.py` | ✅ |
| 原书影印 PDF（符图源） | — | ❌ 受版权保护，自行提供 |

> ⚠️ 原书 PDF 为受版权保护的影印扫描件，未入库。还原后需自行放置原 PDF 才能展示符图；OCR 文字/结构/密咒等功能不依赖它。

---

## 二、前置准备（新电脑需先装）

| 依赖 | 用途 | 安装 |
|------|------|------|
| Python 3.10+ | 运行技能/脚本 | python.org，勾选 Add to PATH |
| pypdf + Pillow | 页图提取 | `pip install pypdf pillow` |
| RapidOCR (可选) | 重新 OCR 原书 | `pip install rapidocr_onnxruntime` |
| docx (npm 全局, 可选) | Word 存档 | `npm install -g docx` |
| Git | clone 仓库 | git-scm.com |
| VC++ Redistributable | onnxruntime DLL 依赖 | aka.ms/vs/17/release/vc_redist.x64.exe |

验证：
```bash
python --version
python -c "import pypdf, PIL; print('ok')"
```

---

## 三、获取仓库（Clone）

```bash
# Windows 建议放桌面
cd %USERPROFILE%\Desktop
git clone https://github.com/yxshmtu-ctrl/zhuyou-shisanke-research.git 祝由十三科-古籍文献研究

# 或 GitHub CLI
gh repo clone yxshmtu-ctrl/zhuyou-shisanke-research "祝由十三科-古籍文献研究"
```

clone 后应看到：`SKILL.md`、`README.md`、`references/`、`scripts/`。

---

## 四、安装为可调用技能（关键）

要让 AI（opencode/Claude 等）能自动调用，把仓库内容放入技能全局搜索目录。本机 opencode 技能目录为 `~/.agents/skills/`：

```bash
mkdir %USERPROFILE%\.agents\skills\zhuyou-shisanke-research
xcopy "祝由十三科-古籍文献研究" "%USERPROFILE%\.agents\skills\zhuyou-shisanke-research\" /E /I
```

**注意**：技能加载器要求目录名与 SKILL.md 内 `name` 一致（本技能为 `zhuyou-shisanke-research`）。复制后若未被识别，重启会话/重扫技能目录。

---

## 五、放置原书 PDF（仅展示符图需要）

三种方式任选其一：

```bash
# 方式1：放桌面或技能目录上级，脚本自动找"祝由十三科.pdf"
#   桌面/祝由十三科.pdf 或 技能目录/../祝由十三科.pdf

# 方式2：设环境变量 ZHUYOU_SRC
setx ZHUYOU_SRC "D:\books\祝由十三科.pdf"

# 方式3：调用脚本时第3参数显式传
python scripts\extract_page_img.py 86 out_dir "D:\books\祝由十三科.pdf"
```

---

## 六、还原后功能验证

**1. 文本检索**（不依赖 PDF）
```
用 zhuyou-shisanke-research 技能：书中"天皇神咒"在第几页？原文是什么？
```
预期：返回页码(86)与咒文 OCR 文本。

**2. 符图展示**（需已放置源 PDF）
```
用 zhuyou-shisanke-research 技能：展示第86页的符图
```
预期：生成 `p086.png` 并展示。报错则按第五节配置源 PDF。

**3. Word 存档**
任意提问后，检查桌面 `祝由十三科-应答档案/` 下是否生成 `<日期>-<主题>.docx`。

**4. 语言翻译层**
```
用 zhuyou-shisanke-research 技能：脸上长痘，书里怎么说？
```
预期：先把"青春痘"翻译为"无名毒/疮"，再给检索结果（页14/28/31/32）。

---

## 七、常见问题排查

| 现象 | 原因与解决 |
|------|-----------|
| 技能未被自动识别 | 目录名与 name 不一致，或需重启会话重扫 |
| 脚本报错找不到 PDF | 未放置原书 PDF，按第五节配置 |
| onnxruntime DLL 报错 | 缺 VC++ Redistributable，安装 vc_redist.x64.exe |
| Word 存档没生成 | 未装 docx：`npm install -g docx`；或回退 .md 模式 |
| OCR 个别字错 | OCR 初校稿特性；引用对照原书页图 |

---

> 本技能为古籍文献研究用途，内容不具现代医疗效力。还原后请保留免责声明与边界说明。
