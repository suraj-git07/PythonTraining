let students = JSON.parse(localStorage.getItem('students')) || [];

function validateForm() {
    let isValid = true;
    const form = document.getElementById('studentForm');
    if (!form) return false; // Exit if form is not found
    const rollNo = document.getElementById('rollNo').value;
    const name = document.getElementById('name').value;
    const dob = document.getElementById('dob').value;
    const score = document.getElementById('score').value;

    document.getElementById('rollNoError').textContent = '';
    document.getElementById('nameError').textContent = '';
    document.getElementById('dobError').textContent = '';
    document.getElementById('scoreError').textContent = '';

    if (!rollNo) {
        document.getElementById('rollNoError').textContent = 'Roll No is required';
        isValid = false;
    }
    if (!name) {
        document.getElementById('nameError').textContent = 'Name is required';
        isValid = false;
    } else if (!/^[a-zA-Z\s]+$/.test(name)) {
        document.getElementById('nameError').textContent = 'Name should contain only letters';
        isValid = false;
    }
    if (!dob) {
        document.getElementById('dobError').textContent = 'Date of Birth is required';
        isValid = false;
    }
    if (!score || score < 0 || score > 100) {
        document.getElementById('scoreError').textContent = 'Score should be between 0 and 100';
        isValid = false;
    }

    if (!isValid) {
        form.classList.add('was-validated');
    }
    return isValid;
}

// Add event listener only if form exists
const form = document.getElementById('studentForm');
if (form) {
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        if (validateForm()) {
            const student = {
                rollNo: document.getElementById('rollNo').value,
                name: document.getElementById('name').value,
                dob: document.getElementById('dob').value,
                score: document.getElementById('score').value
            };
            students.push(student);
            localStorage.setItem('students', JSON.stringify(students));
            alert('Student result added successfully!');
            this.reset();
            this.classList.remove('was-validated');
        }
    });
}

function goBack() {
    window.history.back();
}

function populateTable() {
    const resultsBody = document.getElementById('resultsBody');
    if (!resultsBody) return; // Exit if not on view_all.html
    resultsBody.innerHTML = '';
    if (students.length === 0) {
        resultsBody.innerHTML = '<tr><td colspan="5">No records found</td></tr>';
    } else {
        students.forEach((student, index) => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${student.rollNo}</td>
                <td>${student.name}</td>
                <td>${student.dob}</td>
                <td>${student.score}</td>
                <td><button class="btn btn-danger delete-btn" onclick="deleteStudent(${index})">Delete</button></td>
            `;
            resultsBody.appendChild(row);
        });
    }
}

function deleteStudent(index) {
    if (confirm('Are you sure you want to delete this student?')) {
        students.splice(index, 1);
        localStorage.setItem('students', JSON.stringify(students));
        populateTable();
    }
}

// Call populateTable when view_all.html loads
if (document.getElementById('resultsTable')) {
    populateTable();
}