
# AI-Powered Food Finder 🍔🤖  

**AI-Powered Food Finder** is a web tool that helps you discover food options tailored to your allergies, taste preferences, and budget. Using UberEats data from nearby restaurants, combined with the power of OpenAI's API, this tool filters out the noise and serves you with curated food choices that fit your needs.  

### 🚀 Features  
- **Personalized Filters**: Find meals that match your allergies, taste preferences, and price limits.  
- **AI-Powered Suggestions**: Leverage OpenAI’s language model for intelligent filtering and recommendations.  
- **Restaurant Integration**: Works seamlessly with UberEats data to provide real-time options.  

---

## 🛠️ Getting Started  

Follow these steps to set up and run the project on your local machine:  

### 1. Clone the Repository  
```bash  
git clone https://github.com/Rtfarchitect/FoodSeeker/  
```  

### 2. Set Up the Environment  
Ensure you have **Python 3.10** installed. Create a Conda environment:  
```bash  
conda create -n food-finder python=3.10  
conda activate food-finder  
```  

### 3. Install Dependencies  
Use `pip` to install the required libraries:  
```bash  
pip install -r requirements.txt  
```  

### 4. Add Your OpenAI API Key  
To use the OpenAI API for food filtering, you need to set your API key as an environment variable:  
- Create a `.env` file in the root directory of the project.  
- Add the following line to the `.env` file:  
  ```bash  
  OPENAI_API_KEY=your-openai-api-key  
  ```  

### 5. Run the Web Tool  
Start the application with the following command:  
```bash  
streamlit run app.py  
```  

Access the tool in your browser at `http://localhost:8880`.  

---

## 🧑‍💻 How It Works  
1. The tool retrieves UberEats data for restaurants near you.  
2. Using the OpenAI API, the tool processes your preferences for allergies, taste, and budget.  
3. Results are filtered and displayed in an intuitive web interface for easy browsing.  

---

## 🌟 Contributing  
We welcome contributions! Feel free to fork the repository, create a new branch, and submit a pull request.  

---

## 📜 License  
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.  

---

## 📧 Contact  
Have questions or feedback? Reach out to us at: **your-email@example.com**  

---

Let me know if you'd like any specific changes or additions!
