import asyncio
import logging
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from typing import Generator
from elroy import __version__
from typing import Optional
from prompt_toolkit.completion import WordCompleter
import typer
from colorama import init
from prompt_toolkit import PromptSession
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles import Style
from pygments.lexers.special import TextLexer
from rich.console import Console
from rich.panel import Panel


from alembic import command
from alembic.config import Config
from elroy.cli.updater import _check_latest_version, _check_migrations_status, _restart_command, _upgrade_if_confirmed, _version_tuple, version_callback
from elroy.config import (ROOT_DIR, ElroyContext, get_config,
                          session_manager)
from elroy.docker_postgres import is_docker_running, start_db, stop_db
from elroy.logging_config import setup_logging
from elroy.memory import get_memory_names, get_relevant_memories
from elroy.onboard_user import onboard_user
from elroy.store.goals import get_goal_names
from elroy.store.user import is_user_exists
from elroy.system.parameters import CLI_USER_ID
from elroy.system.parameters import DEFAULT_OUTPUT_COLOR
from elroy.system.parameters import DEFAULT_INPUT_COLOR
from elroy.system.parameters import SYSTEM_MESSAGE_COLOR
from elroy.system_context import context_refresh_if_needed
from elroy.tools.functions.user_preferences import set_user_preferred_name
from elroy.tools.messenger import process_message
from elroy.tools.system_commands import SYSTEM_COMMANDS, invoke_system_command

app = typer.Typer(help="Elroy CLI", context_settings={"obj": {}})

@contextmanager
def get_elroy_context(ctx: typer.Context) -> Generator[ElroyContext, None, None]:
    """Create an ElroyContext as a context manager"""
    console = Console()
    session = None
    
    try:
        with console.status(f"[{DEFAULT_OUTPUT_COLOR}] Initializing Elroy...", spinner="dots"):
            setup_logging(ctx.obj["log_file_path"])

            if ctx.obj["use_docker_postgres"]:
                if ctx.obj["database_url"] is not None:
                    logging.info("use_docker_postgres is set to True, ignoring database_url")

                if not is_docker_running():
                    console.print(f"[{SYSTEM_MESSAGE_COLOR}]Docker is not running. Please start Docker and try again.[/]")
                    exit(1)

                ctx.obj["database_url"] = start_db()

            assert ctx.obj["database_url"], "Database URL is required"
            assert ctx.obj["openai_api_key"], "OpenAI API key is required"

            # Check if migrations need to be run
            _check_migrations_status(console, ctx.obj["database_url"])

            config = get_config(
                database_url=ctx.obj["database_url"],
                openai_api_key=ctx.obj["openai_api_key"],
                local_storage_path=ctx.obj["local_storage_path"],
                context_window_token_limit=ctx.obj["context_window_token_limit"],
            )
        
        with session_manager(config.database_url) as session:
            yield ElroyContext(
                user_id=CLI_USER_ID,
                session=session,
                console=console,
                config=config,
            )
    finally:
        if ctx.obj["use_docker_postgres"] and ctx.obj["stop_docker_postgres_on_exit"]:
            logging.info("Stopping Docker Postgres container...")
            stop_db()


@app.callback()
def common(
    ctx: typer.Context,
    version: bool = typer.Option(None, "--version", callback=version_callback, is_eager=True, help="Show version and exit."),
    database_url: Optional[str] = typer.Option(None, envvar="ELROY_DATABASE_URL"),
    openai_api_key: Optional[str] = typer.Option(None, envvar="OPENAI_API_KEY"),
    local_storage_path: Optional[str] = typer.Option(None, envvar="ELROY_LOCAL_STORAGE_PATH"),
    context_window_token_limit: Optional[int] = typer.Option(None, envvar="ELROY_CONTEXT_WINDOW_TOKEN_LIMIT"),
    log_file_path: str = typer.Option(os.path.join(ROOT_DIR, "logs", "elroy.log"), envvar="ELROY_LOG_FILE_PATH"),
    use_docker_postgres: Optional[bool] = typer.Option(True, envvar="USE_DOCKER_POSTGRES"),
    stop_docker_postgres_on_exit: Optional[bool] = typer.Option(False, envvar="STOP_DOCKER_POSTGRES_ON_EXIT"),
):
    """Common parameters."""
    ctx.obj = {
        "database_url": database_url,
        "openai_api_key": openai_api_key,
        "local_storage_path": local_storage_path,
        "context_window_token_limit": context_window_token_limit,
        "log_file_path": log_file_path,
        "use_docker_postgres": use_docker_postgres,
        "stop_docker_postgres_on_exit": stop_docker_postgres_on_exit,
    }


