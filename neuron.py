"""
Neuron — AI-Powered Research & Workflow Assistant
"""

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from src.agent import  build_agent

console= Console()

def display_welcome():
    console.print(Panel.fit(
        "[bold cyan]Neuron[/bold cyan]\n"
        "[dim]AI-Powered Research & Workflow Assistant[/dim]\n\n"
        "Type naturally. Use 'exit' to leave.",
        border_style= "cyan",
    ))
    console.print()



def main():
    tools = []
    agent = build_agent(tools)
    display_welcome()
    while True:
        try:
            user_input = console.input("[bold green]You > [/bold green]").strip()
            if not user_input:
                continue
            if user_input.lower() in ("exit","quit","q"):
                console.print("\n[cyan]Neuron signing off. See you![/cyan]\n")
                break

            with console.status("[cyan]Thinking...[/cyan]", spinner="dots"):
                response = agent.invoke({"input": user_input})

            console.print()
            console.print(Markdown(response["output"]))
            console.print()

        except KeyboardInterrupt:
            console.print("\n[cyan]Goodbye![/cyan]\n")
            break
        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]\n")

if __name__ == "__main__":
    main()
