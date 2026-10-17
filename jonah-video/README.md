# 约拿的故事 — 圣经绘本动画

一部约 2 分 19 秒的中文绘本风格视频，讲述《约拿书》1–4 章，有旁白配音、背景音乐、音效和字幕。
成片：[`output/jonah_story.mp4`](output/jonah_story.mp4)（1920×1080，30 fps，H.264 + AAC，约 41 MB）。

这个文件夹完全独立，和 Questly 应用的代码无关。画面、配音、配乐、音效都由代码生成，没有使用外部素材。

## 怎么做出来的

| 部分 | 做法 | 主要文件 |
| --- | --- | --- |
| 故事稿 | 按和合本改写成适合 3–8 岁孩子的 13 个场景、42 句旁白；逐个核对多音字读音 | `story.py` |
| 配音 | sherpa-onnx 离线语音合成：旁白用 matcha-zh-baker 女声；上帝用 Kokoro v1.1-zh 101 号低沉男声，加轻微回声；约拿用 Kokoro 91 号男声，鱼腹中的祷告加闷响 | `voice/tts.py` |
| 配音校验 | 用 SenseVoice 语音识别把每句配音转回文字，与原稿比对 | `voice/check.py` |
| 画面 | SVG 分层绘制，用无头 Chromium 光栅化，加水彩纹理和纸张质感；OpenCV 合成器负责动画、镜头和特效 | `art/`、`engine/` |
| 角色与道具 | 约拿、水手、船长、国王、尼尼微人、大鱼、船、蓖麻、动物、建筑等共用库，保证各场景造型一致 | `art/characters.py`、`art/props.py` |
| 场景 | 13 个场景，每个都按旁白时间编排动作 | `art/scenes/s01_title.py` … `s13_end.py` |
| 配乐 | 程序作曲生成 MIDI，用 fluidsynth + MuseScore General 音色渲染，每个场景一段情绪配乐，"约拿主题"贯穿始终 | `audio/score.py`、`audio/music.py` |
| 音效 | 34 种程序合成音效（海浪、风暴、雷声、吞咽、钟声、鸟鸣等） | `audio/sfx.py` |
| 混音 | 音乐和音效在说话时自动压低；每句旁白在 300–4000 Hz 语音频段比背景高至少 12 dB；全片 −16 LUFS | `audio/mix.py` |
| 合成 | 场景之间交叉淡化（鱼腹前淡到黑，出鱼腹用圆形展开），先做高质量母版，再两遍编码成约 41 MB 的成品 | `engine/assemble.py` |

美术规范见 [`ART_GUIDE.md`](ART_GUIDE.md)。上帝始终不画成人形，只用金色光芒和声音表现。

## 重新生成

一键安装依赖和语音模型：`./setup.sh`（Ubuntu 24.04 或装了 Homebrew 的 macOS）。多代理制作流程脚本在 [`workflows/`](workflows/)。

手动安装时的依赖（Ubuntu）：

    apt-get install fluidsynth musescore-general-soundfont fonts-lxgw-wenkai fonts-noto-cjk ffmpeg
    pip install sherpa-onnx==1.13.8 playwright==1.56.0 opencv-python-headless numpy scipy soundfile pyloudnorm \
      pillow mido pypinyin==0.55.0 zstandard

macOS 上 `setup.sh` 会做这些事：`brew install ffmpeg fluid-synth`；把霞鹜文楷 v1.315
（和 Ubuntu 同一版本，之后的版本把 Bold 改名成了 Medium）装进 `~/Library/Fonts`；
`tools/fetch_soundfont.py` 把同一个 MuseScore General 音色库下到 `.cache/soundfonts/`；
`python3 -m playwright install chromium`；Python 包装在 `jonah-video/.venv`（先 `source .venv/bin/activate`）。字体和音色库也可以用环境变量 `JONAH_FONT_DIR`、
`JONAH_SOUNDFONT` 指定。

Chromium 用 Playwright 自带的（Linux 上先找 `PLAYWRIGHT_BROWSERS_PATH`，默认 `/opt/pw-browsers`）。
语音模型放在 `.cache/models/`，由 `setup.sh` 从 https://github.com/k2-fsa/sherpa-onnx/releases 下载：
Kokoro v1.1、Matcha zh-baker、ZipVoice distill zh-en、vocos 声码器，以及校验用的 SenseVoice 识别模型。

    cd jonah-video
    python3 build.py all        # 配音 → 配乐 → 渲染场景 → 混音 → 合成，输出 output/jonah_story.mp4
    python3 build.py check      # 语音识别校验每句配音

单独调试某个场景：

    python3 tools/preview.py s04_storm --lines   # 每句旁白中间各出一张静帧
    python3 tools/preview.py s04_storm --clip    # 带配音的场景小样
    python3 tools/preview.py s04_storm --bench   # 每帧渲染耗时

场景片段有缓存：只有改动过的场景会重新渲染。完整重建在 4 核机器上约 20–30 分钟。

### 在自己电脑上接着做

云端会话可以用 Claude Code 拉到本地继续：在本仓库的本地克隆里（工作区要干净，登录同一个账号）运行
`claude --teleport`，选这个会话即可。它带过去的是对话记录和已推送的分支；云端正在跑的后台任务和
没提交的文件不会带过去，所以中途的生成结果要先提交推送。`build/`、`.cache/` 不进 git，本地第一次运行
`./setup.sh` 下载模型（解压后约 1.5 GB）。已认可的配音原始片段存在 `voice/takes/`（FLAC），
所以本地 `python3 build.py all --jobs 8` 重新生成时用的是同一批配音，不会合成出另一版；
改了台词的句子才会重新合成（之后用 `python3 tools/save_takes.py` 把新的认可版本存进去）。
`--jobs 8` 让 10 核机器并行渲染 8 个场景。

## 验证结果（本次生成）

- 配音：42 句全部通过语音识别比对，平均字错率 2.4%，剩下的差异都是同音字（如 尼尼威/尼尼微）。
- 混音：每句旁白在语音频段比背景高约 12 dB 以上；全片 −16 LUFS，峰值约 −1 dBFS。
- 配乐：自动检查全部通过（时长、无削波、和声无冲突、无平行五度和八度）。
- 画面：先后有 5 个独立代理逐场审片，19 个较严重的问题全部修复，并经第二轮复查确认。

## 已知限制

- 画面是矢量绘制加程序纹理，不是手绘或 AI 生成的插画；动作用分层动画和少量逐帧图实现。
- 配音是离线语音合成，语调比真人朗读平一些。
- 只在桌面和云端环境渲染检查过，没有在实体手机上播放测试。
