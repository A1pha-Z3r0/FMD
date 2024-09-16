# **Bacterial Infection Detection Web App**

## **Description**  
This repository contains two separate web applications for detecting bacterial infections in fruits using image classification:

1. **Microscopic Images:**  
   This app is designed to classify bacterial infections using microscopic images of fruit samples.

2. **Macroscopic Images:**  
   This app focuses on classifying infections using macroscopic images of fruits.

Both applications can classify images into one of seven categories, including five types of bacterial infections, a healthy class, and an unknown class:
- Streptococcal
- Staphylococcus
- E. coli
- Klebsiella
- Pseudomonas
- Healthy
- Unknown

The model was trained specifically on images of three fruits:
- Green Apple
- Tomato
- Strawberry

The application combines VGG19 and Vision Transformer (ViT) models to produce accurate classification results.

## **Installation**  
To set up this project on your local machine, follow these steps:

1. **Clone the repository**  
   ```bash
   git clone https://github.com/A1pha-Z3r0/FMD.git
   cd FMD
   ```
2. **Set up a virtual environment (optional but recommended)**
   ```bash
   python3.10 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
4. **Install the dependencies**
   ```bash
   pip install -r requirements.txt
   ```
6. **Download the necessary model files**
   Before running either project, download the model files:
   ```bash
   bash download_models.sh
   ```

## **Usage**
To use the web application:
1. Navigate into any of the directory
2. Run the FastAPI server
   ```bash
   uvicorn app:app --reload
   ```
4. Access the web app
   Open your web browser and navigate to http://localhost:8000
6. Upload images for classification
   The microscopic model has higher accuracy on microscopic images.
   The macroscopic model has higher accuracy on macroscopic images
   
## **Features**
1. Microscopic App: Classifies microscopic images into 7 categories, including 5 bacterial infections.
2. Macroscopic App: Classifies macroscopic images into the same 7 categories.
3. Combined Models: Utilizes both VGG19 and Vision Transformer (ViT) models for enhanced accuracy.
4. Easy Setup: Built using FastAPI for a simple and quick setup process.
5. User-Friendly Interface: Easy-to-use web interface for uploading images and viewing results.
