# ELOC database

codebase for the Eloc-Database to handle audio data processing and other related tasks.

## Directory Structure

```
ELOC_database/
│
├── config/
│   └── connection_config.yaml      - Configuration file for establishing database connections (not included for security reasons).
│
├── notebooks/
│   ├── trim_btp.ipynb              - Jupyter notebook for trimming audio data related to Bukit Tiga Pulu.
│   ├── trim_sabah.ipynb            - Jupyter notebook for trimming audio data related to Sabah.
│   ├── trim_tangkahan.ipynb        - Jupyter notebook for trimming audio data related to Tangkahan.
│   └── trim_way_kambas.ipynb       - Jupyter notebook for trimming audio data related to Way Kambas.
│
└── src/
    └── s3_utils.py                 - Utility functions for Amazon S3 operations.
```



## Setup

1. **Configuration**: 
    - The `connection_config.yaml` within the `config` directory is crucial for the application but is not provided in the repository for security reasons. To set it up:
        1. Navigate to the `config` directory.
        2. Create a new file named `connection_config.yaml`.
        3. Add the necessary connection parameters. It should look like this:
           ```yaml
           access_key: YOUR_ACCESS_KEY
           secret_key: YOUR_SECRET_KEY
           ```
        4. Save the file.
    - Make sure to **never commit** this file to any public repositories to keep your credentials secure.


## Usage

1. **Jupyter Notebooks**:
    - Navigate to the `notebooks` directory to find notebooks like `trim_tangkahan.ipynb` and `trim_sabah.ipynb`. 
    - You can run these notebooks to process and trim audio data specific to Tangkahan and Sagah respectively.

2. **Amazon S3 Utilities**:
    - The `s3_utils.py` in the `src` directory contains functions to interact with Amazon S3. This includes downloading objects and processing audio data stored in S3.