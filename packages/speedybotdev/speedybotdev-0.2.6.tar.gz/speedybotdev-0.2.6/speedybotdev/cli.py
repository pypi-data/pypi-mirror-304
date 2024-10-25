import argparse
import json
import http.client
from .repo import GitHubRepoExtractor

# Define available project choices
PROJECT_CHOICES = [
    'deno', 'lambda', 'llm-stream', 'azure', 'speedybot-starter',
    'standard-server', 'worker', 'voiceflow', 'voiceflow-kb'
]


# Reset for websockets
def reset_devices(access_token: str) -> bool:
    DEVICES_URL = '/wdm/api/v1/devices'
    HOST = 'wdm-a.wbx2.com'

    """Resets all devices associated with the access token."""
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    try:
        # Create HTTPS connection
        conn = http.client.HTTPSConnection(HOST)
        
        # Get the list of devices
        conn.request("GET", DEVICES_URL, headers=headers)
        response = conn.getresponse()
        if response.status != 200:
            raise Exception(f"Failed to retrieve devices: {response.status} {response.reason}")
        
        devices_data = response.read()
        devices = json.loads(devices_data).get('devices', [])
        
        # Delete each device
        for device in devices:
            device_url = device.get('url')
            if device_url:
                # Extract path from the device URL
                path = device_url.replace(f'https://{HOST}', '')
                conn.request("DELETE", path, headers=headers)
                delete_response = conn.getresponse()
                if delete_response.status != 204:
                    raise Exception(f"Failed to delete device: {delete_response.status} {delete_response.reason}")
        
        # Close the connection
        conn.close()
        return True

    except Exception as e:
        print(f"Error resetting devices: {e}")
        return False


def setup(project: str, boot: bool, install: bool, token: str, debug: bool):
    print(f"Setting up project: {project}")
    if boot:
        print("Booting up the project...")
    if install:
        print("Installing dependencies...")
    print(f"Using token: {token}")

    # Instantiate the extractor with the debug flag
    extractor = GitHubRepoExtractor(
        repo_url='https://github.com/valgaze/speedybot',
        branch='v2',
        debug=debug
    )
    
    # Extract the project based on its subdirectory
    extractor.extract_to_directory(
        subdir_name=f'examples/{project}',
        target_dir=project
    )

def reset(token: str):
    print('reset this')
    reset_devices(token)

def main():
    parser = argparse.ArgumentParser(description="SpeedyBot CLI")
    
    subparsers = parser.add_subparsers(dest="command")

    # Create the setup command
    setup_parser = subparsers.add_parser('setup', help='Setup a new project')
    setup_parser.add_argument('--project', required=True, choices=PROJECT_CHOICES, help='Name of the project')
    setup_parser.add_argument('--boot', action='store_true', help='Boot up the project')
    setup_parser.add_argument('--install', action='store_true', help='Install dependencies')
    setup_parser.add_argument('--token', required=True, help='API token')
    setup_parser.add_argument('--debug', action='store_true', help='Enable debug logging')

    args = parser.parse_args()

    if args.command == 'reset':
        reset_devices(access_token=args.token)

    if args.command == 'setup':
        setup(args.project, args.boot, args.install, args.token, args.debug)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
