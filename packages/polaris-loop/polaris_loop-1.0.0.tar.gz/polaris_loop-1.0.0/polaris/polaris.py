import click
from polaris.loopScore import score
from polaris.loopPool import pool
from polaris.loop import pred
from polaris.utils.util_cool2bcool import cool2bcool
from polaris.utils.util_pileup import pileup

@click.group()
def cli():
    '''
    Polaris

    A Unified Axial-aware Framework for Chromatin Loop Annotation in Bulk and Single-cell Hi-C Data
    '''
    pass

@cli.group()
def loop():
    '''loop annotation

    \b
    run pred to detect loops from Hi-C data and other data types.
    '''
    pass

@cli.group()
def util():
    '''utilities'''
    pass

loop.add_command(pred)
loop.add_command(score)
loop.add_command(pool)

util.add_command(cool2bcool)
util.add_command(pileup)


if __name__ == '__main__':
    cli()