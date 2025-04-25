import streamlit as st
import random
import textwrap
import pandas as pd
import time


# Set page configuration
st.set_page_config(
    page_title="Lyric-to-Storyboard Generator",
    page_icon="🎬",
    layout="wide",
)

# Define visual elements categories
VISUAL_ELEMENTS = {
    "Scenic & Environmental Settings": [
        "Misty forest at dawn",
        "Sun-drenched valley",
        "Neon-lit cityscape at night",
        "Ocean waves crashing at sunset",
        "Snow-covered mountain peak",
        "Desert with golden dunes",
        "Rainy alley with reflections",
        "Twilight over a quiet lake",
        "Abandoned warehouse with dust beams",
        "Star-filled sky over rolling hills"
    ],
    "Mood & Atmosphere": [
        "Dreamlike haze",
        "Melancholic silence",
        "Electric anticipation",
        "Whimsical serenity",
        "Tense and foreboding",
        "Radiant joy",
        "Somber and still",
        "Ethereal glow",
        "Cinematic melancholy",
        "Pulsing with energy"
    ],
    "Character Descriptors": [
        "Woman in flowing white dress",
        "Mysterious figure in a hooded cloak",
        "Child chasing butterflies",
        "Man walking in slow motion",
        "Girl spinning in a flower field",
        "Astronaut floating weightlessly",
        "Dancer under spotlight",
        "Elder sitting by the fire",
        "Lovers holding hands under rain",
        "Warrior standing in ruins"
    ],
    "Visual Style & Techniques": [
        "Black and white film grain",
        "Watercolor painting aesthetic",
        "VHS retro distortion",
        "Cinematic lens flare",
        "Slow-motion camera pan",
        "Close-up with shallow depth of field",
        "Time-lapse sunset",
        "Glitch art overlays",
        "Sepia-toned flashback",
        "Surreal double exposure"
    ],
    "Nature & Elements": [
        "Cherry blossoms falling",
        "Leaves swirling in wind",
        "Thunderstorm in distance",
        "Reflections in still water",
        "Fog creeping over hills",
        "Fireflies glowing at dusk",
        "Raindrops on glass",
        "Lightning flashing across sky",
        "Ember sparks rising",
        "Ice cracking underfoot"
    ]
}

# List of descriptive verbs to enhance scene descriptions
DESCRIPTIVE_VERBS = [
    "unfolds", "reveals", "emerges", "transforms", "transitions",
    "drifts", "glides", "cascades", "illuminates", "radiates",
    "echoes", "resonates", "shimmers", "fades", "dissolves",
    "intensifies", "envelops", "surrounds", "embraces", "captivates"
]

# List of connecting phrases to join elements together
CONNECTING_PHRASES = [
    "as", "while", "where", "beneath", "above",
    "amidst", "alongside", "through", "within", "beyond",
    "against", "between", "throughout", "under", "over"
]

# Description lengths with corresponding word count ranges
DESCRIPTION_LENGTHS = {
    "Concise (30-50 words)": (30, 50),
    "Standard (50-80 words)": (50, 80),
    "Detailed (80-120 words)": (80, 120),
    "Elaborate (120-150 words)": (120, 150)
}

