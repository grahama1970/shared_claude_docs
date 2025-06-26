"""Documentation synchronization utilities."""

from pathlib import Path
import shutil
import os

def sync_documentation(source: str, targets: list) -> dict:
    """Sync documentation from source to target projects."""
    source_path = Path(source)
    results = {}
    
    # Get experiments directory
    experiments_dir = Path(os.getenv("EXPERIMENTS_DIR", "/home/graham/workspace/experiments"))
    
    # Files to sync
    sync_files = ["CLAUDE.md", "docs/guides/TASK_LIST_TEMPLATE_GUIDE_V2.md"]
    
    for target in targets:
        target_path = experiments_dir / target
        if not target_path.exists():
            results[target] = {"status": "error", "message": "Project not found"}
            continue
        
        synced_files = []
        for file in sync_files:
            source_file = source_path / file
            if source_file.exists():
                # Create target directory if needed
                target_file = target_path / file
                target_file.parent.mkdir(parents=True, exist_ok=True)
                
                # Copy file
                shutil.copy2(source_file, target_file)
                synced_files.append(file)
        
        results[target] = {
            "status": "success",
            "synced_files": synced_files
        }
    
    return results
