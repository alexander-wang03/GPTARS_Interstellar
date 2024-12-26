# TARS from Interstellar x ChatGPT

A recreation of the TARS robot from Interstellar, featuring AI capabilities and servo-driven movement. 
- See `ENVSETUP.md` for instructions on setting up the software environment.
- See `WorkingInGitHub.md` for instructions on contributing.

## Table of Contents
- [Hardware Requirements](#hardware-requirements)
- [Printing Specifications](#printing-specifications)
- [Software Stack](#software-stack)
- [Build Modifications](#build-modifications)
- [Additional Resources](#additional-resources)

## Hardware Requirements (IN DEVELOPMENT)

| Category | Component | Description | Link |
|----------|-----------|-------------|------|
| **Core Components** | Raspberry Pi 5 | Main computing unit | [Buy](https://www.amazon.com/Raspberry-Pi-Quad-core-Cortex-A76-Processor/dp/B0CTQ3BQLS/) |
| | 3.5" LCD Display | Interface display | [Buy](https://www.amazon.com/OSOYOO-3-5inch-Display-Protective-Raspberry/dp/B09CD9W6NQ/) |
| | 16-Channel PWM Servo Driver | I2C Interface | [Buy](https://www.amazon.com/gp/product/B00EIB0U7A/) |
| | Buck Converter | Power management | [Buy](https://www.amazon.com/gp/product/B07SGJSLDL/) |
| **Servo Motors** | diymore MG996R | Digital servo motors (2x 90g micro servos per leg) | [Buy](https://www.amazon.com/diymore-6-Pack-MG996R-Digital-Helicopter/dp/B0CGRP59HJ/) |
| | MG996R 55g (Alternative) | Digital RC servo motors with high torque | - |
| **Drive Train** | Bearings | Motion support | [Buy](https://www.amazon.com/gp/product/B07FW26HD4/) |
| | Springs | Motion dampening | [Buy](https://www.amazon.com/gp/product/B076M6SFFP/) |
| | Metal Rods (Option 1) | Structural support | [Buy](https://www.amazon.com/gp/product/B01MAYQ12S/) |
| | Metal Rods (Option 2) | Alternative structural support | [Buy](https://www.amazon.com/gp/product/B0CTSX8SJS/) |
| | Linkage | Motion transfer | [Buy](https://www.amazon.com/gp/product/B0CRDRWYXW/) |
| | Servo Extension Wires | Connection cables | [Buy](https://www.amazon.com/OliYin-7-87in-Quadcopter-Extension-Futaba/dp/B0711TBZY2/) |
| **Audio System** | Raspberry Pi Microphone | Audio input | [Buy](https://www.amazon.com/gp/product/B086DRRP79/) |
| | Audio Amplifier | Sound processing | [Buy](https://www.amazon.com/dp/B0BTBS5NW2) |
| | Speaker | Audio output | [Buy](https://www.amazon.com/dp/B07GJ4GH67) |
| **Camera System** | Camera Module | Visual input | [Buy](https://a.co/d/50BbE8a) |
| | Camera Ribbon Cable | Camera connection | [Buy](https://www.amazon.com/Onyehn-Raspberry-Camera-Cable-Ribbon/dp/B07XZ5DX5H/) |
| **Fasteners** | M3 20mm Screws | Mounting (6x needed) | [Buy](https://www.amazon.com/gp/product/B0CR6DY4SS/) |
| | M3 14mm Screws | Mounting (40x needed) | [Buy](https://www.amazon.com/gp/product/B0D9GW9K4G/) |
| | M3 10mm Screws | Mounting (76x needed) | [Buy](https://www.amazon.com/gp/product/B0CR6G5XWC/) |

## Printing Specifications
- Printer: Bambu Labs P1S, A1, X1C
- Materials:
  - TPU for all "Flexor" parts ([Buy](https://us.store.bambulab.com/products/tpu-for-ams))
    - Another option ([Buy](https://www.amazon.com/Overture-Filament-Flexible-Consumables-Dimensional/dp/B07VDP2S3P/ref=sr_1_1_sspa?dib=eyJ2IjoiMSJ9.FpCSwxR4TyJ78JqBztFgvMq_9RDGP970D4tJ7cVWk4YuN1ZprdFRl0SNhdoSjB1_pwZYBZ9Yu9JLLHMso9yiSbxlQvMt2gAGJ8jdeai8xi0Edn3PEWZtQpIFzZbd0sAZJW7DUhZ6MjGvCAp_vAYGQKSqrvVx2uD3DTRbwfrOzUYWZ8MBZ7OBa5NhZNNOPVgMIGMeLFTA-3hQ-H5nmnkjtodbMiD_NoDluO8PlPLtCY8.GRyPi-8RjtM51J3bE0mOfoS63XI3osq2uBOhHnt8bCU&dib_tag=se&keywords=TPU&qid=1735245429&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1))
  - PETG for all other parts ([Buy](https://us.store.bambulab.com/products/petg-hf))
  - PLA also works for rapid prototyping.

## Software Stack

[![GPTARS Software Demo](https://img.youtube.com/vi/4YObs8BV3Mc/0.jpg)](https://www.youtube.com/watch?v=4YObs8BV3Mc)

- **LLM**: Choice of:
  - OpenAI (Recomemended)
  - Oobabooga
  - Tabby ([tabbyAPI](https://github.com/theroyallab/tabbyAPI))
- **Text-to-Speech**: Choice of:
  - Azure TTS (Recommended) 
  - Local
  - XTTSv2 with voice cloning ([xtts-api-server](https://github.com/daswer123/xtts-api-server))
- **Speech-to-Text**: Vosk

## Build Modifications
![print](./media/PrintComplete.jpg)
- Modified chassis bottom to accommodate SD card installation (See: "Chassis Bottom (Mod SD CARD).stl")

## Additional Resources
- [@wizard.py](https://www.instagram.com/wizard.py/)
- [@charliediaz](https://www.hackster.io/charlesdiaz/how-to-build-your-own-replica-of-tars-from-interstellar-224833)
- [@gptars](https://www.youtube.com/@gptars)
- [@poboisvert](https://github.com/poboisvert/GPTARS_Interstellar)