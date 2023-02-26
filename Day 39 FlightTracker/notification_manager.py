class NotificationManager:
    """Send notifications with the deal flight details."""
    def __init__(self, details: dict):
        flight_dict = details
        self.text = f"SMS: Price alert: Only {flight_dict['lowest price']} NOK " \
                    f"from Oslo-OSL to {flight_dict['to_city']}-{flight_dict['iata']}. " \
                    f"Date(s): {flight_dict['date(s)']}."
        print(self.text)
