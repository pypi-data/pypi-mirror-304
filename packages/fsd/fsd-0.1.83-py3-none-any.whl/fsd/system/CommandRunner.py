import subprocess
import os
import sys
import requests
import threading
import json
from log.logger_config import get_logger
from .FileContentManager import FileContentManager
from .OSEnvironmentDetector import OSEnvironmentDetector
from .ConfigAgent import ConfigAgent
from .TaskErrorPlanner import TaskErrorPlanner
import time
logger = get_logger(__name__)

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.utils import parse_payload

class CommandRunner:
    def __init__(self, repo):
        """
        Initializes the CommandRunner.
        """
        self.repo = repo
        self.config = ConfigAgent(repo)
        self.errorPlanner = TaskErrorPlanner(repo)
        self.config_manager = FileContentManager()  # Initialize CodeManager in the constructor
        self.detector = OSEnvironmentDetector()
        self.directory_path = repo.get_repo_path()
        self.max_retry_attempts = 3  # Set a maximum number of retry attempts

    async def get_config_requests(self, instructions, file_name):
        """Generate coding requests based on instructions and context."""

        main_path = file_name
        logger.debug(f" #### The `ConfigAgent` is initiating the processing of file: {file_name} in {main_path}")
        logger.info(f"\n #### The `ConfigAgent` has been assigned the following task: {instructions}")
        result = await self.config.get_config_requests(instructions, main_path)
        if main_path:
            await self.config_manager.handle_coding_agent_response(main_path, result)
            logger.info(f"\n #### The `Config Agent` has successfully completed its work on {file_name}")
        else:
            logger.debug(f" #### The `ConfigAgent` encountered an issue: Unable to locate the file: {file_name}")

    async def get_error_planner_requests(self, error, config_context, os_architecture, compile_files, original_prompt_language):
        """Generate coding requests based on instructions and context."""
        result = await self.errorPlanner.get_task_plans(error, config_context, os_architecture, compile_files, original_prompt_language)
        return result

    def run_command(self, command, method='bash'):
        """
        Runs a given command using the specified method.
        Shows real-time output during execution within a Bash markdown block.
        Returns a tuple of (return_code, all_output).
        Implements an inactivity timeout to determine command completion.
        """
        markdown_block_open = False  # Flag to track if markdown block is open
        process = None  # Initialize process variable
        inactivity_timeout = 10  # Seconds to wait for new output before considering done

        try:
            # Use bash for all commands
            shell = True
            executable = '/bin/bash'

            # Check if the command is a 'cd' command
            if command.startswith('cd '):
                # Change the working directory
                new_dir = command[3:].strip()
                os.chdir(new_dir)
                logger.info(
                    f"#### Directory Change\n"
                    f"```bash\nChanged directory to: {new_dir}\n```\n"
                    f"----------------------------------------"
                )
                return 0, [f"Changed directory to: {new_dir}"]

            # Log the current working directory and the command to be executed
            current_path = os.getcwd()
            logger.info(
                f"#### Executing Command\n"
                f"```bash\n{command}\n```\n"
                f"**In Directory:** `{current_path}`\n"
                f"#### Command Output\n```bash"
            )
            markdown_block_open = True  # Code block is now open

            # Start the process and capture output
            process = subprocess.Popen(
                command,
                shell=shell,
                executable=executable,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True,
                cwd=current_path  # Explicitly set the working directory
            )

            # Initialize output list
            output = []

            # Variable to track the last time output was received
            last_output_time = time.time()

            # Lock for thread-safe updates to last_output_time
            lock = threading.Lock()

            # Function to read output
            def read_output(stream, output_list):
                nonlocal markdown_block_open, last_output_time
                for line in iter(stream.readline, ''):
                    line = line.rstrip()
                    output_list.append(line)
                    logger.info(line)
                    with lock:
                        last_output_time = time.time()
                stream.close()

            # Start threads to read stdout and stderr
            stdout_thread = threading.Thread(target=read_output, args=(process.stdout, output))
            stderr_thread = threading.Thread(target=read_output, args=(process.stderr, output))
            stdout_thread.start()
            stderr_thread.start()

            # Monitoring loop
            while True:
                if process.poll() is not None:
                    # Process has finished
                    break
                with lock:
                    time_since_last_output = time.time() - last_output_time
                if time_since_last_output > inactivity_timeout:
                    # No output received within the inactivity timeout
                    logger.info(f"\nNo output received for {inactivity_timeout} seconds. Assuming command completion.")
                    break
                time.sleep(0.1)  # Prevent busy waiting

            # If the process is still running, attempt to terminate it gracefully
            if process.poll() is None:
                try:
                    process.terminate()
                    logger.info(f"Terminated process after inactivity timeout of {inactivity_timeout} seconds.")
                    # Wait briefly to allow process to terminate
                    try:
                        process.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        process.kill()
                        logger.info("Killed process forcefully.")
                except Exception as e:
                    logger.error(f"Error terminating process: {e}")

            # Wait for threads to finish reading
            stdout_thread.join()
            stderr_thread.join()

            # Close the markdown code block if it's open
            if markdown_block_open:
                logger.info("```")  # Close the markdown block
                markdown_block_open = False

            return_code = process.returncode
            logger.info(
                f"#### Command Finished with Return Code: `{return_code}`\n"
                f"----------------------------------------"
            )
            logger.info("The `CommandRunner` has completed the current step and is proceeding to the next one.")
            return return_code, output

        except Exception as e:
            # If a markdown block is open, close it to maintain log integrity
            if markdown_block_open:
                logger.info("```")
                markdown_block_open = False

            logger.error(  # Use error level for exceptions
                f"#### Error Executing Command\n"
                f"```bash\n"
                f"{command}\n"
                f"```\n"
                f"Error: {str(e)}\n"
                f"----------------------------------------"
            )
            return -1, [f"Command execution failed: {str(e)}"]

    def update_file(self, file_name, content):
        """
        Updates the content of a file.
        """
        try:
            with open(file_name, 'a') as file:
                file.write(content + '\n')
            logger.info(f"\n #### The `CommandRunner` has successfully updated the file: {file_name}")
            return f"Successfully updated {file_name}"
        except Exception as e:
            logger.error(f" #### The `CommandRunner` encountered an error while attempting to update {file_name}: {str(e)}")
            return f"Failed to update {file_name}: {str(e)}"

    async def execute_steps(self, steps_json, compile_files, original_prompt_language):
        """
        Executes a series of steps provided in JSON format.
        Asks for user permission before executing each step.
        Waits for each command to complete before moving to the next step.
        """
        steps = steps_json['steps']

        for step in steps:
            if step['method'] == 'bash':
                logger.info(f"\n #### `Command Runner`: {step['prompt']}")
                logger.info(f"```bash\n{step['command']}\n```")
            elif step['method'] == 'update':
                logger.info(f"\n #### `Command Runner`:")
                logger.info(f"```yaml\n{step['prompt']}\n```")

            logger.info("")
            logger.info(" ### Press 'a' or 'Approve' to execute this step, or press Enter to skip, or type 'exit' to exit the entire process: ")
            user_permission = input()

            user_prompt, _, _, _, _ = parse_payload(self.repo.get_repo_path(), user_permission)
            user_prompt = user_prompt.lower()

            if user_prompt == 'exit':
                logger.info(" #### The user has chosen to exit. The `CommandRunner` is halting execution.")
                return "Execution stopped by user"
            elif user_prompt == 's':
                logger.info(" #### The user has chosen to skip this step.")
                continue

            logger.info(f"\n #### The `CommandRunner` is now executing the following step: {step['prompt']}")

            retry_count = 0
            while retry_count < self.max_retry_attempts:
                if step['method'] == 'bash':
                    # Run the command and get the return code and output
                    return_code, command_output = self.run_command(step['command'])

                    # Check for errors based on the return code
                    if return_code != 0:
                        error_message = ','.join(command_output)
                        logger.error(f" #### The `CommandRunner` reports: Command execution failed with return code {return_code}: {error_message}")
                        
                        # Check if the error suggests an alternative command
                        if "Did you mean" in error_message:
                            suggested_command = error_message.split("Did you mean")[1].strip().strip('"?')
                            logger.info(f"\n #### `SystemSuggestionHandler` has found an alternative command: {suggested_command}")
                            logger.info(" ### Press 'a' or 'Approve' to execute this step, or press Enter to skip, or type 'exit' to exit the entire process: ")
                            user_choice = input()

                            user_select, _, _, _, _ = parse_payload(self.repo.get_repo_path(), user_choice)
                            user_select = user_select.lower()
                            
                            if user_select == 'a':
                                logger.info(f"\n #### `UserInteractionHandler`: Executing suggested command: {suggested_command}")
                                return_code, command_output = self.run_command(suggested_command)
                                if return_code == 0:
                                    break  # Command executed successfully
                                else:
                                    # Update error_message with new command output
                                    error_message = ','.join(command_output)
                                    logger.error(
                                        f"\n #### `CommandExecutor`: Suggested command also failed with return code {return_code}: {error_message}")
                            elif user_select == 'exit':
                                logger.info(" #### `UserInteractionHandler`: User has chosen to exit. Stopping execution.")
                                return "Execution stopped by user"
                            else:
                                logger.info(" #### `UserInteractionHandler`: User chose not to run the suggested command.")
                        
                        # Proceed to handle the error
                        fixing_steps = await self.get_error_planner_requests(error_message, step['prompt'], self.detector, compile_files, original_prompt_language)
                        fixing_result = await self.execute_fixing_steps(fixing_steps, compile_files, original_prompt_language)
                        if fixing_result == "Execution stopped by user":
                            logger.info(" #### The user has chosen to exit during the fixing steps. The `CommandRunner` is skipping the current step.")
                            break
                        retry_count += 1
                    else:
                        break  # Command executed successfully without errors
                elif step['method'] == 'update':
                    file_name = step.get('file_name', '')
                    if file_name != 'N/A':
                        await self.get_config_requests(step['prompt'], file_name)
                        logger.info(f"\n #### The `CommandRunner` has successfully updated the file: {file_name}")
                    else:
                        logger.debug("\n #### The `CommandRunner` reports: Update method specified but no file name provided.")
                    break
                else:
                    logger.error(f" #### The `CommandRunner` encountered an unknown method: {step['method']}")
                    break

            if retry_count == self.max_retry_attempts:
                logger.error(f" #### The `CommandRunner` reports: Step failed after {self.max_retry_attempts} attempts: {step['prompt']}")
                error_message = f"Step failed after {self.max_retry_attempts} attempts: {step['prompt']}"
                fixing_steps = await self.get_error_planner_requests(error_message, step['prompt'], self.detector, compile_files, original_prompt_language)
                fixing_result = await self.execute_fixing_steps(fixing_steps, compile_files)
                if fixing_result == "Execution stopped by user":
                    logger.info(" #### The user has chosen to exit during the fixing steps. The `CommandRunner` is skipping the current step.")
                    continue
                return f"Step failed after {self.max_retry_attempts} attempts: {step['prompt']}"

            logger.info(" #### The `CommandRunner` has completed the current step and is proceeding to the next one.")

        logger.info(" #### The `CommandRunner` has successfully completed all steps")
        return "All steps completed successfully"

    async def execute_fixing_steps(self, steps_json, compile_files, original_prompt_language):
        """
        Executes a series of steps provided in JSON format to fix dependency issues.
        Asks for user permission before executing each step.
        Waits for each command to complete before moving to the next step.
        """
        steps = steps_json['steps']

        for step in steps:

            if step['method'] == 'bash':
                logger.info(f"\n #### `Command Runner`: {step['error_resolution']}")
                logger.info(f"```bash\n{step['command']}\n```")
            elif step['method'] == 'update':
                logger.info(f"\n #### `Command Runner`:")
                logger.info(f"```yaml\n{step['error_resolution']}\n```")
           
            logger.info("")
            logger.info(" ### Press 'a' or 'Approve' to execute this step, or press Enter to skip, or type 'exit' to exit the entire process: ")
            user_permission = input()

            user_prompt, _, _, _, _ = parse_payload(self.repo.get_repo_path(), user_permission)
            user_prompt = user_prompt.lower()

            if user_prompt == 'exit':
                logger.info(" #### The user has chosen to exit. The `CommandRunner` is halting execution.")
                return "Execution stopped by user"
            elif user_prompt == 's':
                logger.info(" #### The user has chosen to skip this step.")
                continue

            logger.info(f"\n #### The `CommandRunner` is now executing the following fixing step: {step['error_resolution']}")

            retry_count = 0
            while retry_count < self.max_retry_attempts:
                if step['method'] == 'bash':
                    # Run the command and get the return code and output
                    return_code, command_output = self.run_command(step['command'])
                    
                    # Check for errors based on the return code
                    if return_code != 0:
                        error_message = ','.join(command_output)
                        logger.error(f" #### The `CommandRunner` reports: Command execution failed with return code {return_code}: {error_message}")

                        # Check if the error suggests an alternative command
                        if "Did you mean" in error_message:
                            suggested_command = error_message.split("Did you mean")[1].strip().strip('"?')
                            logger.info(f"\n #### `SystemSuggestionHandler` has found an alternative command: {suggested_command}")
                            logger.info(" ### Press 'a' or 'Approve' to execute this step, or press Enter to skip, or type 'exit' to exit the entire process: ")
                            user_choice = input()

                            user_select, _, _, _, _ = parse_payload(self.repo.get_repo_path(), user_choice)
                            user_select = user_select.lower()
                            
                            if user_select == 'a':
                                logger.info(f"\n #### `UserInteractionHandler`: Executing suggested command: {suggested_command}")
                                return_code, command_output = self.run_command(suggested_command)
                                if return_code == 0:
                                    break  # Command executed successfully
                                else:
                                    # Update error_message with new command output
                                    error_message = ','.join(command_output)
                                    logger.error(
                                        f"\n #### `CommandExecutor`: Suggested command also failed with return code {return_code}: {error_message}")
                            elif user_select == 'exit':
                                logger.info(" #### `UserInteractionHandler`: User has chosen to exit. Stopping execution.")
                                return "Execution stopped by user"
                            else:
                                logger.info(" #### `UserInteractionHandler`: User chose not to run the suggested command.")
                        
                        # Proceed to handle the error
                        fixing_steps = await self.get_error_planner_requests(error_message, step['error_resolution'], self.detector, compile_files, original_prompt_language)
                        fixing_result = await self.execute_fixing_steps(fixing_steps, compile_files, original_prompt_language)
                        if fixing_result == "Execution stopped by user":
                            return "Execution stopped by user"
                        retry_count += 1
                    else:
                        break  # Command executed successfully without errors
                elif step['method'] == 'update':
                    file_name = step.get('file_name', '')
                    if file_name != 'N/A':
                        await self.get_config_requests(step['error_resolution'], file_name)
                        logger.info(f"\n #### The `CommandRunner` has successfully updated the file: {file_name}")
                    else:
                        logger.debug("\n #### The `CommandRunner` reports: Update method specified but no file name provided.")
                    break
                else:
                    logger.error(f" #### The `CommandRunner` encountered an unknown method: {step['method']}")
                    break

            if retry_count == self.max_retry_attempts:
                logger.error(f" #### The `CommandRunner` reports: Step failed after {self.max_retry_attempts} attempts: {step['error_resolution']}")
                error_message = f"Step failed after {self.max_retry_attempts} attempts: {step['error_resolution']}"
                fixing_steps = await self.get_error_planner_requests(error_message, step['error_resolution'], self.detector, compile_files, original_prompt_language)
                fixing_result = await self.execute_fixing_steps(fixing_steps, compile_files, original_prompt_language)
                if fixing_result == "Execution stopped by user":
                    return "Execution stopped by user"
                return f"Step failed after {self.max_retry_attempts} attempts: {step['error_resolution']}"

            logger.info(" #### The `CommandRunner` has completed the current fixing step and is proceeding to the next one.")

        logger.info(" #### The `CommandRunner` has successfully completed all fixing steps")
        return "All fixing steps completed successfully"