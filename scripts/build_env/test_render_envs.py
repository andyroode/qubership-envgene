import filecmp
import pytest
import difflib

from main import render_environment
from envgenehelper import *

test_data = [
      ("sample-cloud-name", "composite-full", "composite-full-version-from-tests")
    , ("sample-cloud-name", "composite-with-creds", "composite-with-creds-version-from-tests")
    , ("sample-cloud-name", "composite-with-env-specific", "composite-with-env-specific-version-from-tests")
    , ("another-cloud-name", "composite-full", "another-cloud-name-version-from-tests")
    , ("REPLACED_WORD-ocp-mdc-09", "cse-toolset", "mdc-09-cse-toolset-from-tests")
    , ("cloud-without-passport", "env-without-passport", "env-without-passport-version-from-tests")
    , ("REPLACED_WORD-sb-ocp-01", "pl01", "REPLACED_WORD-sb-ocp-01-pl01-version-from-tests")
    , ("REPLACED_WORD-sb-ocp-01", "platform-with-overrides", "REPLACED_WORD-sb-ocp-01-platform-with-overrides-version-from-tests")
    , ("cloud-with-passport-override", "cse-toolset", "cloud-with-passport-override-cse-toolset-version-from-tests")
    , ("REPLACED_WORD-ocp-01", "env-amber", "REPLACED_WORD-ocp-01-env-amber-version-from-tests")
    , ("cloud-with-passport-override", "cse-toolset-cloud-deployer", "cloud-with-passport-override-cse-toolset-cloud-deployer-version-from-tests")
    , ("cloud-with-passport-override", "cse-toolset-test-deployer", "cloud-with-passport-override-cse-toolset-test-deployer-version-from-tests")
]
g_templates_dir = getAbsPath("../../test_data/test_templates")
g_inventory_dir = getAbsPath("../../test_data/test_environments")
g_output_dir = getAbsPath("../../tmp/test_environments")
g_base_dir = get_parent_dir_for_dir(g_inventory_dir)

@pytest.fixture(autouse=True)
def change_test_dir(request, monkeypatch):
    monkeypatch.chdir(request.fspath.dirname+"/../..")

@pytest.mark.parametrize("cluster_name, env_name, version", test_data)
def test_render_envs(cluster_name, env_name, version):
    render_environment(env_name, cluster_name, g_templates_dir, g_inventory_dir, g_output_dir, version, g_base_dir)
    source_dir = f"{g_inventory_dir}/{cluster_name}/{env_name}"
    generated_dir = f"{g_output_dir}/{cluster_name}/{env_name}"
    files_to_compare = get_all_files_in_dir(source_dir, source_dir+"/")
    logger.info(dump_as_yaml_format(files_to_compare))
    match, mismatch, errors = filecmp.cmpfiles(source_dir , generated_dir, files_to_compare, shallow=False)
    logger.info(f"Match: {dump_as_yaml_format(match)}")
    if len(mismatch) > 0:
        logger.error(f"Mismatch: {dump_as_yaml_format(mismatch)}")
        for file in mismatch:
            file1 = os.path.join(source_dir, file)
            file2 = os.path.join(generated_dir, file)
            try:
                with open(file1, 'r') as f1, open(file2, 'r') as f2:
                    diff = difflib.unified_diff(
                        f1.readlines(),
                        f2.readlines(),
                        fromfile=file1,
                        tofile=file2,
                        lineterm=''
                    )
                    diff_text = '\n'.join(diff)
                    logger.error(f"Diff for {file}:\n{diff_text}")
            except Exception as e:
                logger.error(f"Could not read files for diff: {file1}, {file2}. Error: {e}")
    else:
        logger.info(f"Mismatch: {dump_as_yaml_format(mismatch)}")
    if len(errors) > 0:
        logger.fatal(f"Errors: {dump_as_yaml_format(errors)}")
    else:
        logger.info(f"Errors: {dump_as_yaml_format(errors)}")
    assert len(mismatch) == 0, f"Files from source and rendering result mismatch: {dump_as_yaml_format(mismatch)}"
    assert len(errors) == 0, f"Error during comparing source and rendering result: {dump_as_yaml_format(errors)}"