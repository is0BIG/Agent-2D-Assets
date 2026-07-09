# Generate2DAudio 中文使用手册

`$generate2daudio` 是 Agent-2D-Assets 新增的 2D 游戏音频技能。它面向 Codex 工作流：Codex 负责判断需要什么声音包，本地 Python 脚本负责生成简单音效、清理已有 WAV、分析音量和导出元数据。

## 适合做什么

- UI 音效：click、confirm、cancel、error。
- 动作音效：jump、land、hit、pickup、powerup。
- 战斗和法术：explosion、laser、spell-cast、spell-loop、spell-hit。
- 已有音频清理：裁掉静音、加淡入淡出、标准化音量、输出分析 JSON。
- 引擎交付：Godot、Unity、Web 或 raw 2D 项目的 WAV 和 manifest。

## 快速开始

生成 UI 音效包：

```text
Use $generate2daudio to create a retro UI sound pack with click, confirm, cancel, and error WAV files plus engine-ready metadata.
```

生成火球技能音效包：

```text
Use $generate2daudio to create a fantasy fireball audio bundle with cast, loop, and impact sounds for Godot.
```

处理已有 WAV：

```text
Use $generate2daudio to clean raw.wav, trim silence, fade out 30ms, normalize to -1 dBFS, and export analysis metadata.
```

## 本地脚本用法

生成单个音效：

```powershell
python .\skills\generate2daudio\scripts\synthesize_sfx.py --sound pickup --output .\outputs\audio\pickup.wav
```

生成预设包：

```powershell
python .\skills\generate2daudio\scripts\synthesize_sfx.py --preset ui-pack --output-dir .\outputs\audio\ui
```

清理已有 WAV：

```powershell
python .\skills\generate2daudio\scripts\process_audio.py `
  --input .\raw.wav `
  --output .\outputs\audio\clean.wav `
  --trim-silence `
  --fade-in-ms 5 `
  --fade-out-ms 30 `
  --normalize-peak-db -1
```

分析 WAV：

```powershell
python .\skills\generate2daudio\scripts\analyze_audio.py --input .\outputs\audio\pickup.wav
```

## 输出结构

单个音效通常包含：

```text
pickup.wav
pickup.analysis.json
```

音效包通常包含：

```text
click.wav
confirm.wav
cancel.wav
error.wav
click.analysis.json
confirm.analysis.json
cancel.analysis.json
error.analysis.json
audio-pack.json
```

## 元数据重点

`analysis.json` 会记录：

- `duration_seconds`：时长。
- `sample_rate`：采样率，默认 44100。
- `channels`：声道数，默认输出 mono。
- `peak_dbfs`：峰值音量。
- `rms_dbfs`：平均响度参考。
- `clipping_samples`：削波采样数，理想值是 0。
- `loop`：是否作为循环音频交付。

## 注意事项

- 当前本地合成适合短音效，不适合高质量音乐、人声或复杂环境声。
- 对于 BGM、配音、复杂 ambience，建议把该技能作为规划、清理、分析和交付层，生成源可以接入后续音频模型或人工素材。
- 商业项目请使用原创或已授权的音频素材。
