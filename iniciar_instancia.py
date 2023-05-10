import boto3
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):

    ec2client = boto3.resource('ec2')
    idInstancia = event['detail']['instance-id']
    instancia = ec2client.Instance(idInstancia)
    if instancia.state['Name'] == "stopped":
        iniciada = False
        for tag in instancia.tags:
            if tag['Key'] == 'inactividad' and tag['Value'] == 'no':
                instancia.start()
                mensaje = 'La instancia EC2 con ID '+idInstancia+' estaba parada y se inicia de nuevo'
                iniciada = True
                break
        if not iniciada:
            mensaje = 'La instancia EC2 con ID '+idInstancia+' estaba parada y no se iniciaraá de nuevo'
    else:
        mensaje = 'Evento procesado con anterioridad para la instancia EC2 con ID '+idInstancia
    logger.info(mensaje)
    return {"message":mensaje}