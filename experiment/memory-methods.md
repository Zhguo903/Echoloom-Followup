# 六种实验方法的定义与实现框架

## 总体原则

六种方法使用**同一个底层大语言模型**，主要区别不在模型本身，而在于：

* 当前对话会搭配哪些 memory 输入给模型；
* memory 是否经过筛选；
* 筛选依据是什么；
* 是否采用 one-pass 或 two-pass；
* 被拒绝的 memory 是否会从最终生成阶段中移除。

这样可以尽量保证实验比较的是 **memory-use method 的差异**，而不是不同基础模型之间的能力差异。

---

## Method 1：No Memory

### 定义

模型完全不使用任何长期记忆，只根据当前对话生成回复。

### 基本实现

输入：

**Current Dialogue**

↓

直接发送给固定的 LLM

↓

生成最终回复

不提供任何 candidate memories。

### 主要作用

作为**无个性化基线**。

它用于回答：

> 如果完全不使用长期记忆，回答质量、自然度和关系连续性会怎样？

同时可以帮助判断其他方法的优势是否真正来自"正确使用 memory"。

---

# Method 2：All-Candidate Memory

### 定义

系统已经获得一组 candidate memories，但不进行额外判断，直接把所有候选记忆提供给模型。

### 基本实现

输入：

**Current Dialogue**

*

**All Candidate Memories**

↓

固定 LLM

↓

最终回复

模型自行决定如何使用这些 memory。

### 主要作用

模拟一种比较简单的：

> Retrieve → Put Everything Into Context → Generate

架构。

主要观察当所有相关或可能相关的记忆都暴露给生成模型以后，是否会出现：

* 不必要的个性化；
* 敏感记忆被主动提起；
* stale memory 使用；
* repetition；
* episode-to-trait；
* context leakage。

---

# Method 3：Similarity Top-k

### 定义

系统主要根据**语义相关性**选择与当前对话最相似的若干条 memory，然后交给模型生成回复。

### 基本实现

首先计算：

**Current Dialogue**

与

**Candidate Memories**

之间的 semantic similarity。

然后按照 similarity 排序。

例如：

M1 → 0.87
M2 → 0.76
M3 → 0.42
M4 → 0.15

如果设定 Top-2，则选择：

M1 + M2

↓

将选出的 memory 和当前对话一起交给固定 LLM

↓

生成最终回复。

### 主要作用

代表传统的 **relevance-based retrieval / RAG-style memory use**。

它主要测试：

> "和当前话题相关"是不是已经足够决定一条 memory 应该被使用？

这是 Reconsider-Lite 最核心的对照之一，因为本研究认为：

> **Relevance 不等于 conversational warrant。**

一条 memory 即使语义相关，也可能不适合在当前情境中被提起。

---

# Method 4：One-Pass Selective Prompt

### 定义

所有 candidate memories 都提供给模型，但在 prompt 中明确要求模型：

> 只有在合适的时候才使用 memory。

模型在一次调用里同时完成：

**判断 memory 是否合适 + 生成最终回复。**

### 基本实现

输入：

**Current Dialogue**

*

**All Candidate Memories**

*

一个 selective-use instruction，例如要求模型：

* 只使用真正有帮助且合适的记忆；
* 避免 stale memory；
* 避免敏感内容的不必要 callback；
* 避免 repetition；
* 不要把一次经历扩大成长期人格。

↓

固定 LLM 一次调用

↓

最终回复。

### 主要作用

测试：

> 是否只需要给现有 LLM 一个更好的 prompt，就已经可以解决 memory-use boundary 问题？

这是一个重要 baseline。

如果 One-Pass 已经和 Reconsider-Lite 表现相当，那么两阶段架构的必要性就会减弱。

---

# Method 5：Relevance-Only Two-Pass

### 定义

采用 two-pass architecture，但第一阶段只判断：

> 哪些 memory 与当前话题相关？

不做完整 relational judgment。

### 基本实现

## Stage 1：Relevance Selection

输入：

**Current Dialogue**

*

**Candidate Memories**

↓

第一次调用固定 LLM

↓

输出：

哪些 memory relevant / irrelevant。

例如：

M1 → Keep
M2 → Keep
M3 → Reject
M4 → Reject

---

## Controller

普通程序根据 Stage 1 的结果：

* 保留 selected memories；
* 删除 rejected memories。

---

## Stage 2：Response Generation

第二次调用固定 LLM。

输入只包括：

**Current Dialogue**

*

**Selected Memories**

↓

生成最终回复。

