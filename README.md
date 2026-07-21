# ReAct Agent (Pure Python)

A minimal ReAct-style chat agent implemented in pure Python with OpenAI Chat Completions and function tools.

## What This Project Does

- Runs an interactive CLI chat loop.
- Uses tool calling with a custom `Tool` wrapper.
- Stores conversation memory in-process.
- Executes tool calls and feeds tool results back to the model.
- Exits cleanly with `Ctrl+C`.

## Project Structure

- `main.py`: interactive CLI entrypoint.
- `agent.py`: agent loop, memory handling, tool-call execution.
- `messages.py`: message model classes.
- `tools.py`: tool wrapper and sample tool (`get_random_genre`).
- `CHANGES.md`: migration and implementation notes.

## Requirements

- Python 3.10+
- OpenAI API key in environment

Install dependencies in your environment:

```bash
pip install openai python-dotenv langchain-core
```

Set your API key:

```bash
export OPENAI_API_KEY="your_api_key_here"
```

## Run

From this folder:

```bash
python3 main.py
```

You will see:

- `Interactive chat started. Press Ctrl+C to exit.`

Type your message and press Enter.
Press `Ctrl+C` to stop.

## How It Works

1. `main.py` builds `Agent(system_prompt=..., tools=...)`.
2. User input is wrapped in `HumanMessage` and sent to the agent.
3. `Agent` calls the model with memory + tool schemas.
4. If model returns tool calls, agent executes tools and appends `ToolResult`.
5. Agent loops until it gets a final assistant message or stop condition.

## Notes

- The loop includes safety guards (max iterations and no-tool-calls break).
- Memory is in-memory only (no persistence to disk).
- Current sample tool: random comedy genre generator.

## Next Improvements

1. Add persistent memory (file or DB).
2. Add structured logging instead of print debugging.
3. Add tests for loop stop conditions and tool-call flow.
4. Add package-style imports and `__init__.py` for `python -m` execution.
