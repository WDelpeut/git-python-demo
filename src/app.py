import git
import os

REMOTE_URL = "git@github.com:WDelpeut/test.git"
LOCAL_FOLDER = "tmp/test"

if not os.path.exists(LOCAL_FOLDER):
    repo = git.Repo.clone_from(REMOTE_URL, LOCAL_FOLDER)
else:
    repo = git.Repo(f"{LOCAL_FOLDER}")

assert not repo.bare

manifests_folder_path = f"{LOCAL_FOLDER}/application-manifests"
suspended_manifests_folder_path = f"{LOCAL_FOLDER}/suspended-application-manifests"

if not os.path.isdir(f"{suspended_manifests_folder_path}"):
    os.mkdir(f"{suspended_manifests_folder_path}")

application_manifests = os.listdir(manifests_folder_path)

for manifest in application_manifests:
    manifest_file_path = f"{manifests_folder_path}/{manifest}"
    suspended_manifest_file_path = f"{suspended_manifests_folder_path}/{manifest}"

    with open(manifest_file_path) as reader:
        if "suspendCronRange: '123'" in reader.read():
            os.rename(manifest_file_path, suspended_manifest_file_path)
            print(f"MANIFEST SUSPENDED: {manifest}")
        else:
            print("FALSE")


def git_push(commit_message):
    try:
        repo.git.add(all=True)
        repo.index.commit(commit_message)
        origin = repo.remote(name='origin')
        origin.push()
    except:
        print('Something went wrong while pushing changes.')


git_push("[AUTO] suspend manifest-1")
