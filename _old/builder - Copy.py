import jinja2
import yaml
import datetime
import subprocess

def loadYAML(inpf):
    '''
    Loads YAML inputs
    '''
    with open(inpf, 'r') as stream:
        try:
           return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    
#This stuff just tells JINJA2 how to read templates
templateLoader = jinja2.FileSystemLoader(searchpath="./")
templateEnv = jinja2.Environment(
    loader=templateLoader,
	block_start_string = '\BLOCK{',
	block_end_string = '}',
	variable_start_string = '\VAR{',
	variable_end_string = '}',
	comment_start_string = '\#{',
	comment_end_string = '}',
	line_statement_prefix = '%%',
	line_comment_prefix = '%#',
	trim_blocks = True,
	autoescape = False,
)
mainTemplate = templateEnv.get_template("./templates/OpenProject.tex")
introTemplate = templateEnv.get_template("./templates/introTemplate.tex")
areaTemplate = templateEnv.get_template("./templates/areaTemplate.tex")

#variables
today = datetime.date.today()
inp = loadYAML('input.yaml')

a = mainTemplate.render(inp)
f = open('./sections/'+'main.tex','w')
f.write(a)
f.close()

a = introTemplate.render(inp)
f = open('./sections/'+'intro.tex','w')
f.write(a)
f.close()

for area in inp['areas']:
    a = areaTemplate.render(inp[area], area = area)
    f = open('./sections/areas/'+area+'.tex','w')
    f.write(a)
    f.close()

#Schedule = template.render(Meeting)
#f = open("./Schedules/"+ScheduleDate+"_Schedule.tex",'w')
#f.write(Schedule)
#f.close()
#
#process = subprocess.Popen(['pdflatex', ScheduleDate+"_Schedule.tex"], cwd='./Schedules/')
#process.wait()