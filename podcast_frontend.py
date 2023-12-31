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

# Styling
st.markdown(
    """
    <style>
        /* Gradient Background */
        body {
            background: linear-gradient(90deg, #FF9D9D, #FBD786, #C6FFDD, #A5DFF9);
            margin: 0;
            padding: 0;
        }

        /* Content padding */
        .stApp {
            padding: 2rem;
        }

        /* Sidebar */
        .sidebar .sidebar-content {
            background-color: rgba(255, 255, 255, 0.1); /* Slight white background */
        }

        /* Headers */
        h1, h2, h3, h4 {
            color: #FBD786; /* Yellowish tint */
            margin-bottom: 1rem;
        }

        /* Button */
        .stButton:hover {
            background-color: #FF9D9D !important; /* Pinkish-red tint on hover */
            color: white;
        }

        /* Text inputs */
        input[type="text"], select {
            border: 1px solid #A5DFF9; /* Bluish border for inputs */
            padding: 0.5rem;
            margin-right: 1rem;
        }

        /* Image */
        img {
            border-radius: 0.5rem;
            box-shadow: 0 0 8px rgba(0, 0, 0, 0.2);
        }

        /* Podcast info container */
        .podcast-container {
            display: flex;
            justify-content: space-between;
            margin-bottom: 2rem;
        }

        /* Podcast details */
        .podcast-details {
            flex: 1;
            margin-left: 2rem;
        }

        /* Podcast cover */
        .podcast-cover {
            flex: 0.4;
        }

    </style>
    """,
    unsafe_allow_html=True
)

def main():
    st.title("Newsletter Dashboard")

    available_podcast_info = create_dict_from_json_files('.')

    # Left section - Input fields
    st.sidebar.header("Podcast RSS Feeds")

    # Dropdown box
    st.sidebar.subheader("Available Podcasts Feeds")
    selected_podcast = st.sidebar.selectbox("Select Podcast", options=available_podcast_info.keys())

    if selected_podcast:

        podcast_info = available_podcast_info[selected_podcast]

        # Right section - Newsletter content
        st.header("Newsletter Content")

        # Display the podcast title
        st.subheader("Episode Title")
        st.write(podcast_info['podcast_details']['episode_title'])

        # Display the podcast summary and the cover image in a side-by-side layout
        col1, col2 = st.columns([7, 3])

        with col1:
            # Display the podcast episode summary
            st.subheader("Podcast Episode Summary")
            st.write(podcast_info['podcast_summary'])

        with col2:
            st.image(podcast_info['podcast_details']['episode_image'], caption="Podcast Cover", width=300, use_column_width=True)

        # Display the podcast guest and their details in a side-by-side layout
        col3, col4 = st.columns([3, 7])

        with col3:
            st.subheader("Podcast Guest")
            st.write(podcast_info['podcast_guest']['name'])

        with col4:
            st.subheader("Podcast Guest Details")
            st.write(podcast_info["podcast_guest"]['summary'])

        # Display the five key moments
        st.subheader("Key Moments")
        key_moments = podcast_info['podcast_highlights']
        for moment in key_moments.split('\n'):
            st.markdown(
                f"<p style='margin-bottom: 5px;'>{moment}</p>", unsafe_allow_html=True)

    # User Input box
    st.sidebar.subheader("Add and Process New Podcast Feed")
    url = st.sidebar.text_input("Link to RSS Feed")

    process_button = st.sidebar.button("Process Podcast Feed")
    st.sidebar.markdown("**Note**: Podcast processing can take up to 5 mins, please be patient.")

    if process_button:

        # Call the function to process the URLs and retrieve podcast guest information
        podcast_info = process_podcast_info(url)

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

def process_podcast_info(url):
    f = modal.Function.lookup("corise-podcast-project", "process_podcast")
    output = f.call(url, '/content/podcast/')
    return output

if __name__ == '__main__':
    main()

