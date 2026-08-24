"""
Create Aesthetic, High-Converting Gig Mockup Images and Capture Live Screenshots
for S.M. Nabil Mushfique's Django Portfolio Website.
"""
import os
import asyncio
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

SCREENSHOTS_DIR = os.path.join(os.path.dirname(__file__), "gig_assets")
ARTIFACTS_DIR = r"C:\Users\NABIL\.gemini\antigravity-ide\brain\97472252-df7c-4787-8965-8a337eb0344f"

os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
os.makedirs(ARTIFACTS_DIR, exist_ok=True)


async def capture_website_screenshots():
    if os.path.exists(os.path.join(SCREENSHOTS_DIR, "desktop_home.png")) and os.path.exists(os.path.join(SCREENSHOTS_DIR, "mobile_projects.png")):
        print("[1/3] High-resolution screenshots already captured. Proceeding to gig banners...")
        return
    from playwright.async_api import async_playwright
    
    print("[1/3] Capturing high-resolution screenshots of live Django website...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        # Desktop context (1920x1080 @ 2x DPR for ultra crisp renders)
        context_desktop = await browser.new_context(
            viewport={"width": 1440, "height": 900},
            device_scale_factor=2
        )
        page = await context_desktop.new_page()
        
        # 1. Home Page
        await page.goto("http://127.0.0.1:8000/", wait_until="networkidle")
        await page.wait_for_timeout(1000)
        home_path = os.path.join(SCREENSHOTS_DIR, "desktop_home.png")
        await page.screenshot(path=home_path)
        print(f"Captured: {home_path}")

        # 2. Projects Page
        await page.goto("http://127.0.0.1:8000/about/", wait_until="networkidle")
        await page.wait_for_timeout(1000)
        about_path = os.path.join(SCREENSHOTS_DIR, "desktop_projects.png")
        await page.screenshot(path=about_path)
        print(f"Captured: {about_path}")

        # 3. Services Page
        await page.goto("http://127.0.0.1:8000/services/", wait_until="networkidle")
        await page.wait_for_timeout(1000)
        services_path = os.path.join(SCREENSHOTS_DIR, "desktop_services.png")
        await page.screenshot(path=services_path)
        print(f"Captured: {services_path}")

        # 4. Contact Page
        await page.goto("http://127.0.0.1:8000/contact/", wait_until="networkidle")
        await page.wait_for_timeout(1000)
        contact_path = os.path.join(SCREENSHOTS_DIR, "desktop_contact.png")
        await page.screenshot(path=contact_path)
        print(f"Captured: {contact_path}")

        # Mobile context (iPhone 14 style)
        context_mobile = await browser.new_context(
            viewport={"width": 390, "height": 844},
            device_scale_factor=2,
            is_mobile=True,
            has_touch=True
        )
        mobile_page = await context_mobile.new_page()
        await mobile_page.goto("http://127.0.0.1:8000/", wait_until="networkidle")
        await mobile_page.wait_for_timeout(1000)
        mobile_home_path = os.path.join(SCREENSHOTS_DIR, "mobile_home.png")
        await mobile_page.screenshot(path=mobile_home_path)
        print(f"Captured: {mobile_home_path}")

        await mobile_page.goto("http://127.0.0.1:8000/about/", wait_until="networkidle")
        await mobile_page.wait_for_timeout(1000)
        mobile_projects_path = os.path.join(SCREENSHOTS_DIR, "mobile_projects.png")
        await mobile_page.screenshot(path=mobile_projects_path)
        print(f"Captured: {mobile_projects_path}")

        await browser.close()


def add_rounded_corners(im, rad):
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2 - 1, rad * 2 - 1), fill=255)
    alpha = Image.new('L', im.size, 255)
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    im.putalpha(alpha)
    return im


