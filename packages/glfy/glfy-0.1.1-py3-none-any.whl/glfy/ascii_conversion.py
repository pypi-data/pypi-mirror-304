# glfy/ascii_conversion.py

from .glfy_imports import *
from .utils import create_background, apply_background_removal

def rgb_to_hls_vectorized(r, g, b):
    """
    Vectorized conversion from RGB to HLS.
    """
    maxc = np.maximum(np.maximum(r, g), b)
    minc = np.minimum(np.minimum(r, g), b)
    l = (minc + maxc) / 2.0

    s = np.zeros_like(l)
    mask = maxc != minc
    s[mask] = np.where(l[mask] <= 0.5,
                       (maxc[mask] - minc[mask]) / (maxc[mask] + minc[mask]),
                       (maxc[mask] - minc[mask]) / (2.0 - maxc[mask] - minc[mask]))

    h = np.zeros_like(l)
    mask_max = (maxc == r) & mask
    h[mask_max] = (g[mask_max] - b[mask_max]) / (maxc[mask_max] - minc[mask_max])
    mask_max = (maxc == g) & mask
    h[mask_max] = 2.0 + (b[mask_max] - r[mask_max]) / (maxc[mask_max] - minc[mask_max])
    mask_max = (maxc == b) & mask
    h[mask_max] = 4.0 + (r[mask_max] - g[mask_max]) / (maxc[mask_max] - minc[mask_max])

    h = (h / 6.0) % 1.0
    return h, l, s

def hue_to_rgb(p, q, t):
    """Helper function for HLS to RGB conversion."""
    t = t % 1.0
    return np.where(t < 1/6, p + (q - p) * 6 * t,
                   np.where(t < 1/2, q,
                            np.where(t < 2/3, p + (q - p) * (2/3 - t) * 6, p)))

def hls_to_rgb_vectorized(h, l, s):
    """
    Vectorized conversion from HLS to RGB.
    """
    q = np.where(l < 0.5, l * (1 + s), l + s - l * s)
    p = 2 * l - q
    r = hue_to_rgb(p, q, h + 1/3)
    g = hue_to_rgb(p, q, h)
    b = hue_to_rgb(p, q, h - 1/3)
    return r, g, b

def vectorized_color_adjustment(pixels, lightness_boost, vibrancy_boost):
    """
    Apply lightness and vibrancy boosts to an array of RGB pixels.

    Parameters:
    - pixels: NumPy array of shape (..., 3) with RGB values in [0, 255].
    - lightness_boost: Float multiplier for lightness.
    - vibrancy_boost: Float multiplier for vibrancy (saturation).

    Returns:
    - Adjusted pixels as a NumPy array with RGB values in [0, 255].
    """
    # Normalize RGB values to [0, 1]
    pixels_normalized = pixels / 255.0
    r, g, b = pixels_normalized[..., 0], pixels_normalized[..., 1], pixels_normalized[..., 2]

    # Vectorized RGB to HLS
    h, l, s = rgb_to_hls_vectorized(r, g, b)

    # Apply boosts
    l = np.clip(l * lightness_boost, 0, 1)
    s = np.clip(s * vibrancy_boost, 0, 1)

    # Vectorized HLS to RGB
    r_adj, g_adj, b_adj = hls_to_rgb_vectorized(h, l, s)

    # Convert back to [0, 255]
    adjusted_pixels = np.stack([r_adj, g_adj, b_adj], axis=-1) * 255.0
    return adjusted_pixels.astype(np.uint8)

