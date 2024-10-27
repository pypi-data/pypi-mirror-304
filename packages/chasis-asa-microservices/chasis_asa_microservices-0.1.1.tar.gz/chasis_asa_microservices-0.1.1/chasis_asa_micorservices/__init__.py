from datetime import datetime, timedelta
import logging
import jwt
import pika
import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

### 
### Funciones para enviar mensajes a RabbitMQ ###
###

def get_rabbitmq_channel(exchange: str, exchange_type: str, config: dict):
    """
    Crea un canal de comunicación con RabbitMQ y declara un exchange con el tipo correspondiente.
    
    Args:
        exchange (str): Nombre del exchange.
        exchange_type (str): Tipo de exchange. Puede ser 'direct', 'topic', 'fanout' o 'headers'.
        config (dict): Configuración de RabbitMQ. Debe contener las claves 'RABBIT_HOST', 'RABBIT_USER' y 'RABBIT_PASSWORD'.
        
    Returns:
        pika.channel.Channel: Canal de comunicación con RabbitMQ.
    """
    # Autenticación con credenciales
    credentials = pika.PlainCredentials(config.RABBIT_USER, config.RABBIT_PASSWORD)
    connection_params = pika.ConnectionParameters(config.RABBIT_HOST, credentials=credentials)
    
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()
    
    # Declarar el exchange con el tipo correspondiente
    channel.exchange_declare(exchange=exchange, exchange_type=exchange_type, durable=True)
    return channel

def send_topic_message(message: str, routing_key: str, exchange: str, config: dict):
    """
    Envía un mensaje a un exchange de tipo 'topic' con una clave de enrutamiento.
    
    Args:
        message (str): Mensaje a enviar.
        routing_key (str): Clave de enrutamiento.
        exchange (str): Nombre del exchange.
        config (dict): Configuración de RabbitMQ. Debe contener las claves 'RABBIT_HOST', 'RABBIT_USER' y 'RABBIT_PASSWORD'.
    """
    
    channel = get_rabbitmq_channel(exchange, 'topic')
    channel.basic_publish(exchange=exchange,
                          routing_key=routing_key,
                          body=json.dumps({"message": message}))
    print(f"[x] Sent '{message}' with routing key '{routing_key}' to topic exchange '{exchange}'")
    channel.close()
    
    
###
### Funciones genericas de la base de datos ###
###

async def get_list(db: AsyncSession, model):
    """
    Retrieve a list of elements from database
    
    Args:
        db (AsyncSession): Database session
        model: Database model to retrieve
        
    Returns:
        list: List of elements
    """
    result = await db.execute(select(model))
    item_list = result.unique().scalars().all()
    return item_list


async def get_list_statement_result(db: AsyncSession, stmt):
    """
    Execute given statement and return list of items.
    
    Args:
        db (AsyncSession): Database session
        stmt: Statement to execute
        
    Returns:
        list: List of items
    """
    result = await db.execute(stmt)
    item_list = result.unique().scalars().all()
    return item_list


async def get_element_statement_result(db: AsyncSession, stmt):
    """
    Execute statement and return a single items
    
    Args:
        db (AsyncSession): Database session
        stmt: Statement to execute
        
    Returns:
        Any: Single item
    """
    result = await db.execute(stmt)
    item = result.scalar()
    return item


async def get_element_by_id(db: AsyncSession, model, element_id):
    """
    Retrieve any DB element by id.
    
    Args:
        db (AsyncSession): Database session
        model: Database model to retrieve
        element_id: ID of the element to retrieve
        
    Returns:
        Any: Element retrieved
    """
    if element_id is None:
        return None

    element = await db.get(model, element_id)
    return element

###
### Funciones de jwt ###
###

ALGORITHM = "RS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 30
    
def create_access_token(data: dict, expires_delta: timedelta = None, private_key_pem: bytes = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, private_key_pem, algorithm=ALGORITHM)

def create_refresh_token(data: dict, private_key_pem: bytes = None):
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, private_key_pem, algorithm=ALGORITHM)

# Esta funcion al chasis de la aplicacion
def decode_refresh_token(token: str, public_key_client_pem: bytes = None):
    try:
        payload = json.loads(json.dumps(jwt.decode(token, public_key_client_pem, ['RS256'])))
        return payload
    except Exception as exc:  # @ToDo: To broad exception
        logging.error(f"Error decoding the token: {exc}")
        # raise_and_log_error(logger, status.HTTP_403_CONFLICT, f"Error decoding the token: {exc}")
        
def decode_jwt(token: str, public_key_client_pem: bytes = None):
    try:
        payload = json.loads(json.dumps(jwt.decode(token, public_key_client_pem, ['RS256'])))
        return payload
    except Exception as exc:  # @ToDo: To broad exception
        logging.error(f"Error decoding the token: {exc}")
        # raise_and_log_error(logger, status.HTTP_403_CONFLICT, f"Error decoding the token: {exc}")
        