# Presets for different moods and their corresponding element probabilities
MOOD_PRESETS = {
    "Uplifting": {
        "Scenic & Environmental Settings": [1, 2, 4, 8, 9],
        "Mood & Atmosphere": [3, 4, 6, 8, 10],
        "Character Descriptors": [1, 3, 5, 7, 9],
        "Visual Style & Techniques": [3, 4, 5, 7, 10],
        "Nature & Elements": [1, 2, 4, 6, 8]
    },
    "Melancholic": {
        "Scenic & Environmental Settings": [0, 6, 7, 8, 9],
        "Mood & Atmosphere": [1, 2, 4, 7, 8],
        "Character Descriptors": [0, 1, 7, 8, 9],
        "Visual Style & Techniques": [0, 2, 5, 8, 9],
        "Nature & Elements": [2, 4, 6, 7, 9]
    },
    "Energetic": {
        "Scenic & Environmental Settings": [2, 3, 5, 6, 9],
        "Mood & Atmosphere": [2, 3, 5, 9, 10],
        "Character Descriptors": [2, 3, 4, 6, 9],
        "Visual Style & Techniques": [3, 4, 6, 7, 8],
        "Nature & Elements": [2, 3, 7, 8, 9]
    },
    "Dreamy": {
        "Scenic & Environmental Settings": [0, 1, 3, 7, 9],
        "Mood & Atmosphere": [0, 3, 4, 7, 8],
        "Character Descriptors": [0, 2, 4, 5, 6],
        "Visual Style & Techniques": [1, 4, 8, 9, 10],
        "Nature & Elements": [0, 1, 4, 5, 6]
    },
    "Dramatic": {
        "Scenic & Environmental Settings": [0, 2, 3, 4, 8],
        "Mood & Atmosphere": [2, 4, 5, 8, 9],
        "Character Descriptors": [1, 5, 6, 8, 9],
        "Visual Style & Techniques": [0, 4, 5, 8, 9],
        "Nature & Elements": [2, 3, 7, 8, 9]
    },
    "Random": None  # Will use random selection for all categories
}

# Descriptive adjectives to enhance scene descriptions based on mood
MOOD_ADJECTIVES = {
    "Uplifting": ["radiant", "vibrant", "joyful", "bright", "gleaming", "hopeful", "warm", "inspiring"],
    "Melancholic": ["faded", "distant", "somber", "wistful", "weathered", "lonely", "haunting", "subdued"],
    "Energetic": ["vivid", "dynamic", "pulsing", "electric", "powerful", "intense", "bold", "striking"],
    "Dreamy": ["ethereal", "misty", "surreal", "hazy", "floating", "delicate", "soft", "enchanted"],
    "Dramatic": ["stark", "towering", "fierce", "imposing", "stormy", "shadowed", "profound", "majestic"],
    "Random": ["random", "varied", "eclectic", "diverse", "unexpected", "surprising", "unpredictable", "unpredictable"]

}

