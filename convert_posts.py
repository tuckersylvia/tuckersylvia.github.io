import os
import re

content_dir = "content"

# Regex to capture the exact Jekyll frontmatter block between the triple dashes
jekyll_fm_re = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.MULTILINE | re.DOTALL)

for filename in os.listdir(content_dir):
    if not filename.endswith(".md"):
        continue
        
    filepath = os.path.join(content_dir, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        file_text = f.read()

    match = jekyll_fm_re.match(file_text)
    if not match:
        continue

    old_fm_block = match.group(1)
    body_content = file_text[match.end():]
    
    metadata = {}
    current_key = None
    tag_list = []
    is_parsing_tags = False

    # Parse the frontmatter line by line
    for line in old_fm_block.splitlines():
        # Handle active vertical tag parsing
        if is_parsing_tags:
            if line.strip().startswith("-"):
                tag_name = line.replace("-", "", 1).strip().strip("'").strip('"')
                if tag_name:
                    tag_list.append(tag_name)
                continue
            elif line.strip() and ":" not in line:
                # Still part of the list but no dash
                tag_name = line.strip().strip("'").strip('"')
                if tag_name:
                    tag_list.append(tag_name)
                continue
            else:
                # Hit a new metadata key, stop tracking the block tag list
                is_parsing_tags = False
                if tag_list:
                    metadata["tags"] = ", ".join(tag_list)
                    tag_list = []

        if not line.strip() or ":" not in line:
            continue
            
        key, val = line.split(":", 1)
        key = key.strip().lower()
        val = val.strip().strip("'").strip('"')
        
        if key == "tags":
            if val: # Inline list like [a, b] or "a, b"
                clean_val = val.replace("[", "").replace("]", "").strip()
                metadata["tags"] = clean_val
            else: # It's a block list on the lines below
                is_parsing_tags = True
        else:
            metadata[key] = val

    # Catch tag list if it was at the very end of the frontmatter block
    if is_parsing_tags and tag_list:
        metadata["tags"] = ", ".join(tag_list)

    # Format the attributes into Pelican format
    new_fm_lines = []
    
    if "title" in metadata:
        new_fm_lines.append(f"Title: {metadata['title']}")
    if "date" in metadata:
        # Standardize date formats to YYYY-MM-DD HH:MM
        date_clean = metadata["date"].split(".")[0].strip()
        new_fm_lines.append(f"Date: {date_clean}")
    if "author" in metadata:
        new_fm_lines.append(f"Author: {metadata['author']}")
    if "published" in metadata:
        status = "published" if metadata["published"].lower() == "true" else "draft"
        new_fm_lines.append(f"Status: {status}")
    if "tags" in metadata:
        new_fm_lines.append(f"Tags: {metadata['tags']}")
        
    # Append any custom metadata attributes (like description, mathjax, etc.)
    known_keys = {"title", "date", "author", "published", "tags", "layout"}
    for k, v in metadata.items():
        if k not in known_keys:
            new_fm_lines.append(f"{k.capitalize()}: {v}")

    # Recombine frontmatter with body content
    new_content = "\n".join(new_fm_lines) + "\n\n" + body_content
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"Successfully processed: {filename}")

