import argparse
from .tree_printer import TreePrinter
from .content_writer import ContentWriter

def tree_command() -> None:
    """CLI command for printing directory tree."""
    parser = argparse.ArgumentParser(description="Print directory tree structure")
    parser.add_argument("path", nargs="?", default=".", help="Directory path")
    parser.add_argument("--ignore", nargs="+", help="Directories to ignore")
    args = parser.parse_args()
    
    printer = TreePrinter(ignore_list=args.ignore)
    print(printer.print_tree(args.path))

def content_command() -> None:
    """CLI command for saving directory contents."""
    parser = argparse.ArgumentParser(description="Save directory contents to file")
    parser.add_argument("path", nargs="?", default=".", help="Directory path")
    parser.add_argument("--ignore", nargs="+", help="Directories to ignore")
    parser.add_argument("-o", "--output", required=True, help="Output file")
    args = parser.parse_args()
    
    writer = ContentWriter(ignore_list=args.ignore)
    content = writer.process_directory(args.path)
    
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"Total files: {writer.stats.total_files}")
    print(f"Total lines of code: {writer.stats.total_lines}")
    print(f"Total characters of code: {writer.stats.total_chars}")
