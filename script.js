// Function to send SOAP request
async function sendSoapRequest(data) {
    const response = await fetch("http://localhost:5001/", {
        method: "POST",
        headers: { "Content-Type": "text/xml" },
        body: data
    });
    return response.text();
}

// Create Patient
document.getElementById("createPatientForm").addEventListener("submit", async function(event) {
    event.preventDefault();
    const patientId = document.getElementById("patientId").value;
    const patientName = document.getElementById("patientName").value;
    const patientAge = document.getElementById("patientAge").value;
    const patientHistory = document.getElementById("patientHistory").value;
    const doctorNotes = document.getElementById("doctorNotes").value;

    const soapData = `
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:pat="spyne.examples.patient">
            <soapenv:Header/>
            <soapenv:Body>
                <pat:create_patient>
                    <pat:patient_id>${patientId}</pat:patient_id>
                    <pat:name>${patientName}</pat:name>
                    <pat:age>${patientAge}</pat:age>
                    <pat:medical_history>${patientHistory}</pat:medical_history>
                    <pat:doctor_notes>${doctorNotes}</pat:doctor_notes>
                </pat:create_patient>
            </soapenv:Body>
        </soapenv:Envelope>
    `;
    const result = await sendSoapRequest(soapData);
    document.getElementById("soapResponse").textContent = result;
});

// Get Patient
async function getPatient() {
    const patientId = document.getElementById("getPatientId").value;
    const soapData = `
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:pat="spyne.examples.patient">
            <soapenv:Header/>
            <soapenv:Body>
                <pat:get_patient>
                    <pat:patient_id>${patientId}</pat:patient_id>
                </pat:get_patient>
            </soapenv:Body>
        </soapenv:Envelope>
    `;
    const result = await sendSoapRequest(soapData);
    document.getElementById("soapResponse").textContent = result;
}

// Update Patient
async function updatePatient() {
    const patientId = document.getElementById("updatePatientId").value;
    const field = document.getElementById("updateField").value;
    const value = document.getElementById("updateValue").value;

    const soapData = `
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:pat="spyne.examples.patient">
            <soapenv:Header/>
            <soapenv:Body>
                <pat:update_patient>
                    <pat:patient_id>${patientId}</pat:patient_id>
                    <pat:field>${field}</pat:field>
                    <pat:value>${value}</pat:value>
                </pat:update_patient>
            </soapenv:Body>
        </soapenv:Envelope>
    `;
    const result = await sendSoapRequest(soapData);
    document.getElementById("soapResponse").textContent = result;
}

// Delete Patient
async function deletePatient() {
    const patientId = document.getElementById("deletePatientId").value;
    const soapData = `
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:pat="spyne.examples.patient">
            <soapenv:Header/>
            <soapenv:Body>
                <pat:delete_patient>
                    <pat:patient_id>${patientId}</pat:patient_id>
                </pat:delete_patient>
            </soapenv:Body>
        </soapenv:Envelope>
    `;
    const result = await sendSoapRequest(soapData);
    document.getElementById("soapResponse").textContent = result;
}
