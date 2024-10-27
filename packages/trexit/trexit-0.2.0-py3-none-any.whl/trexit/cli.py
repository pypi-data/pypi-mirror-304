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
    """CLI command for processing directory contents."""
    parser = argparse.ArgumentParser(description="Process directory contents")
    parser.add_argument("path", nargs="?", default=".", help="Directory path")
    parser.add_argument("--ignore", nargs="+", help="Directories to ignore")
    parser.add_argument("-o", "--output", nargs=1, help="Output file")
    args = parser.parse_args()
    
    # Determine whether to collect content based on output file
    collect_content = args.output is not None
    writer = ContentWriter(ignore_list=args.ignore, collect_content=collect_content)
    content = writer.process_directory(args.path)
    print(writer.stats)
    
    if collect_content:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"\nContent written to: {args.output}")
