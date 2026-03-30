import argparse


def save(filename, text):
    with open(filename, 'w', encoding="utf-8") as f:
        f.write(text)
    print("text saved.")


def analyse_file(filename):
    try:
        with open(filename, 'r', encoding="utf-8") as f:
            text = f.read()

        Analyse_text(text)

    except FileNotFoundError:
        print("Error: file not found")
        return None


def Analyse_text(text):
    words = len(text.split())
    characters = len(text)
    sentences = text.count('.') + text.count('?')

    print("\nText analysis results;")
    print(f"text = {text}")
    print(f"words = {words}")
    print(f"characters = {characters}")
    print(f"sentences = {sentences}")


def quick_stats(text):
    print(f"words: {text.split()}")
    print(f"length: {len(text.split())} ")


def interactive():
    print("-- Welcome to an interactive shell --")
    print("- input texts for analysis -")
    print("\ninsert 'quit' to escape program")

    while True:
        text = input("\nEnter text: ")

        if text.lower() == "quit":
            print("\nprogram ended.")
            break

        if not text.strip():
            print("Empty input, please insert text")
            continue

        Analyse_text(text)


def main():
    parser = argparse.ArgumentParser(description="Simple text analyser")

    subparsers = parser.add_subparsers(dest="command")

   # -------- save command --------
    save_parser = subparsers.add_parser("save", help="Save text for later use")
    save_parser.add_argument("filename", help="name of saved file")
    save_parser.add_argument("text", help="Text to save")

   # -------- analyze saved text --------
    analysefile_parser = subparsers.add_parser(
        "analyse_saved", help="Analyze saved text")
    analysefile_parser.add_argument("filename", help="file to be analysed")

    subparsers.add_parser("interact", help="opens interactive mode")

    args = parser.parse_args()

    if args.command == "save":
        save(args.filename, args.text)
    elif args.command == 'analyse_saved':
        analyse_file(args.filename)
    elif args.command == "interact":
        interactive()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
