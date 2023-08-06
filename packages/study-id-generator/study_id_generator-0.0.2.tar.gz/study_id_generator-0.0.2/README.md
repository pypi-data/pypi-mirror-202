# Study ID Generator

The Study ID Generator queries an API and generates a study identifier by finding the one with the greatest Euclidean distance to all the others where each feature is each digit in the identifier.

## Installation

```bash 
pip install study_id_generator
```

## Usage

### Run the application.

```bash
python -m study_id_generator
```

### Click the `Generate Study ID` button.
![Applications](app.png)

## Configuration

Create an `.ini` configuration file at `~/.config/study_id_generator/config.ini`.

```ini
[DEFAULT]
MIN_ID = 
MAX_ID = 
ID_WIDTH = 
ID_FILLCHAR = 0

[API1]
URL =
CERT_PATH =
API_KEY = 
FIELD_NAME = study_id
ID_REGEX = ^\d{N}$

[API2]
URL =
CERT_PATH =
API_KEY = 
FIELD_NAME = study_id
ID_REGEX = ^\d{N}$
```