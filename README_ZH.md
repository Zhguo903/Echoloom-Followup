# Before Bringing It Up / 在提起之前

正确记住，不等于适合在此刻提起。本仓库实现 **Reconsider-Lite**：一个无需训练、位于检索之后的关系记忆决策层。它判断记忆应保持沉默、隐式影响回复、被明确提及，还是先征求许可。

仓库包含离线确定性 demo、六种比较条件、24 个纯合成开发场景、可复现评估工具，以及默认锁定的盲法回复研究界面。Phase 2 还新增了 48 个 held-out 草稿和 16 个 separation-stress 草稿；这 64 个草稿都尚未经过人工内容与研究审核。

最初 24 个场景只用于开发，它们保存的是暂定作者预期，不是人类 gold。未来独立的 Study A 可以收集四种记忆动作的人类分布，但本次没有启用收集；被评估的模型永远看不到作者预期或人类判断。更晚的 Study B 评估最终回复，而不是内部记忆决策。

> 这是研究原型，不是已部署的陪伴服务、治疗工具或安全保证。请先阅读 [研究主张边界](docs/CLAIM_BOUNDARIES.md) 与 [伦理约束](docs/ETHICS.md)。

## 快速开始

需要 Python 3.12+、uv、Node 24+ 与 Corepack/pnpm。

```bash
cp .env.example .env
make setup
make dev
```

浏览器打开 [http://localhost:5173](http://localhost:5173)。API 位于 [http://localhost:8000](http://localhost:8000)。

## Demo 流程

- `/scenarios`：浏览 24 个开发用合成场景；
- `/lab/golden_record_store_weekend_v1`：查看 hard gate、五级决策阶梯和生成上下文物理隔离；
- `/compare/golden_record_store_weekend_v1`：比较六种方法；
- `/sandbox`：本地增删改、纠正或分支合成记忆；
- `/study`：伦理与配置未确认时保持锁定；
- `/runs`：查看本地 SQLite 运行记录。

## 离线 mock 评估

```bash
uv run bbi scenario-lint data/scenarios
uv run bbi scenario-coverage --manifest data/manifests/heldout_core_v1.json
make eval-mock
make analyze-mock
```

Mock 输出只是确定性的合成计算结果，不是参与者研究发现。真实模型密钥只能放在服务端环境变量中，前端不会接收密钥。

Held-out 与 separation manifest 目前明确标记为 `draft` 且未冻结。结构覆盖检查已通过，但在人工完成 `reports/phase2/human_review_queue.csv` 前，研究就绪状态仍是 `not_evaluable`。

## 质量检查

```bash
make lint
make typecheck
make test
make e2e
make build
```

不允许将原始访谈、客户发现问卷、私人聊天、真实参与者资料或未经确认可发布的引语加入本仓库。空结果、混合结果和 `ASK_FIRST` 比沉默更打扰等结果都必须能够被诚实报告。
