# 第三方声明 / Third-Party Notices

本文件列出本项目包含、派生或依赖的第三方作品及其版权归属与许可。
This file lists third-party works that this repository contains, derives from, or depends on,
together with their copyright holders and licenses.

> 本仓库是**第三方修改版**，与下列任何项目、作者均无隶属或背书关系。
> This repository is an **unofficial third-party fork** and is not affiliated with or endorsed by
> any of the projects or authors listed below.

---

## 1. 组件清单 / Components

### 1.1 VOSR2 加速插件（原始版本） / VOSR2 acceleration plugin (original release)

| 项目 | 说明 |
|---|---|
| 作品 | 原 "TE-Speed" 系列 VOSR2 加速插件（节点 + 4 个编译组件） |
| 作者 | **yun**（原 TE-Speed 系列插件作者） |
| 许可证 | **原发行版未附带许可证文件，亦未声明授权条款** |
| 本仓库的使用方式 | `nodes.pyd`、`inference.pyd`、`model_store.pyd`、`settings.pyd` 四个二进制组件按"原样"再分发；其余部分在其基础上改名与修复 |
| 本项目对其的修改 | ① 等长替换其中的品牌字符串（共 80 处）与编译期源码路径；② 节点 ID / 分类 / 显示名统一到 `AICG3D` 命名空间；③ 修复 `backend/tiled_vae.py` 两处问题；④ 重写文档 |

**特别鸣谢：本插件的分块推理、显存调度、视频处理优化、DINO 时序缓存、
SageAttention 集成等全部核心加速能力，均来自这位作者的工作。**

> 由于原发行版未声明许可证，本项目仅以"署名 + 原样再分发 + 可随时下架"的方式处理这些二进制组件。
> 若原作者有任何异议，请联系我们，我们会立即下架或按其要求调整（见第 4 节）。

### 1.2 ComfyUI-VOSR2

| 项目 | 说明 |
|---|---|
| 来源 | <https://github.com/ylchen333/ComfyUI-VOSR2> |
| 作者 | ylchen333 |
| 版权 | Copyright (c) ylchen333 及贡献者 |
| 许可证 | Apache License 2.0 |
| 在本仓库中的位置 | `backend/`、`backend/models/`（VOSR2 推理契约、模型封装）、节点骨架 |
| 本项目对其的修改 | 目录结构调整为 `backend/`；新增 pos-embed 缓存与 SageAttention 适配（来自 1.1）；修复 `tiled_vae.py` 两处问题；改名与文档重写 |

### 1.3 VOSR / VOSR 2.0

| 项目 | 说明 |
|---|---|
| 来源 | <https://github.com/cswry/VOSR> |
| 作者 | Rongyuan Wu (cswry) 等 |
| 许可证 | Apache License 2.0 |
| 在本仓库中的位置 | 模型架构、推理流程与 `models/` 下的实现（经 1.2 派生） |
| 模型权重 | **本仓库不分发**。权重见 <https://huggingface.co/CSWRY/VOSR>，其版权与使用条款归发布者所有 |

### 1.4 LightningDiT

| 项目 | 说明 |
|---|---|
| 来源 | VOSR 项目中的 `models/lightningdit.py`；上游构建于 facebookresearch/DiT 与 willisma/SiT |
| 作者 | Jingfeng Yao（HUST-VL）等 |
| 许可证 | Apache License 2.0 |
| 在本仓库中的位置 | `backend/models/lightningdit.py` |
| 本项目对其的修改 | 裁剪未使用分支（timm 依赖、固定尺寸 `forward`、绝对位置编码）；新增 SageAttention 适配与缓存 |

### 1.5 DINOv2

| 项目 | 说明 |
|---|---|
| 来源 | <https://github.com/facebookresearch/dinov2> |
| 作者 | Meta AI Research |
| 许可证 | Apache License 2.0 |
| 在本仓库中的位置 | `backend/models/dinov2.py`（ViT-L/14 架构的本地实现） |
| 本项目对其的修改 | 仅保留本任务所需的中层特征提取路径；新增位置编码缓存 |

### 1.6 Qwen-Image 2D VAE

| 项目 | 说明 |
|---|---|
| 来源 | Qwen-Image / Wan / HuggingFace 团队的相关开源实现 |
| 许可证 | Apache License 2.0 |
| 在本仓库中的位置 | `backend/models/qwenimage_vae2d.py`（去 diffusers 依赖的本地实现） |
| 本项目对其的修改 | 移除 diffusers 依赖，自带 `DiagonalGaussianDistribution` 与权重加载 |

### 1.7 ComfyUI

| 项目 | 说明 |
|---|---|
| 来源 | <https://github.com/comfyanonymous/ComfyUI> |
| 作者 | comfyanonymous 及贡献者 |
| 许可证 | GNU General Public License v3.0 |
| 在本仓库中的使用方式 | **仅作为运行宿主被调用**（`comfy.ops`、`comfy.ldm.modules.attention` 等），本仓库不包含其代码 |

---

## 2. 许可证原文 / License texts

- 本仓库自身的许可：**Apache License 2.0**，全文见 [LICENSE](LICENSE)。
- 各上游组件的许可证全文可在其各自仓库中获取（见上表链接）。
- `backend/`、`backend/models/` 下的源文件**保留了各自上游的版权与许可注释**，
  再分发或修改时请勿删除。

---

## 3. 为什么本仓库使用 Apache-2.0 而不是 GPL

本插件包含**没有对应源码的编译二进制组件**（见 1.1）。
GPL 系列许可证要求：分发二进制时必须能够提供完整的对应源码。
本项目无法提供这些组件的源码，因此**不适合使用 GPL**。
Apache-2.0 允许在保留版权与许可声明的前提下以二进制形式再分发，且与上游（1.2、1.3）的许可一致。

---

## 4. 侵权处理与下架承诺 / Takedown policy

我们充分尊重每一位原作者的劳动成果：

- 本仓库**已尽最大努力完成署名**，并明确标注其为第三方修改版、非官方版本。
- 如果你是权利人，认为本仓库的任何内容侵犯了你的权利，请通过 **GitHub Issue** 联系我们。
- 我们会在核实后**立即删除或调整相关内容**，不设置前置条件、不要求你先举证。
- 若原作者（1.1）提出要求，我们将**直接下架**相关二进制组件，或按你的要求改为仅提供说明与下载指引。

---

## 5. 免责声明 / Disclaimer

本仓库内容按"现状"（AS IS）提供，不附带任何明示或暗示的担保。使用本仓库内容所产生的一切后果
由使用者自行承担。请遵守你所在国家/地区的法律法规，不得将本项目用于任何违法违规用途。
