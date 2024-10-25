import click , os , yaml , json , jinja2
from nimc import Nimc
from nimc.extension import cpp_code


@click.group()
def cli():
    pass 

@cli.command()
@click.argument('name')
@click.argument('path', default=os.getcwd())
def init(name,path) : 
    projectpath = os.path.join(path,name)
    os.makedirs(projectpath , exist_ok=False )
    os.makedirs(os.path.join(projectpath , 'nim'))
    nimcode = 'proc add*( a : cint , b:cint ): cint {.cdecl,exportc,dynlib.} = \n    return a + b'
    print(nimcode, file=open(os.path.join(projectpath , 'nim',f'{name}.nim'),'w'))
    print(f'name : {name}' , file=open(os.path.join(projectpath , 'info.yml') , 'w'))

@cli.command()
@click.argument('path', default=os.getcwd())
def build(path) : 
    yaml_text = open(os.path.join(path,'info.yml'),'r').read()
    data = yaml.safe_load(yaml_text)
    x = Nimc(prj=path)
    name = data.get('name')
    x.setMainFile(f'{name}.nim')
    x.compile()
    rendred = jinja2.Template(cpp_code).render({'extension' : name }) 
    print(rendred, file = open(os.path.join(x.data.buildsrc , f'{name}.cpp'),"w"))

    

    


def main() : 
    cli()


if __name__ == '__main__' : 
    main()

