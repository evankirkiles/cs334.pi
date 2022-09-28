import json
from websocket import WebSocket, create_connection

class SocketManager():

  # location of the web server, e.g. ws://localhost:3000
  uri: str
  ws: WebSocket

  def __init__(self, uri: str):
    """Listens for input on the specified pins"""
    self.uri = uri
  
  def connect(self):
    """Connects to the websocket server"""
    self.ws = create_connection(self.uri)
  
  def send(self, data: object):
    """Sends information through the websocket"""
    self.ws.send(json.dumps({
        "controller": 1,
        "message": data
    }))
  
  def close(self):
    """Ends the websocket session"""
    self.ws.close()