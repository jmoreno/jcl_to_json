# jcl_to_json
Un par de scripts en python para extraer información de un jcl a json y de ahí pasar a un fichero csv.

Hay veces que toda la información que contiene un JCL estaría mucho mejor en un formato que pudiese ser más "explorable". La idea con este par de scripts en python es poder leer un fichero JCL que contenga uno o varios jobs y extraer determinados campos (los que yo necesitaba) a una estructura de tipo json y de ahí a un fichero csv. De esta manera puedes mostrar en una pagina web los datos más importantes de tus cadenas o llevar un buen control de las mismas en Excel...

## De JCL a JSON.

Con el script 'jcl.py' podemos pasar de esto:

    //TTYYSAMP JOB 'TUTO',CLASS=6,MSGCLASS=X,REGION=8K,
    //         NOTIFY=&SYSUID
    //*
    //STEP010  EXEC PGM=ICETOOL,ADDRSPC=REAL
    //*
    //INPUT1   DD DSN=TUTO.SORT.INPUT1,DISP=SHR
    //INPUT2   DD DSN=TUTO.SORT.INPUT2,DISP=SHR,UNIT=SYSDA,
    //         VOL=SER=(1243,1244)
    //OUTPUT1  DD DSN=MYFILES.SAMPLE.OUTPUT1,DISP=(,CATLG,DELETE),
    //         RECFM=FB,LRECL=80,SPACE=(CYL,(10,20))
    //OUTPUT2  DD SYSOUT=*

a esto:

    [
        {
            "job_name": "TTYYSAMP",
            "steps": [
                {
                    "datasets": [
                        {
                            "dd_name": "INPUT1  ",
                            "dsn": "TUTO.SORT.INPUT1"
                        },
                        {
                            "dd_name": "INPUT2  ",
                            "disp": "SHR",
                            "dsn": "TUTO.SORT.INPUT2"
                        },
                        {
                            "dd_name": "OUTPUT1 ",
                            "disp": "(,CATLG,DELETE)",
                            "dsn": "MYFILES.SAMPLE.OUTPUT1",
                            "space": "(CYL,(10,20)"
                        },
                        {
                            "dd_name": "OUTPUT2 ",
                            "sysout": "*"
                        }
                    ],
                    "program_name": "ICETOOL",
                    "step_name": "STEP010 "
                }
            ]
        }
    ]

## De JSON a CSV.

Con el script 'jsontocsv.py' podemos terminar viendo esto:

    job_name,step_name,program_name,db2_program_name,dd_name,dsn,disp,space,dcb,sysout
    TTYYSAMP,STEP010 ,ICETOOL,,INPUT1  ,TUTO.SORT.INPUT1,,,,
    TTYYSAMP,STEP010 ,ICETOOL,,INPUT2  ,TUTO.SORT.INPUT2,SHR,,,
    TTYYSAMP,STEP010 ,ICETOOL,,OUTPUT1 ,MYFILES.SAMPLE.OUTPUT1,"(,CATLG,DELETE)","(CYL,(10,20)",,
    TTYYSAMP,STEP010 ,ICETOOL,,OUTPUT2 ,,,,,*


