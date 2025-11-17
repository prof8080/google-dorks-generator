import argparse
import webbrowser
import urllib.parse
import os

def load_dorks(file_path):
    """Loads Google Dorks from a file, filtering out empty lines and comments."""
    dorks = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # Filter out empty lines, comments, and non-dork lines
                if line and not line.startswith('#') and any(line.startswith(op + ':') for op in ['site', 'inurl', 'intitle', 'intext', 'filetype', 'allintext', 'allintitle', 'allinurl', 'cache', 'related', 'info', 'link']):
                    dorks.append(line)
    except FileNotFoundError:
        print(f"Error: Dorks file not found at {file_path}")
        exit(1)
    return dorks

def generate_search_url(dork):
    """Generates the full Google search URL for a given dork."""
    base_url = "https://www.google.com/search?q="
    # URL-encode the dork query
    encoded_dork = urllib.parse.quote_plus(dork)
    return base_url + encoded_dork

def main():
    parser = argparse.ArgumentParser(
        description="A simple tool to generate and open Google Dorks search queries from a list.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '-f', '--file',
        default='dorks.txt',
        help="Path to the file containing Google Dorks (one dork per line). Default is 'dorks.txt'."
    )
    parser.add_argument(
        '-l', '--list',
        action='store_true',
        help="List all dorks from the file without opening them."
    )
    parser.add_argument(
        '-o', '--open',
        action='store_true',
        help="Open the generated search URLs in the default web browser."
    )
    parser.add_argument(
        '-s', '--search',
        type=str,
        help="Search for a specific dork (or part of a dork) in the list and open it."
    )
    
    args = parser.parse_args()
    
    dorks = load_dorks(args.file)
    
    if not dorks:
        print("No valid dorks found in the file.")
        return

    if args.list:
        print(f"--- Loaded {len(dorks)} Google Dorks from {args.file} ---")
        for i, dork in enumerate(dorks, 1):
            print(f"{i}. {dork}")
        return

    if args.search:
        matching_dorks = [d for d in dorks if args.search.lower() in d.lower()]
        if not matching_dorks:
            print(f"No dorks found matching '{args.search}'.")
            return
        
        print(f"--- Found {len(matching_dorks)} matching dorks for '{args.search}' ---")
        for i, dork in enumerate(matching_dorks, 1):
            print(f"{i}. {dork}")
            if args.open:
                url = generate_search_url(dork)
                print(f"   Opening: {url}")
                webbrowser.open_new_tab(url)
        return

    if args.open:
        print(f"--- Opening {len(dorks)} Google Dorks in your browser ---")
        for dork in dorks:
            url = generate_search_url(dork)
            print(f"Opening: {url}")
            # Note: In a headless environment, this will likely fail or open a text-based browser.
            # We use it for demonstration of the tool's capability.
            webbrowser.open_new_tab(url)
        print("\nFinished attempting to open all dorks.")
    else:
        print("--- Generated Google Search URLs (Use -o or --open to execute) ---")
        for dork in dorks:
            url = generate_search_url(dork)
            print(url)
        print("\nUse -l to list dorks, -o to open all, or -s <query> to search and open a specific dork.")

if __name__ == "__main__":
    main()
