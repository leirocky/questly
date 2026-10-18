# 约拿的故事 — 圣经绘本动画

一部约 9 分 51 秒的中文绘本风格视频，按《约拿书》1–4 章完整讲述，有旁白和人物配音、背景音乐、音效和字幕。
成片：[`output/jonah_story.mp4`](output/jonah_story.mp4)（仓库里是 1280×720 版本，约 90 MB，因为 GitHub 单个文件
上限 100 MB；1920×1080 完整画质版约 175 MB，运行 `python3 build.py all` 会生成到同一路径，不要提交它）。
第一版（2 分 19 秒）的剧本保留在 `story_v1.py`，场景在 `art/scenes_v1/`。

这个文件夹完全独立，和 Questly 应用的代码无关。画面、配音、配乐、音效都由代码生成，没有使用外部素材。

## 怎么做出来的

| 部分 | 做法 | 主要文件 |
| --- | --- | --- |
| 故事稿 | 按和合本改写成适合 3–8 岁孩子的 24 个场景、91 句（旁白 + 上帝、约拿、船长、水手、国王的台词）；逐个核对多音字读音 | `story.py` |
| 配音 | sherpa-onnx 离线语音合成，所有角色都用 ZipVoice 整句合成、模仿一段音色样本：旁白模仿 matcha-zh-baker 女声（语速 0.85）；上帝、约拿、船长、水手、国王分别模仿 Kokoro v1.1-zh 的不同男声；上帝加轻微回声，鱼腹中加闷响；逗号和句末停顿另外拉长。认可的配音存在 `voice/takes/` | `voice/tts.py`、`voice/lexicons.py` |
| 配音校验 | 用 SenseVoice 语音识别把每句配音转回文字，与原稿比对 | `voice/check.py` |
| 画面 | SVG 分层绘制，用无头 Chromium 光栅化，加水彩纹理和纸张质感；OpenCV 合成器负责动画、镜头和特效 | `art/`、`engine/` |
| 角色与道具 | 约拿、水手、船长、国王、尼尼微人、大鱼、船、蓖麻、动物、建筑等共用库，保证各场景造型一致 | `art/characters.py`、`art/props.py` |
| 场景 | 24 个场景，每个都按旁白和字幕时间编排动作，相邻场景的首尾画面互相对齐 | `art/scenes/s01_title.py` … `s24_end.py` |
| 配乐 | 程序作曲生成 MIDI，用 fluidsynth + MuseScore General 音色渲染，每个场景一段配乐，"约拿主题"贯穿始终；重音对准旁白里的词或画面动作（直接读取场景的音效时间） | `audio/score.py`、`audio/cues_a…e.py`、`audio/picture.py`、`audio/music.py` |
| 音效 | 42 种程序合成音效（海浪、风暴、雷声、吞咽、划桨、号角、锤子、鸡鸣等） | `audio/sfx.py` |
| 混音 | 音乐和音效在说话时自动压低（句间短停顿不回升，避免忽大忽小）；关键动作音效可单独少压；每句台词在 300–4000 Hz 语音频段比背景高至少 12 dB；全片 −16 LUFS，真峰值 −1.7 dBTP | `audio/mix.py` |
| 合成 | 场景之间 1 秒交叉淡化（进鱼腹淡到黑，出鱼腹用清晰的圆形展开），先做高质量母版，再两遍编码 | `engine/assemble.py` |

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

场景片段有缓存：只有改动过的场景（及与它首尾衔接的相邻场景）会重新渲染。v2 完整重建在 4 核机器上约 1 小时（渲染场景约 40 分钟）。

### 在自己电脑上接着做

云端会话可以用 Claude Code 拉到本地继续：在本仓库的本地克隆里（工作区要干净，登录同一个账号）运行
`claude --teleport`，选这个会话即可。它带过去的是对话记录和已推送的分支；云端正在跑的后台任务和
没提交的文件不会带过去，所以中途的生成结果要先提交推送。`build/`、`.cache/` 不进 git，本地第一次运行
`./setup.sh` 下载模型（解压后约 1.5 GB）。已认可的配音原始片段存在 `voice/takes/`（FLAC），
所以本地 `python3 build.py all --jobs 8` 重新生成时用的是同一批配音，不会合成出另一版；
改了台词的句子才会重新合成（之后用 `python3 tools/save_takes.py` 把新的认可版本存进去）。
`--jobs 8` 让 10 核机器并行渲染 8 个场景。

## 验证结果（v2，本次生成）

- 配音：91 句全部用 SenseVoice 语音识别转回文字比对，平均字错率 0.8%，最差一句 14%（"约拿"被识别成同音的"曰拿"）。
- 混音：每句台词在语音频段比背景高 12.3 dB 以上；全片 −16.0 LUFS，成片 AAC 峰值 −1.3 dBFS。
- 配乐：21 项自动检查全部通过（时长、无削波、和声无冲突、无平行五度和八度、重音对准画面）；13 种改变时间轴的稳健性测试通过。
- 画面：每个场景都经过"绘制 → 独立审稿 → 修改"；整片经过分段审片和全片连贯性审查（35 个中高严重度问题经独立复核确认），
  两轮打磨，按场景逐条复查共 90 个问题（80 个当轮确认修好，其余再修）。最后一版由我抽查了全部 23 个转场和几处改动，
  没有再派代理整片复查。
- 以上都是程序测量和看帧检查，没有人用耳朵听过混音，也没有在实体手机上播放测试。

## 已知限制

- 画面是矢量绘制加程序纹理，不是手绘或 AI 生成的插画；动作用分层动画和少量逐帧图实现。
- 配音是离线语音合成，语调比真人朗读平一些。
- 只在桌面和云端环境渲染检查过，没有在实体手机上播放测试。
