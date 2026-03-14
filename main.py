import sys
import requests
from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter city name: ", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get weather", self)
        self.temperature_label = QLabel("", self)
        self.emoji_label = QLabel("☀", self)
        self.description_label = QLabel("", self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")

        vbox = QVBoxLayout() # "Vertical Box." It’s an invisible container that stacks widgets on top of each other.
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.get_weather_button.setObjectName("get_weather_button")
        self.city_input.setObjectName("city_input")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        # ===============================================================

        self.setStyleSheet("""
            QLabel, QPushButton{
                font-family: calibri;
            }
            QLabel#city_label{ 
                font-size: 40px;
                font-style: italic;
            }
            QLineEdit#city_input{
                font-size: 40px;
            }
            QPushButton#get_weather_button{
                font-size: 30px;
                font-weight: bold;
            }
            QLabel#temperature_label{
                font-size: 75px;
            }
            QLabel#emoji_label{
                font-size: 100px;
                font-family: Segoe UI Emoji;
            }
            QLabel#description_label{
                font-size: 50px;}
        
        """)
        # city_label: The # targets the ObjectName you set earlier. It’s like giving a specific person a name tag so you can yell instructions specifically at them.

        self.get_weather_button.clicked.connect(self.get_weather)

    # ===============================================================

    def clear_display(self):
        self.temperature_label.setText("")
        self.emoji_label.setText("")
        self.description_label.setText("")

    def get_weather(self):
        self.clear_display()
        city = self.city_input.text().strip()
        if not city:
            self.temperature_label.setText("Enter city")
            self.emoji_label.setText("ℹ️")
            self.description_label.setText("")
            return
        
        # ===============================================================

        try:
            API_KEY = "f113f0ee229b5c38e108e42611453705"
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={API_KEY}"

            # Make HTTP request and convert response to jsonm
            response = requests.get(url, timeout=10)
            response.raise_for_status()   # if it returns an unsuccesful code raise an http error
            data = response.json() # The server sends back a giant dictionary (JSON).

            # OpenWeather returns code in JSON for invalid city too, so check it
            if data.get("cod") != 200:
                err_msg = data.get("message", "Unknown error").capitalize()
                self.temperature_label.setText("City not found")
                self.emoji_label.setText("❌")
                self.description_label.setText(err_msg)
                return

            temp = data["main"]["temp"] # find the specific number for the temperature.
            weather_id = data["weather"][0]["id"]
            desc = data["weather"][0]["description"].capitalize()
            
            # Map emojis based on ID ranges
            if 200 <= weather_id <= 232:
                emoji = "⛈️"
            elif 300 <= weather_id <= 531:
                emoji = "🌧️"
            elif 600 <= weather_id <= 622:
                emoji = "❄️"
            elif 701 <= weather_id <= 781:
                emoji = "🌫️"
            elif weather_id == 800:
                emoji = "☀️"
            else:
                emoji = "☁️"

            self.temperature_label.setText(f"{temp:.1f}°C")
            self.description_label.setText(desc)
            self.emoji_label.setText(emoji)

        except requests.exceptions.HTTPError as http_error:
            self.temperature_label.setText("HTTP error")
            self.emoji_label.setText("⚠️")

        except requests.exceptions.RequestException as req_error:
            self.temperature_label.setText("Network error")
            self.emoji_label.setText("❌")

        except Exception as unexpected_error:
            self.temperature_label.setText("Error")
            self.emoji_label.setText("❗")

        # ===============================================================


if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp() # create a variable that is the class
    weather_app.show() # show the class
    sys.exit(app.exec_()) # make sure it wont exit after lunch