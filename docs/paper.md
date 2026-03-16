# EnLIghTenED
- **E**mpoweri**n**g the **L**atent **I**ntelli**g**ence of LLMs throug**h** **T**emporal Windows on Log Str**e**ams a**n**d **E**volutionary **D**emocratic Processes
---

Jared Yu

# Abstract 
A view of current implementations of agentic AI systems ("AI Engineering") can be summarized as largely static end-to-end data pipelines where data enters as input and follows roughly deterministic patterns where unstructured data (e.g., text) is sent to an LLM and its output is processed for downstream applications and data lakes. In other words, agentic AI systems lack much agency of their own. We can potentially unlock a new way of multi-agent behavior that is distinct from what can be found in existing research and applications (e.g., AutoGen, CrewAI, LangGraph). With the combination of an efficient log stream (via Apache Fluss) and a simple democratic voting algorithm, what emerges is an organic free-flowing society of LLMs that cocreate and codiscover the world.

# 1. Introduction

The crux of the problem possibly is that the industry as a whole has a narrow view and therefore application of what LLMs are and how they can be used. This is similar to a student's realization in linear regression that $\hat{y}=mx+\hat{b}$ can be rewritten as $\mathbf{\hat{y}}=\mathbf{X\hat{\beta}}=\mathbf{X(X^TX)^{-1}X^Ty}$, the former is just the case for that where $i=1$. Simply reformatting the existing math allows for unlocking a broader view of the problem, and therefore space for novel methods and applications.

The reasoning for this could potentially be contributed to the tools available, when working with AI agents, (Python) developers likely utilize their biases to envision only this sort of left to right, unidirectional pattern of potential actions - with perhaps some loops encoded in between. The key to unlocking a new view lies in the engineering side of the problem (i.e., the infrastructure), not the LLMs themselves.

In this paper, a novel approach towards agentic AI is proposed. We can unlock the underlying strength of LLMs by empowering their latent ability to communicate amongst others in a chatroom-style setting. Combined with a stream-of-consciousness technology, a set of AI agents with corresponding roles (e.g., software architect, project manager, software engineer, software QA tester, and business user) can interact organically in a democratic voting (elaborated on in 2.3) environment, like students collaborating on a group project.

# 2. Methods

## 2.1 The Chatroom Experience
Anecdotally, through an experiemnt using Gemini 3.1 Pro [https://gemini.google.com/app/439e4af37721f8c1], the LLM is capable of roleplaying multiple characters within the chat (beyond the assumed 1:1 chat interface). For example, by simply appending a prefix (i.e., [Human A] and [Human B]) before the user speaks, the LLM is able to follow along and treat each user distinctively, going so far as to add [Gemini] as a prefix to itself before it speaks. This allows for a chatroom-style interaction where LLMs can communicate and navigate amongst various characters in a conversation. This existence of this latent intelligence is logical given that the training data on LLMs likely contains ample chatroom data and plays (e.g., Shakespeare where multiple characters speak in succession).

This format for multi-agent behavior is not too different from what can be seen in AutoGen, the difference being that AutoGen has a single manager that orchestrates the entire flow. The weakness is that this single manager agent is tasked with orchestrating numerous agents over time within a limited context window, this will be elaborated on in 2.2.2.

Some familiarity of how modern LLMs chat with users is needed to understand how this multiuser chatroom can be built into the system.

## 2.2 Log Streams

### 2.2.1 Moving Towards the Streamhouse
Traditional data lake / lakehouse architectures allow for data to be ingested rapidly and processed later for downstream applications (e.g., web apps, dashboards, etc.). However, this process requires batch jobs (e.g., scheduled Apache Spark jobs on top of an Apache Iceberg medallion-based data lake) where data moves from source to destination over periods of time. The data industry still lacked a way to both ingest and analyze data in real-time, a "streamhouse" - until recently.

With Apache Fluss (incubating), this streamhouse architecture is slowly coming to fruition. From the AI perspective, this makes us think, with real-time streaming ingest and inference on data, what are the possibilities? Already, Chinese tech company Alibaba (and its business unit Taobao) already have use cases for this.

Through experimentation, it can be seen that this easy-to-implement streaming log systems enables a novel way of orchestrating AI agents. By funneling LLM outputs to a universally shared log stream, it creates a format where all agents can universally read and write to the same log, creating a shared understanding of the world. Of course, in smaller experiments, this process can be replicated easily using existing database methods. However, the simplicity of Fluss in this case makes the prospects of doing so far more trivial.

This is essentially a Pub/Sub pattern, where actions by agents are sent to the stream and agents in turn all receive the same message.

### 2.2.2 Temporal Window

### 2.2.3 Remember to Forget
- critical forgetting vs catastrophic forgetting

## 2.3 Democratic Processes
- organic conversation - emergent culture/society with a unified purpose (single mind/hive mind)

# 3. Results

# 4. Conclusion

## 4.1 Future Work
- stream consciousness for robotics - agents acting on a unified world view
- container claw for safe tool use

# 5. References
