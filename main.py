import os
import re
import datetime
from pathlib import Path

try:
    from rich.console import Console
    from rich.table import Table
    from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
    from rich.panel import Panel
except ImportError:
    print("Error: 'rich' library not found. The output will not be formatted.")
    print("Install it with the command: pip install rich")
    exit()

TARGET_DIR = Path('/YOURPATH')
DRY_RUN = False

IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.heic', '.heif'}
VIDEO_EXTENSIONS = {'.mp4', '.mov', '.avi', '.mkv', '.wmv', '.flv', '.webm', '.mpeg', '.mpg'}
AUDIO_EXTENSIONS = {'.mp3', '.wav', '.aac', '.flac', '.ogg', '.m4a', '.wma'}
MEDIA_EXTENSIONS = IMAGE_EXTENSIONS | VIDEO_EXTENSIONS | AUDIO_EXTENSIONS

def get_date_from_filename(filename: str) -> str | None:
    match = re.search(r'(20\d{2})[\-_]?(\d{2})[\-_]?(\d{2})', filename)
    if not match:
        return None
    try:
        year, month, day = [int(p) for p in match.groups()]
        date_obj = datetime.date(year, month, day)
        return date_obj.strftime('%Y-%m-%d')
    except ValueError:
        return None

def get_plausible_date_from_metadata(file_path: Path) -> str | None:
    try:
        mtime = file_path.stat().st_mtime
        metadata_date_obj = datetime.datetime.fromtimestamp(mtime)
        if 2000 <= metadata_date_obj.year <= datetime.date.today().year:
            return metadata_date_obj.strftime('%Y-%m-%d')
    except Exception:
        return None
    return None

def organize_media_files():
    console = Console()

    if not TARGET_DIR.is_dir():
        console.print(f"[bold red]Error: The target folder '{TARGET_DIR}' was not found.[/bold red]")
        return
        
    script_dir = Path(__file__).parent
    log_file_path = script_dir / "log.txt"
    
    console.print(Panel(
        f"[bold]Scanning for media in:[/bold] [cyan]{TARGET_DIR}[/cyan]\n"
        f"[bold]Execution Mode:[/] {'[yellow]SIMULATION (DRY RUN)[/yellow]' if DRY_RUN else '[green]REAL[/green]'}\n"
        f"[bold]Log file will be saved to:[/] [cyan]{log_file_path}[/cyan]",
        title="[bold magenta]Media Renamer[/bold magenta]",
        border_style="magenta"
    ))

    files_to_process = [f for f in TARGET_DIR.rglob('*') if f.is_file() and f.suffix.lower() in MEDIA_EXTENSIONS]
    
    if not files_to_process:
        console.print("[yellow]No media files found to process.[/yellow]")
        return

    total_files_found = len(files_to_process)
    renamed_count, correct_count, skipped_count, error_count = 0, 0, 0, 0
    renamed_log, correct_log, skipped_log = [], [], []

    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        "[progress.percentage]{task.percentage:>3.0f}%",
        "({task.completed} of {task.total})",
        TimeRemainingColumn(),
        console=console,
        transient=True
    ) as progress:
        task = progress.add_task("[green]Processing media...", total=total_files_found)

        for source_path in files_to_process:
            progress.update(task, advance=1, description=f"[green]Analyzing [bold]'{source_path.name}'[/bold][/green]")
            
            file_date_str = get_date_from_filename(source_path.name) or get_plausible_date_from_metadata(source_path)

            if not file_date_str:
                skipped_log.append(f"{source_path} -> [INVALID OR UNREADABLE DATE]\n")
                skipped_count += 1
                continue

            time_suffix = datetime.datetime.fromtimestamp(source_path.stat().st_mtime).strftime('_%H%M%S')
            new_base_name = f"{file_date_str}{time_suffix}"
            potential_new_filename = f"{new_base_name}{source_path.suffix}"

            if potential_new_filename == source_path.name:
                correct_log.append(f"{source_path} -> [NAME ALREADY CORRECT]\n")
                correct_count += 1
            else:
                new_filename = potential_new_filename
                dest_path = source_path.with_name(new_filename)
                counter = 1
                while dest_path.exists():
                    new_filename = f"{new_base_name}-{counter}{source_path.suffix}"
                    dest_path = source_path.with_name(new_filename)
                    counter += 1
                
                renamed_log.append(f"{source_path} -> {dest_path}\n")
                renamed_count += 1
                
                if not DRY_RUN:
                    try:
                        source_path.rename(dest_path)
                    except Exception as e:
                        error_count += 1
                        skipped_log.append(f"{source_path} -> [ERROR RENAMING: {e}]\n")
                        renamed_count -= 1
                        skipped_count += 1
                        renamed_log.pop()

    with open(log_file_path, 'w', encoding='utf-8') as log_file:
        log_file.write(f"# MEDIA ORGANIZATION LOG\n# Generated on: {datetime.datetime.now():%Y-%m-%d %H:%M:%S}\n\n")
        if renamed_log:
            log_file.write(f"# RENAMED FILES ({len(renamed_log)})\n" + "="*50 + "\n")
            log_file.writelines(renamed_log)
        if correct_log:
            log_file.write(f"\n# FILES ALREADY NAMED CORRECTLY ({len(correct_log)})\n" + "="*50 + "\n")
            log_file.writelines(correct_log)
        if skipped_log:
            log_file.write(f"\n# SKIPPED OR ERRORED FILES ({len(skipped_log)})\n" + "="*50 + "\n")
            log_file.writelines(skipped_log)

    summary_table = Table(title="[bold]Complete Operation Summary[/bold]", title_style="magenta", border_style="magenta")
    summary_table.add_column("Category", style="cyan", no_wrap=True)
    summary_table.add_column("Total", justify="right", style="bold")
    summary_table.add_row("Total Media Files Found", f"[white]{total_files_found}[/white]")
    summary_table.add_row("Files Renamed", f"[green]{renamed_count}[/green]")
    summary_table.add_row("Names Already Correct", f"[cyan]{correct_count}[/cyan]")
    summary_table.add_row("Files Skipped", f"[yellow]{skipped_count}[/yellow]")
    if error_count > 0:
        summary_table.add_row("Renaming Errors", f"[bold red]{error_count}[/bold red]")

    console.print(summary_table)

if __name__ == "__main__":
    organize_media_files()
