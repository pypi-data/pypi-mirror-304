from pathlib import Path
import yaml
from typing import Optional, Dict, Any, List
import click

class localizerConfig:
    """Manages localizer configuration and file operations"""
    
    DEFAULT_FOLDER = ".localizer"
    CONFIG_FILE = "localizer.config.yaml"
    DEFAULT_REFERENCE_FILE = "reference.yaml"
    DEFAULT_DOCS_FILE = "docs.md"
    
    def __init__(self, project_root: Optional[Path] = None):
        """
        Initialize localizerConfig with project root path
        If not provided, uses current working directory
        """
        self.project_root = project_root or Path.cwd()
        self.localizer_dir = self.project_root / self.DEFAULT_FOLDER
        self._config: Dict[str, Any] = {}
        self._load_config()
    
    @property
    def config_path(self) -> Path:
        """Path to localizer.config.yaml file"""
        return self.localizer_dir / self.CONFIG_FILE
    
    @property
    def reference_path(self) -> Path:
        """Path to reference.yaml file"""
        reference_file = self._config.get('files', {}).get('reference', self.DEFAULT_REFERENCE_FILE)
        return self.localizer_dir / reference_file
    
    @property
    def docs_path(self) -> Path:
        """Path to docs.md file"""
        docs_file = self._config.get('files', {}).get('docs', self.DEFAULT_DOCS_FILE)
        return self.localizer_dir / docs_file
    
    @property
    def languages(self) -> List[str]:
        """Get configured language codes"""
        return self._config.get('languages', ['en'])
    
    def _load_config(self) -> None:
        """Load configuration from localizer.config.yaml"""
        if self.config_path.exists():
            try:
                with self.config_path.open('r', encoding='utf-8') as f:
                    self._config = yaml.safe_load(f) or {}
            except yaml.YAMLError as e:
                raise click.ClickException(f"Error parsing {self.CONFIG_FILE}: {str(e)}")

    def init_folder_structure(self) -> None:
        """Create the initial localizer folder structure with template files"""
        try:
            # Create .localizer directory if it doesn't exist
            self.localizer_dir.mkdir(exist_ok=True)
            
            # Create localizer.config.yaml with template if it doesn't exist
            if not self.config_path.exists():
                template_config = {
                    'files': {
                        'reference': self.DEFAULT_REFERENCE_FILE,
                        'docs': self.DEFAULT_DOCS_FILE
                    },
                    'languages': ['en', 'ko', 'vi']
                }
                self.config_path.write_text(
                    yaml.dump(template_config, allow_unicode=True, sort_keys=False)
                )
            
            # Create reference.yaml with template if it doesn't exist
            if not self.reference_path.exists():
                template_reference = {
                    "tabs": {
                        "index": "Correction",
                        "favorites": "History"
                    }
                }
                self.reference_path.write_text(
                    yaml.dump(template_reference, allow_unicode=True, sort_keys=False)
                )
            
            # Create docs.md with template if it doesn't exist
            if not self.docs_path.exists():
                template_docs = """# Translation Documentation

## Navigation Tabs
- `tabs.index`: Appears in bottom navigation as the main correction tab
- `tabs.favorites`: Shows in bottom navigation for accessing history
"""
                self.docs_path.write_text(template_docs)
                
        except Exception as e:
            raise click.ClickException(f"Failed to initialize localizer structure: {str(e)}")
    
    def read_reference(self) -> Dict[str, Any]:
        """Read and parse the reference.yaml file"""
        try:
            if not self.reference_path.exists():
                raise click.ClickException(
                    f"Reference file not found at {self.reference_path}. "
                    "Run 'localizer init' to create the required files."
                )
            
            with self.reference_path.open('r', encoding='utf-8') as f:
                return yaml.safe_load(f)
                
        except yaml.YAMLError as e:
            raise click.ClickException(f"Error parsing reference file: {str(e)}")
    
    def read_docs(self) -> str:
        """Read the docs.md file content"""
        try:
            if not self.docs_path.exists():
                raise click.ClickException(
                    f"Docs file not found at {self.docs_path}. "
                    "Run 'localizer init' to create the required files."
                )
            
            return self.docs_path.read_text(encoding='utf-8')
            
        except Exception as e:
            raise click.ClickException(f"Error reading docs file: {str(e)}")

    def validate_structure(self) -> bool:
        """
        Validate that the required files and folders exist
        Returns True if valid, raises ClickException if not
        """
        if not self.localizer_dir.exists():
            raise click.ClickException(
                f"localizer directory not found at {self.localizer_dir}. "
                "Run 'localizer init' to create the required files."
            )
            
        if not self.config_path.exists():
            raise click.ClickException(
                f"Config file not found at {self.config_path}. "
                "Run 'localizer init' to create the required files."
            )
            
        if not self.reference_path.exists():
            raise click.ClickException(
                f"Reference file not found at {self.reference_path}. "
                "Run 'localizer init' to create the required files."
            )
            
        if not self.docs_path.exists():
            raise click.ClickException(
                f"Docs file not found at {self.docs_path}. "
                "Run 'localizer init' to create the required files."
            )
            
        return True
    
    def save_config(self, config: Dict[str, Any]) -> None:
        """Save configuration to localizer.config.yaml"""
        try:
            self.config_path.write_text(
                yaml.dump(config, allow_unicode=True, sort_keys=False)
            )
            self._config = config
        except Exception as e:
            raise click.ClickException(f"Failed to save config: {str(e)}")