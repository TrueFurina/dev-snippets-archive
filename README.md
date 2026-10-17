# dev-snippets-archive

> 一份从「开发垃圾抽屉」里**精选**出来的、可安全公开的小工具与 OSS 贡献补丁集合。
> 这不是一个被维护的库，而是一份**清理日志 + 可复用碎片**的存档。

## 这个仓库是怎么来的

作者在家目录顶层堆积了 **54MB / 158 项**散落文件（`C:\Users\Lenovo\_归档区_20261017`）：
一次性调试脚本、截图、HTML 抓取、压缩包、实验残留目录、各种 dotfiles。

在上传 GitHub 之前做了一轮**涉密 / 隐私 / 第三方代码**扫描，最终只保留了下面这些
**原创、独立、且不含任何密钥或个人身份信息（PII）** 的文件。其余全部**排除**，原因见下。

## 包含内容

| 文件 | 用途 | 来源性质 |
|------|------|----------|
| `torch_cuda_test.py` | 3 行 PyTorch CUDA 可用性自检（版本 + 算力 + 异常捕获） | 原创、独立可运行 |
| `scan_mergeable.py` | 拉取自己名下全部 open PR 并按 `mergeable_state` 分类，找出可推进的 PR | 原创；`GITHUB_TOKEN` 从环境变量读取，**无硬编码密钥** |
| `crlf_conflicts_check.py` | 诊断 PR 中由 CRLF 行尾导致的「假冲突 / churn」 | 原创；同上，Token 走环境变量 |
| `contrib-patches/ae76a88-fix.patch` | 修正某项目静态红线测试的误报（`shodan`/`scapy` 子串误判等） | 作者本人的 OSS 贡献 |
| `contrib-patches/tenacity_tenacity_wait.py.patch` | `tenacity` 库 `wait_exponential(multiplier=0)` 在大 attempt 数下 `OverflowError` 的修复（issue #710） | 作者本人的 OSS 贡献 |
| `contrib-patches/tenacity_tests_test_tenacity.py.patch` | 上述修复的回归测试 | 作者本人的 OSS 贡献 |

## 被排除的内容（以及为什么）

原归档里**绝大多数是不能公开**的，公开会泄露密钥 / 隐私或构成对第三方代码的误归属：

- **个人 dotfiles（14 个）**：`.claude.json`、`.npmrc`、`.gitconfig`、`.condarc` 等。
  这些文件可能含有 API Token / 认证信息 / 历史记录，**严禁 `git add` 整个家目录**。
- **截图（48 张 PNG/JPEG）**：登录页、学生/教师后台、面试评估报告、二维码等 —— 含 PII。
- **HTML 抓取（20 个）**：`profile_check*.html`、`*_profile.html` 等被抓取的网页档案 —— 含他人 PII。
- **第三方源码碎片**：`gorequest.go`（整份 parnurzeal/gorequest 库）、`apikey.py.fixed` /
  `websocket_example.py.fixed` / `playground.py.fixed`（OpenALGO 项目的 Blueprint 片段）。
  这些是**别人的开源代码**，不属于我，且不可独立运行，公开即误归属 + 冗余。
- **压缩包（2 个）**：`CTFd.tar.gz`、`fastapi.tar.gz` —— 第三方源码快照，无再分发价值。
- **实验残留目录（10 个，~15MB）**：含竞赛内部文档（`qc_a_tmp`）、向量库数据等，敏感且非通用。
- **论文草稿**：`revised_ch2.md` / `revised_ch6.md` —— 毕设章节，不宜公开。
- **一次性调试脚本（约 50 个）**：`fix_openalgo_*`、`fix_tenacity_*`、`check_round*` 等，
  均绑定特定项目在特定时间点的临时状态，无可复用性。

## 安全经验（重要）

1. **永远不要 `git add .` 你的家目录或桌面**。那里躺着 `.claude.json` / `.npmrc` /
   `.gitconfig`，八成藏着 token。
2. 需要 Token 的脚本，**只从环境变量读取**（`os.environ['GITHUB_TOKEN']`），绝不写死。
3. 公开前做一轮 `grep -iE "token|secret|password|api[_-]?key"` 全量扫描 + 人工复核。
4. 截图 / HTML 抓取 / 登录页 / 二维码 = PII，默认排除。

## License

- 顶层三个 `*.py` 工具与 `contrib-patches/` 下作者本人的补丁：MIT。
- `contrib-patches/` 中的补丁分别针对各自上游项目（tenacity 等），其权利归属按上游许可证执行；
  此处仅作作者贡献记录存档。
