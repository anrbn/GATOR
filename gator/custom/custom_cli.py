# custom/custom_cli.py

import click

INDENT = "  " 

class CustomGroup(click.Group):
    """A custom click.Group class for improved help text formatting."""

    def format_options(self, ctx, formatter):
        """Writes all options into the formatter if they exist."""
        opts = [param for param in self.get_params(ctx) if isinstance(param, click.Option)]
        if opts:
            with formatter.section('OPTIONS'):
                self.write_options(ctx, formatter, opts)

    def format_commands(self, ctx, formatter):
        """Writes command and group lists to the formatter."""
        groups = []
        commands = []

        for subcommand in self.list_commands(ctx):
            command = self.get_command(ctx, subcommand)
            if isinstance(command, click.Group):
                groups.append((subcommand, command.get_short_help_str() or ""))
            else:
                commands.append((subcommand, command.get_short_help_str() or ""))

        if groups:
            with formatter.section('GROUPS'):
                formatter.write_dl(groups)

        if commands:
            with formatter.section('COMMANDS'):
                formatter.write_dl(commands)

    def format_help_text(self, ctx, formatter):
        """Writes the help text to the formatter if it exists."""
        if self.help:
            with formatter.section('DESCRIPTION'):
                cleaned_text = '\n'.join(line.strip() for line in self.help.splitlines())
                formatter.write_text(cleaned_text)

    def format_usage(self, ctx, formatter):
        """Writes the usage format to the formatter."""
        command_path = []
        curr_ctx = ctx
        while curr_ctx is not None:
            command_path.append(curr_ctx.info_name)
            curr_ctx = curr_ctx.parent
        command_path.reverse()
        full_command_path = ' '.join(command_path[1:])

        formatter.write_text("USAGE:")  
        if not full_command_path:  
            formatter.write_text(f"{INDENT}gator [GROUPS | COMMANDS] [OPTIONS]")
        else:
            formatter.write_text(f"{INDENT}gator {full_command_path} [GROUPS | COMMANDS] [OPTIONS]")

    def format_help(self, ctx, formatter):
        """Writes the complete help text to the formatter."""
        self.format_usage(ctx, formatter)
        self.format_help_text(ctx, formatter)
        self.format_commands(ctx, formatter)
        self.format_options(ctx, formatter)

    def write_options(self, ctx, formatter, opts):
        """Writes options into the formatter."""
        
        max_width = max(len(', '.join(opt.opts)) for opt in opts)
        
        for opt in opts:
            opts_str = ', '.join(opt.opts).ljust(max_width)
            help_str = opt.help or ''
            
            formatter.write_dl([(opts_str, help_str)])

"""
class CustomHelpFormatter(click.HelpFormatter):
    def write_dl(self, rows, col_max=30, col_spacing=2):
        rows = [(row[0].upper() if i == 0 else row[0], row[1]) for i, row in enumerate(rows)]
        super().write_dl(rows, col_max, col_spacing)

    def section(self, title):
        title = title.upper()
        super().section(title)
"""

class CustomCommand(click.Command):
    def format_help_text(self, ctx, formatter):
        if self.help:
            formatter.write_paragraph()
            with formatter.indentation():
                formatter.write_text(self.help)

    def format_usage(self, ctx, formatter):
        """Writes the usage format to the formatter."""
        INDENT = '  '  

        command_path = []
        curr_ctx = ctx
        while curr_ctx is not None:
            command_path.append(curr_ctx.info_name)
            curr_ctx = curr_ctx.parent
        command_path.reverse()
        
        full_command_path = ' '.join(command_path[1:])
        
        formatter.write_text("USAGE:")
        if not full_command_path:
            formatter.write_text(f"{INDENT}gator [GROUPS | COMMANDS] [OPTIONS]")
        else:
            formatter.write_text(f"{INDENT}gator {full_command_path} [GROUPS | COMMANDS] [OPTIONS]")
        # formatter.write_paragraph()

    def format_options(self, ctx, formatter):
        opts = []
        for param in self.get_params(ctx):
            rv = param.get_help_record(ctx)
            if rv is not None:
                opts.append(rv)
        if opts:
            with formatter.section('OPTIONS'):
                formatter.write_dl(opts)

    def format_help_text(self, ctx, formatter):
        """Writes the help text to the formatter if it exists."""
        if self.help:
            with formatter.section('DESCRIPTION'):
                cleaned_text = '\n'.join(line.strip() for line in self.help.splitlines())
                formatter.write_text(cleaned_text)

    def format_help(self, ctx, formatter):
        self.format_usage(ctx, formatter)
        self.format_help_text(ctx, formatter)
        self.format_options(ctx, formatter)