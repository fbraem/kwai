# Command Line Interface
A command line interface (CLI) is provided to help managing the kwai system. To run the cli, use the kwai_cli.py
script:

`python -m kwai.cli --help`

::: kwai.cli.commands.bus
    options:
        show_root_full_path: False
        show_signature: False
        members:
            - show
            - test

::: kwai.cli.commands.db
    options:
        show_root_full_path: False
        show_signature: False
        members:
            - show
            - test

::: kwai.cli.commands.identity
    options:
        show_root_full_path: False
        show_signature: False
        members:
            - create
