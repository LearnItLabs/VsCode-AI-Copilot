import json

def load_config():
    try:
        with open("demo-config.json", "r") as file:
            config = json.load(file)
        
        # Validate config structure
        if not isinstance(config, dict):
            raise ValueError("Config must be a dictionary")
        
        return config
    except FileNotFoundError:
        raise FileNotFoundError("demo-config.json not found")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in config file: {e}")

if __name__ == "__main__":
    config = load_config()
    print("Config loaded successfully!")
    
    # Create a copy for display and check for sensitive data
    display_config = json.loads(json.dumps(config))
    has_sensitive_data = False
    
    # Check and redact sensitive information
    if "database" in display_config:
        if "user" in display_config["database"]:
            display_config["database"]["user"] = "***REDACTED***"
            has_sensitive_data = True
        if "password" in display_config["database"]:
            display_config["database"]["password"] = "***REDACTED***"
            has_sensitive_data = True
    
    if has_sensitive_data:
        print("\n⚠️  WARNING: Config file contains sensitive credentials (user/password)")
    
    print("\nConfiguration content:")
    print(json.dumps(display_config, indent=4))