@app.command()
def chat(ctx: typer.Context):
    """Start the Elroy chat interface"""
    
    current_version, latest_version = _check_latest_version()
    if _version_tuple(latest_version) > _version_tuple(current_version):
        _upgrade_if_confirmed(current_version, latest_version)
        _restart_command()
    with get_elroy_context(ctx) as context:
        asyncio.run(main_chat(context))
        context.console.print(f"[{SYSTEM_MESSAGE_COLOR}]Exiting...[/]")

@app.command()
def upgrade(ctx: typer.Context):
    """Run Alembic database migrations"""
    with get_elroy_context(ctx) as context:
        alembic_cfg = Config("alembic.ini")
        alembic_cfg.set_main_option("sqlalchemy.url", context.config.database_url)
        command.upgrade(alembic_cfg, "head")
        typer.echo("Database upgrade completed.")
        
def process_and_deliver_msg(context: ElroyContext, user_input: str):
    if user_input.startswith("/"):
        cmd = user_input[1:].split()[0]

        if cmd.lower() not in {f.__name__ for f in SYSTEM_COMMANDS}:
            context.console.print(f"Unknown command: {cmd}")
        else:
            try:
                response = invoke_system_command(context, user_input)
                context.console.print(f"[{DEFAULT_OUTPUT_COLOR}]{response}[/]", end="")
                context.console.print()  # New line after complete response
            except Exception as e:
                print(f"Error invoking system command: {e}")
    else:
        for partial_response in process_message(context, user_input):
            context.console.print(f"[{DEFAULT_OUTPUT_COLOR}]{partial_response}[/]", end="")
        context.console.print()  # New line after complete response



class SlashCompleter(WordCompleter):
    def __init__(self, goals, memories):
        self.goals = goals
        self.memories = memories
        super().__init__(self.get_words(), sentence=True, pattern=r"^/")  # type: ignore

    def get_words(self):
        from elroy.tools.system_commands import (GOAL_COMMANDS,
                                                 MEMORY_COMMANDS,
                                                 SYSTEM_COMMANDS)

        words = [f"/{f.__name__}" for f in SYSTEM_COMMANDS - (GOAL_COMMANDS | MEMORY_COMMANDS)]
        words += [f"/{f.__name__} {goal}" for f in GOAL_COMMANDS for goal in self.goals]
        words += [f"/{f.__name__} {memory}" for f in MEMORY_COMMANDS for memory in self.memories]
        return words



def display_memory_titles(titles):
    console = Console()
    if titles:
        panel = Panel("\n".join(titles), title="Relevant Context", expand=False, border_style=DEFAULT_INPUT_COLOR)
        console.print(panel)


async def async_context_refresh_if_needed(context):
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as pool:
        await loop.run_in_executor(pool, context_refresh_if_needed, context)



async def main_chat(context: ElroyContext):
    init(autoreset=True)

    history = InMemoryHistory()

    style = Style.from_dict(
        {
            "prompt": "bold",
            "user-input": DEFAULT_INPUT_COLOR + " bold",
            "": DEFAULT_INPUT_COLOR,
            "pygments.literal.string": f"bold italic {DEFAULT_INPUT_COLOR}",
        }
    )

    # Asynchronously refresh context, this will drop old message from context.
    asyncio.create_task(async_context_refresh_if_needed(context))

    session = PromptSession(
        history=history,
        style=style,
        lexer=PygmentsLexer(TextLexer),
    )

    if not is_user_exists(context):
        name = await session.prompt_async(HTML("<b>Welcome to Elroy! What should I call you? </b>"), style=style)
        user_id = onboard_user(context.session, context.console, context.config, name)
        assert isinstance(user_id, int)

        set_user_preferred_name(context, name)
        msg = f"[This is a hidden system message. Elroy user {name} has been onboarded. Say hello and introduce yourself.]"
        process_and_deliver_msg(context, msg)

    while True:
        try:
            context.console.rule(style=DEFAULT_INPUT_COLOR)
            session.completer = SlashCompleter(get_goal_names(context),get_memory_names(context),)
            relevant_memories = get_relevant_memories(context)
            if relevant_memories:
                display_memory_titles(relevant_memories)

            user_input = await session.prompt_async(HTML("<b>> </b>"), style=style)
            if user_input.lower().startswith("/exit") or user_input == "exit":
                break
            elif user_input:
                process_and_deliver_msg(context, user_input)
                asyncio.create_task(async_context_refresh_if_needed(context))
        except KeyboardInterrupt:
            context.console.clear()
            continue
        except EOFError:
            break

def main():
    if len(sys.argv) == 1:
        sys.argv.append("chat")
    app()


if __name__ == "__main__":
    main()
