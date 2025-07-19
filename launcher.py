#!/usr/bin/env python3

import subprocess
import sys
import os

def run_with_venv():
    """Run superhero_updated.py with the virtual environment"""
    
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    venv_python = os.path.join(current_dir, 'venv', 'bin', 'python')
    script_path = os.path.join(current_dir, 'superhero_updated.py')
    
    print("🚀 Running superhero script with virtual environment...")
    
    try:
        # Run the script with the venv Python
        result = subprocess.run([venv_python, script_path], 
                              capture_output=False, 
                              text=True)
        
        if result.returncode == 0:
            print("✅ Script completed successfully!")
        else:
            print(f"❌ Script failed with return code: {result.returncode}")
            
    except FileNotFoundError:
        print("❌ Virtual environment not found!")
        print("Please make sure the venv folder exists in this directory.")
    except Exception as e:
        print(f"❌ Error running script: {e}")

if __name__ == "__main__":
    run_with_venv()
