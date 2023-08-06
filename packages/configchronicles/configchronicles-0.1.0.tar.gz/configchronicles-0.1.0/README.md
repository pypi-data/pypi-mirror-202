# ConfigChronicles

ConfigChronicles is a Git-based rule change log library for storing and querying historical changes to business rule configurations. It supports serializing rules into plain text documents (e.g., JSON, YAML, etc.) and storing them in a Git repository.

## Installation

Install using pip:
pip install configchronicles

## Usage

Here's an example of how to use the ConfigChronicles library:

1. Import the required classes:

```python
from configchronicles import ConfigChroniclesOperator, CCSettings
```

2. Create a CCSettings instance, which includes the Git repository URL for storing the rule change logs (supports remote repositories or local repositories). If you need to access a private remote repository, you can configure the private key (file path or private key string) for access.

```python
# Use a local repository
settings = CCSettings(repo_url="/path/to/local/repo")

# Use a remote repository
settings = CCSettings(repo_url="https://xxx.bitbucket.xxx/path/to/repo.git", repo_type="remote")

# Use a custom private key path to access a remote repository
settings = CCSettings(repo_url="https://xxx.bitbucket.xxx/path/to/repo.git", credentials="/path/to/custom/id_rsa", repo_type="remote")

# Use a private key string to access a remote repository
private_key_str = "-----BEGIN RSA PRIVATE KEY-----\n...\n-----END RSA PRIVATE KEY-----"
settings = CCSettings(repo_url="https://xxx.bitbucket.xxx/path/to/repo.git", credentials=private_key_str, repo_type="remote")
```

3. Initialize ConfigChroniclesOperator with the CCSettings instance:

```python
operator = ConfigChroniclesOperator(settings)
```

4. When the application layer wants to modify a configuration document in a specific path, call the update method of ConfigChroniclesOperator and pass in the path of the document to be modified and the latest value of the document:

```python
file_path = "path/to/config.json"
new_content = '{"key": "new_value"}'
author = "John Doe <johndoe@example.com>"
comment = "Update config with new key-value pair"
operator.update(file_path, new_content, author=author, comment=comment)
```

5. When the application layer wants to view the historical modification records of a document, call the query method of ConfigChroniclesOperator and pass in parameters such as time range, sorting method, pagination parameters, etc. By default, the document modification logs are viewed in reverse chronological order. The method returns JSON-formatted modification logs, including the diffs between document versions, which is convenient for frontend rendering.

```python
from datetime import datetime, timedelta

file_path = "path/to/config.json"
start_time = datetime.now() - timedelta(days=30)
end_time = datetime.now()
sort_order = "desc"
limit = 10
offset = 0

history = operator.query(file_path, start_time, end_time, sort_order, limit, offset)
```

