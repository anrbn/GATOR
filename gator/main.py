from gator.utils.arg_parsers import parse_args

def main():
    args = parse_args()

    if hasattr(args, 'func'):
        result = args.func(args)
        print(result)
    else:
        print("No command provided. Use '--help' to see available commands.")

if __name__ == "__main__":
    main()
