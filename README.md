# Speech-to-Text (STT) Service

## Overview

This repository contains the **Speech-to-Text (STT)** microservice for the **Podcast Recommendation Platform**.  
It is designed to **convert podcast audio into text** using the **Vosk speech recognition engine**, and expose the functionality through a **FastAPI** application with **gRPC** support for high-performance communication.

The service is containerized for easy deployment and scalability.

---

## Key Features

-  **Speech Recognition** powered by [Vosk](https://alphacephei.com/vosk/)  
-  **FastAPI** REST and **gRPC** endpoints for real-time transcription  
-  **Dockerized** for deployment consistency  
-  Supports streaming or batch transcription modes  
-  Can be integrated with Kafka for asynchronous processing  

---

