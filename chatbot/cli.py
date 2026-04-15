#!/usr/bin/env python3
"""
Velero Chatbot CLI Interface
"""
import sys
import os
from pathlib import Path

# Add parent directory to path to import src modules
sys.path.insert(0, str(Path(__file__).parent))

import click
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from rich import box

from src.config import Config
from src.chatbot import VeleroChatbot

console = Console()


@click.group()
def cli():
    """Velero Chatbot - Interactive assistant for Velero documentation and queries"""
    pass


@cli.command()
@click.option('--env-file', default=None, help='Path to .env file')
def index(env_file):
    """Index repository documents for RAG"""
    console.print("\n[bold cyan]Velero Chatbot - Repository Indexing[/bold cyan]\n")
    
    # Load environment
    if env_file:
        from dotenv import load_dotenv
        load_dotenv(env_file)
    
    try:
        # Initialize configuration
        config = Config()
        
        if not config.chatbot.enable_rag:
            console.print("[yellow]RAG is not enabled in configuration[/yellow]")
            console.print("Set ENABLE_RAG=true in your .env file")
            return
        
        # Initialize chatbot
        console.print("[cyan]Initializing chatbot...[/cyan]")
        chatbot = VeleroChatbot(config)
        
        # Index repository
        console.print("[cyan]Starting repository indexing...[/cyan]")
        console.print(f"Repository path: {config.chatbot.repo_path}")
        console.print(f"Documentation path: {config.chatbot.docs_path}")
        console.print(f"Vector DB: {config.vector_db.db_type}\n")
        
        success = chatbot.index_repository()
        
        if success:
            console.print("\n[bold green]✓ Indexing completed successfully![/bold green]")
        else:
            console.print("\n[bold red]✗ Indexing failed[/bold red]")
            sys.exit(1)
    
    except Exception as e:
        console.print(f"\n[bold red]Error: {str(e)}[/bold red]")
        sys.exit(1)


@cli.command()
@click.option('--env-file', default=None, help='Path to .env file')
@click.option('--query', '-q', default=None, help='Single query to execute')
@click.option('--no-sources', is_flag=True, help='Do not show sources')
def chat(env_file, query, no_sources):
    """Interactive chat interface"""
    
    # Load environment
    if env_file:
        from dotenv import load_dotenv
        load_dotenv(env_file)
    
    try:
        # Initialize configuration
        config = Config()
        
        # Initialize chatbot
        console.print("\n[bold cyan]Velero Chatbot[/bold cyan]")
        console.print("Initializing...\n")
        
        chatbot = VeleroChatbot(config)
        
        # Show status
        status = chatbot.get_status()
        status_panel = Panel(
            f"[cyan]RAG Mode:[/cyan] {'Enabled' if status['rag_enabled'] else 'Disabled'}\n"
            f"[cyan]Vector DB:[/cyan] {status['vector_db_type'] or 'N/A'}\n"
            f"[cyan]Index Ready:[/cyan] {'Yes' if status['vector_db_ready'] else 'No'}",
            title="[bold]Chatbot Status[/bold]",
            box=box.ROUNDED
        )
        console.print(status_panel)
        console.print()
        
        # Handle single query mode
        if query:
            _process_query(chatbot, query, not no_sources)
            return
        
        # Interactive mode
        console.print("[dim]Type your questions about Velero. Type 'exit' or 'quit' to end the session.[/dim]\n")
        
        while True:
            try:
                question = Prompt.ask("\n[bold green]You[/bold green]")
                
                if question.lower() in ['exit', 'quit', 'q']:
                    console.print("\n[cyan]Goodbye! 👋[/cyan]\n")
                    break
                
                if not question.strip():
                    continue
                
                _process_query(chatbot, question, not no_sources)
            
            except KeyboardInterrupt:
                console.print("\n\n[cyan]Goodbye! 👋[/cyan]\n")
                break
            except EOFError:
                break
    
    except Exception as e:
        console.print(f"\n[bold red]Error: {str(e)}[/bold red]")
        sys.exit(1)


def _process_query(chatbot, question, include_sources):
    """Process a query and display results"""
    console.print("\n[cyan]Thinking...[/cyan]")
    
    result = chatbot.query(question, include_sources=include_sources)
    
    console.print("\n[bold blue]Assistant[/bold blue]")
    
    # Display answer
    answer_panel = Panel(
        Markdown(result['answer']),
        title=f"[bold]Answer ({result['method'].upper()})[/bold]",
        box=box.ROUNDED,
        border_style="blue"
    )
    console.print(answer_panel)
    
    # Display sources if available
    if include_sources and result.get('sources'):
        sources_text = "\n".join([
            f"• {source['source']} (relevance: {source['score']:.2f})"
            for source in result['sources']
        ])
        sources_panel = Panel(
            sources_text,
            title="[bold]Sources[/bold]",
            box=box.ROUNDED,
            border_style="dim"
        )
        console.print(sources_panel)


@cli.command()
@click.option('--env-file', default=None, help='Path to .env file')
def status(env_file):
    """Show chatbot status"""
    
    # Load environment
    if env_file:
        from dotenv import load_dotenv
        load_dotenv(env_file)
    
    try:
        config = Config()
        chatbot = VeleroChatbot(config)
        
        status_info = chatbot.get_status()
        
        console.print("\n[bold cyan]Velero Chatbot Status[/bold cyan]\n")
        
        status_panel = Panel(
            f"[cyan]RAG Mode:[/cyan] {'✓ Enabled' if status_info['rag_enabled'] else '✗ Disabled'}\n"
            f"[cyan]Vector Database Type:[/cyan] {status_info['vector_db_type'] or 'N/A'}\n"
            f"[cyan]Index Ready:[/cyan] {'✓ Yes' if status_info['vector_db_ready'] else '✗ No'}\n"
            f"[cyan]Azure OpenAI:[/cyan] {'✓ Configured' if config.azure_openai.api_key else '✗ Not configured'}",
            title="[bold]Status Information[/bold]",
            box=box.ROUNDED
        )
        console.print(status_panel)
        console.print()
        
        if status_info['rag_enabled'] and not status_info['vector_db_ready']:
            console.print("[yellow]⚠ Vector database index not found. Run 'index' command first.[/yellow]\n")
    
    except Exception as e:
        console.print(f"\n[bold red]Error: {str(e)}[/bold red]")
        sys.exit(1)


if __name__ == '__main__':
    cli()
