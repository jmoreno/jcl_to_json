import json 
import csv 

# csv header
fieldnames = ['job_name', 'step_name', 'program_name', 'db2_program_name', 'dd_name', 'dsn', 'disp', 'space', 'dcb', 'sysout']
rows = []

with open('jobs.json') as json_file: 
	jobs = json.load(json_file) 

for job in jobs:
    row = {}
    if 'job_name' in job:
        row['job_name'] = job['job_name']        
    else:
        row['job_name'] = ''

    if len(job['steps']) > 0 :
        for step in job['steps']:
            if 'step_name' in step:
                row['step_name'] = step['step_name']
            else:
                row['step_name'] = ''                                

            if 'program_name' in step:
                row['program_name'] = step['program_name']
            else:
                row['program_name'] = ''

            if 'db2_program_name' in step:
                row['db2_program_name'] = step['db2_program_name']
            else:
                row['db2_program_name'] = ''

            if len(step['datasets']) > 0 :
                for dataset in step['datasets']:
                    if 'dd_name' in dataset:
                        row['dd_name'] = dataset['dd_name']
                    else:
                        row['dd_name'] = ''

                    if 'dsn' in dataset:
                        row['dsn'] = dataset['dsn']
                    else:
                        row['dsn'] = ''

                    if 'disp' in dataset:
                        row['disp'] = dataset['disp']
                    else:
                        row['disp'] = ''

                    if 'space' in dataset:
                        row['space'] = dataset['space']
                    else:
                        row['space'] = ''

                    if 'dcb' in dataset:
                        row['dcb'] = dataset['dcb']
                    else:
                        row['dcb'] = ''

                    if 'sysout' in dataset:
                        row['sysout'] = dataset['sysout']
                    else:
                        row['sysout'] = ''

                    rows.append(row.copy())
            else:
                rows.append(row.copy())
    else:
        rows.append(row.copy())


with open('jobs.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