### 主要作用

这个方法主要用于控制：

> Reconsider-Lite 的优势是不是仅仅来自 "two-pass + filtering"？

因此：

**Method 4 vs Method 5**

可以帮助观察：

> 物理过滤 memory 是否比 one-pass prompt 更有效？

而：

**Method 5 vs Method 6**

可以进一步观察：

> relational deliberation 是否比单纯 relevance 判断提供额外价值？

---

# Method 6：Reconsider-Lite

### 定义

这是本研究的 proposed method。

它不只判断：

> memory 是否相关，

而是单独建立一个 **Relational Deliberation Stage**，判断：

> 这条 memory 在当前关系和情境下，到底应不应该被使用，以及应该以什么方式使用。

---

## Stage 1：Relational Deliberation

输入：

**Current Dialogue**

*

**Structured Memory Cards**

每条 memory card 可以包含：

* memory content；
* memory type；
* timestamp；
* source；
* currentness；
* sensitivity；
* owner；
* branch；
* callback count；
* scope qualifier。

Deliberator 根据 relational criteria 判断，例如：

* Relevance；
* Conversational Warrant；
* Currentness；
* Scope；
* Sensitivity；
* Repetition；
* Ownership / Branch；
* Overgeneralization Risk。

然后为每条 memory 选择一种 action：

### IGNORE

本轮完全不使用。

### SCOPED_IMPLICIT

可以利用 memory，但不明确告诉用户"我记得"。

### SCOPED_EXPLICIT

可以明确 callback，但必须保留原来的时间、情境和范围限定。

### ASK_FIRST

在使用敏感或关系风险较高的 memory 前先询问用户。

---

## Stage 2：Deterministic Controller

普通程序根据 Stage 1 输出处理 memory。

例如：

* IGNORE → 从 generation context 中删除；
* SCOPED_IMPLICIT → 保留，并标记 implicit；
* SCOPED_EXPLICIT → 保留，并标记 explicit；
* ASK_FIRST → 不直接暴露 memory 内容，只允许生成 permission question。

关键点是：

> 被拒绝的 memory 会被真正从第二阶段输入中移除。

生成模型不是"看到了但被要求不要用"，而是根本看不到它。

---

## Stage 3：Constrained Response Generation

第二次调用同一个固定 LLM。

输入：

**Current Dialogue**

*

**Only Admitted Memories**

*

对应的使用方式和 scope constraints。

↓

生成最终回复。

### 主要作用

测试本研究的核心假设：

> 在 memory retrieval 和 response generation 之间加入一个独立的 relational decision layer，是否可以减少不合适的 memory use，同时保留真正有益的个性化和关系连续性。

---

# 六种方法之间的整体关系

可以把它们理解成一个逐步增加 memory-control 能力的梯度：

**Method 1 — No Memory**
完全不用 memory

↓

**Method 2 — All Candidates**
有 memory 就全部交给模型

↓

**Method 3 — Similarity Top-k**
先按照语义相关性筛选

↓

**Method 4 — One-Pass Selective Prompt**
让模型自己在一次生成中判断什么该用

↓

**Method 5 — Relevance-Only Two-Pass**
把筛选和生成分开，但只判断 relevance

↓

**Method 6 — Reconsider-Lite**
把筛选和生成分开，并加入完整 relational judgment

---

# Human Oracle

Human Oracle 建议**不计入六种正式方法**，而作为额外 reference condition。

它直接使用人类标注者认为最合适的：

* selected memories；
* preferred actions；
* required qualifiers。

然后再让同一个 generator 生成回复。

它的作用是提供一个近似的：

> **Human-grounded upper bound**

帮助判断：

如果 memory decision 已经完全按照人的判断完成，最终回答理论上能够达到什么水平。

---

# 最终实验框架

正式实验时，每一个 canonical scenario 都分别经过六种方法：

**同一个 Scenario
×
同一个 Candidate Memory Set
×
同一个底层 LLM**

唯一改变的是：

**Memory Processing Method**

最终形成：

**24 个 scenarios × 6 种 methods × 5 次重复 = 720 条模型输出。**

这样可以系统比较：

* inappropriate memory use；
* beneficial memory retention；
* scope fidelity；
* context / branch leakage；
* stale memory use；
* repetition；
* episode-to-trait；
* relational appropriateness；
* 最终用户体验。

具体的 prompt wording、Top-k 参数、JSON schema、controller rules 和 API 实现方式，在正式开发阶段再基于 development / pilot scenarios 进一步确定并冻结。
