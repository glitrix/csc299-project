from .pkms import PKMSCore, run_demo


def inc(n: int) -> int:
    return n + 1


def main() -> None:
    """Main entry point for tasks3 application."""
    print("Hello from tasks3!")
    print("Running PKMS demo...")
    run_demo()
