@echo off

REM 1. Create a venv folder
echo Creating virtual environment inside venv folder...
python -m venv venv

REM 2. Activate the venv
echo Activating venv...
call venv\Scripts\activate.bat

REM 3. Install dependencies from requirements.txt
echo Installing dependencies from requirements.txt
pip install -r requirements.txt

REM 4. Download stable-diffusion-v1-5
echo Downloading stable-diffusion-v1-5
git clone --branch fp16 https://huggingface.co/runwayml/stable-diffusion-v1-5 repos\animatediff\models\StableDiffusion\stable-diffusion-v1-5

REM 5. Download Motion Modules
echo Downloading Motion Modules
git clone https://huggingface.co/guoyww/animatediff repos\animatediff\models\Motion_Module

REM 6. Download toonyou model
set /p downloadModel=Do you want to download toonyou model? (y/n):
if "%downloadModel%"=="y" (
    echo Downloading toonyou model
    curl -k -L https://civitai.com/api/download/models/78775 -o models\checkpoints\toonyou_beta3.safetensors
) else (
    echo Skipping toonyou model download
)

REM 7. Run VisionCrafter
echo Launching VisionCrafter
python main.py

pause
