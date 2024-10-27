from pathlib import Path

from package_schemes.interfaces import Project, UvLockV1
from package_schemes.interfaces.pyproject import Pyproject
from rich.console import Console, Group
from rich.markdown import Markdown
from rich.padding import Padding
from rich.panel import Panel
from rich.tree import Tree

from uv_audit.scan.safery import SafetyScanProvider

console = Console()

tree = Tree('Rich Tree')


class UvAuditManager(object):
    def __init__(self) -> None:
        path = Path.cwd()
        self.scan_manager = SafetyScanProvider()
        self.project = Project(
            Pyproject(path / 'pyproject.toml'),
            UvLockV1(path / 'uv.lock'),
        )

    def set_options(self, verbose: bool, ignore_codes: list[str], scan_extra_deps: bool, scan_dev_deps: bool):
        pass

    def scan(self):
        total_error = 0
        for package in self.project.get_packages():
            for vulnerability in self.scan_manager.get_package_vulnerability(package):
                total_error += 1

                url = f'https://pyup.io{vulnerability.more_info_path}'
                da = Group(
                    f'[bright_cyan italic]{url}',
                    Padding(Markdown(markup=f'> {vulnerability.advisory}'), (0, 0, 1, 0)),
                    'Affected versions: [bright_yellow]'
                    + '[/bright_yellow] | [bright_yellow]'.join(vulnerability.specs),
                )
                console.print(
                    Panel(
                        da,
                        title_align='left',
                        title=f'[bold bright_red]{package.name}[/bold bright_red] '
                        f'[bright_yellow]{package.version}[/bright_yellow] - '
                        f'[bold bright_red]{vulnerability.cve}[/bold bright_red]',
                    )
                )
        return total_error
