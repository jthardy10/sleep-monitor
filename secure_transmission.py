from cryptography.fernet import Fernet
from datetime import datetime
import base64
import json
import zmq
import ssl
import logging

class SecureTransmitter:
    def __init__(self):
        self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        
        self.ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.ssl_context.load_cert_chain(certfile="server.crt", keyfile="server.key")
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def encrypt_payload(self, data):
        try:
            json_data = json.dumps(data)
            encrypted_data = self.cipher_suite.encrypt(json_data.encode())
            return base64.b64encode(encrypted_data).decode()
        except Exception as e:
            self.logger.error(f"Encryption error: {str(e)}")
            raise

    def decrypt_payload(self, encrypted_data):
        try:
            decoded_data = base64.b64decode(encrypted_data.encode())
            decrypted_data = self.cipher_suite.decrypt(decoded_data)
            return json.loads(decrypted_data.decode())
        except Exception as e:
            self.logger.error(f"Decryption error: {str(e)}")
            raise

    def send_data(self, data):
        try:
            encrypted_payload = self.encrypt_payload(data)
            timestamp = datetime.now().isoformat()
            
            message = {
                "payload": encrypted_payload,
                "timestamp": timestamp,
                "signature": self.generate_signature(encrypted_payload + timestamp)
            }
            
            self.socket.send_json(message)
            self.logger.info("Data sent successfully")
            return True
        except Exception as e:
            self.logger.error(f"Transmission error: {str(e)}")
            return False

    def generate_signature(self, data):
        import hmac
        import hashlib
        key = b"your-secret-key-here"
        signature = hmac.new(key, data.encode(), hashlib.sha256).hexdigest()
        return signature
