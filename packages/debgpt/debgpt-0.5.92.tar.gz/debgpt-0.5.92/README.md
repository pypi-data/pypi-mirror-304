% DebGPT(1) | Chatting LLM with Debian-Specific Knowledge
% Copyright (C) 2024 Mo Zhou <lumin@debian.org>; MIT License.

NAME
====

DebGPT - Chatting LLM with Debian-Specific Knowledge

> "AI" = "Artificial Idiot"


SYNOPSIS
========

`debgpt [GENERAL-OPTIONS] [LOADERS] [--frontend {dryrun,zmq,openai}] [--ask ASK]`
`debgpt [SUBCOMMAND] ...`

[GENERAL-OPTIONS]

`-h, --help`
: show this help message and exit

`--monochrome <true|false>`
: disable colorized output during the conversation

[LOADERS]

`-f FILE, --file FILE`
: load specified file(s) in prompt. A special syntax is supported: "--file filename:start_line:end_line"

`--cmd CMD`
: add the command line output to the prompt

[SUBCOMMAND]

`debgpt genconfig`

`debgpt git commit [--amend]`


DESCRIPTION
===========

*This tool is currently experimental.*

Large language models (LLMs) are newly emerged tools, which are capable of
handling tasks that traditional software could never achieve, such as writing
code based on the specification provided by the user. With this tool, we
attempt to experiment and explore the possibility of leveraging LLMs to aid
Debian development, in any extent.

Essentially, the idea of this tool is to gather some pieces of
Debian-specific knowledge, combine them together in a prompt, and then send
them all to the LLM. This tool provides convenient functionality for
automatically retrieving information from BTS, buildd, Debian Policy, system
manual pages, tldr manuals, Debian Developer References, etc. It also provides
convenient wrappers for external tools such as git, where debgpt can
automatically generate the git commit message and commit the changes for you.

This tool supports multiple frontends, including OpenAI and ZMQ.
The ZMQ frontend/backend are provided in this tool to make it self-contained.

INSTALLATION
============

Install from PyPI or Git repository:

```
pip3 install debgpt
pip3 install git+https://salsa.debian.org/deeplearning-team/debgpt.git
```

Install from source:

```
git clone https://salsa.debian.org/deeplearning-team/debgpt.git
cd debgpt
pip3 install -e .
```

By default, it will only pull the dependencies needed to run the OpenAI
and the ZMQ frontends. The dependencies for other frontends such as
Anthropic, Gemini, are not installed by default. The dependencies for
the self-included LLM backend are also not automatically installed.

CONFIGURATION
=============

Upon fresh installation or not configured at all, running `debgpt` command
will simply print the fresh install instructions. Follow the guide to setup.

By default, the configuration file is placed at `$HOME/.debgpt/config.toml`.
Use `debgpt genconfig` or `debgpt config.toml` to generate a config template.
System-wide configuration file location is not supported.

The minimum configuration needed for `debgpt` to work only involves one
line: `openai_api_key = "your-api-key"`. You can also export the API key
in the environment variable `OPENAI_API_KEY`.

FRONTENDS
=========

Frontend is a client which communicates with an LLM inference backend.
The frontend is responsible for sending the user input to the backend,
and receive the response from the backend, while maintaining a history.

The tool currently have the following list of frontend implementations.
They are specified through the `-F | --frontend` argument.

* `openai`: Connects with a OpenAI API-compatible
  server. For instance, by specifying `--openai_base_url`, you can switch to
  a different service provider than the default OpenAI API server.

* `anthropic`: Connects with Anthropic service. You need to specify
  `--anthropic_api_key` or environt variable `ANTHROPIC_API_KEY` to use this.

* `gemini`: Connects with Google's Gemini service. You need to specify
  `--gemini_api_key` to use this.

* `llamafile`: Connects with a llamafile (single-file LLM distribution).
  See https://github.com/Mozilla-Ocho/llamafile for more information.
  This frontend is implemented in the OpenAI-API compatible way.
  Setting up `--llamafile_base_url` to point to the llamafile service you want
  to use should be enough.

