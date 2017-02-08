async def send_to_client(packet_type, packet_data):
    """Implementation of this function not shown."""
    raise RuntimeError('Nope')


async def trigger_event(event_name, event_data):
    """Implementation of this function not shown."""
    raise RuntimeError('Nope')


async def receive(packet_type, packet_data):
    """Receive packet from the client."""
    if packet_type == 'PING':
        await send_to_client("PONG", packet_data)
    elif packet_type == 'MESSAGE':
        response = await trigger_event('message', packet_data)
        await send_to_client('MESSAGE', response)
    else:
        raise ValueError('Invalid packet type')
