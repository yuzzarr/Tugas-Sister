def create_xml(id, name, email, prodi):
    return f'''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="spyne.examples.excel.soap">
        <soapenv:Header/>
        <soapenv:Body>
            <tns:create>
                <tns:id>{id}</tns:id>
                <tns:name>{name}</tns:name>
                <tns:email>{email}</tns:email>
                <tns:prodi>{prodi}</tns:prodi>
            </tns:create>
        </soapenv:Body>
    </soapenv:Envelope>'''

def read_xml(record_id):
    return f'''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="spyne.examples.excel.soap">
        <soapenv:Header/>
        <soapenv:Body>
            <tns:read>
                <tns:record_id>{record_id}</tns:record_id>
            </tns:read>
        </soapenv:Body>
    </soapenv:Envelope>'''

def read_all_xml():
    return '''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="spyne.examples.excel.soap">
        <soapenv:Header/>
        <soapenv:Body>
            <tns:readAll/>
        </soapenv:Body>
    </soapenv:Envelope>'''

def update_xml(id, name, email, prodi):
    return f'''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="spyne.examples.excel.soap">
        <soapenv:Header/>
        <soapenv:Body>
            <tns:update>
                <tns:id>{id}</tns:id>
                <tns:name>{name}</tns:name>
                <tns:email>{email}</tns:email>
                <tns:prodi>{prodi}</tns:prodi>
            </tns:update>
        </soapenv:Body>
    </soapenv:Envelope>'''

def delete_xml(record_id):
    return f'''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="spyne.examples.excel.soap">
        <soapenv:Header/>
        <soapenv:Body>
            <tns:delete>
                <tns:record_id>{record_id}</tns:record_id>
            </tns:delete>
        </soapenv:Body>
    </soapenv:Envelope>'''
