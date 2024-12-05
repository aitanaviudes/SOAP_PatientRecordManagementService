from spyne import Application, rpc, ServiceBase, Integer, Unicode, ComplexModel
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server

# Patient model
class Patient(ComplexModel):
    id = Integer
    name = Unicode
    age = Integer
    medical_history = Unicode
    doctor_notes = Unicode

# Initial patient data
patients = {
    1: {
        "id": 1,
        "name": "Inés Rodriguez Perez",
        "age": 45,
        "medical_history": "Diabetes, Hypertension",
        "doctor_notes": "Needs regular check-ups for blood sugar and pressure."
    },
    2: {
        "id": 2,
        "name": "Eric Alexander",
        "age": 29,
        "medical_history": "Asthma",
        "doctor_notes": "Prescribed inhaler, monitor for improvement."
    }
}

class PatientService(ServiceBase):
    @rpc(Integer, Unicode, Integer, Unicode, Unicode, _returns=Unicode)
    def create_patient(ctx, patient_id, name, age, medical_history, doctor_notes):
        """Create a new patient."""
        if patient_id in patients:
            return "Patient with this ID already exists."
        patients[patient_id] = {
            "id": patient_id,
            "name": name,
            "age": age,
            "medical_history": medical_history,
            "doctor_notes": doctor_notes
        }
        return "Patient created successfully."

    @rpc(Integer, _returns=Patient)
    def get_patient(ctx, patient_id):
        """Retrieve patient details by ID."""
        patient = patients.get(patient_id)
        if patient:
            return Patient(**patient)
        else:
            raise ValueError("Patient not found.")

    @rpc(Integer, Unicode, Unicode, _returns=Unicode)
    def update_patient(ctx, patient_id, field, value):
        """Update specific field of a patient's record."""
        patient = patients.get(patient_id)
        if not patient:
            raise ValueError("Patient not found.")
        if field not in patient:
            raise ValueError(f"Invalid field '{field}'. Valid fields are: {', '.join(patient.keys())}")
        patient[field] = value
        return f"Patient's {field} updated successfully."

    @rpc(Integer, _returns=Unicode)
    def delete_patient(ctx, patient_id):
        """Delete a patient's record."""
        if patient_id in patients:
            del patients[patient_id]
            return "Patient deleted successfully."
        else:
            raise ValueError("Patient not found.")

application = Application(
    [PatientService],
    tns="spyne.examples.patient",
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

wsgi_app = WsgiApplication(application)

def add_cors_headers(environ, start_response):
    def cors_start_response(status, headers, exc_info=None):
        headers.append(('Access-Control-Allow-Origin', '*'))
        headers.append(('Access-Control-Allow-Methods', 'POST, GET, OPTIONS'))
        headers.append(('Access-Control-Allow-Headers', 'Content-Type'))
        return start_response(status, headers, exc_info)

    if environ['REQUEST_METHOD'] == 'OPTIONS':
        start_response('200 OK', [
            ('Access-Control-Allow-Origin', '*'),
            ('Access-Control-Allow-Methods', 'POST, GET, OPTIONS'),
            ('Access-Control-Allow-Headers', 'Content-Type')
        ])
        return [b'']

    return wsgi_app(environ, cors_start_response)

if __name__ == '__main__':
    server = make_server('0.0.0.0', 5001, add_cors_headers)
    print("SOAP API for Patient Management running on http://localhost:5001")
    server.serve_forever()
