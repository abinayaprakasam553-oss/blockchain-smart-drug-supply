
import hashlib
import json
import time


class Blockchain:
    def __init__(self):
        self.chain = []
        self.add_block({"message": "Genesis Block"})

    def add_block(self, data):
        previous_hash = (
            self.chain[-1]["hash"] if self.chain else "0"
        )

        block = {
            "index": len(self.chain) + 1,
            "timestamp": time.time(),
            "data": data,
            "previous_hash": previous_hash
        }

        block["hash"] = self.calculate_hash(block)
        self.chain.append(block)
        return block

    @staticmethod
    def calculate_hash(block):
        contents = {
            key: value
            for key, value in block.items()
            if key != "hash"
        }
        encoded = json.dumps(
            contents, sort_keys=True
        ).encode()

        return hashlib.sha256(encoded).hexdigest()

    def verify_chain(self):
        for i, block in enumerate(self.chain):
            if block["hash"] != self.calculate_hash(block):
                return False

            if i > 0:
                if block["previous_hash"] != self.chain[i - 1]["hash"]:
                    return False

        return True


if __name__ == "__main__":
    supply_chain = Blockchain()

    supply_chain.add_block({
        "batch_id": "BATCH001",
        "drug_name": "Sample Medicine",
        "manufacturer": "ABC Pharma",
        "status": "Manufactured"
    })

    print(json.dumps(supply_chain.chain, indent=4))
    print("Blockchain valid:", supply_chain.verify_chain())
