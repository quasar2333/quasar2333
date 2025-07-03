import os
from datetime import datetime
import sys

def read_file_content(filepath):
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except Exception as e:
            print(f"Error reading file {filepath}: {e}")
            return "Error loading content."
    return "Not currently specified."

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(base_dir, "README_TEMPLATE.md") # Assuming template is named this
    output_path = os.path.join(base_dir, "README.md")
    dynamic_info_dir = os.path.join(base_dir, "_dynamic_info")

    if not os.path.exists(template_path):
        print(f"Error: Template file not found at {template_path}")
        print("Please ensure your main profile content is in a file named README_TEMPLATE.md in the same directory as this script.")
        # As a fallback for this run, let's assume the current README.md IS the template
        # and we will overwrite it. This is to make the first run work if user hasn't renamed.
        # A better long-term solution is for user to maintain README_TEMPLATE.md separately.
        if os.path.exists(output_path):
             template_path = output_path
             print(f"Using existing {output_path} as template for this run.")
        else:
            sys.exit(1)


    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
    except Exception as e:
        print(f"Error reading template file {template_path}: {e}")
        sys.exit(1)

    if not os.path.exists(dynamic_info_dir):
        os.makedirs(dynamic_info_dir)
        print(f"Created directory: {dynamic_info_dir}")
        # Create sample files if they don't exist
        sample_files = {
            "minecraft_project.txt": "Working on a new exciting Minecraft mod!",
            "ai_learning.txt": "Exploring the fundamentals of neural networks.",
            "status.txt": "Learning and growing every day!"
        }
        for fname, fcontent in sample_files.items():
            with open(os.path.join(dynamic_info_dir, fname), 'w', encoding='utf-8') as f:
                f.write(fcontent)
        print(f"Created sample dynamic info files in {dynamic_info_dir}")


    dynamic_content_map = {
        "MINECRAFT_PROJECT_INFO": read_file_content(os.path.join(dynamic_info_dir, "minecraft_project.txt")),
        "AI_LEARNING_INFO": read_file_content(os.path.join(dynamic_info_dir, "ai_learning.txt")),
        "STATUS_UPDATE": read_file_content(os.path.join(dynamic_info_dir, "status.txt")),
        "LAST_UPDATED": datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    }

    output_content = template_content
    for key, value in dynamic_content_map.items():
        output_content = output_content.replace(f"{{{{{key}}}}}", value)

    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(output_content)
        print(f"Profile updated successfully: {output_path}")
    except Exception as e:
        print(f"Error writing output file {output_path}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # To make this script work correctly, we need to rename the README.md (which has placeholders)
    # to README_TEMPLATE.md first. The script will then generate the new README.md from this template.
    # This is a one-time setup step.
    base_dir = os.path.dirname(os.path.abspath(__file__))
    current_readme_path = os.path.join(base_dir, "README.md")
    template_readme_path = os.path.join(base_dir, "README_TEMPLATE.md")

    if not os.path.exists(template_readme_path) and os.path.exists(current_readme_path):
        print(f"Renaming {current_readme_path} to {template_readme_path} to serve as the template.")
        try:
            os.rename(current_readme_path, template_readme_path)
        except Exception as e:
            print(f"Could not rename README.md to README_TEMPLATE.md: {e}")
            print("Please manually rename README.md (the one with {{PLACEHOLDERS}}) to README_TEMPLATE.md")
            # sys.exit(1) # Don't exit, let main() try to handle it or inform user.

    main()
