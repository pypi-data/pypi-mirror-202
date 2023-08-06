"""
Runs SikuliX scripts from Python.
"""

import os
import requests
import subprocess


def run_sikuli_script(script_path):
    """Runs a SikuliX script from Python.

    Args:
        script_path (str): The path to the script to run.

    Returns:
        int: The exit code of the SikuliX script.
    """
    # Check if Sikuli is installed
    sikuli_jar = os.path.join(os.path.dirname(__file__), "lib", "sikulixide-2.0.5.jar")
    if not os.path.isfile(sikuli_jar):
        # Create lib directory and download Sikuli
        print("(First time running, downloading SikuliX... you better not queue...)")
        os.makedirs(os.path.dirname(sikuli_jar), exist_ok=True)
        url = "https://launchpad.net/sikuli/sikulix/2.0.5/+download/sikulixide-2.0.5.jar"
        with open(sikuli_jar, "wb") as f:
            f.write(requests.get(url).content)
    
    # Run Sikuli
    return subprocess.call(
        ["java", "-jar", sikuli_jar, "-r", script_path],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
