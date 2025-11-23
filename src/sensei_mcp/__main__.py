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
  sensei-mcp --demo             # Run interactive demo (5 scenarios)
  sensei-mcp --version          # Show version information

The server communicates via JSON-RPC over stdio and is designed to be
used with MCP clients like Claude Desktop, Cursor, Windsurf, or Cline.

Demo mode showcases 5 real-world scenarios with multi-persona collaboration:
  1. Architecture Decision (microservices migration)
  2. Production Crisis (database outage)
  3. Security Review (authentication audit)
  4. Cost Optimization (cloud spending)
  5. Code Quality (technical debt)

For more information, visit: https://github.com/amarodeabreu/sensei-mcp
        """
    )
    parser.add_argument(
        "--version",
        action="version",
        version="sensei-mcp 0.4.0"
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run interactive demo showcasing persona capabilities"
    )

    # Parse arguments
    args = parser.parse_args()

    # Handle demo mode
    if args.demo:
        from .demo import run_demo
        run_demo()
        return

    # If we get here (no --help or --version), start the server
    from .server import mcp
    mcp.run()

if __name__ == "__main__":
    main()
