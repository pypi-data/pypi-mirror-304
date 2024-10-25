import socket
import json

class Client:
    """
    A class to handle communication with a remote server.

    Attributes:
        host (str): The server host address.
        port (int): The server port number.
    """
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def _send_request(self, message: str = None, image_path: str = None) -> str:
        """
        Sends a request to the server and receives a response.

        Args:
            message (str, optional): Text message to send.
            image_path (str, optional): Path to the image file to send.

        Raises:
            NotImplementedError: If both message and image_path are provided or both are None.

        Returns:
            str: The server response.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.host, self.port))
            if message is not None and image_path is None:
                sock.sendall(message.encode())
            elif message is None and image_path is not None:
                sock.sendall(b'IMAGE')
                with open(image_path, 'rb') as image_file:
                    image_data = image_file.read()
                    sock.sendall(image_data)
                sock.sendall(b'END')
            else:
                raise NotImplementedError(f"Please enter one of the text or image")
            response = sock.recv(1024)
        return response.decode()

    def get_mass(self, object_name: str, volume: float) -> float:
        """
        Retrieves the mass of a specified object.

        Args:
            object_name (str): Name of the object.
            volume (float): Volume of the object.

        Returns:
            float: The mass of the object.
        """
        message = f"mass:{object_name}:{volume}"
        response = self._send_request(message)
        return float(response)

    def get_friction_coefficient(self, object_name: str) -> float:
        """
        Retrieves the friction coefficient of a specified object.

        Args:
            object_name (str): 
                Name of the object for which to retrieve the friction coefficient.

        Returns:
            float: The friction coefficient of the object.
        """
        message = f"friction_coefficient:{object_name}"
        response = self._send_request(message)
        return float(response)

    def get_scene_tag(self, object_name: str) -> list[str]:
        """
        Retrieves the scene tag for a specified object.

        Args:
            object_name (str): 
                Name of the object for which to retrieve the scene tag.

        Returns:
            list: The scene tag information for the object.
        """
        message = f"scene:{object_name}"
        response = self._send_request(message)
        return json.loads(response)

    def get_material(self, object_name: str) -> list[str]:
        """
        Retrieves the material information for a specified object.

        Args:
            object_name (str): 
                Name of the object for which to retrieve material information.

        Returns:
            list: The material information for the object.
        """
        message = f"material:{object_name}"
        response = self._send_request(message)
        return json.loads(response)

    def get_fuzzy_name(self, object_name: str) -> list[str]:
        """
        Retrieves fuzzy name information for a specified object.

        Args:
            object_name (str): 
                Name of the object for which to retrieve fuzzy name information.

        Returns:
            list: The fuzzy name information for the object.
        """
        message = f"fuzzy_name:{object_name}"
        response = self._send_request(message)
        return json.loads(response)
    
    def get_spatial_semantics(self, object_name: str) -> tuple[list[str], list[str]]:
        """
        Retrieves spatial semantics (parent and children) for a specified object.

        Args:
            object_name (str): 
                Name of the object for which to retrieve spatial semantics.

        Returns:
            tuple: A tuple containing lists of parent and child names.
        """
        try:
            message = f"spatial:{object_name}"
            response = self._send_request(message)
            parts = response.split('], [')
            parents = json.loads(parts[0] + "]")
            children = json.loads("[" + parts[1])
        except:
            return ["None"], ["None"]
        return parents, children
    
    def get_asset_name(self, image_path: str) -> str:
        """
        Retrieves the asset name based on the provided image path.

        Args:
            image_path (str): 
                The path to the image.

        Returns:
            str: The name of the asset.
        """
        response = self._send_request(image_path=image_path)
        return str(response)