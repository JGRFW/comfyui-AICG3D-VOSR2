# AICG3D-VOSR2

**VOSR2 图像 / 视频超分辨率放大的 ComfyUI 加速节点** · 完全免费 · 开源

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![ComfyUI](https://img.shields.io/badge/ComfyUI-Custom%20Node-green.svg)](https://github.com/comfyanonymous/ComfyUI)

> ⚠️ **本仓库是第三方修改版，非官方版本。**
> 本插件基于公开发布的 VOSR2 加速插件整理、改名并修复问题而来，
> 与 VOSR / VOSR2 的模型作者、节点包作者均**无隶属、赞助或背书关系**。
> 原始版权归属与完整致谢见下方「致谢」与 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。

---

## 这是什么

VOSR 2.0 是一个一步式（one-step）、1.4B 参数的超分辨率模型（LightningDiT + Qwen-Image 2D VAE + DINOv2-L 条件编码）。

本插件把 VOSR2 搬进 ComfyUI，并针对实际使用做了大量工程优化：**分块推理、显存调度、视频处理优化、SageAttention 加速**，让 VOSR2 在 ComfyUI 里跑得又快又稳。

本版本在原加速版基础上做了两件事：

1. 全部统一到 **AICG3D** 命名空间（节点 ID `AICG3D_VOSR2*`、菜单分类 `AICG3D/VOSR2`）；
2. 修复了两个实际问题（见「本版改动」）。

---

## 致谢

这个插件能存在，靠的是下面这些人和项目。**特别感谢最初的 VOSR2 插件创造者。**

| 贡献者 / 项目 | 贡献 | 许可 |
|---|---|---|
| **yun**（原 TE-Speed 系列插件作者） | 分块推理、显存调度、视频流式处理、DINO 时序缓存、SageAttention 集成等**全部加速能力** | 原发行版未附带许可证 |
| **ylchen333** — [ComfyUI-VOSR2](https://github.com/ylchen333/ComfyUI-VOSR2) | 本插件的节点骨架与推理契约（`backend/` 由其派生） | Apache-2.0 |
| **Rongyuan Wu (cswry) 等** — [cswry/VOSR](https://github.com/cswry/VOSR) | VOSR / VOSR 2.0 模型与原始推理实现 | Apache-2.0 |
| **Jingfeng Yao（HUST-VL）** | LightningDiT 主干（基于 facebookresearch/DiT 与 willisma/SiT） | Apache-2.0 |
| **Meta AI** — [facebookresearch/dinov2](https://github.com/facebookresearch/dinov2) | DINOv2-L 条件编码器 | Apache-2.0 |
| **Qwen / Wan / HuggingFace 团队** | Qwen-Image 2D VAE 潜空间编解码 | Apache-2.0 |
| **comfyanonymous** — [ComfyUI](https://github.com/comfyanonymous/ComfyUI) | 运行环境、ops 与 attention 适配层 | GPL-3.0 |

模型权重来自 [CSWRY/VOSR](https://huggingface.co/CSWRY/VOSR)，**本仓库不包含任何模型权重**，权重版权与使用条款归其发布者所有。

如果你认为本仓库的署名有遗漏或不当之处，请提 Issue，我们会立即补充或修正。

---

## 功能特性

- 支持 VOSR 2.0 1.4B one-step 模型
- 支持图片**原尺寸修复**与**整数倍放大**
- 支持视频 **IMAGE 帧批次**放大
- `manual` / `speed` 两套推理配置，按显存与速度需求切换
- **空间分块**与 **VAE 分块**，大图/大视频不会一跑就爆显存
- 可选的**视频 DINO 时序缓存**（跨帧复用条件特征）
- 自动使用 ComfyUI 的 **SageAttention**，未安装时回退 SDPA
- 可选 **torch.compile**，失败自动回退 eager
- 显存调度策略（`resident` / `staged`），可与系统内存协同

---

## 安装

放进 ComfyUI 的 `custom_nodes` 目录即可：

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/JGRFW/AICG3D-VOSR2.git
```

或直接下载本仓库压缩包，解压为 `ComfyUI/custom_nodes/AICG3D-VOSR2/`。

**环境要求**

- Windows x64（其他系统未测试）
- NVIDIA GPU
- ComfyUI
- Python 3.12 / 3.13
- PyTorch 与 CUDA 版本需与当前 ComfyUI 环境兼容
- 可选：SageAttention（ComfyUI 能识别即可，节点里不用选）
- 可选：Triton（仅启用 `torch_compile` 时需要）

---

## 模型准备（不随仓库分发）

把模型放到：

```text
ComfyUI/models/vosr2/VOSR2/
|-- args.json
|-- checkpoints/
|   `-- ema_model.safetensors
|-- Qwen-Image-vae-2d/
|   |-- config.json
|   `-- diffusion_pytorch_model.safetensors
`-- dinov2_vitl14.safetensors
```

DINOv2 权重文件名兼容 `dinov2_vitl14_pretrain.pth`。

权重来源（约 7 GB）：官方仓库 <https://huggingface.co/CSWRY/VOSR>。
**请先阅读权重发布者的许可条款再使用。**

---

## 节点

菜单分类：**`AICG3D/VOSR2`**

| 显示名 | 节点 ID | 说明 |
|---|---|---|
| AICG3D-VOSR2 Loader | `AICG3D_VOSR2Loader` | 加载 VOSR2 模型 |
| AICG3D-VOSR2 Settings | `AICG3D_VOSR2Settings` | 推理配置（manual / speed、分块、策略等） |
| AICG3D-VOSR2 Image | `AICG3D_VOSR2Image` | 图片修复 / 放大 |
| AICG3D-VOSR2 Video Frames | `AICG3D_VOSR2Video` | 视频帧批次放大 |

**建议接线**：`Loader → Settings → Image / Video`。

> ⚠️ **如果你用过改名前的版本**：节点 ID 与连线类型都变了，旧工作流里这几个节点会显示为 missing node，
> 需要重新拖入并连线（或做一次 JSON 批量替换）。详见「本版改动」。

---

## 使用与调优

显存不足、或速度不对劲时，按这个顺序试：

1. `tile_size` 保持 **512**，不要先往上加。
2. `vae_tile_size` 保持 **1024**；图片节点会自动限制到 1024。
3. `image_batch` 设为 1，或视频 `frame_batch` 降到 1。
4. `quality_profile` 换成 **`manual`**。
5. `memory_policy` 换成 **`staged`**。
6. 关掉 `torch_compile`（尤其是出现 CUDA Graph 或 `cudaMallocAsync` 警告时）。
7. 降低输出倍率，或先把输入缩小一点。

`speed` 比 `manual` 慢通常不是玄学：更大的 tile batch 或视频 VAE tile 会抬高显存峰值，
导致模型反复换载、或 Windows WDDM 用上共享显存。
此时 **`manual` + `tile_size=512` + `vae_tile_size=1024`** 通常最稳。

---

## 本版改动（相对原加速版）

**改名**

- 节点 ID：统一为 `AICG3D_VOSR2*`
- 菜单分类：统一为 `AICG3D/VOSR2`
- 显示名、日志标签、报错信息：统一为 `AICG3D-VOSR2`
- 四个 `.pyd` 内共 80 处品牌字符串以**等长替换**方式改写
  （直接改短会让 `.pyd` 内部地址偏移错位、文件损坏，所以短出的字节用空格补齐，再由 `__init__.py` 统一去掉）
- 同时清除了编译进 `.pyd` 的原始构建路径与作者痕迹

**修复**

1. `backend/tiled_vae.py` — 输入边长小于 8 像素时，`reflect` 填充会直接抛 `RuntimeError`
   （reflect 要求填充量小于边长），现在自动回退 `replicate`。
2. `backend/tiled_vae.py` — 分块编解码的加权累加改用 `float32`：
   重叠区是多块加权叠加，原来按潜变量自身精度（可能是 bf16）累加会累积舍入误差。

**说明**

- 核心推理调度（分块策略、显存策略、视频流式、DINO 时序缓存）编译在
  `nodes.pyd` / `inference.pyd` / `model_store.pyd` / `settings.pyd` 内，
  发行版未附带源码，因此本仓库无法修改或进一步优化这部分。
- `backend/` 与 `backend/models/` 保留了各自上游的版权与许可注释，请勿删除。

---

## 许可

本仓库以 **Apache License 2.0** 发布，全文见 [LICENSE](LICENSE)。

**为什么不是 GPL？** 本插件包含原作者的 **编译后二进制（`.pyd`）且没有对应源码**。
GPL 会要求分发二进制时提供完整源码，我们提供不了；Apache-2.0 则允许以二进制形式再分发
（前提是保留版权与许可声明）。此外上游的 ComfyUI-VOSR2 与 VOSR 本身也是 Apache-2.0，兼容且授权明确。

---

## 版权与法律声明

**1. 免费开源**

本插件**永久免费、开源**。任何人都可以自由使用、修改、再分发（遵循 Apache-2.0 条款）。
本项目不收取任何费用，也不存在任何"付费版""解锁版"。

**2. 署名**

再分发或整合本插件时，请保留本 README、[LICENSE](LICENSE) 与
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) 中的全部署名与许可声明。
删除原作者署名后再分发，属于违反上游许可的行为，请不要这么做。

**3. 非官方声明**

本仓库是**第三方修改版**，与原加速版作者、`ylchen333`、`cswry`、ComfyUI 官方均
**无隶属、赞助、合作或背书关系**。请勿把本插件误认为任何上游项目的官方发布。
本仓库使用的第三方名称与商标归其各自所有者，此处仅作说明性引用。

**4. 免责声明**

- 本插件按"现状"提供，**不提供任何明示或暗示的担保**，包括但不限于适销性、特定用途适用性与非侵权担保。
- 使用本插件产生的任何后果（包括但不限于运行失败、显存耗尽、数据损坏、输出内容不合预期）
  由使用者自行承担，作者不承担任何责任。
- 本插件仅提供超分辨率/放大功能，**不对使用者输入与输出的内容负责**。
- 请遵守你所在国家/地区的法律法规使用本插件，**不得**将其用于生成、制作、传播任何违法违规内容。

**5. 模型权重**

本仓库**不包含、也不分发任何模型权重**。VOSR2 权重来自 [CSWRY/VOSR](https://huggingface.co/CSWRY/VOSR)，
其版权与使用条款归发布者所有，使用前请自行阅读并遵守。

**6. 侵权处理**

我们尊重每一位原作者的权利。如果你是权利人，认为本仓库的内容侵犯了你的权益，请通过
**GitHub Issue** 或在本仓库留下联系方式告知我们。我们会在核实后**立即删除或调整相关内容**，
不设任何门槛、不要求你先证明什么。我们无意侵占任何人的劳动成果。

**7. 关于二进制组件**

`nodes.pyd` / `inference.pyd` / `model_store.pyd` / `settings.pyd` 是原加速版作者编译发布的二进制组件，
原发行版**未附带源码、也未声明许可证**。本仓库按"原样"再分发这些组件，并在此**明确署名原始作者**。
如原作者对此有异议，请联系我们，我们会立刻下架相关组件或按你的要求处理。

---

## 更新日志

### v1.0（AICG3D 整理版）

- 统一到 AICG3D 命名空间（节点 ID / 分类 / 显示名 / 日志 / 报错 / 编译期路径）
- 修复极小输入下 `reflect` 填充崩溃
- 修复分块编解码累加精度损失
- 补齐 README、LICENSE、第三方声明

---

## English

**AICG3D-VOSR2** is a community ComfyUI custom node for **VOSR 2.0** image / video super-resolution,
with tiled inference, VRAM-aware scheduling, video optimizations and SageAttention support.

> This is an **unofficial third-party fork**, renamed into the `AICG3D` namespace and with two bug fixes.
> It is **not affiliated with, sponsored by, or endorsed by** the original authors of VOSR / VOSR2 or ComfyUI.
> All credit for the original model, node package and acceleration work belongs to the authors listed in
> [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

- Nodes: `AICG3D_VOSR2Loader`, `AICG3D_VOSR2Settings`, `AICG3D_VOSR2Image`, `AICG3D_VOSR2Video`
  (category `AICG3D/VOSR2`)
- Model weights are **not** included; get them from <https://huggingface.co/CSWRY/VOSR> and read their terms.
- Licensed under **Apache-2.0**. Provided **as is**, without warranty of any kind.
- Rights holders: if you believe this repository infringes your rights, open an issue and we will
  remove or adjust the content promptly.
