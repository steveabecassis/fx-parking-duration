import subprocess
from pathlib import Path

current_path = Path().cwd()
model_dependency_folder = "parking_duration"
model_data_bucket = "cerebro-data-staging"
dependency_folder_path = "dependencies"

tfidf_cmd = f"aws s3 sync s3://{model_data_bucket}/common/tfidf {dependency_folder_path}/tfidf_files && cd {dependency_folder_path}/tfidf_files && tar xfz 8m.tgz && rm -rf 8m.tgz && cd {current_path}"
nltk_cmd = f"aws s3 cp s3://{model_data_bucket}/common/nltk_data.tgz {current_path}/nltk_data.tgz && tar xvf nltk_data.tgz && rm -rf nltk_data.tgz"
spacy_en_model_cmd = "python3 -m spacy download en_core_web_sm"
model_dir_cmd = f"aws s3 cp s3://{model_data_bucket}/{model_dependency_folder}/ {dependency_folder_path} --recursive"

s3_dependency_commands = {
    'prepare': f"mkdir -p {dependency_folder_path}",
    'nltk': nltk_cmd,
    'spacy_model_en': spacy_en_model_cmd,
}

for dependency_cmd_key, dependency_cmd in s3_dependency_commands.items():
    try:
        print(f'Executing dependency command: {dependency_cmd_key}', flush=True)
        subprocess.run(dependency_cmd, shell=True, check=True)
    except subprocess.CalledProcessError as err:
        print(f'ERROR: unable to acquire dependency: {dependency_cmd_key}')
        raise err

if 'nltk' in s3_dependency_commands:
    import nltk
    nltk.download('punkt')