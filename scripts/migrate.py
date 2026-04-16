import os
import re
import json
import datetime
import shutil

POSTS_DIR = "/home/jrhoun/projects/jrhoun.com/content/posts"
ABOUT_FILE = "/home/jrhoun/projects/jrhoun.com/content/about.md"
IMG_ROOT = "/home/jrhoun/projects/jrhoun.com/static/img"
WORKING_DIR = "/home/jrhoun/projects/jrhoun.com/ghost_migration_tmp"
OUTPUT_JSON = os.path.join(WORKING_DIR, "ghost_import.json")
ZIP_FILE = "/home/jrhoun/projects/jrhoun.com/ghost_import.zip"
AUTHOR_EMAIL = "jr.houn@gmail.com"

import markdown
import frontmatter
from dateutil import parser

global_tags = {}
posts_tags = []
tag_id_counter = 1

def process_tags(post_tags, post_id):
    global tag_id_counter
    if not post_tags: return
    for tag_name in post_tags:
        if not tag_name: continue
        slug = tag_name.lower().replace(' ', '-')
        if slug not in global_tags:
            global_tags[slug] = {
                "id": tag_id_counter,
                "name": tag_name,
                "slug": slug
            }
            tag_id_counter += 1
        
        posts_tags.append({
            "post_id": post_id,
            "tag_id": global_tags[slug]["id"]
        })

def convert_youtube_shortcode(match):
    video_id = match.group(1).replace('"', '').strip()
    return f'<figure class="kg-card kg-embed-card"><iframe width="560" height="315" src="https://www.youtube.com/embed/{video_id}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></figure>'

def convert_figure_shortcode(match):
    attrs = match.group(0)
    src_m = re.search(r'src=["\']([^"\']+)["\']', attrs)
    caption_m = re.search(r'caption=["\']([^"\']+)["\']', attrs)
    
    src = src_m.group(1) if src_m else ''
    caption = caption_m.group(1) if caption_m else ''
    
    if src.startswith('/img/'):
        src = src.replace('/img/', '/content/images/')
    
    if caption:
        return f'<figure class="kg-card kg-image-card"><img src="{src}" class="kg-image" alt="{caption}" /><figcaption>{caption}</figcaption></figure>'
    return f'<figure class="kg-card kg-image-card"><img src="{src}" class="kg-image" alt="" /></figure>'

def convert_relref_shortcode(match):
    target = match.group(1).replace('"', '').strip()
    target = target.replace('.md', '')
    return f"/{target}/"

def convert_post(filepath, post_id, is_page=False):
    with open(filepath, 'r', encoding='utf-8') as f:
        post = frontmatter.load(f)
        
    title = post.get('title', 'Draft')
    date_str = post.get('date', None)
    post_tags = post.get('tags', [])
    
    if not is_page:
        process_tags(post_tags, post_id)
    
    if isinstance(date_str, datetime.datetime):
        published_at = int(date_str.timestamp() * 1000)
    elif isinstance(date_str, datetime.date):
        published_at = int(datetime.datetime.combine(date_str, datetime.datetime.min.time()).timestamp() * 1000)
    elif date_str:
        try:
            dt = parser.parse(str(date_str))
            published_at = int(dt.timestamp() * 1000)
        except Exception:
            published_at = int(datetime.datetime.now().timestamp() * 1000)
    else:
        published_at = int(datetime.datetime.now().timestamp() * 1000)
        
    status = 'draft' if post.get('draft', False) else 'published'
    slug = os.path.basename(filepath).replace('.md', '')
    
    content = post.content

    # String replacements for newsletter text requested by user
    content = content.replace("Thanks for hanging out and reading all the way to the end. If you're interested in keeping up with future posts, consider signing up for the newsletter or subscribing to the RSS feed.", "")
    # Cleanup about page variants
    content = re.sub(r'If you\'re interested in receiving updates.*?RSS feed.*?\.', '', content, flags=re.IGNORECASE|re.DOTALL)
    content = content.replace("## Updates", "")

    # Extract first image for feature_image
    feature_image = None
    
    # Try finding figure shortcode
    first_fig = re.search(r'\{\{\<\s+figure\s+src=["\']([^"\']+)["\']', content)
    if first_fig:
        feature_image = first_fig.group(1)
    else:
        # Try finding standard markdown image
        first_md = re.search(r'\!\[.*?\]\((.*?)\)', content)
        if first_md:
            feature_image = first_md.group(1)
            
    if feature_image and feature_image.startswith('/img/'):
        feature_image = feature_image.replace('/img/', '/content/images/')

    content = re.sub(r'\{\{\<\s+youtube\s+([^>]+)\s+\>\}\}', convert_youtube_shortcode, content)
    content = re.sub(r'\{\{\<\s+figure\s+(.*?)\>\}\}', convert_figure_shortcode, content)
    content = re.sub(r'\{\{\<\s+relref\s+([^>]+)\s+\>\}\}', convert_relref_shortcode, content)
    
    content = re.sub(r'\!\[(.*?)\]\(/img/(.*?)\)', r'![\1](/content/images/\2)', content)
    
    html_content = markdown.markdown(content)

    paid_posts = ["2020-time-capsule", "coffee-hour-35-years-edition", "hello-world"]
    visibility = "paid" if slug in paid_posts else "public"

    post_obj = {
        "id": post_id,
        "title": title,
        "slug": slug,
        "html": html_content,
        "status": status,
        "visibility": visibility,
        "published_at": published_at,
        "author_id": 1,
        "type": "page" if is_page else "post"
    }
    
    if feature_image:
        post_obj["feature_image"] = feature_image
        
    return post_obj

def build_import_file():
    if os.path.exists(WORKING_DIR):
        shutil.rmtree(WORKING_DIR)
    os.makedirs(WORKING_DIR)
    
    content_images_dir = os.path.join(WORKING_DIR, "content", "images")
    os.makedirs(content_images_dir)
    
    if os.path.exists(IMG_ROOT):
        for item in os.listdir(IMG_ROOT):
            s = os.path.join(IMG_ROOT, item)
            d = os.path.join(content_images_dir, item)
            if os.path.isfile(s):
                shutil.copy2(s, d)
    
    posts_data = []
    idx = 1
    
    for filename in os.listdir(POSTS_DIR):
        if filename.endswith('.md'):
            filepath = os.path.join(POSTS_DIR, filename)
            p = convert_post(filepath, idx)
            posts_data.append(p)
            idx += 1
            
    if os.path.exists(ABOUT_FILE):
        about_page = convert_post(ABOUT_FILE, idx, is_page=True)
        posts_data.append(about_page)
            
    ghost_import = {
        "db": [
            {
                "meta": {
                    "exported_on": int(datetime.datetime.now().timestamp() * 1000),
                    "version": "5.0.0"
                },
                "data": {
                    "posts": posts_data,
                    "tags": list(global_tags.values()),
                    "posts_tags": posts_tags,
                    "users": [
                        {
                            "id": 1,
                            "name": "JR Houn",
                            "email": AUTHOR_EMAIL,
                            "roles": ["Owner"]
                        }
                    ]
                }
            }
        ]
    }
    
    with open(OUTPUT_JSON, 'w') as f:
        json.dump(ghost_import, f, indent=4)
        
    shutil.make_archive(ZIP_FILE.replace('.zip', ''), 'zip', WORKING_DIR)
    print(f"Generated {ZIP_FILE} successfully with {len(posts_data)} objects and {len(global_tags)} tags.")

if __name__ == "__main__":
    build_import_file()