* `ollama`: Connects with ollama service instance.
  See https://github.com/ollama/ollama for more information.
  We currently implement this frontend in the OpenAI-API compatible way.
  Make sure to specify `--ollama_model` to the one being served by the ollama
  service you point to with `--ollama_base_url`.

* `vllm`: Connects with a vllm service instance.
  See https://docs.vllm.ai/en/latest/ for more information.
  This is a OpenAI-API compatible self-hosted service.

* `zmq`: Connects with the built-in ZMQ backend.
  The ZMQ backend is provided for self-hosted LLM inference server. This
  implementation is very light weight, and not compatible with the OpenAI API.
  To use this frontend, you may need to set up a corresponding ZMQ backend.

* `dryrun`: Fake frontend that does nothing.
  Instead, we will simply print the generated initial prompt to the screen,
  so the user can can copy it, and paste into web-based LLMs, including but
  not limited to ChatGPT (OpenAI), Claude (Anthropic), Bard (google),
  Gemini (google), HuggingChat (HuggingFace), Perplexity AI, etc.
  This frontend does not need to connect with any backend.

**DISCLAIMER:** Unless you connect to a self-hosted LLM Inference backend, we
are uncertain how the third-party API servers will handle the data you created.
Please refer their corresponding user agreements before adopting one of them.
Be aware of such risks, and refrain from sending confidential information such
like paid API keys to LLM.

TUTORIAL
========

The following examples are carefully ordered. You can start from the first
example and gradually move to the next one.

#### 1. Quick Start by Chatting with LLM

When no arguments are given, `debgpt` leads you into a general terminal
chatting client with LLM backends. Use `debgpt -h` to see detailed usage.

```
debgpt
```

The first prompt can be provided through argument (`--ask|-A|-a`):

```
debgpt -A "Who are you? And what can LLM do?"
```

By specifying the `--quit|-Q` option, the program will quit after receiving
the first response from LLM. For instance, we can let it mimic `fortune`
with temperature 1.0 ('--temperature|-T 1.0') for higher randomness:

```
debgpt -T 1.0 -QA 'Greet with me, and tell me a joke.'
```

After each session, the chatting history will be saved in `~/.debgpt` as a
json file in a unique name. The command `debgpt replay <file_name>` can be
used to replay the session in specified file. When `<file_name>` is not given,
`debgpt replay` will replay the last session.

During the interactive mode, you may press `/` and see a list of available
escaped commands that will not be seen as LLM prompt.

* `/save <path.txt>`: save the last LLM response to the specified file.

* `/reset`: clear the context. So you can start a new conversation without quiting.

#### 2. Special MapReduce Prompt Composer for Any Length Context

Generally, LLMs have a limited context length. If you want to ask a question
regarding a very long context, you can split the context into multiple parts,
and extract the relevant information from each part. Then, you can ask the
LLM to answer the question based on the extracted information.

We have implemented it as a special feature in the `debgpt` tool. You can use
this functionality through the `--mapreduce|-x` argument.  We need the
`--ask|-A` argument to tell LLM what kind of question we want to ask so it can
extract the right information. If `--ask|-A` is not provided, the tool will
simply assume that you want to summarize the provided information.

Some usage examples are as follows:

```
debgpt -Hx <path-specifier> -A <your-question>
debgpt -Hx ./debian -A 'how is this package built? how many binary packages will be produced?'
debgpt -Hx :policy -A 'what is the changes of the latest version compared to the previous version?'
debgpt -Hx :policy -A 'what package should enter contrib instead of main or non-free?'
debgpt -Hx :devref -A 'How can I become a debian developer?'
debgpt -Hx :sbuild -A 'why does the build fail? do you have any suggestion?'
debgpt -Hx resume.pdf -A 'Does this person know AI? To what extent?'
```

See https://salsa.debian.org/deeplearning-team/debgpt/-/issues/6 for some
examples with their corresponding outputs.

