import requests
import xml.etree.ElementTree as ET
from soapxml import create_xml, read_xml, read_all_xml, update_xml, delete_xml

def parse_response(response_text):
    """Parse the SOAP response and return the relevant data from specific tags."""
    root = ET.fromstring(response_text)
    # Find the namespace
    namespace = {'soapenv': 'http://schemas.xmlsoap.org/soap/envelope/', 'tns': 'spyne.examples.excel.soap'}
    
    # Extract the body of the response
    body = root.find('soapenv:Body', namespace)
    if body is not None:
        # Check for the create response
        create_result = body.find('.//tns:createResponse/tns:createResult', namespace)
        if create_result is not None:
            return create_result.text.strip()
        
        # Check for the read response
        read_result = body.find('.//tns:readResponse/tns:readResult', namespace)
        if read_result is not None:
            return read_result.text.strip()
        
        # Check for the readAll response
        read_all_result = body.find('.//tns:readAllResponse/tns:readAllResult', namespace)
        if read_all_result is not None:
            return read_all_result.text.strip()
        
        # Check for the update response
        update_result = body.find('.//tns:updateResponse/tns:updateResult', namespace)
        if update_result is not None:
            return update_result.text.strip()
        
        # Check for the delete response
        delete_result = body.find('.//tns:deleteResponse/tns:deleteResult', namespace)
        if delete_result is not None:
            return delete_result.text.strip()
        
        return "No relevant data found."
    
    return "No response body found."

# Function to check if an ID already exists in the Excel file
def id_exists(record_id):
    response = requests.post('http://127.0.0.1:8000', data=read_xml(record_id), headers={'Content-Type': 'text/xml'})
    return "Record not found" not in response.text

def read_all_records():
    """Function to read all records from the Excel file."""
    xml_request = read_all_xml()
    response = requests.post('http://127.0.0.1:8000', data=xml_request, headers={'Content-Type': 'text/xml'})
    return response.text

def main():
    while True:
        print("\nChoose an operation:")
        print("1. Create")
        print("2. Read")
        print("3. Read All")
        print("4. Update")
        print("5. Delete")
        print("6. Exit")
        
        choice = input("Enter your choice (1-6): ")

        if choice == '1':  # Create
            id = input("Enter ID: ")
            if id_exists(id):
                print("ID already exists. Please choose a different ID.")
                continue
            name = input("Enter Name: ")
            email = input("Enter Email: ")
            prodi = input("Enter Prodi: ")
            xml_request = create_xml(id, name, email, prodi)
            response = requests.post('http://127.0.0.1:8000', data=xml_request, headers={'Content-Type': 'text/xml'})
            parsed_result = parse_response(response.text)
            print(parsed_result)

        elif choice == '2':  # Read
            record_id = input("Enter ID to read: ")
            xml_request = read_xml(record_id)
            response = requests.post('http://127.0.0.1:8000', data=xml_request, headers={'Content-Type': 'text/xml'})
            parsed_result = parse_response(response.text)
            print(parsed_result)

        elif choice == '3':  # Read All
            print("Fetching all records...")
            response = read_all_records()
            parsed_result = parse_response(response)
            print(parsed_result)

        elif choice == '4':  # Update
            id = input("Enter ID to update: ")
            if not id_exists(id):
                print("Record not found. Please enter a valid ID.")
                continue
            name = input("Enter new Name: ")
            email = input("Enter new Email: ")
            prodi = input("Enter new Prodi: ")
            xml_request = update_xml(id, name, email, prodi)
            response = requests.post('http://127.0.0.1:8000', data=xml_request, headers={'Content-Type': 'text/xml'})
            parsed_result = parse_response(response.text)
            print(parsed_result)

        elif choice == '5':  # Delete
            record_id = input("Enter ID to delete: ")
            if not id_exists(record_id):
                print("Record not found. Please enter a valid ID.")
                continue
            xml_request = delete_xml(record_id)
            response = requests.post('http://127.0.0.1:8000', data=xml_request, headers={'Content-Type': 'text/xml'})
            parsed_result = parse_response(response.text)
            print(parsed_result)

        elif choice == '6':  # Exit
            print("Exiting the program.")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    main()
