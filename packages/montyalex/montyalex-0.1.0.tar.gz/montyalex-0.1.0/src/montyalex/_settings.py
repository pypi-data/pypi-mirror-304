from typer import Option, Typer

from .console_tools import richconsole
from .uo_tools import json, toml, yaml, mpck


print = richconsole.print

settings_: Typer = Typer(
    name='settings',
    add_help_option=False,
    pretty_exceptions_show_locals=False)

@settings_.command(name='init', hidden=True)
def init_(
    dirname: str = Option('.mtax', '--directory-name', '-dir'),
    filename: str = Option('settings', '--file-name', '-name'),
    *,
    overwrite: bool = Option(False, '--overwrite', '-o'),
    use_json: bool = Option(False, '--json', '-j'),
    use_toml: bool = Option(False, '--toml', '-t'),
    use_yaml: bool = Option(False, '--yaml', '-y'),
    use_mpck: bool = Option(False, '--mpck', '-m')):
    uo: json | toml | yaml | mpck | None = None
    if use_json:
        uo = json(directory=dirname, filename=filename)
    if use_toml:
        uo = toml(directory=dirname, filename=filename)
    if use_yaml:
        uo = yaml(directory=dirname, filename=filename)
    if use_mpck:
        uo = mpck(directory=dirname, filename=filename)
    if uo is None:
        uo = json(directory=dirname, filename=filename)

    if overwrite:
        if isinstance(uo, json):
            uo.change('$schema', '../.mtax-cache/schema.json')
        uo.change('mtax', {'toggles': {'app': True}}, append=False)
    else:
        if isinstance(uo, json):
            uo.change('$schema', '../.mtax-cache/schema.json')
        uo.change('mtax', {'toggles': {'app': True}})

@settings_.command(name='delete', hidden=True)
def delete_(
    dirname: str = Option('.mtax', '--directory-name', '-dir'),
    filename: str = Option('settings', '--file-name', '-name'),
    key: str = Option(None, '--key', '-k'),
    *,
    use_json: bool = Option(False, '--json', '-j'),
    use_toml: bool = Option(False, '--toml', '-t'),
    use_yaml: bool = Option(False, '--yaml', '-y'),
    use_mpck: bool = Option(False, '--mpck', '-m')):
    uo: json | toml | yaml | mpck | None = None
    if use_json:
        uo = json(directory=dirname, filename=filename)
    if use_toml:
        uo = toml(directory=dirname, filename=filename)
    if use_yaml:
        uo = yaml(directory=dirname, filename=filename)
    if use_mpck:
        uo = mpck(directory=dirname, filename=filename)
    if uo is None:
        uo = json(directory=dirname, filename=filename)

    if key:
        uo.change(key, None, overwrite=True)
    uo.remove()

@settings_.command(name='inspect')
def inspect_(
    dirname: str = Option('.mtax', '--directory-name', '-dir'),
    filename: str = Option('settings', '--file-name', '-name'),
    use_json: bool = Option(False, '--json', '-j'),
    use_toml: bool = Option(False, '--toml', '-t'),
    use_yaml: bool = Option(False, '--yaml', '-y'),
    use_mpck: bool = Option(False, '--mpck', '-m'),
    full_inspection: bool = Option(False, '--full', '-fi'),
    mem_alloc_inspection: bool = Option(False, '--memory', '-mi'),
    repr_inspection: bool = Option(False, '--repr', '-ri'),
    exists_inspection: bool = Option(False, '--exists', '-ei'),
    key_inspection: str = Option(None, '--key', '-ki'),
):
    uo: json | toml | yaml | mpck | None = None
    if use_json:
        juo: json = json(directory=dirname, filename=filename)
        uo = juo
    if use_toml:
        tuo: toml = toml(directory=dirname, filename=filename)
        uo = tuo
    if use_yaml:
        yuo: yaml = yaml(directory=dirname, filename=filename)
        uo = yuo
    if use_mpck:
        muo: mpck = mpck(directory=dirname, filename=filename)
        uo = muo
    if uo is None:
        uo = json(directory=dirname, filename=filename)

    inspection: bool = False
    if full_inspection:
        inspection = True
        uo.inspect(full=True)
    if mem_alloc_inspection:
        inspection = True
        uo.inspect(mem_alloc=True)
    if repr_inspection:
        inspection = True
        uo.inspect(representation=True)
    if key_inspection:
        inspection = True
        uo.inspect(key=key_inspection)
    if exists_inspection:
        inspection = True
        if uo.exists:
            print(f'Found! [green]{uo.modelpath}[/]')
        else:
            print(f'Not Found! [red]{uo.modelpath}[/]')
    if not inspection:
        uo.inspect()
        if not uo.exists:
            print('Creating new settings file...')
            init_(
                dirname=dirname,
                filename=filename,
                overwrite=False,
                use_json=use_json,
                use_toml=use_toml,
                use_yaml=use_yaml,
                use_mpck=use_mpck)
            uo.inspect()
