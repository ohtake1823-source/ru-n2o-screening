def main():
    try:
        import fairchem  # noqa: F401
        print("fairchem import OK")
    except ImportError:
        print("fairchem is not installed")


if __name__ == "__main__":
    main()