"""py++ command-line interface."""

import os
import sys
import argparse
from pathlib import Path

class PyPPCLI:
    """Command-line interface for py++."""
    
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description='py++ programming language interpreter'
        )
        self.setup_commands()
    
    def setup_commands(self):
        subparsers = self.parser.add_subparsers(dest='command')
        
        # pypp run <file>
        run_parser = subparsers.add_parser('run', help='Run a py++ file')
        run_parser.add_argument('file', help='File to run (.pypp)')
        run_parser.add_argument('--verbose', action='store_true', help='Verbose output')
        
        # pypp build <project>
        build_parser = subparsers.add_parser('build', help='Build a project')
        build_parser.add_argument('project', nargs='?', default='.', help='Project directory')
        build_parser.add_argument('--output', default='build', help='Output directory')
        
        # pypp new <project_name>
        new_parser = subparsers.add_parser('new', help='Create a new project')
        new_parser.add_argument('name', help='Project name')
        new_parser.add_argument('--template', default='basic', help='Project template')
        
        # pypp version
        subparsers.add_parser('version', help='Show version')
        
        # pypp help
        subparsers.add_parser('help', help='Show help')
    
    def run_command(self, args):
        """Run a py++ file."""
        from interpreter import interpret
        
        if not os.path.exists(args.file):
            print(f"Error: File not found: {args.file}")
            sys.exit(1)
        
        try:
            with open(args.file, 'r') as f:
                source = f.read()
            
            if args.verbose:
                print(f"[INFO] Executing {args.file}")
            
            interpret(source)
            
            if args.verbose:
                print(f"[INFO] Execution completed")
        
        except Exception as e:
            print(f"Error: {e}")
            if args.verbose:
                import traceback
                traceback.print_exc()
            sys.exit(1)
    
    def build_command(self, args):
        """Build a project."""
        pypp_toml = os.path.join(args.project, 'pypp.toml')
        if not os.path.exists(pypp_toml):
            print(f"Error: No pypp.toml found in {args.project}")
            sys.exit(1)
        
        print(f"[INFO] Building project from {args.project}")
        print(f"[INFO] Output: {args.output}")
        
        os.makedirs(args.output, exist_ok=True)
        
        # Copy source files to output
        src_dir = os.path.join(args.project, 'src')
        if os.path.exists(src_dir):
            for root, dirs, files in os.walk(src_dir):
                for file in files:
                    if file.endswith('.pypp'):
                        src = os.path.join(root, file)
                        rel = os.path.relpath(src, src_dir)
                        dst = os.path.join(args.output, rel)
                        os.makedirs(os.path.dirname(dst), exist_ok=True)
                        with open(src, 'r') as f:
                            content = f.read()
                        with open(dst, 'w') as f:
                            f.write(content)
        
        print(f"[INFO] Build completed")
    
    def new_command(self, args):
        """Create a new py++ project."""
        project_dir = args.name
        
        if os.path.exists(project_dir):
            print(f"Error: Directory already exists: {project_dir}")
            sys.exit(1)
        
        os.makedirs(project_dir)
        os.makedirs(os.path.join(project_dir, 'src'))
        
        # pypp.toml
        toml_content = f"""[project]
name = "{args.name}"
version = "0.1.0"
author = "Your Name"
description = "A py++ project"

[build]
main = "src/main.pypp"
output = "build"
"""
        with open(os.path.join(project_dir, 'pypp.toml'), 'w') as f:
            f.write(toml_content.strip())
        
        # main.pypp template
        main_code = """// My py++ project

fn main() {
    print("Hello from py++!");
}

main();
"""
        with open(os.path.join(project_dir, 'src', 'main.pypp'), 'w') as f:
            f.write(main_code)
        
        # README
        readme = f"""# {args.name}

A py++ project.

## Running

```
pypp run src/main.pypp
```

## Building

```
pypp build .
```
"""
        with open(os.path.join(project_dir, 'README.md'), 'w') as f:
            f.write(readme)
        
        print(f"[INFO] Created project: {project_dir}")
        print(f"[INFO] Run: pypp run {project_dir}/src/main.pypp")
    
    def version_command(self):
        """Show version."""
        print("py++ version 0.1.0")
    
    def help_command(self):
        """Show help."""
        self.parser.print_help()
    
    def run(self, argv=None):
        """Parse arguments and execute command."""
        if argv is None:
            argv = sys.argv[1:]
        
        if not argv:
            self.help_command()
            return
        
        args = self.parser.parse_args(argv)
        
        if args.command == 'run':
            self.run_command(args)
        elif args.command == 'build':
            self.build_command(args)
        elif args.command == 'new':
            self.new_command(args)
        elif args.command == 'version':
            self.version_command()
        elif args.command == 'help' or args.command is None:
            self.help_command()

def main():
    cli = PyPPCLI()
    cli.run()

if __name__ == '__main__':
    main()
