from setuptools import setup, find_packages

setup(
    name="TurboTalk",
    version="0.1.4",  # Increment the version number
    packages=find_packages(),
    install_requires=[
        "g4f",
        "colorama",
    ],
    description=[

        f"usage:",
        f"",
        f"import TurboTalk",
        f"",
        f"bot_name = \"Rushi\"",
        f"company_name = \"Rango Production\"",
        f"",
        f"TurboTalk.start_chat(bot_name, company_name)"

        ]

)
