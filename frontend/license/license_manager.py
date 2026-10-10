"""
Cloud Secure Hospital ERP
Customer-side license validation.

IMPORTANT:
- Keep only public_key.pem + license.key on customer PCs.
- NEVER ship the developer private key.
"""

import base64
import json
import os
from datetime import date, datetime
from pathlib import Path

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric.utils import Prehashed


class LicenseManager:
    APP_NAME = "Cloud Secure Hospital ERP"
    LICENSE_DIR_NAME = "license"
    LICENSE_FILE_NAME = "license.key"
    PUBLIC_KEY_FILE_NAME = "public_key.pem"

    def __init__(self, license_directory=None):
        if license_directory is None:
            license_directory = os.path.join(
                os.getenv("LOCALAPPDATA", os.path.expanduser("~")),
                "Cloud Secure Hospital ERP",
                self.LICENSE_DIR_NAME,
            )

        self.license_directory = Path(license_directory)
        self.license_directory.mkdir(parents=True, exist_ok=True)
        self.license_file = self.license_directory / self.LICENSE_FILE_NAME

        # The customer app expects the public key here. Put public_key.pem beside
        # the packaged application or next to the copied license folder.
        app_license_dir = Path(__file__).resolve().parent
        self.public_key_file = app_license_dir / self.PUBLIC_KEY_FILE_NAME

    @staticmethod
    def _canonical_payload(data):
        payload = {
            "product": str(data.get("product", "")).strip(),
            "customer_name": str(data.get("customer_name", "")).strip(),
            "license_id": str(data.get("license_id", "")).strip(),
            "license_type": str(data.get("license_type", "")).strip(),
            "duration_days": int(data.get("duration_days", 0)),
            "start_date": str(data.get("start_date", "")).strip(),
            "expiry_date": str(data.get("expiry_date", "")).strip(),
        }
        return json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")

    def _load_public_key(self):
        if not self.public_key_file.exists():
            raise FileNotFoundError(
                f"Public key not found: {self.public_key_file}"
            )

        return serialization.load_pem_public_key(
            self.public_key_file.read_bytes()
        )

    def load_license(self, path=None):
        target = Path(path) if path else self.license_file
        if not target.exists():
            return None

        with target.open("r", encoding="utf-8") as file:
            return json.load(file)

    def save_license(self, license_data):
        with self.license_file.open("w", encoding="utf-8") as file:
            json.dump(license_data, file, indent=4)
        return True

    def validate_license_data(self, license_data):
        if not isinstance(license_data, dict):
            return {
                "valid": False,
                "status": "INVALID",
                "message": "License data is invalid.",
            }

        required = [
            "product",
            "customer_name",
            "license_id",
            "license_type",
            "duration_days",
            "start_date",
            "expiry_date",
            "signature",
        ]

        missing = [key for key in required if key not in license_data]
        if missing:
            return {
                "valid": False,
                "status": "INVALID",
                "message": "License fields missing: " + ", ".join(missing),
            }

        if license_data.get("product") != self.APP_NAME:
            return {
                "valid": False,
                "status": "INVALID",
                "message": "This license is not for this software.",
            }

        try:
            duration_days = int(license_data["duration_days"])
        except (TypeError, ValueError):
            return {
                "valid": False,
                "status": "INVALID",
                "message": "License duration is invalid.",
            }

        if duration_days <= 0:
            return {
                "valid": False,
                "status": "INVALID",
                "message": "License duration must be greater than zero.",
            }

        try:
            start_date = datetime.strptime(
                license_data["start_date"], "%Y-%m-%d"
            ).date()
            expiry_date = datetime.strptime(
                license_data["expiry_date"], "%Y-%m-%d"
            ).date()
        except (TypeError, ValueError):
            return {
                "valid": False,
                "status": "INVALID",
                "message": "License dates are invalid.",
            }

        expected_expiry = start_date.fromordinal(
            start_date.toordinal() + duration_days - 1
        )
        if expiry_date != expected_expiry:
            return {
                "valid": False,
                "status": "INVALID",
                "message": "License date information does not match duration.",
            }

        try:
            signature = base64.b64decode(
                str(license_data["signature"]).encode("ascii"),
                validate=True,
            )
        except Exception:
            return {
                "valid": False,
                "status": "INVALID",
                "message": "License signature is invalid.",
            }

        try:
            public_key = self._load_public_key()
            public_key.verify(
                signature,
                self._canonical_payload(license_data),
                padding.PKCS1v15(),
                hashes.SHA256(),
            )
        except Exception as exc:
            return {
                "valid": False,
                "status": "INVALID",
                "message": f"License signature verification failed: {exc}",
            }

        today = date.today()
        customer_name = str(license_data["customer_name"]).strip()

        if today < start_date:
            return {
                "valid": False,
                "status": "NOT_STARTED",
                "message": "License activation date has not arrived.",
                "customer_name": customer_name,
                "start_date": str(license_data["start_date"]),
                "expiry_date": str(license_data["expiry_date"]),
                "license_id": str(license_data["license_id"]),
            }

        if today > expiry_date:
            return {
                "valid": False,
                "status": "EXPIRED",
                "message": "Your software license has expired.",
                "customer_name": customer_name,
                "start_date": str(license_data["start_date"]),
                "expiry_date": str(license_data["expiry_date"]),
                "license_id": str(license_data["license_id"]),
            }

        remaining_days = (expiry_date - today).days + 1

        return {
            "valid": True,
            "status": "ACTIVE",
            "message": "License is valid.",
            "customer_name": customer_name,
            "start_date": str(license_data["start_date"]),
            "expiry_date": str(license_data["expiry_date"]),
            "license_id": str(license_data["license_id"]),
            "license_type": str(license_data["license_type"]),
            "remaining_days": remaining_days,
        }

    def validate_license(self):
        try:
            license_data = self.load_license()
            if not license_data:
                return {
                    "valid": False,
                    "status": "MISSING",
                    "message": "License file not found.",
                }
            return self.validate_license_data(license_data)
        except Exception as exc:
            return {
                "valid": False,
                "status": "ERROR",
                "message": f"License check failed: {exc}",
            }

    def import_license_file(self, source_path):
        data = self.load_license(source_path)
        if not data:
            raise ValueError("Selected license file is empty or unreadable.")

        result = self.validate_license_data(data)
        if not result["valid"]:
            raise ValueError(result["message"])

        self.save_license(data)
        return result
