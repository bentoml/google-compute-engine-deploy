OPERATOR_NAME = "google-compute-engine"

OPERATOR_MODULE = "google-compute-engine"

OPERATOR_SCHEMA = {
    "project_id": {
        "required": True,
        "type": "string",
    },
    "zone": {
        "required": True,
        "type": "string",
        "default": "us-central1-a",
    },
    "machine_type": {
        "required": True,
        "type": "string",
        "default": "n1-standard-1",
    },
    "gpu_type": {
        "required": False,
        "type": "string",
    },
    "gpu_count": {
        "required": False,
        "type": "integer",
        "coerce": int,
    }
}