Here is the list of supported paths specifiers:

* `:policy`: Load the Debian Policy document (plain text).
* `:devref`: Load the Debian Developer Reference document (plain text).
* `:sbuild`: Load the latest sbuild log file from the parent directory.
* `<file_path>`: Load the file as plain text. Non-text formats including PDF are supported.
* `<directory_path>`: Load every file from the given directory.

To further tweak the mapreduce behavior, you may want to check the
`--mapreduce_chunksize <int>` and `--mapreduce_parallelism <int>` arguments.

The idea behind this is fairly simple: binary split the input text until the
chunk size is smaller than a pre-defined size, and then pairwise reduce those
results using LLM until there is only one chunk left.  As a result, this
functionality can be very quota-consuming if you are going to deal with long
texts. Please keep an eye on your bill when you try this on a paied API
service.

#### 3. Standard Query Composers for Texts that Fit in Context Window

Ask LLM to summarize the BTS page for `src:pytorch`.

```
debgpt -HQ --bts src:pytorch -A :summary_table
debgpt -HQ --bts 1056388 -A :summary
```

Lookup the build status for package `glibc` and summarize as a table.

```
debgpt -HQ --buildd glibc -A :summary_table
```

When the argument to `-A/--ask` is a tag starting with a colon sign `:`, such
as `:summary`, it will be automatically replaced into a default question
template. Use `debgpt -A :` to lookup available templates.

The `-H` argument will skip printing the first prompt generated by `debgpt`,
because it is typically very lengthy, and people may not want to read it.


Load a section of debian policy document, such as section "4.6", and ask a question

```
debgpt -H --policy 7.2 -A "what is the difference between Depends: and Pre-Depends: ?"
debgpt -H --devref 5.5 -A :summary
```


Load the debhelper manpage and ask it to extract a part of it.

```
debgpt -HQ --man debhelper-compat-upgrade-checklist -A "what's the change between compat 13 and compat 14?"
debgpt -HQ --tldr curl --cmd 'curl -h' -A "download https://localhost/bigfile.iso to /tmp/workspace, in silent mode"
```


We can add code file and Debian Policy simultaneously. The combination
is actually very flexible, and you can put anything in the prompt.
In the following example, we put the `debian/control` file from the
PyTorch package, as well as the Debian Policy section 7.4, and asks the LLM
to explain some details:

```
debgpt -H -f pytorch/debian/control --policy 7.4 -A "Explain what Conflicts+Replaces means in pytorch/debian/control based on the provided policy document"
```

Similarly, we can also let LLM read the Policy section 4.9.1, and ask it to
write some code:

```
debgpt -H -f pytorch/debian/rules --policy 4.9.1 -A "Implement the support for the 'nocheck' tag based on the example provided in the policy document."
```


Being able to pipe the inputs and outputs among different programs is one of
the reasons why I love the UNIX philosophy.

For example, we can let debgpt read the command line outputs of `apt`, and
summarize the upgradable packages for us:

```
debgpt -HQ --cmd 'apt list --upgradable' -A 'Briefly summarize the upgradable packages. You can categorize these packages.' -F openai --openai_model 'gpt-3.5-turbo-16k'
```

And we can also ask LLM to automatically generate a git commit message for you
based on the currently staged changes:

```
debgpt -HQ --cmd 'git diff --staged' -A 'Briefly describe the change as a git commit message.'
```

This looks interesting, right? In the next example, we have something even
more convenient!

Let LLM explain code files:
```
debgpt -Hf debgpt/llm.py -A 'explain this file'  # --file|-f for small file
debgpt -Hx debgpt/llm.py -a 'explain this file'  # --mapreduce|-x for large file
debgpt -Hf pyproject.toml -A 'what is the purpose of this file'
```

You can also specify the line range in a special grammar for `-f/--file`:
```
debgpt -H -f pyproject.toml:3-10 -A :what  # select the [3,10) lines
debgpt -H -f pyproject.toml:-10 -A :what   # select from beginning to 10th (excluding 10th)
debgpt -H -f pyproject.toml:3- -A :what  # select from 3th line (including) to end of file
```

