# 📝 Result Management System

## 📌 Overview

The **Result Management System** is a web-based application designed to allow teachers to add and manage student results. Built using **HTML5**, **CSS3**, **JavaScript**, and **Bootstrap**, this system provides a user-friendly interface to input student details and view all recorded results.

---

## ✨ Features

- Add student results with **roll number**, **name**, **date of birth**, and **score**.
- Validate form inputs with appropriate **error messages**.
- Persist data using **localStorage** to retain information across page refreshes.
- View all student results on a **separate page**.
- Delete individual student records from the **results list**.

---

## ✅ Prerequisites

- A modern web browser (Chrome, Firefox, Edge, etc.)
- Internet connection for loading **Bootstrap CDN**

---

## 🛠️ Installation

1. **Clone the repository** or download the files to your local machine.
2. Ensure all files (`index.html`, `view_all.html`, `script.js`, `styles.css`) are in the same directory.
3. Open `index.html` in a web browser to start using the application.

---

## 🚀 Usage

### ➕ Add Student Result

1. Navigate to `index.html`.
2. Fill in the **roll number**, **name**, **date of birth**, and **score**.
3. Click the **"Add"** button to submit the form.  
   Correct any validation errors if they appear.
4. Data will be saved and an alert will confirm the addition.

### 📋 View All Results

1. Click the **"View All"** button/link to navigate to `view_all.html`.
2. The table will display all saved student records.

### 🗑️ Delete a Result

1. On the **"View All"** page, click the **"Delete"** button next to a student record.
2. Confirm the deletion prompt to remove the record.

---

## 🗂️ File Structure

- `index.html` — Main page for adding student results  
- `view_all.html` — Page to view all student results  
- `script.js` — JavaScript logic for form validation, data management, and table population  
- `styles.css` — Custom CSS styles to enhance the UI  

---

## 💻 Technologies Used

- **HTML5** — For semantic structure and form elements  
- **CSS3** — For styling, with Bootstrap for responsive layout  
- **JavaScript** — For dynamic functionality and localStorage persistence  
- **Bootstrap 5.3.0** — For pre-built components and styling  

---
