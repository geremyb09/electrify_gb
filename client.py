import requests
from rich.console import Console
from rich.markdown import Markdown

console = Console()


def generate_titles(channel_id: str, summary: str, top_n: int = 15):
    """Generate titles via API"""
    try:
        response = requests.post(
            "http://localhost:8000/generate-titles",
            json={"channel_id": channel_id, "summary": summary, "top_n": top_n},
            timeout=180,
        )

        # Check if request was successful
        if response.status_code != 200:
            console.print(f"[bold red]Error {response.status_code}:[/bold red]")
            console.print(response.json())
            return

        data = response.json()

        # Display
        console.print("\n[bold cyan]Pattern Analysis:[/bold cyan]\n")
        if data.get("pattern_analysis"):
            console.print(Markdown(data["pattern_analysis"]))
        else:
            console.print("[dim]No pattern analysis available[/dim]")

        console.print("\n[bold green]Generated Titles:[/bold green]\n")
        if data.get("generated_titles"):
            console.print(Markdown(data["generated_titles"]))
        else:
            console.print("[dim]No titles generated[/dim]")

        if "metadata" in data:
            console.print(f"\n[dim]Analyzed {data['metadata'].get('top_n', 'N/A')} videos[/dim]\n")

    except requests.exceptions.ConnectionError:
        console.print("[bold red]Error: Cannot connect to API. Is it running?[/bold red]")
        console.print("[dim]Start with: python api.py[/dim]")
    except requests.exceptions.Timeout:
        console.print("[bold red]Error: Request timed out[/bold red]")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="YouTube Title Optimizer - Generate optimized video titles",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python client.py UC510QYlOlKNyhy_zdQxnGYw "A tutorial on AI apps"
  python client.py UC510QYlOlKNyhy_zdQxnGYw "Building web apps with Python" --top-n 20
        """,
    )

    parser.add_argument("channel_id", help="YouTube channel ID (e.g., UC510QYlOlKNyhy_zdQxnGYw)")

    parser.add_argument("summary", help="Single-sentence video summary (in quotes)")

    parser.add_argument(
        "--top-n", type=int, default=15, help="Number of top videos to analyze (default: 15)"
    )

    args = parser.parse_args()

    # Show what we're doing
    console.print("\n[bold]Generating titles for:[/bold]")
    console.print(f"  Channel: {args.channel_id}")
    console.print(f"  Summary: {args.summary}")
    console.print(f"  Analyzing top {args.top_n} videos\n")

    generate_titles(args.channel_id, args.summary, args.top_n)