Mimicking `licensecheck`:

```
debgpt -H -f debgpt/llm.py -A :licensecheck
```

Make the mailing list long story short:

```
debgpt -H --html 'https://lists.debian.org/debian-project/2023/12/msg00029.html' -A :summary
```

Explain the differences among voting options:

```
debgpt -H --html 'https://www.debian.org/vote/2022/vote_003' -A :diff --openai_model gpt-3.5-turbo-16k
```

In this example, we had to switch to a model supporting a long context (the
HTML page has roughly 5k tokens).

#### 4. Command Line Behavior

Let LLM write some code for you and save the output to a file:

```
debgpt -Qa 'write a hello world in rakudo for me' -o hello.raku
debgpt -HQ stdin < question.txt | tee result.txt
```

#### 5. External Command Wrapper and Subcommands

Let LLM automatically generate the git commit message, and call git to commit it:

```
debgpt git commit --amend
```





#### 99. You Name It

The usage of LLM is limited by our imaginations. I am glad to hear from you if
you have more good ideas on how we can make LLMs useful for Debian development:
https://salsa.debian.org/deeplearning-team/debgpt/-/issues


HINTS: PROMPT ENGINEERING
=========================

When you chat with LLM, note that the way you ask a question significant
impacts the quality of the results you will get. make sure to provide as much
information as possible. The following are some references on this topic:

1. OpenAI's Guide https://platform.openai.com/docs/guides/prompt-engineering
2. Chain-of-Thought (CoT): https://arxiv.org/pdf/2205.11916.pdf


SELF-CONTAINED BACKEND
======================

## Available Backend Implementations

This tool provides one backend implementation: `zmq`.

* `zmq`: Only needed when you choose the ZMQ front end for
  self-hosted LLM inference server.

If you plan to use the `openai` or `dryrun` frontends, there is no specific
hardware requirement. If you would like to self-host the LLM inference backend
(ZMQ backend), powerful hardware is required.

## LLM Selections

The concrete hardware requirement depends on the
LLM you would like to use. A variety of open-access LLMs can be found here
> `https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard`
Generally, when trying to do prompt engineering only, the "instruction-tuned"
LLMs and "RL-tuned" (RL is reinforcement learning) LLMs are recommended.

The pretrained (raw) LLMs are not quite useful in this case, as they have not
yet gone through instruction tuning, nor reinforcement learning tuning
procedure.  These pretrained LLMs will more likely generate garbage and not
follow your instructions, or simply repeat your instruction.  We will only
revisit the pretrained LLMs when we plan to start collecting data and fine-tune
(e.g., LoRA) a model in the far future.

The following is a list of supported LLMs for self-hosting (this list will
be updated when there are new state-of-the-art open-access LLMs available):

* Mistral7B (`Mistral-7B-Instruct-v0.2`) (default)
: This model requires roughly 15GB of disks space to download.

* Mixtral8x7B (`Mixtral-8x7B-Instruct-v0.1`)
: This model is larger yet more powerful than the default LLM. In exchange, it
poses even higher hardware requirements. It takes roughly 60~100GB disk space
(I forgot this number. Will check later).

Different LLMs will pose different hardware requirements. Please see the
"Hardware Requirements" subsection below.

## Hardware Requirements

By default, we recommend doing LLM inference in `fp16` precision. If the VRAM
(such as CUDA memory) is limited, you may also switch to even lower preicisions
such as `8bit` and `4bit`. For pure CPU inference, we only support `fp32`
precision now.

Note, Multi-GPU inference is supported by the underlying transformers library.
If you have multiple GPUs, this memory requirement is roughly divided by your number of GPUs.

Hardware requirements for the `Mistral7B` LLM:

