
import re
import json

input_file = 'example.jcl'

jobs = []
job = {}
step = {}
dataset = {}

def initialize_job():
    job.clear()
    step.clear()
    dataset.clear()

def initialize_step():
    step.clear()
    dataset.clear()

def initialize_dataset():
    dataset.clear()

def check_jcl_line(line):
    # Si la linea comienza con un comentario se deja de leer
    if line.startswith('//*'):
        return
    elements = {}
    # Comprobamos si es linea de JOB
    m = re.search('//(.+?) JOB', line)
    if m:
        found = m.group(1)
        elements['JOB'] = found
    # Comprobamos si es linea de EXEC
    m = re.search('//(.+?) EXEC ', line)
    if m:
        found = m.group(1)
        elements['EXEC'] = found
    # Comprobamos si la linea contiene el nombre del programa
    m = re.search('PGM=(.+?),', line)
    if m:
        found = m.group(1)
        elements['PGM'] = found
    else:
        m = re.search('PGM=(.+?), ', line)
        if m:
            found = m.group(1)
            elements['PGM'] = found
    # Comprobamos si es linea de DD
    m = re.search('//(.+?) DD ', line)
    if m:
        found = m.group(1)
        elements['DD'] = found
    # Comprobamos si la linea contiene el nombre del fichero
    m = re.search('DSN=(.+?),', line)
    if m:
        found = m.group(1)
        elements['DSN'] = found
    else:
        m = re.search('DSN=(.+?), ', line)
        if m:
            found = m.group(1)
            elements['DSN'] = found
    # Comprobamos si la linea contiene el nombre del fichero
    m = re.search('DSN=(.+?),', line)
    if m:
        found = m.group(1)
        elements['DSN'] = found
    else: 
        m = re.search('DSN=(.+?) ', line)
        if m:
            found = m.group(1)
            elements['DSN'] = found
    # Comprobamos si la linea contiene el estado del fichero
    m = re.search('DISP=\((.+?)\)', line)
    if m:
        found = m.group(1)
        elements['DISP'] = '({})'.format(found)
    else: 
        m = re.search('DISP=(.+?),', line)
        if m:
            found = m.group(1)
            elements['DISP'] = found
        else: 
            m = re.search('DISP=(.+?) ', line)
            if m:
                found = m.group(1)
                elements['DISP'] = found
    # Comprobamos si la linea contiene el espacio del fichero
    m = re.search('SPACE=\((.+?)\)', line)
    if m:
        found = m.group(1)
        elements['SPACE'] = '({})'.format(found)
    # Comprobamos si la linea contiene el bloque de control de datos
    m = re.search('DCB=\((.+?)\)', line)
    if m:
        found = m.group(1)
        elements['DCB'] = '({})'.format(found)
    # Comprobamos si la linea contiene el bloque de salida a consola
    m = re.search('SYSOUT=(.+?)', line)
    if m:
        found = m.group(1)
        elements['SYSOUT'] = found
    # Comprobamos si la linea contiene el bloque de programa con DB2
    m = re.search('PROGRAM\((.+?)\)', line)
    if m:
        found = m.group(1)
        elements['PROGRAM'] = found
    return elements

def main():
    with open(input_file) as fp:
        for line in fp:
            results = check_jcl_line(line[:72])
            if results:
                if 'JOB' in results:
                    if len(job)>0:
                        if len(step)>0:
                            if len(dataset)>0:
                                step['datasets'].append(dataset.copy())
                            job['steps'].append(step.copy())
                        jobs.append(job.copy())
                        initialize_job()
                    job['job_name'] = results['JOB']
                    job['steps'] = []
                if 'EXEC' in results:
                    if len(step)>0:
                        if len(dataset)>0:
                            step['datasets'].append(dataset.copy())
                        job['steps'].append(step.copy())
                        initialize_step()
                    step['step_name'] = results['EXEC']
                    step['datasets'] = [] 
                if 'PGM' in results:
                    step['program_name'] = results['PGM']
                if 'PROGRAM' in results:
                    step['db2_program_name'] = results['PROGRAM']
                if 'DD' in results:
                    if len(dataset)>0:
                        step['datasets'].append(dataset.copy())
                        initialize_dataset()
                    dataset['dd_name'] = results['DD']
                if 'DSN' in results:
                    dataset['dsn'] = results['DSN']
                if 'DISP' in results:
                    dataset['disp'] = results['DISP']
                if 'DCB' in results:
                    dataset['dcb'] = results['DCB']
                if 'SPACE' in results:
                    dataset['space'] = results['SPACE']
                if 'SYSOUT' in results:
                    dataset['sysout'] = results['SYSOUT']
        
        if len(job)>0:
            if len(step)>0:
                if len(dataset)>0:
                    step['datasets'].append(dataset.copy())
                job['steps'].append(step.copy())
            jobs.append(job.copy())

        output_file = open("jobs.json", "w")
        output_file.write(json.dumps(jobs, indent=4, sort_keys=True))
        output_file.close()
        # print(json.dumps(jobs, indent=4, sort_keys=True))
                
if __name__ == '__main__':
    main()
