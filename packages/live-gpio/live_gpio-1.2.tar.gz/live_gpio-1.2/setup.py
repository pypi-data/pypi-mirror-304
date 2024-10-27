from setuptools import setup, find_packages

setup(
    name="live-gpio",
    version="1.2",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Flask",
        "pigpio",
        "Flask-SocketIO"
    ],
    entry_points={
        "console_scripts": [
            "live-gpio=live_gpio.app:main"
        ]
    },
    package_data={
        "live_gpio": ["templates/*.html", "static/*"]
    },
)