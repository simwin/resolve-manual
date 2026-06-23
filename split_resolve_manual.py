#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
split_resolve_manual.py
Режет DaVinci Resolve 20 Reference Manual на отдельные PDF по главам.

Запуск:
    pip install --break-system-packages pypdf
    python3 split_resolve_manual.py /путь/к/DaVinci_Resolve_20_Reference_Manual.pdf

Необязательно: второй аргумент — папка вывода (по умолчанию ./resolve_chapters).
Сухой прогон без PDF (только показать диапазоны):
    python3 split_resolve_manual.py --dry-run 4240
"""

import sys, os, re

# (номер_главы или None для раздела, "Название", печатный_стартовый_номер)
CHAPTERS = [
    (None, "Getting Started", 11),
    (1,  "Introduction to DaVinci Resolve", 14),
    (2,  "Using the DaVinci Resolve User Interface", 56),
    (3,  "Managing Projects and Project Libraries", 75),
    (4,  "System and User Preferences", 96),
    (5,  "DaVinci Control Panels Setup", 130),
    (6,  "Project Settings", 137),
    (7,  "Camera Raw Settings", 165),
    (8,  "Improving Performance, Proxies, and the Render Cache", 191),
    (9,  "Data Levels, Color Management, and ACES", 219),
    (10, "HDR Setup and Grading", 253),
    (11, "Image Sizing and Resolution Independence", 282),
    (12, "Data Burn-In", 297),
    (13, "Frame.io and Dropbox Replay Integration", 303),
    (14, "Resolve Live", 312),
    (15, "Stereoscopic Workflows", 320),
    (16, "Using Variables and Keywords", 343),
    (17, "Using the Media Page", 350),
    (18, "Adding and Organizing Media with the Media Pool", 368),
    (19, "Using Clip Metadata", 408),
    (20, "Using the Inspector in the Media Page", 423),
    (21, "Syncing Audio and Video", 437),
    (22, "Modifying Clips and Clip Attributes", 444),
    (23, "Using Scene Detection", 457),
    (24, "Ingesting From Tape", 465),
    (25, "Capturing From the Cintel Film Scanner", 473),
    (26, "Using the Cut Page", 497),
    (27, "Importing and Organizing Media in the Cut Page", 516),
    (28, "Fast Editing in the Cut Page", 542),
    (29, "Trimming in the Cut Page", 578),
    (30, "Using the Inspector in the Cut Page", 597),
    (31, "Video and Audio Effects in the Cut Page", 619),
    (32, "Quick Export", 650),
    (33, "Using the Edit Page", 654),
    (34, "Creating and Working with Timelines", 697),
    (35, "Preparing Clips for Editing and Viewer Playback", 720),
    (36, "Editing Basics", 743),
    (37, "Using the Inspector in the Edit Page", 773),
    (38, "Modifying Clips in the Timeline", 795),
    (39, "Three- and Four-Point Editing", 818),
    (40, "Text Based Editing", 847),
    (41, "Marking and Finding Clips in the Timeline", 863),
    (42, "Multicam Editing", 889),
    (43, "Take Selectors, Compound Clips, and Nested Timelines", 904),
    (44, "Trimming", 915),
    (45, "Working with Audio in the Edit Page", 949),
    (46, "Media Management", 993),
    (47, "Editing, Adding, and Copying Effects and Filters", 1002),
    (48, "Using Transitions", 1017),
    (49, "Titles, Generators, and Stills", 1037),
    (50, "Compositing and Transforms in the Timeline", 1053),
    (51, "Speed Effects", 1070),
    (52, "Subtitles and Closed Captioning", 1083),
    (53, "Keyframing Effects", 1103),
    (54, "VFX Connect", 1121),
    (55, "Preparing Timelines for Import and Comparison", 1130),
    (56, "Conforming and Relinking Clips", 1144),
    (57, "Creating Digital Dailies for Round Trip Workflows", 1170),
    (58, "Conforming XML Files", 1177),
    (59, "Conforming AAF Files", 1182),
    (60, "Conforming EDL Files", 1196),
    (61, "Conforming OTIO Files", 1202),
    (62, "Conforming ADL Files", 1207),
    (63, "Introduction to Compositing in Fusion", 1210),
    (64, "Exploring the Fusion Interface", 1216),
    (65, "Getting Clips into Fusion", 1265),
    (66, "Rendering Using Saver Nodes", 1292),
    (67, "Working in the Node Editor", 1316),
    (68, "Node Groups, Macros, and Fusion Templates", 1366),
    (69, "Using Viewers", 1389),
    (70, "Editing Parameters in the Inspector", 1432),
    (71, "Animating in Fusion's Keyframes Editor", 1458),
    (72, "Animating in Fusion's Spline Editor", 1476),
    (73, "Animating with Motion Paths", 1508),
    (74, "Using Modifiers, Expressions, and Custom Controls", 1526),
    (75, "Preferences", 1538),
    (76, "Controlling Image Processing and Resolution", 1587),
    (77, "Managing Color for Visual Effects", 1598),
    (78, "Understanding Image Channels", 1611),
    (79, "Compositing Layers in Fusion", 1647),
    (80, "Rotoscoping with Masks", 1672),
    (81, "Paint", 1696),
    (82, "Using the Tracker Node", 1724),
    (83, "Planar Tracking", 1760),
    (84, "Using Open FX, Resolve FX, and Fuse Plugins", 1767),
    (85, "3D Compositing Basics", 1772),
    (86, "3D Camera Tracking", 1827),
    (87, "Particle Systems", 1845),
    (88, "Optical Flow and Stereoscopic Nodes", 1854),
    (89, "3D Nodes", 1867),
    (90, "3D Light Nodes", 1985),
    (91, "3D Material Nodes", 2004),
    (92, "3D Texture Nodes", 2033),
    (93, "Blur Nodes", 2058),
    (94, "Color Nodes", 2083),
    (95, "Composite Nodes", 2158),
    (96, "Deep Image Nodes", 2178),
    (97, "Deep Pixel Nodes", 2197),
    (98, "Effect Nodes", 2213),
    (99, "Film Nodes", 2250),
    (100, "Filter Nodes", 2269),
    (101, "Flow Nodes", 2286),
    (102, "Flow Organizational Nodes", 2289),
    (103, "Fuses", 2294),
    (104, "Generator Nodes", 2296),
    (105, "I/O Nodes", 2336),
    (106, "Layer Nodes", 2363),
    (107, "LUT Nodes", 2377),
    (108, "Mask Nodes", 2386),
    (109, "Matte Nodes", 2427),
    (110, "Metadata Nodes", 2498),
    (111, "Miscellaneous Nodes", 2506),
    (112, "Optical Flow", 2545),
    (113, "Paint Node", 2565),
    (114, "Particle Nodes", 2575),
    (115, "Position Nodes", 2635),
    (116, "Resolve Connect", 2654),
    (117, "Shape Nodes", 2660),
    (118, "Stereo Nodes", 2700),
    (119, "Tracking Nodes", 2732),
    (120, "Transform Nodes", 2788),
    (121, "USD Nodes", 2816),
    (122, "VR Nodes", 2869),
    (123, "Warp Nodes", 2880),
    (124, "Modifiers", 2910),
    (125, "Introduction to Color Grading", 2953),
    (126, "Using the Color Page", 2965),
    (127, "Viewers, Monitoring, and Video Scopes", 2983),
    (128, "Color Page Timeline and Lightbox", 3023),
    (129, "Automated Grading Commands and Imported Grades", 3038),
    (130, "Camera Raw Palette", 3052),
    (131, "Primaries Palette", 3058),
    (132, "HDR Palette", 3077),
    (133, "Primary Grading Controls", 3101),
    (134, "Curves", 3107),
    (135, "ColorSlice", 3128),
    (136, "Color Warper", 3135),
    (137, "Secondary Qualifiers", 3157),
    (138, "Secondary Windows", 3185),
    (139, "Magic Mask", 3201),
    (140, "Motion Tracking Windows", 3229),
    (141, "Using the Gallery", 3256),
    (142, "Grade Management", 3273),
    (143, "Node Editing Basics", 3308),
    (144, "Image Processing Order of Operations", 3329),
    (145, "Serial, Parallel, and Layer Nodes", 3332),
    (146, "Combining Keys and Using Mattes", 3340),
    (147, "Channel Splitting and Image Compositing", 3365),
    (148, "Keyframing in the Color Page", 3380),
    (149, "Copying and Importing Grades Using ColorTrace", 3395),
    (150, "Using LUTs", 3405),
    (151, "Using Open FX and Resolve FX", 3416),
    (152, "Sizing and Image Stabilization", 3429),
    (153, "The Motion Effects and Blur Palettes", 3445),
    (154, "Resolve FX", 3458),
    (155, "Resolve FX Blur", 3461),
    (156, "Resolve FX Color", 3467),
    (157, "Resolve FX Film Emulation", 3480),
    (158, "Resolve FX Generate", 3494),
    (159, "Resolve FX Key", 3496),
    (160, "Resolve FX Light", 3509),
    (161, "Resolve FX OpenColorIO", 3521),
    (162, "Resolve FX Refine", 3524),
    (163, "Resolve FX Revival", 3550),
    (164, "Resolve FX Sharpen", 3572),
    (165, "Resolve FX Stylize", 3576),
    (166, "Resolve FX Temporal", 3599),
    (167, "Resolve FX Texture", 3603),
    (168, "Resolve FX Transform", 3614),
    (169, "Resolve FX Warp", 3653),
    (170, "Using the Fairlight Page", 3663),
    (171, "Setting Up Tracks, Busses, and Patching", 3719),
    (172, "Transport Controls, Timeline Navigation, and Markers", 3743),
    (173, "Recording", 3752),
    (174, "ADR Automated Dialog Replacement", 3762),
    (175, "Editing Basics in the Fairlight Page", 3772),
    (176, "The Fairlight Inspector", 3823),
    (177, "Mixing in the Fairlight Page", 3843),
    (178, "Mix Automation", 3892),
    (179, "Track Groups", 3916),
    (180, "Audio Effects", 3922),
    (181, "Fairlight FX", 3935),
    (182, "Audio Meters and Audio Monitoring", 3978),
    (183, "Signal Flow Diagrams", 3991),
    (184, "Immersive Audio Workflows", 3993),
    (185, "Delivery Effects Processing", 4019),
    (186, "Using the Deliver Page", 4024),
    (187, "Rendering Media", 4033),
    (188, "Delivering DCP and IMF", 4067),
    (189, "Delivering to Tape", 4082),
    (190, "Exporting Timelines to Other Applications", 4090),
    (191, "Blackmagic Cloud Project Server", 4102),
    (192, "Blackmagic Cloud Storage", 4112),
    (193, "Blackmagic Cloud Presentations", 4126),
    (194, "Blackmagic Cloud Organizations", 4138),
    (195, "Live Sync", 4150),
    (196, "Managing Project Libraries and Project Servers", 4158),
    (197, "Collaborative Workflow", 4178),
    (198, "Remote Grading and Remote Monitor", 4193),
    (199, "Workflow Integrations", 4203),
    (200, "Creating DCTL LUTs", 4210),
    (201, "TCP Protocol for DaVinci Resolve Transport Control", 4215),
    (None, "Menu Descriptions", 4220),
]

# Якоря для авто-определения сдвига: (печатный_номер, кусок_заголовка_для_поиска)
# Берём главы поглубже, чтобы не цеплять оглавление в начале документа.
ANCHORS = [
    (14,   "introduction to davinci resolve"),
    (1210, "introduction to compositing in fusion"),
    (2575, "particle nodes"),
    (2953, "introduction to color grading"),
    (3663, "using the fairlight page"),
    (4019, "delivery effects processing"),
]

def slug(s):
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "_", s)
    return re.sub(r"_+", "_", s).strip("_")

def norm(s):
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", s.lower())).strip()

def detect_offset(reader, default=0):
    """Подбирает offset так, чтобы заголовки глав попадали на стартовые страницы."""
    total = len(reader.pages)
    best, best_hits = default, -1
    for off in range(-4, 9):
        hits = 0
        for printed, needle in ANCHORS:
            idx = printed + off - 1          # 0-based индекс страницы в PDF
            if 0 <= idx < total:
                try:
                    txt = norm(reader.pages[idx].extract_text() or "")
                except Exception:
                    txt = ""
                if needle in txt:
                    hits += 1
        # при равенстве предпочитаем offset, ближайший к нулю
        if hits > best_hits or (hits == best_hits and abs(off) < abs(best)):
            best, best_hits = off, hits
    return best, best_hits, len(ANCHORS)

def main():
    if len(sys.argv) >= 3 and sys.argv[1] == "--dry-run":
        total = int(sys.argv[2]); offset = 0; reader = None
        outdir = None
        print(f"[СУХОЙ ПРОГОН] всего страниц (гипотетически) = {total}, offset = {offset}\n")
    else:
        if len(sys.argv) < 2:
            print(__doc__); sys.exit(1)
        try:
            from pypdf import PdfReader, PdfWriter
        except ImportError:
            print("Нет pypdf. Установи:  pip install --break-system-packages pypdf")
            sys.exit(1)
        pdf_path = sys.argv[1]
        outdir = sys.argv[2] if len(sys.argv) >= 3 else "resolve_chapters"
        reader = PdfReader(pdf_path)
        total = len(reader.pages)
        offset, hits, n = detect_offset(reader)
        print(f"Всего страниц в PDF: {total}")
        print(f"Авто-offset: {offset}  (совпало якорей {hits}/{n})")
        if hits < 2:
            print("⚠️  Мало совпадений — проверь первую главу после нарезки; "
                  "при сдвиге поправь вручную переменной offset в detect_offset.")
        os.makedirs(outdir, exist_ok=True)

    # границы: глава i = [start_i, start_{i+1}-1] в печатных номерах
    rows = []
    for i, (num, title, start) in enumerate(CHAPTERS):
        nxt = CHAPTERS[i + 1][2] if i + 1 < len(CHAPTERS) else None
        if nxt is None:
            p_start, p_end = start, (total - offset)   # последний раздел — до конца PDF
        else:
            p_start, p_end = start, nxt - 1
        rows.append((i, num, title, p_start, p_end))

    print(f"{'#':>3}  {'гл':>4}  {'печ.стр':>9}  файл")
    for i, num, title, p_start, p_end in rows:
        tag = f"ch{num:03d}" if num is not None else "sec"
        fname = f"{i:03d}_{tag}_{slug(title)}.pdf"
        i0 = p_start + offset - 1            # 0-based начало
        i1 = p_end + offset - 1              # 0-based конец (включительно)
        gl = str(num) if num is not None else "—"
        print(f"{i:>3}  {gl:>4}  {p_start:>4}-{p_end:<4}  {fname}")
        if reader is None:
            continue
        i0 = max(0, i0); i1 = min(len(reader.pages) - 1, i1)
        if i1 < i0:
            print(f"     пропуск (пустой диапазон)"); continue
        from pypdf import PdfWriter
        w = PdfWriter()
        for p in range(i0, i1 + 1):
            w.add_page(reader.pages[p])
        with open(os.path.join(outdir, fname), "wb") as f:
            w.write(f)

    if reader is not None:
        print(f"\nГотово. Файлы в: {os.path.abspath(outdir)}/")

if __name__ == "__main__":
    main()
