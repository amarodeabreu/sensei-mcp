"""Entry point for uvx execution"""
import sys
import argparse

def main():
    """Run the Sensei MCP server"""
    parser = argparse.ArgumentParser(
        prog="sensei-mcp",
        description="Sensei MCP Server - Engineering standards mentor with active context injection",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  sensei-mcp                    # Start the MCP server
  sensei-mcp --version          # Show version information

The server communicates via JSON-RPC over stdio and is designed to be
used with MCP clients like Claude Desktop, Cursor, Windsurf, or Cline.

For more information, visit: https://github.com/amarodeabreu/sensei-mcp
        """
    )
    parser.add_argument(
        "--version",
        action="version",
        version="sensei-mcp 0.1.0"
    )

    # Parse arguments
    args = parser.parse_args()

    # If we get here (no --help or --version), start the server
    from .server import mcp
    mcp.run()

if __name__ == "__main__":
    main()
