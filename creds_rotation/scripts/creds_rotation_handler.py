import os
import time
import  json
from typing import List
from models import PayloadEntry, RotationResult
from utils.yaml_utils import convert_json_to_yaml, write_yaml_to_file
from utils.file_utils import  scan_and_get_yaml_files
from utils.cred_utils import decrypt_file, update_cred_content, write_updated_cred_into_file, get_shared_cred_files, read_cred_files, collects_shared_credentials
from core_rotation import process_entry_in_payload
from envgenehelper import getenv_with_error, crypt
import envgenehelper.logger as logger

def check_if_many_envs_exist(env: str) -> str:
    envs = env.strip().splitlines()
    if len(envs) > 1:
        raise ValueError("Expected only one environment to be passed. Failing the job")
    return envs[0]

def load_payload(payload: str):
    if isinstance(payload, str):
        try:
            config = json.loads(payload)
            return config
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Payload JSON: {e}. Please check payload JSON content")
            raise
    else:
        logger.error(f"Unsupported Payload type: {e}. Please provide JSON in string format")


def cred_rotation():
    start = time.time()
    logger.info(f"CPU cores available: {os.cpu_count()}")

    env_name = getenv_with_error('ENV_NAME')
    envgene_age_public_key = getenv_with_error('ENVGENE_AGE_PUBLIC_KEY')
    creds_rotation_enabled = getenv_with_error('CRED_ROTATION_FORCE') == "true"
    cred_payload = load_payload(getenv_with_error('CRED_ROTATION_PAYLOAD'))
    cluster_name = getenv_with_error('CLUSTER_NAME')
    work_dir = getenv_with_error('CI_PROJECT_DIR')
    env = check_if_many_envs_exist(env_name)

    logger.info(f"Starting rotation for: ENV={env_name}, CLUSTER={cluster_name}, WORKDIR={work_dir}")

    encrypt_type, is_encrypted = crypt.get_configured_encryption_type()
    logger.info(f"Detected encryption={is_encrypted}, type={encrypt_type}")
    if encrypt_type == 'Fernet':
        raise Exception("Only SOPS encryption is currently supported for cred rotation")
    
    base_env_path = f"{work_dir}/environments/{cluster_name}/{env}"
    env_cred_file = f"{base_env_path}/Credentials/credentials.yml"
    output_path = f"{work_dir}/affected-sensitive-parameters.yaml"
    
    creds_path = "/tmp/payload.yml"
    logger.info(f"base env path is {base_env_path}")
    convert_json_to_yaml(creds_path, cred_payload)
    #Decrypt Payload file if encrypted
    payload_data = decrypt_file(envgene_age_public_key, creds_path, True, 'SOPS', 'Please check if encryption type is SOPS') 
    
    shared_creds =  collects_shared_credentials(base_env_path)
    fileread = time.time()
    final_creds_map = {}
    get_shared_cred_files(shared_creds, base_env_path, work_dir, final_creds_map)
    shared_content_map = read_cred_files(final_creds_map, is_encrypted, envgene_age_public_key)
    ns_files_map = scan_and_get_yaml_files(base_env_path, env_name)
  
    env_cred_map ={}
    #Decrypt Environment credential file if encrypted
    env_cred_map[env_cred_file] = decrypt_file(envgene_age_public_key, env_cred_file, False, encrypt_type, '')  

    
    logger.info(f"✅ Fileread Completed in {round(time.time() - fileread, 2)} seconds.")
    payload_raw =  payload_data.get("rotation_items", [])
    payload_objects: List[PayloadEntry] = [PayloadEntry.from_dict(entry) for entry in payload_raw]
    
    final_result: List[RotationResult] = []
    processed_cred_and_files = {}
    #Collect affected parameters from ns and app files
    for entry in payload_objects:
        result = process_entry_in_payload(
            entry, env, shared_content_map, env_cred_map, ns_files_map, processed_cred_and_files
        )
        if result:
            final_result.append(result)

    if final_result:
        write_yaml_to_file(output_path, [r.to_dict() for r in final_result])
    else:
        raise Exception("No affected parameters found for the given target keys. Hence Failing the job")

    if not creds_rotation_enabled:
        logger.info(f"✅ Cred Rotation without file update completed in {round(time.time() - start, 2)} seconds.")
        raise Exception("Credential rotation is disabled. Set CRED_ROTATION_FORCE=true to enable it.")
    updated_content, original_content = update_cred_content(processed_cred_and_files)
    write_updated_cred_into_file(updated_content, original_content, is_encrypted, envgene_age_public_key)

    
    logger.info(f"✅ Cred Rotation completed in {round(time.time() - start, 2)} seconds.")



if __name__ == "__main__":
    cred_rotation()