* `Mistral7B` + `fp16` (cuda): 24GB+ VRAM preferred, but needs a 48GB GPU to run all the demos (some of them have a context as long as 8k). Example: Nvidia RTX A5000, Nvidia RTX 4090.
* `Mistral7B` + `8bit` (cuda): 12GB+ VRAM at minimum, but 24GB+ preferred so you can run all demos.
* `Mistral7B` + `4bit` (cuda): 6GB+ VRAM at minimum but 12GB+ preferred so you can run all demos. Example: Nvidia RTX 4070 (mobile) 8GB.
* `Mistral7B` + `fp32` (cpu): Requires 64GB+ of RAM, but a CPU is 100~400 times slower than a GPU for this workload and thus not recommended.

Hardware requirement for the `Mixtral8x7B` LLM:

* `Mixtral8x7B` + `fp16` (cuda): 90GB+ VRAM.
* `Mixtral8x7B` + `8bit` (cuda): 45GB+ VRAM.
* `Mixtral8x7B` + `4bit` (cuda): 23GB+ VRAM, but in order to make it work with long context such as 8k tokens, you still need 2x 48GB GPUs in 4bit precision.

See https://huggingface.co/blog/mixtral for more.

## Usage of the ZMQ Backend

If you want to run the default LLM with different precisions:

```
debgpt backend --max_new_tokens=1024 --device cuda --precision fp16
debgpt backend --max_new_tokens=1024 --device cuda --precision bf16
debgpt backend --max_new_tokens=1024 --device cuda --precision 8bit
debgpt backend --max_new_tokens=1024 --device cuda --precision 4bit
```

The only supported precision on CPU is fp32 (for now).
If you want to fall back to CPU computation (very slow):

```
debgpt backend --max_new_tokens=1024 --device cpu --precision fp32
```

If you want to run a different LLM, such as `Mixtral8x7B`  than the default `Mistral7B`:

```
debgpt backend --max_new_tokens=1024 --device cuda --precision 4bit --llm Mixtral8x7B
```

The argument `--max_new_tokens` does not matter much and you can adjust it (it
is the maximum length of each llm reply). You can adjust it as wish.

TODO
====

The following is the current **TODO List**.Some ideas might be a little bit far away.

1. add `--google` search option. should dive into the links from search results with depth 1.
1. https://github.com/openai/chatgpt-retrieval-plugin
1. implement `--archwiki` `--gentoowiki` `--debianwiki` `--fedorawiki` `--wikipedia` (although the LLM have already read the wikipedia dump many times)
1. analyze udd, ddpo, contributors, nm
1. How can LLM help CPython transition? failing tests, API changes, etc.
1. What else can we do about the Debian patching workflow? adding patch description?
1. find upstream bug that matches debian bug (bug triage)
1. connect with debian codesearch API https://codesearch.debian.net/faq
1. Let LLM imitate [Janitor](https://wiki.debian.org/Janitor), and possibly do some more complicated things
1. Extend Lintian with LLM for complicated checks?
1. Let LLM do mentoring (lists.debian.org/debian-mentors) e.g., reviewing a .dsc package. This is very difficult given limited context length. Maybe LLMs are not yet smart enough to do this.
1. Apart from the `str` type, the frontend supports other return types like `List` or `Dict` (for advanced usage such as in-context learning) are possible (see `debgpt/frontend.py :: ZMQFrontend.query`, but those are not explored yet.
1. The current implementation stays at prompt-engineering an existing Chatting LLM with debian-specific documents, like debian-policy, debian developer references, and some man pages. In the future, we may want to explore how we can use larger datasets like Salsa dump, Debian mailing list dump, etc. LoRA or RAG or any new methods are to be investegated with the datasets. Also see follow-ups at https://lists.debian.org/debian-project/2023/12/msg00028.html
1. Should we really train or fine-tune a model? How do we organize the data?

REFERENCES
==========

[1] Access large language models from the command-line
: https://github.com/simonw/llm

[2] Turn your task descriptions into precise shell commands
: https://github.com/sderev/shellgenius

LICENSE
=======

Copyright (C) 2024 Mo Zhou <lumin@debian.org>; MIT/Expat License
