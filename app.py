
from flask import Flask, jsonify
from blockchain import Blockchain
import qrcode
import os

app = Flask(__name__)
blockchain = Blockchain()

os.makedirs("qrcodes", exist_ok=True)


@app.route("/")
def home():
    return """
    <h1>Smart Drug Supply System</h1>
    <p>Blockchain and QR Code Verification</p>
    <p>Visit /add-drug to register a sample drug.</p>
    <p>Visit /verify/BATCH001 to verify it.</p>
    """


@app.route("/add-drug")
def add_drug():
    batch_id = "BATCH001"

    block = blockchain.add_block({
        "batch_id": batch_id,
        "drug_name": "Sample Medicine",
        "manufacturer": "ABC Pharma",
        "status": "Manufactured"
    })

    qr = qrcode.make(
        "http://127.0.0.1:5000/verify/" + batch_id
    )
    qr.save("qrcodes/BATCH001.png")

    return jsonify({
        "message": "Drug batch added",
        "block": block,
        "qr_code": "qrcodes/BATCH001.png"
    })


@app.route("/verify/<batch_id>")
def verify_drug(batch_id):
    if not blockchain.verify_chain():
        return jsonify({
            "verified": False,
            "message": "Blockchain integrity check failed"
        }), 400

    for block in blockchain.chain:
        if block["data"].get("batch_id") == batch_id:
            return jsonify({
                "verified": True,
                "drug": block["data"]
            })

    return jsonify({
        "verified": False,
        "message": "Drug batch not found"
    }), 404


if __name__ == "__main__":
    app.run(debug=True)

ook for the qrcodes folder. Inside, you should find BATCH001.png.