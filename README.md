# 🚺 StreeTranam - Smart Women Safety Route System

## 🌟 Overview

**StreeTranam** is an AI-powered women safety application that helps users find the **safest travel routes** using real-time data, user reports, and safety analysis.

The system uses **maps, clustering, and user inputs** to identify unsafe zones and guide users through safer paths.

---

## 🚀 Features

* 🗺️ Interactive map using Folium
* 📍 Detect and display unsafe locations
* 📊 Safety score calculation
* 🤖 AI-based clustering of danger zones (KMeans)
* 📸 Image upload for incident reporting
* 📡 Real-time data visualization
* 🛣️ Smart safest route suggestion

---

## 🛠️ Tech Stack

* **Frontend:** Streamlit
* **Backend:** Python
* **Database:** MySQL
* **Libraries:**

  * pandas
  * numpy
  * folium
  * streamlit-folium
  * scikit-learn
  * requests

---

## 📂 Project Structure

```
streetranamproject/
│
├── chatui.py
├── safety_data.csv
├── requirements.txt
├── README.md
└── .gitignore
```
## ⭐UI
---
<img width="915" height="801" alt="image" src="https://github.com/user-attachments/assets/1f2f36fb-b69d-4939-aca4-370e8a7ab848" />
<img width="914" height="782" alt="image" src="https://github.com/user-attachments/assets/8a45d30a-b67a-4824-8d85-e6ae808f988b" />
<img width="923" height="682" alt="image" src="https://github.com/user-attachments/assets/854a9539-b8ea-4e57-9187-87ab1f85499b" />
<img width="891" height="759" alt="image" src="https://github.com/user-attachments/assets/07629aed-18a0-4add-8e86-0a8d2dde8789" />
<img width="926" height="808" alt="image" src="https://github.com/user-attachments/assets/a9e08a19-c6f5-4fac-a5f2-0aec3600b2da" />

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```
git clone https://github.com/harshithareddy-p/streetranam-safety-app.git
cd streetranam-safety-app
```

---

### 2️⃣ Install Dependencies

```
pip install -r requirements.txt
```

---

### 3️⃣ Setup MySQL Database

* Create a database:

```
CREATE DATABASE women_safety;
```

* Import dataset:

```
LOAD DATA INFILE 'safety_data.csv'
INTO TABLE safety_table
FIELDS TERMINATED BY ','
IGNORE 1 ROWS;
```

---

### 4️⃣ Run the Application

```
streamlit run chatui.py
```

---

## 🌐 Deployment

You can deploy this project using:

* Streamlit Cloud (Frontend)
* Railway (MySQL Database)
* Render (Full-stack hosting)

---

## ⚠️ Important Notes

* Local MySQL will not work in deployment
* Use cloud database services for production
* Add `.env` file for credentials (do not upload to GitHub)

---

## 🔮 Future Improvements

* 🔐 User authentication system
* 📱 Mobile app integration
* 🧠 Advanced AI risk prediction
* 🚨 Emergency SOS feature
* 📡 Live GPS tracking

---

## 🤝 Contribution

Contributions are welcome! Feel free to fork and improve the project.

---

## 📜 License

This project is open-source and available under the MIT License.

---

## 👩‍💻 Author

**Harshitha R**

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub!
