import subprocess
from pathlib import Path

def format_size(size_bytes: int) -> str:
    """Converts a size in bytes to a human-readable string (KB, MB, GB)."""
    if size_bytes == 0:
        return "0 B"
    power = 1024
    n = 0
    power_labels = {0: 'B', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB'}
    while size_bytes >= power and n < len(power_labels) - 1:
        size_bytes /= power
        n += 1
    return f"{size_bytes:.2f} {power_labels[n]}" if n > 0 else f"{int(size_bytes)} {power_labels[n]}"

def get_git_state(target_dir="."):
    """Safely attempts to get the current Git repository state for a given directory."""
    try:
        target_path = str(target_dir)
        # Check if we are inside a git repository
        subprocess.run(['git', 'rev-parse', '--is-inside-work-tree'], cwd=target_path, check=True, capture_output=True)
        
        # Get short commit ID
        short_id = subprocess.run(['git', 'rev-parse', '--short', 'HEAD'], cwd=target_path, capture_output=True, text=True).stdout.strip()
        
        # Get the commit message
        commit_msg = subprocess.run(['git', 'log', '-1', '--pretty=%s'], cwd=target_path, capture_output=True, text=True).stdout.strip()
        
        # Check for untracked or uncommitted changes
        status = subprocess.run(['git', 'status', '--porcelain'], cwd=target_path, capture_output=True, text=True).stdout.strip()
        is_dirty = len(status) > 0
        
        return short_id, commit_msg, is_dirty
    except Exception:
        # Fails silently if Git isn't installed or we aren't in a repo
        return None, None, None

def summary(command_args, files_with_sizes, commit_id=None, target_dir="."):
    """
    Generates a formatted summary string of the execution.
    files_with_sizes: list of tuples (file_path_string, size_in_bytes)
    """
    total_size_bytes = sum(size for _, size in files_with_sizes)
    sorted_files = sorted(files_with_sizes, key=lambda x: x[1], reverse=True)
    
    lines = [
        "=== EXECUTION SUMMARY ===",
        f"Command Arguments   : {' '.join(command_args)}"
    ]
    
    # Add target commit parameter (mostly used by save_commits.py)
    if commit_id:
        lines.append(f"Target Commit(s)    : {commit_id}")
        
    # Dynamically inject current workspace Git context using the target directory
    short_id, commit_msg, is_dirty = get_git_state(target_dir)
    if short_id:
        lines.append(f"Current Repo HEAD   : {short_id} {commit_msg}")
        lines.append(f"Uncommitted Changes : {'Yes' if is_dirty else 'No'}")
        
    lines.append(f"Total Size          : {format_size(total_size_bytes)}")
    lines.append(f"Total Files         : {len(sorted_files)}")
    lines.append("Files Included      :")
    
    if not sorted_files:
        lines.append("  (No files)")
    else:
        for f_path, f_size in sorted_files:
            lines.append(f"  - [{format_size(f_size).rjust(10)}] {f_path}")
            
    lines.append("=" * 80 + "\n")
    return "\n".join(lines)
