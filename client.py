import requests
from rich.console import Console
from rich.markdown import Markdown

console = Console()

# Call API
response = requests.post(
    "http://localhost:8000/generate-titles",
    json={
        "channel_id": "UC510QYlOlKNyhy_zdQxnGYw",
        "summary": "A tutorial on building AI apps",
        "top_n": 15
    }
)

data = response.json()

console.print("\n[bold cyan]Pattern Analysis:[/bold cyan]\n")
console.print(Markdown(data['pattern_analysis']))

console.print("\n[bold green]Generated Titles:[/bold green]\n")
console.print(Markdown(data['generated_titles']))

console.print(f"\n[dim]Analyzed {data['metadata']['top_n']} videos[/dim]\n")