# Function to generate descriptive scenes from lyrics
def generate_scene_from_lyric(lyric, mood, description_length):
    # Clean the lyric text
    lyric = lyric.strip()
    if not lyric:
        return "Please enter a lyric to generate a scene."
    
    # Get word count range for the selected description length
    min_words, max_words = DESCRIPTION_LENGTHS[description_length]
    
    # Get elements based on mood
    elements = {}
    
    if mood == "Random":
        # Select random elements from each category
        for category, options in VISUAL_ELEMENTS.items():
            elements[category] = random.choice(options)
    else:
        # Select elements based on mood preset preferences
        for category, options in VISUAL_ELEMENTS.items():
            if category in MOOD_PRESETS[mood]:
                # Get indices preferred for this mood
                preferred_indices = MOOD_PRESETS[mood][category]
                # Select from preferred options
                selected_index = random.choice(preferred_indices)
                # Check the index of the selected_index to be within range
                if selected_index < len(VISUAL_ELEMENTS[category]):
                    elements[category] = VISUAL_ELEMENTS[category][selected_index]
                # set to default first first element if index is out of range                
                else:
                    print(f"Warning: Invalid index {selected_index} for category '{category}', using default, 3.")
                    elements[category] = VISUAL_ELEMENTS[category][3]
            else:
                elements[category] = random.choice(VISUAL_ELEMENTS[category])
    
    # Get mood-specific adjectives
    adjectives = MOOD_ADJECTIVES.get(mood, MOOD_ADJECTIVES["Random"])
    
    # Start building the scene
    scene = f"Scene inspired by \"{lyric}\": "
    
    # Add setting with adjective
    scene += f"A {random.choice(adjectives)} {elements['Scenic & Environmental Settings']} {random.choice(CONNECTING_PHRASES)} "
    
    # Add character with action
    scene += f"a {elements['Character Descriptors']} {random.choice(DESCRIPTIVE_VERBS)} "
    
    # Add mood element
    scene += f"in a {elements['Mood & Atmosphere']}. "
    
    # Add visual style detail
    scene += f"The scene {random.choice(DESCRIPTIVE_VERBS)} with {elements['Visual Style & Techniques']}, "
    
    # Add nature element
    scene += f"{random.choice(CONNECTING_PHRASES)} {elements['Nature & Elements']}. "
    
    # Add emotional interpretation of the lyric
    emotional_interpretations = [
        f"The visual metaphor reinforces the lyric's sentiment of {random.choice(['longing', 'hope', 'transformation', 'reflection', 'connection'])}.",
        f"This imagery {random.choice(['amplifies', 'echoes', 'contrasts with', 'complements', 'reinterprets'])} the emotional undercurrent of the words.",
        f"The scene {random.choice(['evokes', 'suggests', 'highlights', 'mirrors', 'enhances'])} the {random.choice(['vulnerability', 'strength', 'ambiguity', 'clarity', 'tension'])} inherent in the lyric."
    ]
    
    scene += random.choice(emotional_interpretations)
    
    # Add transition suggestion
    transitions = [
        f" The frame could {random.choice(['slowly dissolve', 'cut sharply', 'fade gently', 'transition smoothly'])} to the next scene.",
        f" As the scene {random.choice(['fades', 'lingers', 'dissolves', 'transitions'])}, it leaves a {random.choice(['poignant', 'powerful', 'subtle', 'striking'])} impression.",
        f" This moment {random.choice(['bridges', 'connects', 'contrasts with', 'complements'])} what comes next in the visual narrative."
    ]
    
    scene += random.choice(transitions)
    
    # Adjust word count to match selected description length
    current_words = len(scene.split())
    
    if current_words < min_words:
        # Add more descriptive details if needed
        additional_details = [
            f" {random.choice(['Light', 'Shadow', 'Color', 'Texture', 'Movement'])} plays a crucial role, creating a {random.choice(['dynamic', 'subtle', 'striking', 'nuanced'])} visual rhythm.",
            f" The {random.choice(['composition', 'framing', 'perspective', 'visual flow'])} emphasizes the {random.choice(['emotional', 'thematic', 'symbolic', 'narrative'])} weight of the moment.",
            f" {random.choice(['Time', 'Space', 'Perspective', 'Scale'])} feels {random.choice(['distorted', 'amplified', 'intimate', 'expansive'])} in this interpretation.",
            f" The {random.choice(['foreground', 'background', 'lighting', 'color palette'])} {random.choice(['contrasts with', 'complements', 'enhances', 'defines'])} the central imagery."
        ]
        
        while current_words < min_words and additional_details:
            detail = random.choice(additional_details)
            additional_details.remove(detail)
            scene += detail
            current_words = len(scene.split())
    
    elif current_words > max_words:
        # Trim the scene if it's too long
        words = scene.split()
        trimmed_words = words[:max_words]
        
        # Make sure to end with a complete sentence
        last_period_index = " ".join(trimmed_words).rfind(".")
        if last_period_index > 0:
            scene = " ".join(trimmed_words)[:last_period_index + 1]
        else:
            scene = " ".join(trimmed_words) + "."
    
    return scene

# Function to process all lyrics and generate scenes
def process_lyrics(lyrics, mood, description_length):
    scenes = []
    split_lyrics = [line for line in lyrics.split('\n') if line.strip()]
    
    with st.spinner("Generating storyboard..."):
        progress_bar = st.progress(0)
        for i, lyric in enumerate(split_lyrics):
            scene = generate_scene_from_lyric(lyric, mood, description_length)
            scenes.append({"Lyric": lyric, "Scene Description": scene})
            progress_bar.progress((i + 1) / len(split_lyrics))
            time.sleep(0.1)  # Add slight delay for visual effect
    
    return scenes

