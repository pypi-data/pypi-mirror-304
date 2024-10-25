import requests

BASE_URL = "https://365SMS.ru/stubs/handler_api.php"  # Base URL of the API


class Sms365Client:
    """
    This is a class for API requests to 365SMS.

    Attributes:
        api_key (str): Your 365SMS API Key.
    """
    def __int__(self, api_key):
        """
        The constructor for Sms365Client class.

        Parameters:
            api_key (str): Your 365SMS API Key.
        """
        self.api_key = api_key

    def get_number_status(self, country, operator=None) -> dict:
        """
        Gets the quantity of available numbers in the specified country for services.

        Args:
            country (str | int): The country number.
            operator (str | int): The operator of the country. If not specified, a random one will be used.

        Returns:
            dict: JSON answer from server with quantity list.
        """
        if operator is None:
            response = requests.get(BASE_URL + "?api_key={}&action=getNumbersStatus&country={}".format(
                self.api_key,
                country
            ))
            return response.json()
        return requests.get(BASE_URL + "?api_key={}&action=getNumbersStatus&country={}&operator={}".format(
            self.api_key,
            country,
            operator
        )).json()

    def get_balance(self):
        """
        Gets the balance of client account.

        Returns:
            str: String with balance value.
        """
        return requests.get(BASE_URL + "?api_key={}&action=getBalance".format(self.api_key)).text

    def get_number(self, service, country, operator=None):
        """
        Buys and gets a number from 365SMS for the specified country, service and operator.

        Args:
            service (str): The service where the code will come from.
            country (str | int): The country number.
            operator (str | int): The operator of the country. If not specified, a preferable one will be used.

        Returns:
            str: String with number and activation ID.
        """
        if operator is None:
            response = requests.get(BASE_URL + "?api_key={}&action=getNumber&service={}&country={}".format(
                self.api_key,
                service,
                country
            ))
            return response.text
        return requests.get(BASE_URL + "?api_key={}&action=getNumber&service={}&operator={}&country={}".format(
            self.api_key,
            service,
            operator,
            country
        )).text

    def set_status(self, status, activation_id):
        """
        Sets a status of the order.

        Args:
            status (str | int): The number(code) of the operation (3 | 6 | 8).
            activation_id (str | int): The activation ID of the number.

        Returns:
            str: String with server answer.
        """
        response = requests.get(BASE_URL + "?api_key={}&action=setStatus&status={}&id={}".format(
            self.api_key,
            status,
            activation_id
        ))
        return response.text

    def get_status(self, activation_id):
        """
        Gets a status or the sms-code of the order.

        Args:
            activation_id (str | int): The activation ID of the number.

        Returns:
            str: String with sms-code.
        """
        response = requests.get(BASE_URL + "?api_key={}&action=getStatus&id={}".format(self.api_key, activation_id))
        return response.text

    def get_prices(self, country, service=None):
        """
        Gets a price list of the specified country and service.

        Args:
            country (str | int): The country number.
            service (str): The service where the code will come from.

        Returns:
            dict: JSON answer from server with price list.
        """
        if service is None:
            response = requests.get(BASE_URL + "?api_key={}&action=getPrices&country={}".format(
                self.api_key,
                country
            ))
            return response.json()
        return requests.get(BASE_URL + "?api_key={}&action=getPrices&service={}&country={}".format(
            self.api_key,
            service,
            country
        )).json()
