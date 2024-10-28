import argparse

def main():
    parser = argparse.ArgumentParser(description='My CLI Tool')
    parser.add_argument('name', help='Your name')
    args = parser.parse_args()
    print(f'Hello, {args.name}!')

if __name__ == '__main__':
    main()
