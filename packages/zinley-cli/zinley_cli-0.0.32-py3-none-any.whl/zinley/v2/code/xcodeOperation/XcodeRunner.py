import os
import aiohttp
import asyncio
import json
import sys
import subprocess
import time
import requests
import re

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from coding_agent.SelfHealingAgent import SelfHealingAgent
from coding_agent.FileManagerAgent import FileManagerAgent
from coding_agent.BugExplainer import BugExplainer
from util.utils import get_preferred_simulator_uuid
from util.utils import get_current_time_formatted
from .XcodeProjectManager import XcodeProjectManager

class XcodeRunner:
    def __init__(self, role, directory_path, api_key, endpoint, deployment_id, max_tokens):
        self.directory_path = directory_path
        self.api_key = api_key
        self.endpoint = endpoint
        self.deployment_id = deployment_id
        self.max_tokens = max_tokens
        self.role = role
        self.headers = {
            "api-key": self.api_key,
            "Content-Type": "application/json"
        }
        self.self_healing = SelfHealingAgent(role, os.path.join(directory_path), api_key, endpoint, deployment_id, max_tokens)
        self.bugExplainer = BugExplainer(role, os.path.join(directory_path), api_key, endpoint, deployment_id, max_tokens)
        self.xcode_operations = XcodeProjectManager(os.path.join(directory_path))
        self.fileManager = FileManagerAgent(os.path.join(directory_path), api_key, endpoint, deployment_id, max_tokens)

    def scan_txt_files(self, path):
        """
        Scan for 'tree.txt' in the specified directory.

        Returns:
            list: Path to 'tree.txt' if found, else an empty list.
        """
        txt_files = []

        if not os.path.exists(path):
            print(f"Directory does not exist: {path}")
            return txt_files

        for root, dirs, files in os.walk(path):
            for file in files:
                if file == 'tree.txt':
                    file_path = os.path.join(root, file)
                    txt_files.append(file_path)
                    # Assuming you want to stop after finding the first 'tree.txt'
                    return txt_files

        return txt_files

    def read_txt_files(self, files):
        """
        Get development plans for a list of txt files from OpenAI based on user prompt.

        Args:
            files (list): List of file paths.
            user_prompt (str): The user's prompt.

        Returns:
            dict: Development plan or error reason.
        """
        all_file_contents = ""

        for file_path in files:
            file_content = self.read_file_content(file_path)
            if file_content:
                all_file_contents += f"\n\nFile: {file_path}\n{file_content}"

        return all_file_contents

    def read_file_content(self, file_path):
        try:
            with open(file_path, "r") as file:
                return file.read()
        except Exception as e:
            print(f"Failed to read file {file_path}: {e}")
            return None

    async def run_xcode_project(self, basename, scheme, max_retries=10):
        """
        Builds and runs an Xcode project using xcodebuild.

        Parameters:
        - basename (list): The base name list to update.
        - scheme (str): The scheme to build and run.
        - max_retries (int): Maximum number of retries for building the project.

        Returns:
        - output (str): The output of the xcodebuild command or an error message if the build fails.
        """
        project_directory = os.path.expanduser(self.directory_path)
        print(f"Building project at: {project_directory}")
        os.chdir(project_directory)

        # Get the preferred simulator UUID
        preferred_simulator_uuid = get_preferred_simulator_uuid()

        totalfile = set()
        fixing_related_files = set()

        xcodebuild_command = [
            'xcodebuild',
            '-scheme', scheme,
            '-destination', f'platform=iOS Simulator,id={preferred_simulator_uuid}',
            'build'
        ]

        bug_log_path = os.path.join(project_directory, 'bug_logs.txt')
        retries = 0
        cleaned = False

        while retries < max_retries:
            self.self_healing.clear_conversation_history()
            self.bugExplainer.clear_conversation_history()

            self.bugExplainer.initial_setup()
            self.self_healing.initial_setup()

            try:
                if retries > 0 and not cleaned:
                    # Clean the build folder and reset the builder on subsequent retries
                    subprocess.run(['xcodebuild', 'clean', '-scheme', scheme], check=True, text=True, capture_output=True)
                    build_folder_path = os.path.join(project_directory, 'build')
                    if os.path.exists(build_folder_path):
                        subprocess.run(['rm', '-rf', build_folder_path], check=True)
                    subprocess.run(['xcodebuild', '-scheme', scheme, 'clean'], check=True, text=True, capture_output=True)
                    cleaned = True

                result = subprocess.run(xcodebuild_command, check=True, text=True, capture_output=True)

                # Ensure the bug log file is removed if the build succeeds
                if os.path.exists(bug_log_path):
                    os.remove(bug_log_path)

                self.self_healing.clear_conversation_history()
                self.bugExplainer.clear_conversation_history()

                print(f"Build succeeded after {retries + 1} tries" if retries > 0 else "Build succeeded on the first try")
                return list(totalfile)

            except subprocess.CalledProcessError as e:
                print("Oops! Something went wrong, I will work on the fix right now.")

                if e.returncode == 70:
                    print("Build failed with exit status 70 or 65. I will finalize now and try again later.")
                    return list(totalfile)

                # Ensure the project directory exists before writing the bug log file
                if not os.path.exists(project_directory):
                    os.makedirs(project_directory)

                bug_log_content = e.stdout if e.stdout else e.stderr
                with open(bug_log_path, 'w') as bug_log_file:
                    bug_log_file.write(bug_log_content)

                txt_files = self.scan_txt_files(os.path.join(project_directory, 'Zinley/Project_analysis'))
                tree = await self.get_tree_txt_files()
                overview = self.read_txt_files(txt_files)
                damagefile = self.log_errors(bug_log_path)

                # Ensure basename list is updated without duplicates
                fixing_related_files.update(list(basename))
                fixing_related_files.update(damagefile)
                fixing_related_files.update(list(totalfile))

                # Retry OpenAI API call with delay on HTTP 429 error
                try:
                    print("Start examining bugs and creating fixing plan")
                    fix_plans = await self.bugExplainer.get_bugFixed_suggest_requests(bug_log_path, list(fixing_related_files), overview)
                    print("Done examining bugs and creating fixing plan")

                    print("Now, I am working on file processing")
                    file_result = await self.get_file_planning(fix_plans, tree)
                    await self.process_creation(file_result)
                    print("Completed processing files")

                    print(f"Attempt to fix for {retries + 1} try")
                    steps = fix_plans.get('steps', [])
                    
                    for step in steps:
                        file_name = step['file_name']
                        totalfile.update([file_name])

                    await self.self_healing.get_fixing_requests(steps)

                except requests.exceptions.HTTPError as http_error:
                    if http_error.response.status_code == 429:
                        wait_time = 2 ** retries
                        print(f"Rate limit exceeded, retrying in {wait_time} seconds...")
                        time.sleep(wait_time)  # Exponential backoff
                    else:
                        raise

                retries += 1

        self.self_healing.clear_conversation_history()
        self.bugExplainer.clear_conversation_history()
        print("Build failed after maximum retries")
        return []

    def log_errors(self, log_file_path):
        error_lines = []
        damaged_files = set()
        error_details = []

        # Regular expression to match file path and error line details
        error_regex = re.compile(r'(/[^:]+\.swift):(\d+):(\d+): error: (.+)')

        with open(log_file_path, 'r') as file:
            lines = file.readlines()

        for line in lines:
            if "error:" in line.lower():
                error_lines.append(line)
                match = error_regex.search(line)
                if match:
                    full_file_path = match.group(1)
                    file_name = os.path.basename(full_file_path)  # Extract the filename
                    line_number = int(match.group(2))
                    column_number = int(match.group(3))
                    error_message = match.group(4)

                    damaged_files.add(file_name)

                    # Read the damaged file to get the specific line with the error
                    try:
                        with open(full_file_path, 'r') as swift_file:
                            swift_lines = swift_file.readlines()

                        if line_number <= len(swift_lines):
                            damaged_code = swift_lines[line_number - 1].strip()
                        else:
                            damaged_code = "Line number exceeds file length."

                        # Get additional context around the error line
                        error_details.append({
                            'file': file_name,
                            'line': line_number,
                            'column': column_number,
                            'message': error_message,
                            'code': damaged_code
                        })
                    except FileNotFoundError:
                        error_details.append({
                            'file': file_name,
                            'line': line_number,
                            'column': column_number,
                            'message': error_message,
                            'code': "File not found."
                        })
                else:
                    # If the error couldn't be parsed, add the original line
                    error_details.append({
                        'file': 'unknown',
                        'line': 'unknown',
                        'column': 'unknown',
                        'message': line.strip(),
                        'code': 'N/A'
                    })

        with open('bug_logs.txt', 'w') as output_file:
            for error in error_details:
                output_file.write(f"Damaged code: {error['code']} - Error: {error['message']} - File path: {error['file']}\n")
                output_file.write("\n" + "-"*80 + "\n\n")  # Adds a separator between errors

        damaged_files_list = list(damaged_files)  # Convert set to list before returning

        print(f"All error lines have been logged. {damaged_files_list}")

        return damaged_files_list

    async def get_file_planning(self, idea_plan, tree):
        """Generate idea plans based on user prompt and available files."""
        return await self.fileManager.get_file_plannings(idea_plan, tree)


    async def process_creation(self, data):
        # Check if 'Is_creating' is True
        if data.get('Is_creating'):
            # Extract the processes array
            processes = data.get('Adding_new_files', [])
            # Create a list of process details
            await self.xcode_operations.execute_files_creation(processes)
            await self.update_tree()
        else:
            print("No new file to be added.")

    async def get_tree_txt_files(self):
        """
        Scan for tree.txt files in the specified directory.

        Returns:
            list: Paths to all tree.txt files.
        """
        await self.update_tree()
        tree_txt_files = []
        tree_path = self.directory_path + "/Zinley/Project_analysis"

        if not os.path.exists(tree_path):
            print(f"Directory does not exist: {tree_path}")
            return tree_txt_files

        for root, dirs, files in os.walk(tree_path):
            for file in files:
                if file == 'tree.txt':
                    file_path = os.path.join(root, file)
                    tree_txt_files.append(file_path)

        return tree_txt_files

    async def update_tree(self):
        """Update the project directory tree and save to tree.txt."""
        tree_path = self.directory_path
        output_dir = os.path.join(tree_path, "Zinley", "Project_analysis")
        os.makedirs(output_dir, exist_ok=True)
        tree_file_path = os.path.join(output_dir, "tree.txt")
        # Open the file to write the tree output
        with open(tree_file_path, 'w') as f:
            # Run the tree command and capture the output
            result = subprocess.run(['tree', self.directory_path, '-I', 'Zinley'], stdout=subprocess.PIPE, text=True)
            # Write the output to the file
            f.write(result.stdout)

# Usage
async def main():
    project_path = "../../projects/DemoApp/"
    api_key = os.getenv("AZURE_OPENAI_API_KEY", "your-azure-openai-api-key")
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "https://your-azure-openai-endpoint")
    deployment_id = os.getenv("AZURE_OPENAI_DEPLOYMENT_ID", "your-deployment-id")
    max_tokens = 4096
    basename = ["ChatView.swift", "LoginView.swift", "HomeView.swift"]
    scheme = "DemoApp"
    runner = XcodeRunner(project_path, api_key, endpoint, deployment_id, max_tokens)
    result = await runner.run_xcode_project(basename, scheme)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