# Function to create a storyboard display
def display_storyboard(scenes_data):
    st.subheader("📋 Generated Storyboard")
    
    for i, scene in enumerate(scenes_data):
        with st.expander(f"Scene {i+1}: {textwrap.shorten(scene['Lyric'], width=50, placeholder='...')}"):
            st.markdown("**Original Lyric:**")
            st.write(scene["Lyric"])
            st.markdown("**Scene Description:** *(60-second video sequence)*")
            st.write(scene["Scene Description"])
            st.markdown("---")
            
            # Allow editing of scene description
            # make sure the i is unique for each scene
           
            new_desc = st.text_area("Edit Scene Description:", scene["Scene Description"], key=f"edit_{i}")
            print(f"New description for scene {i}: {new_desc}")
            scene["Scene Description"] = new_desc

    # Download options
    st.markdown("### 📥 Export Options")
    col1, col2 = st.columns(2)
    
    # Convert scenes to DataFrame for CSV export
    df = pd.DataFrame(scenes_data)
    
    # CSV download
    csv = df.to_csv(index=False).encode('utf-8')
    col1.download_button(
        label="Download CSV",
        data=csv,
        file_name="storyboard_scenes.csv",
        mime="text/csv"
    )
    
    # Text download
    text_content = ""
    for i, scene in enumerate(scenes_data):
        text_content += f"SCENE {i+1}\n"
        text_content += f"LYRIC: {scene['Lyric']}\n"
        text_content += f"DESCRIPTION: {scene['Scene Description']}\n"
        text_content += "="*80 + "\n\n"
    
    col2.download_button(
        label="Download Text",
        data=text_content,
        file_name="storyboard_scenes.txt",
        mime="text/plain"
    )

# Main app layout
def main():
    st.title("🎬 Lyric-to-Storyboard Generator")
    st.markdown("""
    Transform song lyrics into detailed visual scenes for AI video generation.
    Each scene is designed as input for a text-to-video generator with 60-second scene duration.
    """)
    
    # Sidebar controls
    st.sidebar.header("Scene Controls")
    
    # Mood selection
    selected_mood = st.sidebar.selectbox(
        "Scene Mood",
        list(MOOD_PRESETS.keys()),
        index=0
    )
    
    # Description length selection
    selected_length = st.sidebar.selectbox(
        "Description Detail Level",
        list(DESCRIPTION_LENGTHS.keys()),
        index=1
    )
    
    # Custom elements (advanced)
    with st.sidebar.expander("Custom Element Preferences (Advanced)"):
        st.markdown("Select preferred elements for each category:")
        
        custom_elements = {}
        for category, options in VISUAL_ELEMENTS.items():
            custom_elements[category] = st.multiselect(
                category,
                options,
                default=[options[0]],
                key=f"custom_{category}"
            )
    
    # Main input area
    st.header("📝 Enter Lyrics")
    st.markdown("Enter each line of lyrics on a new line. Each line will become a separate scene.")
    
    lyrics_input = st.text_area(
        "Song Lyrics (one line per scene)",
        height=200,
        placeholder="Enter lyrics here...\nOne line per scene...\nEach becoming a 60-second video segment..."
    )
    
    # Process button
    if st.button("Generate Storyboard"):
        if not lyrics_input.strip():
            st.error("Please enter some lyrics to generate scenes.")
        else:
            scenes = process_lyrics(lyrics_input, selected_mood, selected_length)
            st.session_state['scenes'] = scenes
            display_storyboard(scenes)
    
    # Display previously generated storyboard if available
    if 'scenes' in st.session_state:
        display_storyboard(st.session_state['scenes'])
    
    # Help and information
    with st.expander("ℹ️ Help & Tips"):
        st.markdown("""
        ### How to use this tool:
        
        1. Enter your song lyrics in the text area above, with each line on a new line
        2. Select the overall mood for your scenes
        3. Choose how detailed you want the scene descriptions to be
        4. Click "Generate Storyboard" to create your scenes
        5. Edit any generated scenes as needed
        6. Download your storyboard in CSV or text format
        
        ### Tips for best results:
        
        - Each line will be treated as a separate scene (60-second video sequence)
        - Keep lyrics relatively short for more focused scene descriptions
        - Try different mood settings to see varied interpretations
        - Edit generated scenes to refine them for your specific vision
        - The descriptions are designed to work with text-to-video AI generators
        """)

if __name__ == "__main__":
    main()