def create_ascii_overlay(ascii_matrix, pixels, font, step_x, step_y, black_and_white=False):
    """
    Create an overlay image with ASCII characters colored appropriately.

    Parameters:
    - ascii_matrix: 2D NumPy array of ASCII characters.
    - pixels: 3D NumPy array of RGB pixels corresponding to each character.
    - font: PIL ImageFont object.
    - step_x: Horizontal spacing per character.
    - step_y: Vertical spacing per character.
    - black_and_white: If True, render characters in white color.

    Returns:
    - PIL Image object with ASCII characters rendered.
    """
    num_chars_y, num_chars_x = ascii_matrix.shape
    # Create a transparent image for the overlay
    overlay = Image.new('RGBA', (int(step_x * num_chars_x), int(step_y * num_chars_y)), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # Iterate through characters and draw them
    for y in range(num_chars_y):
        for x in range(num_chars_x):
            ascii_char = ascii_matrix[y, x]
            position = (x * step_x, y * step_y)
            if black_and_white:
                fill_color = (255, 255, 255, 255)  # White characters
            else:
                r, g, b = pixels[y, x]
                fill_color = (r, g, b, 255)
            draw.text(position, ascii_char, fill=fill_color, font=font)

    return overlay

def image_to_ascii_art(
    image, brightness_boost, contrast_boost,
    lightness_boost, vibrancy_boost, gamma,
    horizontal_spacing, vertical_spacing, ascii_chars,
    background_vibrancy, background_brightness, background_blur_radius,
    font, black_and_white=False, background_removal=False,
    selfie_segmentation=None
):
    """Convert an image to ASCII art, maintaining original size."""

    if background_removal and selfie_segmentation:
        image = apply_background_removal(image, selfie_segmentation)

    image = adaptive_enhance_image(image, brightness_boost, contrast_boost)
    original_width, original_height = image.size

    step_x = horizontal_spacing
    step_y = vertical_spacing

    num_chars_x = max(1, int(original_width / step_x))
    num_chars_y = max(1, int(original_height / step_y))

    # To ensure the background and overlay sizes match, recalculate new_width and new_height
    new_width = num_chars_x * step_x
    new_height = num_chars_y * step_y

    # Resize image to new_width and new_height
    image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    frame_np = np.array(image)
    frame_resized = cv2.resize(frame_np, (num_chars_x, num_chars_y), interpolation=cv2.INTER_LINEAR)

    image_resized = Image.fromarray(frame_resized)
    pixels = np.array(image_resized)

    if black_and_white:
        pixels_gray = np.mean(pixels, axis=2, keepdims=True).astype(np.uint8)
        adjusted_pixels = np.repeat(pixels_gray, 3, axis=2)
    else:
        adjusted_pixels = vectorized_color_adjustment(pixels, lightness_boost, vibrancy_boost)

    grayscale = 0.299 * pixels[..., 0] + 0.587 * pixels[..., 1] + 0.114 * pixels[..., 2]
    corrected_brightness = ((grayscale / 255.0) ** (1.0 / gamma)) * 255
    ascii_indices = (corrected_brightness / 255 * (len(ascii_chars) - 1)).astype(int)

    ascii_chars_arr = np.array(list(ascii_chars))
    ascii_matrix = ascii_chars_arr[ascii_indices]

    # Create the background image with the same dimensions as the ASCII overlay
    background_image = create_background(
        image, new_width, new_height,
        background_vibrancy, background_brightness,
        background_blur_radius
    )

    ascii_overlay = create_ascii_overlay(ascii_matrix, adjusted_pixels, font, step_x, step_y, black_and_white)

    # Check if background and overlay sizes match
    if background_image.size != ascii_overlay.size:
        logging.warning(f"Background size {background_image.size} does not match overlay size {ascii_overlay.size}. Resizing background.")
        background_image = background_image.resize(ascii_overlay.size, Image.Resampling.LANCZOS)

    # Ensure both images are in RGBA
    background_image = background_image.convert('RGBA')
    ascii_overlay = ascii_overlay.convert('RGBA')

    # Composite the ASCII overlay on the background
    try:
        ascii_image = Image.alpha_composite(background_image, ascii_overlay)
    except ValueError as e:
        logging.error(f"images do not match: {e}")
        raise

    return ascii_image.convert('RGB')

def adaptive_enhance_image(image, brightness_boost, contrast_boost):
    """Adaptively enhance image brightness and contrast with increased sensitivity."""
    image_gray = image.convert('L')
    avg_brightness = np.mean(np.array(image_gray))
    
    # Allow scaling factor to go to a minimum limit of 0.9
    scaling_factor = max(0.9, 1 + (128 - avg_brightness) / 128 * 0.1)
    scaling_factor = min(scaling_factor, 1.1)  # Maximum limit at 1.1
    
    brightness_factor = brightness_boost * scaling_factor
    contrast_factor = contrast_boost * scaling_factor
    
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(brightness_factor)
    
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(contrast_factor)
    
    return image

def process_batch_frames(batch_files, frame_dir,
    brightness_boost, contrast_boost,
    lightness_boost, vibrancy_boost,
    gamma, horizontal_spacing, vertical_spacing,
    ascii_chars,
    background_vibrancy, background_brightness, background_blur_radius,
    font, black_and_white=False, background_removal=False
):
    """Process a batch of frames."""
    for file_name in batch_files:
        process_frame(
            file_name, frame_dir,
            brightness_boost, contrast_boost,
            lightness_boost, vibrancy_boost,
            gamma, horizontal_spacing, vertical_spacing,
            ascii_chars,
            background_vibrancy,
            background_brightness,
            background_blur_radius,
            font,
            black_and_white,
            background_removal
        )

def worker_init(background_removal_enabled):
    """Initializer function for multiprocessing Pool workers."""
    global selfie_segmentation
    if background_removal_enabled:
        mp_selfie_segmentation = mp.solutions.selfie_segmentation
        selfie_segmentation = mp_selfie_segmentation.SelfieSegmentation(model_selection=0)
    else:
        selfie_segmentation = None

def convert_frames_to_ascii_art(
    frame_dir, brightness_boost, contrast_boost,
    lightness_boost, vibrancy_boost, gamma, ascii_chars,
    horizontal_spacing, vertical_spacing,
    background_vibrancy, background_brightness, background_blur_radius,
    font,
    black_and_white=False,
    background_removal=False
):
    """Convert frames to ASCII art using multiprocessing with batch processing."""
    frame_files = sorted([f for f in os.listdir(frame_dir) if f.endswith('.png')])

    # Set the number of processes and batch size internally
    max_processes = max(1, int(cpu_count() / 4))
    batch_size = 10

    # Split frame_files into batches
    batches = [frame_files[i:i + batch_size] for i in range(0, len(frame_files), batch_size)]

    # Create a pool of worker processes with an initializer
    with Pool(processes=max_processes, initializer=worker_init, initargs=(background_removal,)) as pool:
        pool.starmap(
            process_batch_frames,
            [
                (
                    batch,
                    frame_dir,
                    brightness_boost,
                    contrast_boost,
                    lightness_boost,
                    vibrancy_boost,
                    gamma,
                    horizontal_spacing,
                    vertical_spacing,
                    ascii_chars,
                    background_vibrancy,
                    background_brightness,
                    background_blur_radius,
                    font,
                    black_and_white,
                    background_removal
                )
                for batch in batches
            ]
        )

def combine_ascii_frames_to_video(frame_dir, output_video_path, fps):
    """Combine ASCII frames into a video using h264_nvenc or fallback to libx264."""
    logging.info("Combining ASCII frames into video...")
    
    # Create a temporary directory to hold sequentially named frames
    sequential_dir = os.path.join(frame_dir, "sequential")
    os.makedirs(sequential_dir, exist_ok=True)

    # Rename frames to 'frame_%04d.png' sequentially
    sequential_files = sorted([f for f in os.listdir(frame_dir) if f.startswith('frame_') and f.endswith('.png')])
    for index, file_name in enumerate(sequential_files, start=1):
        src = os.path.join(frame_dir, file_name)
        dst = os.path.join(sequential_dir, f"frame_{index:04d}.png")
        shutil.move(src, dst)

    frame_path_pattern = os.path.join(sequential_dir, "frame_%04d.png")
    
    # Primary command using h264_nvenc
    primary_command = [
        "ffmpeg", "-y", "-framerate", str(fps), "-i", frame_path_pattern,
        "-c:v", "h264_nvenc",    # Hardware-accelerated encoder
        "-preset", "p7",         # Speed preset optimized for fastest encoding
        "-profile:v", "high",    # High profile for better quality
        "-pix_fmt", "yuv444p",   # Preserve color information
        "-b:v", "10M",           # Set bitrate to 10 Mbps (example)
        "-threads", "0",         # Utilize all available CPU cores
        output_video_path
    ]
    
    # Fallback command using libx264 with -tune animation
    fallback_command = [
        "ffmpeg", "-y", "-framerate", str(fps), "-i", frame_path_pattern,
        "-c:v", "libx264",         # Software encoder
        "-preset", "veryslow",     # Slower encoding with better compression
        "-crf", "18",              # Quality control (lower CRF for higher quality)
        "-profile:v", "high",      # High profile for better quality
        "-pix_fmt", "yuv444p",     # Preserve color information
        "-tune", "animation",      # Tune for animations
        "-threads", "0",           # Utilize all available CPU cores
        output_video_path
    ]
    
    success = execute_ffmpeg_with_fallback(primary_command, fallback_command)
    if not success:
        logging.error("Error combining frames into video with both encoders.")
    
    # Clean up the sequential frames directory
    shutil.rmtree(sequential_dir, ignore_errors=True)

def merge_audio_with_ascii_video(ascii_video, audio_path, final_output):
    """Combine the ASCII video with the original audio."""
    logging.info("Merging audio with ASCII video...")
    if audio_path:
        success = execute_ffmpeg_command([
            "ffmpeg", "-y", "-i", ascii_video, "-i", audio_path,
            "-c:v", "copy", "-c:a", "aac", "-b:a", "320k", "-strict", "experimental", "-threads", "0",
            final_output
        ])  # Set highest bitrate and utilize all CPU cores
        if success:
            logging.info(f"Final video with audio saved to {final_output}.")
        else:
            logging.error("Failed to merge audio with ASCII video.")
    else:
        # If there's no audio, just copy the video
        shutil.copy(ascii_video, final_output)
        logging.info("No audio to merge. Final video saved without audio.")

def process_frame(
    file_name, frame_dir,
    brightness_boost, contrast_boost,
    lightness_boost, vibrancy_boost,
    gamma, horizontal_spacing, vertical_spacing,
    ascii_chars,
    background_vibrancy, background_brightness, background_blur_radius,
    font, black_and_white=False, background_removal=False
):
    """Process a single frame."""
    frame_path = os.path.join(frame_dir, file_name)
    try:
        with Image.open(frame_path) as image:
            ascii_img = image_to_ascii_art(
                image,
                brightness_boost,
                contrast_boost,
                lightness_boost,
                vibrancy_boost,
                gamma,
                horizontal_spacing,
                vertical_spacing,
                ascii_chars,
                background_vibrancy,
                background_brightness,
                background_blur_radius,
                font,
                black_and_white,
                background_removal
            )
            ascii_img.save(frame_path)
    except Exception as e:
        logging.error(f"Error processing frame {file_name}: {e}")


