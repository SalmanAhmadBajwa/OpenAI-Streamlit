import streamlit as st
import modal
import json
import os

# Set page configuration
st.set_page_config(
    page_title="Newsletter Dashboard",
    page_icon="🎙️",
    layout="wide"
)

# Dark Theme
# You can further customize the dark theme colors to your preference
dark_theme = """
    <style>
        body {
            background-color: #121212;
            color: #FFFFFF;
        }
        .stTextInput > div {
            background-color: #333333 !important;
        }
    </style>
"""
st.markdown(dark_theme, unsafe_allow_html=True)

def main():
    st.title("Newsletter Dashboard")

    available_podcast_info = create_dict_from_json_files('.')

    # Left section - Input fields
    st.sidebar.header("Podcast RSS Feeds")

    # Dropdown box for selecting pre-existing podcasts
    st.sidebar.subheader("Available Podcasts")
    selected_podcast = st.sidebar.selectbox("Select Podcast", options=[""] + list(available_podcast_info.keys()))

    # Show podcast details only when a podcast is selected
    if selected_podcast:
        podcast_info = available_podcast_info[selected_podcast]
        display_podcast_details(podcast_info)

def display_podcast_details(podcast_info):
    # Right section - Newsletter content
    st.header("Newsletter Content")

    # Podcast Container
    with st.container(key="podcast", class_="podcast-container"):
        # Podcast Cover
        with st.container(key="cover", class_="podcast-cover"):
            st.image(
                podcast_info['podcast_details']['episode_image'],
                caption="Podcast Cover",
                width=300,
                use_column_width=True
            )

        # Podcast Details
        with st.container(key="details", class_="podcast-details"):
            st.subheader("Episode Title")
            st.write(podcast_info['podcast_details']['episode_title'])

            st.subheader("Podcast Episode Summary")
            st.write(podcast_info['podcast_summary'])

            st.subheader("Podcast Guest")
            st.write(podcast_info['podcast_guest']['name'])

            st.subheader("Podcast Guest Details")
            st.write(podcast_info["podcast_guest"]['summary'])

            st.subheader("Key Moments")
            key_moments = podcast_info['podcast_highlights']
            for moment in key_moments.split('\n'):
                st.markdown(
                    f"<p style='margin-bottom: 5px;'>{moment}</p>", unsafe_allow_html=True)

def create_dict_from_json_files(folder_path):
    json_files = [f for f in os.listdir(folder_path) if f.endswith('.json')]
    data_dict = {}

    for file_name in json_files:
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'r') as file:
            try:
                podcast_info = json.load(file)
                if 'podcast_details' in podcast_info and 'podcast_title' in podcast_info['podcast_details']:
                    podcast_name = podcast_info['podcast_details']['podcast_title']
                    data_dict[podcast_name] = podcast_info
                else:
                    print(f"Error: Missing keys in {file_name}")
            except json.JSONDecodeError:
                print(f"Error decoding JSON in {file_name}")

    return data_dict

if __name__ == '__main__':
    main()