def create_device_mockup(screen_img_path, target_width, target_height, is_phone=False):
    """Creates a high-end dark hardware frame mockup around the screenshot."""
    screen = Image.open(screen_img_path).convert("RGBA")
    
    if not is_phone:
        # Laptop / Desktop Display frame
        frame_w = target_width
        frame_h = int(target_width * 0.62)
        screen_w = int(frame_w * 0.94)
        screen_h = int(frame_h * 0.90)
        
        # Resize screen
        screen_resized = screen.resize((screen_w, screen_h), Image.Resampling.LANCZOS)
        screen_rounded = add_rounded_corners(screen_resized, 12)
        
        # Frame canvas with top camera bezel and sleek border
        frame = Image.new("RGBA", (frame_w, frame_h + 24), (0, 0, 0, 0))
        draw = ImageDraw.Draw(frame)
        
        # Outer chassis (dark titanium)
        draw.rounded_rectangle([0, 0, frame_w, frame_h], radius=16, fill=(15, 23, 42, 255), outline=(51, 65, 85, 255), width=3)
        # Web camera dot
        draw.ellipse([frame_w//2 - 3, 6, frame_w//2 + 3, 12], fill=(71, 85, 105, 255))
        # Inner screen bezel
        draw.rounded_rectangle([frame_w*0.028, 16, frame_w*0.028 + screen_w + 4, 16 + screen_h + 4], radius=12, fill=(10, 15, 28, 255))
        
        # Paste screen
        frame.paste(screen_rounded, (int(frame_w * 0.03), 18), screen_rounded)
        
        # Laptop bottom base / hinge
        base_w = int(frame_w * 1.14)
        base_h = 18
        base = Image.new("RGBA", (base_w, base_h), (0, 0, 0, 0))
        b_draw = ImageDraw.Draw(base)
        b_draw.rounded_rectangle([0, 0, base_w, base_h], radius=8, fill=(30, 41, 59, 255), outline=(71, 85, 105, 255), width=2)
        # Center notch
        b_draw.rounded_rectangle([base_w//2 - 45, 0, base_w//2 + 45, 6], radius=3, fill=(15, 23, 42, 255))
        
        # Combine screen + base
        mockup = Image.new("RGBA", (base_w, frame_h + 28), (0, 0, 0, 0))
        mockup.paste(frame, ((base_w - frame_w)//2, 0), frame)
        mockup.paste(base, (0, frame_h + 8), base)
        return mockup
    else:
        # Mobile / iPhone style mockup
        phone_w = target_width
        phone_h = target_height
        screen_w = int(phone_w * 0.90)
        screen_h = int(phone_h * 0.94)
        
        screen_resized = screen.resize((screen_w, screen_h), Image.Resampling.LANCZOS)
        screen_rounded = add_rounded_corners(screen_resized, 24)
        
        frame = Image.new("RGBA", (phone_w, phone_h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(frame)
        
        # Outer phone body
        draw.rounded_rectangle([0, 0, phone_w, phone_h], radius=32, fill=(15, 23, 42, 255), outline=(99, 102, 241, 255), width=3)
        # Paste screen
        frame.paste(screen_rounded, (int(phone_w * 0.05), int(phone_h * 0.03)), screen_rounded)
        # Dynamic Island pill
        draw.rounded_rectangle([phone_w//2 - 32, 14, phone_w//2 + 32, 26], radius=6, fill=(10, 15, 28, 255))
        return frame


def render_gig_main_showcase():
    """Generates the primary 16:9 and 1280x769 Fiverr/Upwork Gig Showcase Cover."""
    print("[2/3] Generating aesthetic primary gig banner...")
    width, height = 1920, 1080
    bg = Image.new("RGBA", (width, height), (10, 15, 30, 255))
    
    # 1. Radiant Ambient Lighting (Indigo and Cyan glows)
    glow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(glow)
    
    # Indigo radial aura (top left / center)
    for r in range(450, 0, -15):
        alpha = int((1 - r/450) * 80)
        g_draw.ellipse([600 - r, 380 - r, 600 + r, 380 + r], fill=(99, 102, 241, alpha))
        
    # Cyan neon glow (bottom right)
    for r in range(350, 0, -15):
        alpha = int((1 - r/350) * 70)
        g_draw.ellipse([1400 - r, 700 - r, 1400 + r, 700 + r], fill=(6, 182, 212, alpha))
        
    bg = Image.alpha_composite(bg, glow)
    
    # 2. Modern Grid Pattern Overlay
    grid_img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    grid_draw = ImageDraw.Draw(grid_img)
    for x in range(0, width, 60):
        grid_draw.line([(x, 0), (x, height)], fill=(255, 255, 255, 8), width=1)
    for y in range(0, height, 60):
        grid_draw.line([(0, y), (width, y)], fill=(255, 255, 255, 8), width=1)
    bg = Image.alpha_composite(bg, grid_img)
    
    # 3. Create and place Laptop Mockup (Home page)
    desktop_home = os.path.join(SCREENSHOTS_DIR, "desktop_home.png")
    laptop = create_device_mockup(desktop_home, target_width=1020, target_height=650, is_phone=False)
    
    # Add shadow behind laptop
    shadow = Image.new("RGBA", (laptop.width + 80, laptop.height + 80), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    s_draw.ellipse([30, laptop.height - 30, laptop.width + 50, laptop.height + 60], fill=(0, 0, 0, 160))
    shadow = shadow.filter(ImageFilter.GaussianBlur(25))
    
    bg.paste(shadow, (480, 260), shadow)
    bg.paste(laptop, (520, 250), laptop)
    
    # 4. Create and place Mobile Mockup (Projects page)
    mobile_projects = os.path.join(SCREENSHOTS_DIR, "mobile_projects.png")
    phone = create_device_mockup(mobile_projects, target_width=250, target_height=510, is_phone=True)
    
    # Phone shadow
    p_shadow = Image.new("RGBA", (phone.width + 60, phone.height + 60), (0, 0, 0, 0))
    ps_draw = ImageDraw.Draw(p_shadow)
    ps_draw.rounded_rectangle([15, 15, phone.width + 45, phone.height + 45], radius=30, fill=(0, 0, 0, 190))
    p_shadow = p_shadow.filter(ImageFilter.GaussianBlur(20))
    
    bg.paste(p_shadow, (1480, 410), p_shadow)
    bg.paste(phone, (1500, 420), phone)
    
    # 5. Header & High-Converting Value Badges
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    try:
        font_headline = ImageFont.truetype("arialbd.ttf", 52)
        font_sub = ImageFont.truetype("arialbd.ttf", 26)
        font_tag = ImageFont.truetype("arialbd.ttf", 18)
        font_badge = ImageFont.truetype("arialbd.ttf", 16)
        font_star = ImageFont.truetype("arialbd.ttf", 20)
    except:
        font_headline = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_tag = ImageFont.load_default()
        font_badge = ImageFont.load_default()
        font_star = ImageFont.load_default()
        
    # Top Rating Pill
    pill_w, pill_h = 360, 44
    draw.rounded_rectangle([80, 70, 80 + pill_w, 70 + pill_h], radius=22, fill=(30, 41, 59, 230), outline=(99, 102, 241, 255), width=2)
    draw.text((105, 82), "★ ★ ★ ★ ★  TOP EXPERT DEVELOPER", font=font_badge, fill=(251, 191, 36, 255))
    
    # Main Gig Title
    draw.text((80, 135), "Full Stack Django & Python", font=font_headline, fill=(255, 255, 255, 255))
    draw.text((80, 198), "Websites • REST APIs • Enterprise Apps", font=font_headline, fill=(56, 189, 248, 255))
    
    # Subtitle
    draw.text((80, 275), "Bespoke Web Platforms Built with Django, Scalable APIs & Responsive UI", font=font_sub, fill=(203, 213, 225, 255))
    
    # Feature Bullet Cards on the Left Side
    features = [
        ("⚡ High-Performance Django Architecture", "Fast, modular, clean & domain-driven"),
        ("🛡️ Robust Authentication & RBAC", "Enterprise security, CSRF & SQL protection"),
        ("🚀 20+ Production Applications", "Full portfolio of verified production systems"),
        ("📱 100% Mobile & Responsive UI", "Pixel-perfect across all screens & browsers"),
    ]
    
    card_y = 350
    for title, desc in features:
        card_w, card_h = 420, 72
        draw.rounded_rectangle([80, card_y, 80 + card_w, card_y + card_h], radius=12, fill=(15, 23, 42, 210), outline=(51, 65, 85, 255), width=2)
        # Accent indicator
        draw.rounded_rectangle([80, card_y + 12, 85, card_y + card_h - 12], radius=3, fill=(99, 102, 241, 255))
        draw.text((98, card_y + 14), title, font=font_tag, fill=(255, 255, 255, 255))
        draw.text((98, card_y + 40), desc, font=font_badge, fill=(148, 163, 184, 255))
        card_y += 88
        
    # Floating Tech Stack Pills at the Bottom
    techs = ["Django 6.1", "Python 3.12", "REST API", "PostgreSQL", "JavaScript", "Docker", "PyQt6", "OpenCV"]
    tx = 80
    ty = 970
    for t in techs:
        tw = len(t) * 11 + 28
        draw.rounded_rectangle([tx, ty, tx + tw, ty + 38], radius=8, fill=(30, 41, 59, 240), outline=(99, 102, 241, 220), width=2)
        draw.text((tx + 14, ty + 10), t, font=font_badge, fill=(241, 245, 249, 255))
        tx += tw + 14
        
    # Developer Tag Badge (Top Right)
    dev_w = 340
    draw.rounded_rectangle([width - dev_w - 80, 70, width - 80, 118], radius=10, fill=(15, 23, 42, 220), outline=(56, 189, 248, 255), width=2)
    draw.text((width - dev_w - 60, 84), "S.M. NABIL MUSHFIOUE", font=font_tag, fill=(255, 255, 255, 255))
    
    bg = Image.alpha_composite(bg, overlay)
    
    # Save 1920x1080 version
    out_1080p = os.path.join(SCREENSHOTS_DIR, "gig_showcase_1080p.png")
    bg.convert("RGB").save(out_1080p, quality=95)
    
    # Save standard Fiverr recommended 1280x769 version
    out_fiverr = os.path.join(SCREENSHOTS_DIR, "gig_showcase_fiverr_recommended.png")
    bg_fiverr = bg.resize((1280, 769), Image.Resampling.LANCZOS)
    bg_fiverr.convert("RGB").save(out_fiverr, quality=95)

    # Save to artifacts directory as well
    artifact_1080p = os.path.join(ARTIFACTS_DIR, "gig_showcase_1080p.png")
    artifact_fiverr = os.path.join(ARTIFACTS_DIR, "gig_showcase_fiverr_recommended.png")
    bg.convert("RGB").save(artifact_1080p, quality=95)
    bg_fiverr.convert("RGB").save(artifact_fiverr, quality=95)

    print(f"[SUCCESS] Gig cover images created at:\n- {out_1080p}\n- {out_fiverr}")


def render_gig_services_banner():
    """Generates the secondary gig banner showcasing the 6 core services and projects."""
    print("[3/3] Generating secondary services & features showcase banner...")
    width, height = 1920, 1080
    bg = Image.new("RGBA", (width, height), (10, 15, 30, 255))
    
    # Neon glow
    glow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(glow)
    for r in range(400, 0, -15):
        alpha = int((1 - r/400) * 70)
        g_draw.ellipse([960 - r, 300 - r, 960 + r, 300 + r], fill=(99, 102, 241, alpha))
    bg = Image.alpha_composite(bg, glow)

    # Place Services & Projects screen mockups side by side
    services_img = os.path.join(SCREENSHOTS_DIR, "desktop_services.png")
    projects_img = os.path.join(SCREENSHOTS_DIR, "desktop_projects.png")
    
    laptop1 = create_device_mockup(services_img, target_width=860, target_height=540, is_phone=False)
    laptop2 = create_device_mockup(projects_img, target_width=860, target_height=540, is_phone=False)
    
    bg.paste(laptop1, (60, 360), laptop1)
    bg.paste(laptop2, (980, 360), laptop2)
    
    # Headline and title
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    try:
        font_h = ImageFont.truetype("arialbd.ttf", 46)
        font_s = ImageFont.truetype("arialbd.ttf", 22)
        font_b = ImageFont.truetype("arialbd.ttf", 16)
    except:
        font_h = ImageFont.load_default()
        font_s = ImageFont.load_default()
        font_b = ImageFont.load_default()
        
    draw.text((width//2, 80), "Comprehensive Full Stack Services & 20+ Production Projects", font=font_h, fill=(255, 255, 255, 255), anchor="mt")
    draw.text((width//2, 145), "Web Applications • REST APIs • Query Optimization • Web Scraping • Computer Vision • Desktop GUI", font=font_s, fill=(56, 189, 248, 255), anchor="mt")
    
    # 6 Feature Badges
    services = [
        "1. Full Stack Web Apps", "2. REST APIs & Microservices", "3. Database & SQL Tuning",
        "4. Automated Scraping & ETL", "5. Computer Vision & AI", "6. Cross-Platform Desktop GUI"
    ]
    sx = 100
    for s in services:
        sw = len(s) * 11 + 24
        draw.rounded_rectangle([sx, 220, sx + sw, 265], radius=8, fill=(30, 41, 59, 240), outline=(99, 102, 241, 240), width=2)
        draw.text((sx + 12, 233), s, font=font_b, fill=(241, 245, 249, 255))
        sx += sw + 16

    bg = Image.alpha_composite(bg, overlay)
    
    out_services = os.path.join(SCREENSHOTS_DIR, "gig_services_showcase_1080p.png")
    bg.convert("RGB").save(out_services, quality=95)
    
    artifact_services = os.path.join(ARTIFACTS_DIR, "gig_services_showcase_1080p.png")
    bg.convert("RGB").save(artifact_services, quality=95)
    print(f"[SUCCESS] Secondary services banner created at: {out_services}")


async def main():
    await capture_website_screenshots()
    render_gig_main_showcase()
    render_gig_services_banner()

if __name__ == "__main__":
    asyncio.run(main())
