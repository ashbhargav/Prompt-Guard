import argparse
import sys
import json
import uvicorn
from ..core.detector import PromptGuard

def main():
    parser = argparse.ArgumentParser(description="PromptGuard CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Analyze command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze a prompt")
    analyze_parser.add_argument("text", nargs="?", help="Text to analyze")
    analyze_parser.add_argument("--file", help="File containing text to analyze")
    
    # Serve command
    serve_parser = subparsers.add_parser("serve", help="Start the API server")
    serve_parser.add_argument("--port", type=int, default=8000, help="Port to run server on")
    serve_parser.add_argument("--host", default="0.0.0.0", help="Host to run server on")

    args = parser.parse_args()
    
    if args.command == "analyze":
        input_text = ""
        if args.file:
            try:
                with open(args.file, 'r') as f:
                    input_text = f.read()
            except Exception as e:
                print(f"Error reading file: {e}", file=sys.stderr)
                sys.exit(1)
        elif args.text:
            input_text = args.text
        else:
            print("Error: Must provide text or file to analyze", file=sys.stderr)
            parser.print_help()
            sys.exit(1)
            
        guard = PromptGuard()
        result = guard.analyze(input_text)
        print(json.dumps(result, indent=2))
        
    elif args.command == "serve":
        # We need to import the app from the api module
        # But uvicorn needs an import string. 
        print(f"Starting server on {args.host}:{args.port}")
        uvicorn.run("promptguard.api.server:app", host=args.host, port=args.port, reload=False)
        
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
