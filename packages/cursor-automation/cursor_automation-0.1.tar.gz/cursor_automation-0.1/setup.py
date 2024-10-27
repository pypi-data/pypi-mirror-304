from setuptools import setup, find_packages

setup(
    name="cursor_automation",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "PyQt6==6.5.2",
        "pyautogui==0.9.54",
        "opencv-python==4.8.0.76",
        "numpy==1.25.2",
    ],
    entry_points={
        "console_scripts": [
            "cursor_automation=cursor_automation:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.png", "*.json"],
    },
)
