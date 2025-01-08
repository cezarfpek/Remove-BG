import streamlit as st
from rembg import remove
from PIL import Image, ImageColor
import numpy as np
import io

def remove_background(input_image, background_color=None):
    """
    Remove the background from the input image and optionally replace with a specific color.
    
    Args:
        input_image (PIL.Image): Input image to process
        background_color (tuple): RGB color tuple for background replacement
    
    Returns:
        PIL.Image: Image with background removed/replaced
    """
    # Convert image to RGB mode if it's not already
    if input_image.mode != 'RGBA':
        input_image = input_image.convert('RGBA')
    
    # Convert PIL Image to numpy array
    input_array = np.array(input_image)
    
    # Remove background
    output_array = remove(input_array)
    
    # If a background color is specified, replace transparent background
    if background_color:
        # Create a new image with the specified background color
        colored_background = Image.new('RGBA', input_image.size, background_color)
        colored_background.paste(Image.fromarray(output_array), (0, 0), Image.fromarray(output_array))
        output_array = np.array(colored_background)
    
    # Convert back to PIL Image
    output_image = Image.fromarray(output_array)
    
    return output_image

def main():
    # Set page title and icon
    st.set_page_config(page_title="Background Remover", page_icon=":scissors:")
    
    # App title and description
    st.title("🖼️ Background Removal App")
    st.write("Upload an image, remove its background, and optionally replace it with a custom color!")
    st.write("Great for linkedIn profile pictures!")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose an image...", 
        type=['jpg', 'jpeg', 'png', 'webp'], 
        help="Upload an image to remove its background"
    )
    
    # Background color selection
    background_option = st.radio(
        "Background Option:", 
        ["Transparent", "Custom Color"],
        horizontal=True
    )
    
    # Color picker (only enabled for custom color)
    background_color = None
    if background_option == "Custom Color":
        color_input = st.color_picker("Choose background color", "#FFFFFF")
        # Convert hex to RGB
        background_color = ImageColor.getrgb(color_input)
    
    if uploaded_file is not None:
        # Read the uploaded image
        input_image = Image.open(uploaded_file)
        
        # Display original image
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Original Image")
            st.image(input_image, use_column_width=True)
        
        # Remove background
        try:
            # Process image with selected background option
            output_image = remove_background(input_image, background_color)
            
            # Display processed image
            with col2:
                st.subheader("Processed Image")
                st.image(output_image, use_column_width=True)
            
            # Download button for processed image
            buffered = io.BytesIO()
            output_image.save(buffered, format="PNG")
            img_byte = buffered.getvalue()
            
            st.download_button(
                label="Download Image",
                data=img_byte,
                file_name="processed_image.png",
                mime="image/png",
                help="Download the processed image"
            )
        
        except Exception as e:
            st.error(f"An error occurred: {e}")
    
    # Sidebar information
    st.sidebar.info(
        "How to use:\n"
        "1. Upload an image\n"
        "2. Choose background option\n"
        "3. Select a custom color (optional)\n"
        "4. Download the processed image"
    )

if __name__ == "__main__":
    main()